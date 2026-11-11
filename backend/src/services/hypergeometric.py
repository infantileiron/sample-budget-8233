import math
from decimal import Decimal,ROUND_CEILING
from fractions import Fraction

def estimated_defects(size,rate):
 return int((Decimal(size)*Decimal(str(rate))).to_integral_value(rounding=ROUND_CEILING))

def miss_probability(N,D,n):
 if not isinstance(N,int) or not isinstance(D,int) or not isinstance(n,int) or N<1 or not 0<=D<=N or not 0<=n<=N:raise ValueError("N,D,n范围无效")
 if n>N-D:return 0.
 return math.comb(N-D,n)/math.comb(N,n)

def minimum_sample(N,D,target):
 if not math.isfinite(target) or not 0<=target<=1:raise ValueError("目标检出率须在0至1之间")
 miss_probability(N,D,0)
 if target==0:return 0
 if D==0:return None
 # For 100% target, enforce a guaranteed hit rather than a float rounded to 1.
 if target==1:return N-D+1
 requested=Fraction(str(target))
 lo,hi=0,N-D+1
 while lo<hi:
  mid=(lo+hi)//2
  if mid>N-D or math.comb(N-D,mid)*requested.denominator <= (requested.denominator-requested.numerator)*math.comb(N,mid):hi=mid
  else:lo=mid+1
 return lo
