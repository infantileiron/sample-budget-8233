import time,logging
from pathlib import Path
from .config.database import Session
from .utils.queue import client,QUEUE
from .services.run_service import compute,recover_pending
heartbeat=Path("/artifacts/worker-heartbeat")
with Session() as db:
 try:recover_pending(db)
 except Exception:logging.exception("Recover pending runs failed")
while True:
 try:
  heartbeat.touch()
  item=client().blpop(QUEUE,timeout=2)
  if item:
   with Session() as db:compute(db,item[1])
 except Exception:logging.exception("Worker error");time.sleep(2)
