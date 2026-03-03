"""Tests for the jokes route and root endpoint."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
from unittest.mock import AsyncMock, patch

import httpx
import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.models.joke import Joke


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Create a test client with lifespan managed app state."""
    app.state.http_client = httpx.AsyncClient()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    await app.state.http_client.aclose()


async def test_root_endpoint(client: AsyncClient) -> None:
    """Test the root endpoint returns welcome message."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to the Dad Joke API"
    assert data["docs"] == "/docs"


@patch("app.routes.jokes.fetch_random_joke")
async def test_get_joke_success(
    mock_fetch: AsyncMock, client: AsyncClient
) -> None:
    """Test GET /joke returns a joke on success."""
    mock_fetch.return_value = Joke(id="abc123", joke="I'm a dad joke")
    response = await client.get("/joke")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "abc123"
    assert data["joke"] == "I'm a dad joke"


@patch("app.routes.jokes.fetch_random_joke")
async def test_get_joke_upstream_error(
    mock_fetch: AsyncMock, client: AsyncClient
) -> None:
    """Test GET /joke returns 502 when upstream returns non-2xx."""
    mock_response = httpx.Response(
        500, request=httpx.Request("GET", "https://icanhazdadjoke.com/")
    )
    mock_fetch.side_effect = httpx.HTTPStatusError(
        "Server Error",
        request=mock_response.request,
        response=mock_response,
    )
    response = await client.get("/joke")
    assert response.status_code == 502
    assert "500" in response.json()["detail"]


@patch("app.routes.jokes.fetch_random_joke")
async def test_get_joke_network_error(
    mock_fetch: AsyncMock, client: AsyncClient
) -> None:
    """Test GET /joke returns 502 when network error occurs."""
    mock_fetch.side_effect = httpx.ConnectError("Connection refused")
    response = await client.get("/joke")
    assert response.status_code == 502
    assert "Could not reach" in response.json()["detail"]
