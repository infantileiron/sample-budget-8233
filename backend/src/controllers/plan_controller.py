from ..services import plan_service
from ..models.plan import SamplingPlan
from ..models.common import serialize
from .common import listing,require
def list_all(db):return listing(db,SamplingPlan)
def detail(db,ident):return serialize(require(db,SamplingPlan,ident))
def create(db,body):return serialize(plan_service.create(db,body))
