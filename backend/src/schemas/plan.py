from pydantic import BaseModel,Field,model_validator
class PlanCreate(BaseModel):
 name:str=Field(min_length=2,max_length=180)
 lot_ids:list[str]=Field(min_length=1,max_length=30)
 target_detection:float=Field(default=.95,ge=0,le=1,allow_inf_nan=False)
 budget:int=Field(default=480,ge=1,le=5000)
 seed:int=Field(default=20261112,ge=0,le=2147483647)
 @model_validator(mode="after")
 def unique_lots(self):
  if len(set(self.lot_ids))!=len(self.lot_ids):raise ValueError("批次不能重复选择")
  return self
