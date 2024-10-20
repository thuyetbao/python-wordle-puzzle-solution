#!/bin/python3

# Global

# External
import httpx

# Company name
COMPANY_NAME: str = "Votee"

# Project name
PROJECT_NAME: str = "wordle-random-guess"

# The origin of base API
BASE_ORIGIN_URL: httpx.URL = httpx.URL("https://wordle.votee.dev:8000")

# Documentation
DOCS_DOCUMENTATION_URL: str = BASE_ORIGIN_URL.join("/docs")
REDOC_DOCUMENTATION_URL: str = BASE_ORIGIN_URL.join("/redoc")

# The origin path route of the random
ROUTE_PATH: str = "/random"

# Size of string to guess
DEFAULT_LENGTH_STRING: int = 5

# The seed
DEFAULT_SEED: int = 1234
