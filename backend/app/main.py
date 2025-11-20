from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import settings
from .database import init_db
from .routes import auth, identities, institutions, scan

init_db()

app = FastAPI(
    title=settings.app_name,
    description="AI-powered Smart Identity Generator",
    version="0.1.0",
    openapi_url=f"{settings.api_prefix}/openapi.json",
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(institutions.router, prefix=settings.api_prefix)
app.include_router(identities.router, prefix=settings.api_prefix)
app.include_router(scan.router, prefix=settings.api_prefix)

app.mount(
    f"{settings.api_prefix}/storage",
    StaticFiles(directory=settings.storage_dir, check_dir=False),
    name="storage",
)


@app.get("/")
def healthcheck():
    return {"status": "ok", "message": "Smart Identity Generator backend ready"}

