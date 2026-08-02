import time


# add to lock_service.py

_attempt_state = {
    "attempts": 0,
    "blocked_until": None  # epoch timestamp
}

MAX_ATTEMPTS = 3
BLOCK_DURATION = 3600  # 1 hour block on failure

def register_attempt(success: bool):
    import time
    now = int(time.time())
    if _attempt_state["blocked_until"] and now < _attempt_state["blocked_until"]:
        return False  # still blocked

    if success:
        _attempt_state["attempts"] = 0
        _attempt_state["blocked_until"] = None
        return True

    # failed attempt
    _attempt_state["attempts"] += 1
    if _attempt_state["attempts"] >= MAX_ATTEMPTS:
        _attempt_state["blocked_until"] = now + BLOCK_DURATION
        _attempt_state["attempts"] = 0  # reset attempts after block
    return True

def is_blocked():
    import time
    now = int(time.time())
    blocked = _attempt_state.get("blocked_until")
    if blocked and now < blocked:
        return True, blocked - now  # return seconds left
    return False, 0

