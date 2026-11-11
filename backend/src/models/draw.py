from sqlalchemy import String,Text,JSON,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column
from .common import RecordMixin
from ..config.database import Base
class SampleDraw(RecordMixin,Base):
 __tablename__="draws"
 run_id:Mapped[str]=mapped_column(ForeignKey("runs.id"),unique=True)
 seed:Mapped[int]
 manifest:Mapped[list]=mapped_column(JSON)
