"""
In-Memory Job Store
-------------------

Stores analysis jobs and background task state.

Used by:
- orchestrator
- background workers
- polling endpoint
"""

from threading import Lock
from datetime import datetime
import uuid
from copy import deepcopy


class JobStore:
    _jobs = {}
    _lock = Lock()

    # ============================================
    # CREATE
    # ============================================

    @classmethod
    def create_job(
        cls,
        prediction_payload
    ):
        """
        Create new analysis job.
        """

        job_id = str(
            uuid.uuid4()
        )

        job_data = {
            "job_id": job_id,

            "created_at":
                datetime.utcnow().isoformat(),

            "prediction":
                prediction_payload,

            "status": {
                "gradcam": "queued",
                "report": "queued",
                "lime": "not_requested"
            },

            "results": {
                "gradcam": None,
                "report": None,
                "lime": None
            },

            "errors": {}
        }

        with cls._lock:
            cls._jobs[job_id] = job_data

        return job_id

    # ============================================
    # READ
    # ============================================

    @classmethod
    def get_job(
        cls,
        job_id
    ):
        with cls._lock:
            if job_id not in cls._jobs:
                return None

            return deepcopy(
                cls._jobs[job_id]
            )

    @classmethod
    def exists(
        cls,
        job_id
    ):
        with cls._lock:
            return job_id in cls._jobs


    # ============================================
    # STATUS UPDATE
    # ============================================

    @classmethod
    def set_task_running(
        cls,
        job_id,
        task_name
    ):
        with cls._lock:
            cls._jobs[job_id]["status"][
                task_name
            ] = "running"


    @classmethod
    def set_task_done(
        cls,
        job_id,
        task_name,
        result
    ):
        with cls._lock:

            cls._jobs[job_id]["status"][
                task_name
            ] = "done"

            cls._jobs[job_id]["results"][
                task_name
            ] = result


    @classmethod
    def set_task_failed(
        cls,
        job_id,
        task_name,
        error_message
    ):
        with cls._lock:

            cls._jobs[job_id]["status"][
                task_name
            ] = "failed"

            cls._jobs[job_id]["errors"][
                task_name
            ] = error_message


    # ============================================
    # SPECIAL LIME HELPERS
    # ============================================

    @classmethod
    def mark_lime_requested(
        cls,
        job_id
    ):
        with cls._lock:
            cls._jobs[job_id]["status"][
                "lime"
            ] = "queued"


    # ============================================
    # FULL RESPONSE FOR API
    # ============================================

    @classmethod
    def build_analysis_response(
        cls,
        job_id
    ):
        job = cls.get_job(
            job_id
        )

        if not job:
            return None

        return {
            "job_id":
                job["job_id"],

            "prediction":
                job["prediction"],

            "status":
                job["status"],

            "gradcam":
                job["results"]["gradcam"],

            "report":
                job["results"]["report"],

            "lime":
                job["results"]["lime"]
        }


    # ============================================
    # DEBUG / ADMIN
    # ============================================

    @classmethod
    def list_jobs(cls):
        with cls._lock:
            return list(
                cls._jobs.keys()
            )


    @classmethod
    def count_jobs(cls):
        with cls._lock:
            return len(
                cls._jobs
            )


    @classmethod
    def clear_all(cls):
        with cls._lock:
            cls._jobs.clear()


    @classmethod
    def get_job_summary(cls):

        with cls._lock:

            return {
                "total_jobs":
                    len(cls._jobs),

                "jobs":
                    {
                        k: v["status"]
                        for k,v in cls._jobs.items()
                    }
            }