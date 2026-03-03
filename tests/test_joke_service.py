"""Tests for the joke service layer."""

import httpx
import pytest

from app.models.joke import Joke
from app.services.joke_service import fetch_random_joke


async def test_fetch_random_joke_success(respx_mock=None) -> None:
    """Test successful joke fetch returns a Joke model."""
    mock_response = {"id": "abc123", "joke": "Why did the scarecrow win an award? He was outstanding in his field.", "status": 200}

    transport = httpx.MockTransport(
        lambda request: httpx.Response(200, json=mock_response)
    )
    async with httpx.AsyncClient(transport=transport) as client:
        joke = await fetch_random_joke(client)

    assert isinstance(joke, Joke)
    assert joke.id == "abc123"
    assert "scarecrow" in joke.joke


async def test_fetch_random_joke_http_error() -> None:
    """Test that non-2xx response raises HTTPStatusError."""
    transport = httpx.MockTransport(
        lambda request: httpx.Response(500, text="Internal Server Error")
    )
    async with httpx.AsyncClient(transport=transport) as client:
        with pytest.raises(httpx.HTTPStatusError):
            await fetch_random_joke(client)


async def test_fetch_random_joke_network_error() -> None:
    """Test that network errors raise RequestError."""

    def raise_connect_error(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("Connection refused")

    transport = httpx.MockTransport(raise_connect_error)
    async with httpx.AsyncClient(transport=transport) as client:
        with pytest.raises(httpx.RequestError):
            await fetch_random_joke(client)
