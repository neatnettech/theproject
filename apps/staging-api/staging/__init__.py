import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from staging.api.v1.staging.routes import staging_router
from staging.database import init_db
from staging.containers import Container
from staging.logging_config import setup_logger
from dotenv import load_dotenv


load_dotenv(".env")


logger = setup_logger("staging", level="DEBUG")


if os.getenv("DEBUGPY", "0") == "1":
    import debugpy

    debugpy.listen(("0.0.0.0", 5678))
    logger.info("🛠 Waiting for debugger to attach (port 5678)...")


def create_app(container: Container) -> FastAPI:
    app = FastAPI(title="Staging API")
    import os

    APP_ENV = os.getenv("APP_ENV", "dev")
    print(f"🔧 Running in {APP_ENV} mode")
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
            "staging.acquisition.importer",  # optional, if using inject
        ]
    )

    app.container = container

    init_db(container.engine())

    app.include_router(staging_router, prefix="/api/v1/staging")

    return app


app = create_app(Container())  # default for uvicorn entrypoint
