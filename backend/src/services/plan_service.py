from uuid import uuid4
from sqlalchemy import select
from fastapi import HTTPException
from ..models.plan import SamplingPlan
from ..models.lot import ArchiveLot

def create(db,body):
 if any(db.get(ArchiveLot,i) is None for i in body.lot_ids):raise HTTPException(422,"所选档案批次不存在")
 if db.scalar(select(SamplingPlan).where(SamplingPlan.name==body.name)):raise HTTPException(409,"抽样计划名称已存在")
 row=SamplingPlan(id=str(uuid4()),**body.model_dump());db.add(row);db.commit();return row
