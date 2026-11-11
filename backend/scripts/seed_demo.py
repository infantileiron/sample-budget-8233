import json
from sqlalchemy import select,func
from src.config.database import initialize,Session
from src.models import ArchiveLot,SamplingPlan,AllocationRun,SampleDraw,ReviewDecision,Report,User
from src.utils.security import hash_password
from src.services.run_service import compute

def seed():
 initialize()
 with Session() as db:
  for role in ["admin","analyst","viewer"]:
   email=role+"@sample.demo"
   if not db.scalar(select(User).where(User.email==email)):db.add(User(id="user-"+role,email=email,role=role,password_hash=hash_password("ArchiveDemo2026!")))
  ids=[]
  for layer,p,label in [("low",.01,"常规"),("moderate",.03,"关注"),("high",.06,"高风险"),("critical",.12,"重点")]:
   for i,N in enumerate([100,150,200]):
    ident=f"demo-{layer}-{i}";ids.append(ident)
    if not db.get(ArchiveLot,ident):db.add(ArchiveLot(id=ident,name=f"{label}档案批次 {i+1}",stratum=layer,size=N,estimated_error_rate=p,doc_prefix=f"GL-{layer.upper()}-{i+1}",description="模拟数字化验收批次；预估差错率用于抽样设计，不是实际已测差错率"))
  db.commit()
  if not db.get(SamplingPlan,"demo-plan"):db.add(SamplingPlan(id="demo-plan",name="十一月档案四层复核",lot_ids=ids,target_detection=.95,budget=480,seed=20261112))
  db.commit()
  if not db.get(AllocationRun,"demo-run"):db.add(AllocationRun(id="demo-run",plan_id="demo-plan",status="queued",result={},error=""));db.commit();compute(db,"demo-run")
  draw=db.scalar(select(SampleDraw).where(SampleDraw.run_id=="demo-run"))
  if draw and not db.get(ReviewDecision,"demo-review"):db.add(ReviewDecision(id="demo-review",draw_id=draw.id,action="核对四层抽样口径与预算，按不可变文档编号复核；检出率依赖预估差错数假设，不代表质量保证。",state="approved",reviewer="admin@sample.demo"))
  db.commit()
  if draw and not db.get(Report,"demo-report"):db.add(Report(id="demo-report",review_id="demo-review",title="四层档案复核抽样底册",snapshot={"manifest":draw.manifest,"allocation":db.get(AllocationRun,"demo-run").result,"action":db.get(ReviewDecision,"demo-review").action,"reviewer":"admin@sample.demo"}))
  db.commit()
  return {cls.__tablename__:db.scalar(select(func.count()).select_from(cls)) for cls in [User,ArchiveLot,SamplingPlan,AllocationRun,SampleDraw,ReviewDecision,Report]}
if __name__=="__main__":print(json.dumps(seed(),ensure_ascii=False))
