from sqlalchemy import create_engine,text
from sqlalchemy.orm import DeclarativeBase,sessionmaker
from .settings import DATABASE_URL
class Base(DeclarativeBase): pass
engine=create_engine(DATABASE_URL,pool_pre_ping=True)
Session=sessionmaker(bind=engine,expire_on_commit=False)
def get_db():
 with Session() as db: yield db
# 运行快照列的幂等补齐：新库由元数据直接建出，存量库自动补列，不做破坏性升级。
_RUN_BACKFILL_COLUMNS={"plan_snapshot":"JSON","lot_snapshots":"JSON"}
def _backfill_run_snapshots():
 with engine.begin() as conn:
  if engine.dialect.name=="mysql":
   existing={row[0] for row in conn.execute(text("SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='runs'"))}
   for column,column_type in _RUN_BACKFILL_COLUMNS.items():
    if column not in existing:conn.execute(text(f"ALTER TABLE runs ADD COLUMN {column} {column_type} NULL"))
  else:
   existing={row[1] for row in conn.execute(text("PRAGMA table_info(runs)"))}
   for column in _RUN_BACKFILL_COLUMNS:
    if column not in existing:conn.execute(text(f"ALTER TABLE runs ADD COLUMN {column} JSON"))
def initialize():
 from .. import models
 Base.metadata.create_all(engine)
 try:_backfill_run_snapshots()
 except Exception:pass
