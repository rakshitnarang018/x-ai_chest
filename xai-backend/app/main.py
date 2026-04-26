"""
Main FastAPI App
----------------
Application bootstrap.
"""

import tensorflow as tf

tf.config.optimizer.set_jit(True)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import (
    API_TITLE,
    API_VERSION
)

from app.core.model_registry import (
    startup_load_models
)

from app.core.executor import (
    shutdown_executor
)


# Routers
from app.api.analyze import (
    router as analyze_router
)

from app.api.jobs import (
    router as jobs_router
)

from app.api.lime import (
    router as lime_router
)

from app.api.health import (
    router as health_router
)


# ======================================================
# APP
# ======================================================

app = FastAPI(
    title=API_TITLE,
    version=API_VERSION
)


# ======================================================
# CORS
# ======================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# ======================================================
# STARTUP
# ======================================================

@app.on_event(
    "startup"
)
def startup_event():

    print(
      "Loading models..."
    )

    startup_load_models()

    print(
      "Backend ready."
    )


# ======================================================
# SHUTDOWN
# ======================================================

@app.on_event(
    "shutdown"
)
def shutdown_event():

    shutdown_executor()


# ======================================================
# ROUTES
# ======================================================

app.include_router(
    health_router
)

app.include_router(
    analyze_router
)

app.include_router(
    jobs_router
)

app.include_router(
    lime_router
)