from enum import StrEnum
class Role(StrEnum):
 ADMIN="admin"
 ANALYST="analyst"
 VIEWER="viewer"
class RunStatus(StrEnum):
 QUEUED="queued"
 RUNNING="running"
 COMPLETED="completed"
 INFEASIBLE="infeasible"
 FAILED="failed"
class Stratum(StrEnum):
 LOW="low"
 MODERATE="moderate"
 HIGH="high"
 CRITICAL="critical"
