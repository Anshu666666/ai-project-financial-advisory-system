"""
================================================================================
FINWISE AI – FASTAPI PRODUCTION APPLICATION
Author: Anshuman (Core Backend & API Orchestration Lead)
================================================================================
Entry point for the FinWise AI API Server. Configures CORS, mounts routers,
manages application lifecycle, and exposes health check endpoints.
================================================================================
"""

import logging
import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Any, Dict

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.models.database import get_db_connection, init_db
from backend.routers.advisory import router as advisory_router
from agent.openrouter_client import DEFAULT_MODEL

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("finwise.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle hook for startup and shutdown procedures."""
    logger.info("Starting FinWise AI Backend Service...")
    init_db()
    logger.info("SQLite database verified and initialized.")
    yield
    logger.info("Shutting down FinWise AI Backend Service.")


app = FastAPI(
    title="FinWise AI – Intelligent Financial Advisory API",
    description="""
    ## 📈 Hybrid Financial Advisory System (Academic AI Architecture)
    FinWise AI combines:
    1. **Fuzzy Logic Risk Evaluator**: Continuous Mamdani inference modeling investor risk tolerance.
    2. **Rule-Based Expert System**: Forward-chaining engine executing production rules with audit traces.
    3. **Intelligent Agent (PydanticAI)**: Utility-based agent executing live web search & OpenRouter synthesis.
    4. **SQLite Persistence**: Stateful session storage and conversational chat memory.
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS Middleware for Aryan's Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permits local React, Vite, or file-based frontend access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(advisory_router, prefix="/api/v1")


@app.get("/", include_in_schema=False)
async def root_redirect():
    """Redirects root visitors directly to interactive OpenAPI Swagger documentation."""
    return RedirectResponse(url="/docs")


@app.get(
    "/api/v1/health",
    status_code=status.HTTP_200_OK,
    tags=["System & Monitoring"],
    summary="Health Check & System Diagnostics",
)
async def health_check() -> Dict[str, Any]:
    """
    Verifies that the database, AI modules, and API server are operational.
    """
    db_ok = False
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            db_ok = bool(cursor.fetchone())
    except Exception as e:
        logger.error(f"Database health check failed: {e}")

    openrouter_configured = bool(
        os.getenv("OPENROUTER_API_KEY")
        and not os.getenv("OPENROUTER_API_KEY", "").startswith("your_")
    )

    return {
        "status": "healthy" if db_ok else "degraded",
        "service": "FinWise AI Advisory Backend",
        "version": "1.0.0",
        "database_connected": db_ok,
        "openrouter_configured": openrouter_configured,
        "default_llm_model": os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL),
        "docs_url": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=True)
