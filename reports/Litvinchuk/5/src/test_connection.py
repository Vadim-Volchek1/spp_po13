"""Точка входа FastAPI приложения."""

from fastapi import FastAPI

from src.routers.country import router as country_router

app = FastAPI(title="European Football API")

app.include_router(country_router)
