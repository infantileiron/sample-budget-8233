import math

def allocate(capacities,weights,budget,minimums=None):
 keys=sorted(capacities);minimums=minimums or {k:0 for k in keys}
 if budget<sum(minimums.values()) or budget>sum(capacities.values()):raise ValueError("预算不满足下限或层容量")
 if any(capacities[k]<minimums[k] or minimums[k]<0 or weights[k]<0 or not math.isfinite(weights[k]) for k in keys):raise ValueError("配额参数无效")
 positive=[k for k in keys if weights[k]>0];zero=[k for k in keys if weights[k]==0]
 positive_target=min(budget-sum(minimums[k] for k in zero),sum(capacities[k] for k in positive))
 result={k:minimums[k] for k in keys};ideal={k:float(minimums[k]) for k in keys}
 if positive:
  def total(lam):return sum(min(capacities[k],max(minimums[k],lam*weights[k])) for k in positive)
  low,high=0.,1.
  while total(high)<positive_target:high*=2
  for _ in range(100):
   mid=(low+high)/2
   if total(mid)<positive_target:low=mid
   else:high=mid
  for k in positive:ideal[k]=min(capacities[k],max(minimums[k],high*weights[k]));result[k]=max(minimums[k],min(capacities[k],math.floor(ideal[k])))
  left=positive_target-sum(result[k] for k in positive)
  for k in sorted(positive,key=lambda k:(-(ideal[k]-math.floor(ideal[k])),k)):
   if left<=0:break
   if result[k]<capacities[k]:result[k]+=1;left-=1
 # Zero-variance strata only receive residual budget after positive strata saturate.
 left=budget-sum(result.values())
 while left:
  eligible=[k for k in keys if result[k]<capacities[k]]
  if not eligible:raise ValueError("层容量不足")
  for k in eligible:
   if left==0:break
   result[k]+=1;left-=1
 assert sum(result.values())==budget and all(minimums[k]<=result[k]<=capacities[k] for k in keys)
 return result,ideal
