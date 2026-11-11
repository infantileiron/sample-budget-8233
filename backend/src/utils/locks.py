from threading import RLock
# 进程内按运行ID互斥：MySQL依赖行锁串行化，SQLite等不支持行锁的方言由此保证同一运行只被处理一次
_locks={}
_guard=RLock()
def lock_for(key):
 with _guard:
  lock=_locks.get(key)
  if lock is None:
   lock=RLock();_locks[key]=lock
  return lock
