from uuid import uuid4
from sqlalchemy import select
from fastapi import HTTPException
from ..models.run import AllocationRun
from ..models.plan import SamplingPlan
from ..models.lot import ArchiveLot
from ..utils.queue import enqueue
from ..utils.locks import lock_for
from .allocation import calculate
from .draw_service import generate

def _snapshot_plan(plan):
 return {"id":plan.id,"name":plan.name,"lot_ids":list(plan.lot_ids),"target_detection":plan.target_detection,"budget":plan.budget,"seed":plan.seed}

def _snapshot_lot(lot):
 return {"id":lot.id,"name":lot.name,"stratum":lot.stratum,"size":lot.size,"estimated_error_rate":lot.estimated_error_rate,"doc_prefix":lot.doc_prefix}

def create(db,body):
 plan=db.get(SamplingPlan,body.plan_id)
 if plan is None:raise HTTPException(422,"抽样计划不存在")
 lots=[db.get(ArchiveLot,i) for i in plan.lot_ids]
 if any(lot is None for lot in lots):raise HTTPException(422,"所选档案批次不存在")
 # 与运行同事务冻结发起时的底册与计划，后续修正不再作用于本次运行
 row=AllocationRun(id=str(uuid4()),plan_id=plan.id,status="queued",result={},error="",
  plan_snapshot=_snapshot_plan(plan),lot_snapshots=[_snapshot_lot(lot) for lot in lots])
 db.add(row);db.commit()
 try:enqueue(row.id)
 except Exception:
  row.status="failed";row.error="Redis队列不可用，请重试";db.commit();raise HTTPException(503,row.error)
 return row

def claim(db,run_id):
 """原子认领一个未完成运行；重复投递/并发处理只有一个执行者能进入。"""
 row=db.get(AllocationRun,run_id,with_for_update=True)
 if row is None or row.status not in ["queued","running"]:return None
 row.status="running";db.commit()
 return row

def finish(db,run_id,status,result=None,error=""):
 row=db.get(AllocationRun,run_id)
 if row is None:return
 row.status=status
 if result is not None:row.result=result
 row.error=error
 db.commit()

def compute(db,run_id):
 with lock_for(run_id):
  row=claim(db,run_id)
  if row is None:return
  plan=row.plan_snapshot;lots=row.lot_snapshots
  try:
   result=calculate([{"stratum":lot["stratum"],"size":lot["size"],"estimated_error_rate":lot["estimated_error_rate"]} for lot in lots],plan["target_detection"],plan["budget"])
   result={**result,"plan_name":plan["name"],"seed":plan["seed"]}
   if not result["feasible"]:
    # 不可行运行不产生任何文档清单
    finish(db,run_id,"infeasible",result)
    return
   draw=generate(db,row,result)
   db.commit()
   # 清单份数必须逐层等于配额、总数等于预算，否则视为失败而非半成品
   if len(draw.manifest)!=plan["budget"] or any(sum(1 for item in draw.manifest if item["stratum"]==layer["stratum"])!=layer["quota"] for layer in result["strata"]):
    raise ValueError("抽样清单份数与配额/预算不一致")
   finish(db,run_id,"completed",result)
  except Exception as e:
   db.rollback()
   # 并发下其他执行者可能已完成；只有仍未终结的运行才落失败，避免覆盖既有产物
   current=db.get(AllocationRun,run_id)
   if current is not None and current.status in ["queued","running"]:
    current.status="failed";current.error=str(e)[:1000];db.commit()

def recover_pending(db):
 """启动时把中断遗留的未完成运行重新入队，已完成/已批准产物保持原样。"""
 pending=db.scalars(select(AllocationRun.id).where(AllocationRun.status.in_(["queued","running"]))).all()
 for run_id in pending:
  try:enqueue(run_id)
  except Exception:pass
 return list(pending)
