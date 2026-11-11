from uuid import uuid4
from sqlalchemy import select,or_
from fastapi import HTTPException
from ..models.lot import ArchiveLot

def create(db,body):
 if db.scalar(select(ArchiveLot).where(or_(ArchiveLot.name==body.name,ArchiveLot.doc_prefix==body.doc_prefix))):raise HTTPException(409,"批次名称或文档前缀已存在")
 row=ArchiveLot(id=str(uuid4()),**body.model_dump());db.add(row);db.commit();return row
