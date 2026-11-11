from fastapi import APIRouter,Depends
from ..config.database import get_db
from ..utils.auth import current,write_user,admin
from ..schemas.lot import LotCreate
from ..controllers import lot_controller as controller,common
from ..models.lot import ArchiveLot
from ..models.common import serialize
router=APIRouter(prefix="/lots",tags=["lots"])
@router.get("")
def listing(db=Depends(get_db),user=Depends(current)):return controller.list_all(db)
@router.get("/{ident}")
def detail(ident:str,db=Depends(get_db),user=Depends(current)):return controller.detail(db,ident)
@router.post("",status_code=201)
def create(body:LotCreate,db=Depends(get_db),user=Depends(write_user)):return controller.create(db,body)
from ..schemas.lot import LotEdit
@router.patch("/{ident}")
def edit(ident:str,body:LotEdit,db=Depends(get_db),user=Depends(write_user)):
 row=common.require(db,ArchiveLot,ident);row.description=body.description;db.commit();return serialize(row)
