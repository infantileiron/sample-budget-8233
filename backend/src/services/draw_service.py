import random
from uuid import uuid4
from sqlalchemy import select
from fastapi import HTTPException
from ..models.draw import SampleDraw
from ..models.run import AllocationRun
from ..models.plan import SamplingPlan
from ..models.lot import ArchiveLot

def manifest(lots,strata,seed):
 rng=random.Random(seed);rows=[]
 for layer in sorted(strata,key=lambda x:x["stratum"]):
  population=[]
  for lot in sorted(lots,key=lambda x:x["id"]):
   if lot["stratum"]==layer["stratum"]:
    population.extend({"document_id":lot["doc_prefix"]+"-"+str(i+1).zfill(5),"lot_id":lot["id"],"lot_name":lot["name"],"stratum":lot["stratum"]} for i in range(lot["size"]))
  rows.extend(rng.sample(population,layer["quota"]))
 return [dict(row,position=i+1) for i,row in enumerate(rows)]

def generate(db,run):
 existing=db.scalar(select(SampleDraw).where(SampleDraw.run_id==run.id))
 if existing:return existing
 if run.status!="completed" or not run.result.get("feasible"):raise HTTPException(409,"仅预算可行且已完成的运行可生成抽样")
 plan=db.get(SamplingPlan,run.plan_id);lots=[db.get(ArchiveLot,i) for i in plan.lot_ids]
 records=[{"id":l.id,"name":l.name,"size":l.size,"stratum":l.stratum,"doc_prefix":l.doc_prefix} for l in lots]
 row=SampleDraw(id=str(uuid4()),run_id=run.id,seed=plan.seed,manifest=manifest(records,run.result["strata"],plan.seed));db.add(row);db.commit();return row

def create(db,body):
 run=db.get(AllocationRun,body.run_id)
 if not run:raise HTTPException(404,"运行不存在")
 return generate(db,run)
