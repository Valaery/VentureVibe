from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.config.settings import settings
from src.infrastructure.database import db
from src.infrastructure.web.routers import auth, api
import logfire

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    db.connect()
    yield
    # Shutdown
    db.close()

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        lifespan=lifespan
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # In production, set to frontend domain
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Configure Logfire
    logfire.configure()
    logfire.instrument_fastapi(app)

    # Include Routers
    app.include_router(auth.router)
    app.include_router(api.router)

    @app.get("/")
    async def root():
        return {"message": "Welcome to Story LLM Backend"}

    return app

app = create_app()
