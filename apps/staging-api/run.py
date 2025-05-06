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
    workers = int(os.getenv("WORKERS", 1))
    uvicorn.run("staging:app", host=host, port=port, reload=True, workers=workers)
