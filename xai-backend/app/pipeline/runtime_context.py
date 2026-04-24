"""
Temporary runtime context
for deferred LIME requests.
"""

from threading import Lock


MAX_CONTEXT_ITEMS = 100


class RuntimeContext:

    _ctx={}
    _lock=Lock()

    @classmethod
    def set(
        cls,
        job_id,
        payload
    ):
        with cls._lock:
            cls._ctx[job_id]=payload

    @classmethod
    def get(
        cls,
        job_id
    ):
        with cls._lock:
            return cls._ctx.get(
                job_id
            )

    @classmethod
    def delete(
        cls,
        job_id
    ):
        with cls._lock:
            if job_id in cls._ctx:
                del cls._ctx[job_id]