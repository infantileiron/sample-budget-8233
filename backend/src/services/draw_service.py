import random
from uuid import uuid4
from sqlalchemy import select
from fastapi import HTTPException
from ..models.draw import SampleDraw
from ..models.run import AllocationRun
from ..utils.locks import lock_for

def manifest(lots,strata,seed):
 rng=random.Random(seed);rows=[]
 for layer in sorted(strata,key=lambda x:x["stratum"]):
  population=[]
  for lot in sorted(lots,key=lambda x:x["id"]):
   if lot["stratum"]==layer["stratum"]:
    population.extend({"document_id":lot["doc_prefix"]+"-"+str(i+1).zfill(5),"lot_id":lot["id"],"lot_name":lot["name"],"stratum":lot["stratum"]} for i in range(lot["size"]))
  rows.extend(rng.sample(population,layer["quota"]))
 return [dict(row,position=i+1) for i,row in enumerate(rows)]

def _persist(db,run,result):
 plan=run.plan_snapshot
 rows=manifest(run.lot_snapshots,result["strata"],plan["seed"])
 draw=SampleDraw(id=str(uuid4()),run_id=run.id,seed=plan["seed"],manifest=rows)
 db.add(draw)
 return draw

def generate(db,run,result=None):
 """同一运行只保留一份清单；并发请求在运行行锁上串行后返回原清单。"""
 locked=db.get(AllocationRun,run.id,with_for_update=True)
 if locked is None:raise HTTPException(404,"运行不存在")
 existing=db.scalar(select(SampleDraw).where(SampleDraw.run_id==locked.id))
 if existing:return existing
 if locked.status!="completed" or not locked.result.get("feasible"):
  # 工作流在同一事务内调用时直接落清单；外部直接调用保持409语义
  if result is None:raise HTTPException(409,"仅预算可行且已完成的运行可生成抽样")
  return _persist(db,locked,result)
 return _persist(db,locked,locked.result)

def create(db,body):
 run=db.get(AllocationRun,body.run_id)
 if not run:raise HTTPException(404,"运行不存在")
 # 与后台计算共用同一把运行锁，保证并发处理同次运行只保留一份清单
 with lock_for(run.id):
  draw=generate(db,run)
  db.commit()
 return draw
