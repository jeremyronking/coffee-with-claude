# API Reference

## Base URL

```
http://localhost:8000
```

## Endpoints

### `GET /`

Health check and welcome endpoint.

**Response** `200 OK`

```json
{
  "message": "Welcome to the Dad Joke API",
  "docs": "/docs"
}
```

### `GET /joke`

Returns a random dad joke from icanhazdadjoke.com.

**Response** `200 OK`

```json
{
  "id": "R7UfaahVfFd",
  "joke": "My dog used to chase people on a bike a lot. It got so bad I had to take his bike away."
}
```

**Error Response** `502 Bad Gateway`

Returned when the upstream joke API is unreachable or returns an error.

```json
{
  "detail": "Upstream API returned 500"
}
```

```json
{
  "detail": "Could not reach the joke API"
}
```

### `GET /docs`

Auto-generated interactive OpenAPI documentation (Swagger UI), provided by FastAPI.

## Running Locally

```bash
uvicorn app.main:app --reload
```

Then visit `http://localhost:8000/docs` for interactive API docs.

## Running with Docker

```bash
docker build -t dad-joke-api .
docker run -p 8000:8000 dad-joke-api
```
