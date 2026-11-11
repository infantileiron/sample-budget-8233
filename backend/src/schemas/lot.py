from pydantic import BaseModel,Field
from ..constants.enums import Stratum
class LotCreate(BaseModel):
 name:str=Field(min_length=2,max_length=180)
 stratum:Stratum
 size:int=Field(ge=1,le=5000)
 estimated_error_rate:float=Field(ge=0,le=1,allow_inf_nan=False)
 doc_prefix:str=Field(min_length=2,max_length=30,pattern=r"^[A-Za-z0-9-]+$")
 description:str=Field(default="",max_length=2000)
class LotEdit(BaseModel):
 description:str=Field(max_length=2000)
