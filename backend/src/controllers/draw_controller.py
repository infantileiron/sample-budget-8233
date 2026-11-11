from ..services import draw_service
from ..models.draw import SampleDraw
from ..models.common import serialize
from .common import listing,require
def list_all(db):return listing(db,SampleDraw)
def detail(db,ident):return serialize(require(db,SampleDraw,ident))
def create(db,body):return serialize(draw_service.create(db,body))
