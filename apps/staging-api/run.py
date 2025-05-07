# run.py
import os
from dotenv import load_dotenv
import uvicorn
from staging import create_app
from staging.containers import Container

load_dotenv()

container = Container()
app = create_app(container)

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debugpy_enabled = os.getenv("DEBUGPY", "0") == "1"

    if debugpy_enabled:
        import debugpy

        debugpy.listen(("0.0.0.0", 5678))
        print("✅ Waiting for debugger to attach...")
        debugpy.wait_for_client()

    uvicorn.run(
        "staging:app", host=host, port=port, reload=not debugpy_enabled, workers=1
    )
