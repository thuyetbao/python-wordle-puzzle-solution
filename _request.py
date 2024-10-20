#!/bin/python3

"""Implementation the API with httpx"""

# External
import httpx

# Internal
from _constant import (
    BASE_ORIGIN_URL, ROUTE_PATH,
    DEFAULT_LENGTH_STRING, DEFAULT_SEED
)
from _model import (
    ModelSlotGuessResult,
    adapterBucketSlotGuessResult
)


def make_guess_random(word: str, size: int = DEFAULT_LENGTH_STRING, seed: int = DEFAULT_SEED) -> list[ModelSlotGuessResult]:
    """Makes a random guess by sending a GET request to the API and returns a list of ModelSlotGuessResult.

    Return
    ------
    list[ModelSlotGuessResult]: A list of objects representing the results of the guess, including slot position, guessed character, and result.
    """

    if not len(word) == size:
        raise ValueError("The length of the word must be equal to the size.")

    resp = httpx.get(
        url=BASE_ORIGIN_URL.join(ROUTE_PATH),
        params={"guess": word, "size": size, "seed": 1234},
        headers={"Content-Type": "application/json"},
        timeout=None
    )
    resp.raise_for_status()
    return adapterBucketSlotGuessResult.validate_json(resp.content)
