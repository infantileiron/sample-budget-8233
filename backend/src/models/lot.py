from sqlalchemy import String,Text,JSON,ForeignKey,Double
from sqlalchemy.orm import Mapped,mapped_column
from .common import RecordMixin
from ..config.database import Base
class ArchiveLot(RecordMixin,Base):
 __tablename__="lots"
 name:Mapped[str]=mapped_column(String(180),unique=True)
 stratum:Mapped[str]=mapped_column(String(20))
 size:Mapped[int]
 estimated_error_rate:Mapped[float]=mapped_column(Double)
 doc_prefix:Mapped[str]=mapped_column(String(40),unique=True)
 description:Mapped[str]=mapped_column(Text,default="")
