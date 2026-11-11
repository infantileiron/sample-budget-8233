from sqlalchemy import String,Text,JSON,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column
from .common import RecordMixin
from ..config.database import Base
class AllocationRun(RecordMixin,Base):
 __tablename__="runs"
 plan_id:Mapped[str]=mapped_column(ForeignKey("plans.id"))
 status:Mapped[str]=mapped_column(String(20),default="queued")
 result:Mapped[dict]=mapped_column(JSON,default=dict)
 error:Mapped[str]=mapped_column(Text,default="")
 # 发起运行时冻结的底册与计划快照；之后批次/计划修正不影响本次运行
 plan_snapshot:Mapped[dict]=mapped_column(JSON,default=dict)
 lot_snapshots:Mapped[list]=mapped_column(JSON,default=list)
