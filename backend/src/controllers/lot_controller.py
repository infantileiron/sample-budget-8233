from ..services import lot_service
from ..models.lot import ArchiveLot
from ..models.common import serialize
from .common import listing,require
def list_all(db):return listing(db,ArchiveLot)
def detail(db,ident):return serialize(require(db,ArchiveLot,ident))
def create(db,body):return serialize(lot_service.create(db,body))
