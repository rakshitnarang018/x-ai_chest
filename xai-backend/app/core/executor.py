"""
Background Task Executor
------------------------

Runs asynchronous enrichment tasks:

- GradCAM generation
- LLM report generation
- On-demand LIME

Uses ThreadPoolExecutor (v1)
"""

from concurrent.futures import (
    ThreadPoolExecutor
)

from app.core.config import (
    MAX_WORKERS
)

from app.core.job_store import (
    JobStore
)


# =============================================
# GLOBAL EXECUTOR
# =============================================

executor = ThreadPoolExecutor(
    max_workers=MAX_WORKERS
)


# =============================================
# GENERIC SAFE TASK WRAPPER
# =============================================

def run_background_task(
    job_id,
    task_name,
    task_fn,
    *args,
    **kwargs
):
    """
    Wrapper:
    Updates job states safely.
    """

    try:

        JobStore.set_task_running(
            job_id,
            task_name
        )

        result = task_fn(
            *args,
            **kwargs
        )

        JobStore.set_task_done(
            job_id,
            task_name,
            result
        )

        return result


    except Exception as e:

        JobStore.set_task_failed(
            job_id,
            task_name,
            str(e)
        )

        print(
            f"❌ {task_name} failed "
            f"for {job_id}: {e}"
        )

        return None


# =============================================
# SUBMIT SINGLE TASK
# =============================================

def submit_task(
    job_id,
    task_name,
    task_fn,
    *args,
    **kwargs
):
    """
    Submit one background task.
    """

    future = executor.submit(
        run_background_task,
        job_id,
        task_name,
        task_fn,
        *args,
        **kwargs
    )

    return future


# =============================================
# SUBMIT DEFAULT ENRICHMENT TASKS
# =============================================

def submit_enrichment_tasks(
    job_id,
    image_bundle,
    prediction_payload,
    gradcam_fn,
    report_fn
):
    """
    Default automatic background tasks:

    - GradCAM
    - Report
    """

    futures = {}

    futures["gradcam"] = submit_task(
        job_id,
        "gradcam",
        gradcam_fn,
        image_bundle,
        prediction_payload
    )

    futures["report"] = submit_task(
        job_id,
        "report",
        report_fn,
        prediction_payload
    )

    return futures


# =============================================
# ON DEMAND LIME
# =============================================

def submit_lime_task(
    job_id,
    lime_fn,
    *args,
    **kwargs
):
    """
    Called when user requests LIME.
    """

    JobStore.mark_lime_requested(
        job_id
    )

    return submit_task(
        job_id,
        "lime",
        lime_fn,
        *args,
        **kwargs
    )


# =============================================
# EXECUTOR STATUS
# =============================================

def executor_status():
    return {
        "max_workers":
            MAX_WORKERS,

        "alive":
            True
    }


# =============================================
# CLEAN SHUTDOWN
# =============================================

def shutdown_executor():
    """
    For graceful app shutdown.
    """

    executor.shutdown(
        wait=False
    )