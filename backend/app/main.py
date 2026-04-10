import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.takeout import router as takeout_router
from app.routers.analytics import router as analytics_router
from app.routers.insights import router as insights_router

from app.db.session import engine
from app.models.db_models import Base

# Configure minimal standard logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Initialize the SQLAlchemy models identically mapped to Postgres via the engine
# This keeps it lightweight while remaining Alembic-ready.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Google Pay Parser API",
    description="FastAPI endpoint for parsing Google Takeout 'My Activity.html' files.",
    version="1.0.0"
)

# CORS — allow React dev server origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(takeout_router)
app.include_router(analytics_router)
app.include_router(insights_router)


@app.get("/")
def root():
    return {"message": "Welcome to the Google Pay Parser API. Head over to /docs to test the API!"}