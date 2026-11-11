import math
from .hypergeometric import estimated_defects,minimum_sample,miss_probability
from .neyman import allocate

def calculate(lots,target,budget):
 strata={}
 for lot in lots:
  group=strata.setdefault(lot["stratum"],{"N":0,"D":0,"expected_errors":0.,"lot_count":0})
  group["N"]+=lot["size"];group["D"]+=estimated_defects(lot["size"],lot["estimated_error_rate"]);group["expected_errors"]+=lot["size"]*lot["estimated_error_rate"];group["lot_count"]+=1
 for key,group in strata.items():
  group["stratum"]=key;group["estimated_rate"]=group["expected_errors"]/group["N"];group["minimum"]=minimum_sample(group["N"],group["D"],target);group["weight"]=group["N"]*math.sqrt(group["estimated_rate"]*(1-group["estimated_rate"]))
 impossible=[k for k,g in strata.items() if g["minimum"] is None]
 required=None if impossible else sum(g["minimum"] for g in strata.values())
 reason="假设差错数D=0，非零检出目标不可达："+", ".join(impossible) if impossible else "预算低于各风险层目标检出率的精确最小样本量之和" if budget<required else "预算超过所选档案总容量" if budget>sum(g["N"] for g in strata.values()) else ""
 result={"feasible":not bool(reason),"reason":reason,"required_budget":required,"budget":budget,"target":target,"capacity":sum(g["N"] for g in strata.values()),"strata":[strata[k] for k in sorted(strata)],"assumption":"每个风险层汇总所选批次，D=sum ceil(N_lot*p_lot)；目标按风险层判断，不保证每批分别达标。层内文档等概率、无放回抽取。"}
 if reason:return result
 quotas,ideals=allocate({k:g["N"] for k,g in strata.items()},{k:g["weight"] for k,g in strata.items()},budget,{k:g["minimum"] for k,g in strata.items()})
 for key,group in strata.items():
  group["quota"]=quotas[key];group["ideal"]=ideals[key];group["miss_probability"]=miss_probability(group["N"],group["D"],quotas[key]);group["detection_probability"]=1-group["miss_probability"];group["guaranteed"]=group["D"]>0 and quotas[key]>group["N"]-group["D"]
 return result
