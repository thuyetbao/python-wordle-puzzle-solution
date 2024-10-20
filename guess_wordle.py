#!/bin/python3

# Global
import sys
import os
import logging
from typing import Optional
from datetime import datetime
import string
import argparse
import textwrap

# Path
sys.path.append(os.getcwd())

# External
import structlog

# Internal
from _constant import COMPANY_NAME, PROJECT_NAME
from _enum import EnumerationOnResult
from _model import ModelSlotGuessResult
from _request import make_guess_random

# Set up
logging.basicConfig(level=logging.INFO)

# Config
structlog.configure(
    processors=[
        # Filter log entries by level
        structlog.stdlib.filter_by_level,
        # Add the name of the logger to the event dictionary
        structlog.stdlib.add_logger_name,
        # Add the log level to the event dictionary
        structlog.stdlib.add_log_level,
        # Merge context variables
        structlog.contextvars.merge_contextvars,
        # Perform %-style formatting
        structlog.stdlib.PositionalArgumentsFormatter(),
        # Add a timestamp in ISO 8601 format
        structlog.processors.TimeStamper(fmt="iso"),
        # Render stack info if the "stack_info" key is true
        structlog.processors.StackInfoRenderer(),
        # Render exception info if the "exc_info" key is true or a sys.exc_info() tuple
        structlog.processors.format_exc_info,
        # Decode bytes to Unicode strings
        structlog.processors.UnicodeDecoder(),
        # Render the log entry as Console formatted output
        structlog.dev.ConsoleRenderer(),
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    context_class=None,
    cache_logger_on_first_use=False
)

# Construct
LOG: structlog.stdlib.BoundLogger = structlog.get_logger()
structlog.contextvars.bind_contextvars(project=COMPANY_NAME, service=PROJECT_NAME)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="python guess_wordle.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""
        [Votee]::Guess random wordle

        Usage
        -----

        Make random guess with size and default seed
        >>> python guess_wordle.py --size 5

        Help
        >>> python guess_wordle.py --help
        """),
        epilog="Copyright (c) of Thuyet Bao"
    )
    parser.add_argument("--size", type=int, default=5, help="The size of the string to guess")
    parser.add_argument("--seed", type=int, default=1234, help="The seed value")
    parameters = parser.parse_args()

    # Constraint
    if parameters.size != 5:
        raise ValueError("The size of the string to guess must be 5. ")

    # Metadata
    LOG.info("Starting guess random wordle")

    # The targeted output
    GUESS_STRING: str = ""

    # Initation
    GUESS_STRING_SIZE = parameters.size
    GUESS_STRING_SEED = parameters.seed

    # Start time
    START_AT: datetime = datetime.now()

    # End time
    END_AT: Optional[datetime] = None

    # Container of characters
    GUESS_CHARACTER_CONTAINER: list[str] = [None] * GUESS_STRING_SIZE

    # Start bucket of character to guess
    GUESS_CHARACTER_POSSIBLE: list[str] = list(string.ascii_lowercase)

    # The set of guess that has been already guessed
    BUCKET_ALREADY_GUESS: set = set()

    # Number of attempts of guess
    NUMBER_GUESS_ATTEMPTS: int = 0
    os.environ.setdefault("NUMBER_GUESS_ATTEMPTS", str(NUMBER_GUESS_ATTEMPTS))

    # Override function guess
    def _internal_guess_random(word: str) -> list[ModelSlotGuessResult]:
        global NUMBER_GUESS_ATTEMPTS
        NUMBER_GUESS_ATTEMPTS += 1
        os.environ["NUMBER_GUESS_ATTEMPTS"] = str(NUMBER_GUESS_ATTEMPTS)
        return make_guess_random(word=word, size=GUESS_STRING_SIZE, seed=GUESS_STRING_SEED)

    # Then
    while True:

        # Handle
        if len(GUESS_CHARACTER_POSSIBLE) == 0:
            LOG.info("The bucket possible is empty")
            break

        # Start
        on_letter = GUESS_CHARACTER_POSSIBLE.pop(0) # Left to right

        # Define word based on fillted the container if None
        on_word = "".join([
            c if c is not None else on_letter
            for c in GUESS_CHARACTER_CONTAINER
        ])
        LOG.info(f"Guess: {on_word}")

        # Handle
        on_result = _internal_guess_random(word=on_word)

        # Update
        BUCKET_ALREADY_GUESS.add(on_letter)

        # Handle
        for elem in on_result:

            # Strategy: go to all element to:
            # (a) If exit CORRECT, push to GUESS_CHARACTER_CONTAINER with that position (slot is 0-based index too)
            # (b) If it present, continue to different
            # (c) If it absent, break go to another part

            if elem.result == EnumerationOnResult.PRESENT.value:
                LOG.info(f"Letter {elem.guess} present in the word at position {elem.slot}, but in a different position.")
                continue

            elif elem.result == EnumerationOnResult.ABSENT.value:
                LOG.info(f"Letter {elem.guess} not present in the word at position {elem.slot}. Break go to another part")
                try:
                    GUESS_CHARACTER_POSSIBLE.remove(elem.guess)
                except ValueError:
                    continue

            elif elem.result == EnumerationOnResult.CORRECT.value:
                LOG.info(f"Correct guess! Letter {elem.guess} is at position {elem.slot}")
                GUESS_CHARACTER_CONTAINER[elem.slot] = elem.guess
                BUCKET_ALREADY_GUESS.add(elem.guess)

    # Result
    GUESS_STRING = "".join(GUESS_CHARACTER_CONTAINER)
    END_AT = datetime.now()

    # Echo
    LOG.info(
        f"The result string: {GUESS_STRING}"
        f"\nTotal time: {(END_AT - START_AT).total_seconds()} seconds"
        f"\nTotal of attempts: {os.environ['NUMBER_GUESS_ATTEMPTS']} with length {GUESS_STRING_SIZE} and seed {GUESS_STRING_SEED}"
    )

    # Exit
    sys.exit(0)
