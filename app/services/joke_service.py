"""Service layer for fetching dad jokes from icanhazdadjoke.com."""

import httpx

from app.models.joke import Joke

JOKE_API_URL = "https://icanhazdadjoke.com/"


async def fetch_random_joke(client: httpx.AsyncClient) -> Joke:
    """Fetch a random dad joke from icanhazdadjoke.com.

    Args:
        client: An httpx async client for making HTTP requests.

    Returns:
        A Joke instance with the id and joke text.

    Raises:
        httpx.HTTPStatusError: If the upstream API returns a non-2xx response.
        httpx.RequestError: If a network error occurs.
    """
    response = await client.get(
        JOKE_API_URL,
        headers={"Accept": "application/json"},
    )
    response.raise_for_status()
    data = response.json()
    return Joke(id=data["id"], joke=data["joke"])
