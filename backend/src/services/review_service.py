from uuid import uuid4
from fastapi import HTTPException
from ..models.review import ReviewDecision
from ..models.draw import SampleDraw

def create(db,body):
 if not db.get(SampleDraw,body.draw_id):raise HTTPException(409,"请选择已生成的实际抽样清单")
 row=ReviewDecision(id=str(uuid4()),**body.model_dump(),state="submitted",reviewer="");db.add(row);db.commit();return row

def approve(db,row,user):
 if row.state!="submitted":raise HTTPException(409,"复核已处理")
 row.state="approved";row.reviewer=user.email;db.commit();return row
