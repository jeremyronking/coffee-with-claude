"""FastAPI application for the Dad Joke API."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

import httpx
from fastapi import FastAPI

from app.routes.jokes import router as jokes_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage the shared httpx client lifecycle.

    Creates an async HTTP client on startup and closes it on shutdown.
    """
    app.state.http_client = httpx.AsyncClient()
    yield
    await app.state.http_client.aclose()


app = FastAPI(
    title="Dad Joke API",
    description="A simple API that returns random dad jokes.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(jokes_router)


@app.get("/")
async def root() -> dict[str, str]:
    """Health check and welcome endpoint."""
    return {"message": "Welcome to the Dad Joke API", "docs": "/docs"}
