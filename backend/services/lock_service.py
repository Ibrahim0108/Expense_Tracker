# backend/services/lock_service.py
import time

# Simple in-memory lock info. This resets when Flask restarts.
# For a single small app this is OK. On multi-instance hosting use a persistent store.
_lock_state = {
    "locked": False,
    "locked_at": None,   # epoch
    "session_expires_at": None
}


def lock_acquire(duration_seconds: int):
    _lock_state["locked"] = True
    _lock_state["locked_at"] = int(time.time())
    _lock_state["session_expires_at"] = int(time.time()) + duration_seconds

def lock_release():
    _lock_state["locked"] = False
    _lock_state["locked_at"] = None
    _lock_state["session_expires_at"] = None

def lock_status():
    # expire automatically if time passed
    if _lock_state["locked"] and _lock_state["session_expires_at"]:
        import time
        if time.time() > _lock_state["session_expires_at"]:
            lock_release()
    return _lock_state.copy()
