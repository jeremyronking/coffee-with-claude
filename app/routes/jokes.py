"""Routes for joke endpoints."""

import httpx
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.models.joke import Joke
from app.services.joke_service import fetch_random_joke

router = APIRouter()


@router.get("/joke", response_model=Joke)
async def get_joke(request: Request) -> Joke:
    """Return a random dad joke.

    Proxies the request to icanhazdadjoke.com and returns the joke.
    Returns 502 Bad Gateway if the upstream API is unavailable or errors.
    """
    client: httpx.AsyncClient = request.app.state.http_client
    try:
        return await fetch_random_joke(client)
    except httpx.HTTPStatusError as exc:
        return JSONResponse(
            status_code=502,
            content={
                "detail": f"Upstream API returned {exc.response.status_code}"
            },
        )
    except httpx.RequestError:
        return JSONResponse(
            status_code=502,
            content={"detail": "Could not reach the joke API"},
        )
