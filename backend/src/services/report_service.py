import csv,io
from uuid import uuid4
from sqlalchemy import select
from fastapi import HTTPException
from ..models.review import ReviewDecision
from ..models.draw import SampleDraw
from ..models.run import AllocationRun
from ..models.report import Report

def create(db,body):
 review=db.get(ReviewDecision,body.review_id)
 if review is None or review.state!="approved":raise HTTPException(409,"报告必须关联已批准复核")
 existing=db.scalar(select(Report).where(Report.review_id==body.review_id))
 if existing:return existing
 draw=db.get(SampleDraw,review.draw_id);run=db.get(AllocationRun,draw.run_id)
 row=Report(id=str(uuid4()),review_id=review.id,title=body.title,snapshot={"manifest":draw.manifest,"allocation":run.result,"action":review.action,"reviewer":review.reviewer});db.add(row);db.commit();return row

def export(row):
 out=io.StringIO();writer=csv.writer(out);writer.writerow(["position","document_id","lot_name","stratum","stratum_N","assumed_D","stratum_quota","detection_probability","miss_probability","guaranteed_detection"])
 layers={s["stratum"]:s for s in row.snapshot["allocation"]["strata"]}
 for r in row.snapshot["manifest"]:
  s=layers[r["stratum"]];writer.writerow([r["position"],r["document_id"],r["lot_name"],r["stratum"],s["N"],s["D"],s["quota"],s["detection_probability"],s["miss_probability"],s["guaranteed"]])
 return "\ufeff"+out.getvalue()
