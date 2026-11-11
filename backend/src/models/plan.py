from sqlalchemy import String,Text,JSON,ForeignKey,Double
from sqlalchemy.orm import Mapped,mapped_column
from .common import RecordMixin
from ..config.database import Base
class SamplingPlan(RecordMixin,Base):
 __tablename__="plans"
 name:Mapped[str]=mapped_column(String(180),unique=True)
 lot_ids:Mapped[list]=mapped_column(JSON)
 target_detection:Mapped[float]=mapped_column(Double)
 budget:Mapped[int]
 seed:Mapped[int]
