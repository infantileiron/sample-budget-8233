from sqlalchemy import String,Text,JSON,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column
from .common import RecordMixin
from ..config.database import Base
class ReviewDecision(RecordMixin,Base):
 __tablename__="reviews"
 draw_id:Mapped[str]=mapped_column(ForeignKey("draws.id"))
 action:Mapped[str]=mapped_column(Text)
 state:Mapped[str]=mapped_column(String(20),default="submitted")
 reviewer:Mapped[str]=mapped_column(String(160),default="")
