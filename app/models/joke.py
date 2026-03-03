"""Pydantic models for joke responses."""

from pydantic import BaseModel


class Joke(BaseModel):
    """A dad joke returned from the API.

    Attributes:
        id: Unique identifier for the joke.
        joke: The joke text.
    """

    id: str
    joke: str
