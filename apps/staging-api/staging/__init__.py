from dotenv import load_dotenv

load_dotenv()

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from staging.api.v1.staging.routes import staging_router
from staging.database import init_db
from staging.containers import Container
from staging.logging_config import setup_logger
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from staging.middleware.logging import LoggingMiddleware
from staging.config import settings

# ─────────────────────────────────────────────────────────────
# App debug
# ─────────────────────────────────────────────────────────────
if os.getenv("DEBUGPY", "0") == "1":
    import debugpy

    debugpy.listen(("0.0.0.0", 5678))


# ─────────────────────────────────────────────────────────────
# Application startup/shutdown lifecycle hook
# ─────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


# ─────────────────────────────────────────────────────────────
# Create FastAPI app
# ─────────────────────────────────────────────────────────────
def create_app(container: Container) -> FastAPI:
    app = FastAPI(title="Staging API", lifespan=lifespan)

    app.add_middleware(LoggingMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*", "http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    container.init_resources()
    container.wire(
        modules=[
            "staging.api.v1.staging.routes",
            "staging.acquisition.importer",
        ]
    )

    app.container = container

    init_db(container.engine())

    # API ROUTES
    api_prefix = f"{settings.API_PREFIX}/{settings.API_VERSION}"
    app.include_router(staging_router, prefix=api_prefix, tags=["staging"])

    return app


app = create_app(Container())
