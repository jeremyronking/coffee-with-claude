# Architecture

## Overview

The Dad Joke API is a lightweight proxy service that fetches random dad jokes from [icanhazdadjoke.com](https://icanhazdadjoke.com) and serves them via a FastAPI-based REST API.

## Technology Stack

| Tool | Purpose |
|------|---------|
| **FastAPI** | Web framework with automatic OpenAPI docs |
| **httpx** | Async HTTP client for upstream API calls |
| **uvicorn** | ASGI server |
| **Docker** | Containerization via `python:3.12-slim` |

## Layers

The application follows a three-layer architecture:

### 1. Models (`app/models/`)

Pydantic models that define the shape of API responses.

- `joke.py` — `Joke` model with `id` and `joke` fields.

### 2. Services (`app/services/`)

Business logic and external API integration.

- `joke_service.py` — Async function that calls `GET https://icanhazdadjoke.com/` with `Accept: application/json`, returning a `Joke` instance.

### 3. Routes (`app/routes/`)

HTTP endpoint handlers that orchestrate services and map errors.

- `jokes.py` — `GET /joke` endpoint that calls the joke service and maps upstream failures to HTTP 502.

### Application Entry Point (`app/main.py`)

- Creates the FastAPI app with lifespan management.
- A shared `httpx.AsyncClient` is created on startup and stored in `app.state` for connection pooling.
- Includes the joke router and a root health-check endpoint.

## Error Handling

The API acts as a proxy, so upstream failures are mapped to **502 Bad Gateway**:

- **Upstream non-2xx response** — Returns 502 with the upstream status code in the detail message.
- **Network error / timeout** — Returns 502 with "Could not reach the joke API".

## Project Structure

```
app/
├── __init__.py
├── main.py              # FastAPI app, lifespan, root endpoint
├── models/
│   ├── __init__.py
│   └── joke.py          # Pydantic response model
├── routes/
│   ├── __init__.py
│   └── jokes.py         # GET /joke endpoint
└── services/
    ├── __init__.py
    └── joke_service.py  # httpx call to icanhazdadjoke.com
```
