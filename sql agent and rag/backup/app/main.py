# app/main.py
from fastapi import FastAPI
from app.api.routes import router as api_router

def create_app() -> FastAPI:
    app = FastAPI(title="Covid-19 Jakarta Agentic API", version="1.0")
    app.include_router(api_router, prefix="/api")

    @app.get("/")
    def root():
        return {"message": "Backend API is running"}

    return app

app = create_app()
