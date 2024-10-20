#!/bin/python3

# External
from pydantic import BaseModel, Field, TypeAdapter

# Internal
from _enum import EnumerationOnResult


class ModelSlotGuessResult(BaseModel):
    slot: int = Field(default=..., description="The slot position of the character")
    guess: str = Field(default=..., description="The guessed character")
    result: EnumerationOnResult = Field(default=EnumerationOnResult.PRESENT, description="The state of the character in the word")

# Define adapter bucket
adapterBucketSlotGuessResult = TypeAdapter(list[ModelSlotGuessResult])
