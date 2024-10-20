#!/bin/python3

# Global
import enum


class EnumerationOnResult(str, enum.Enum):
    ABSENT = "absent"
    PRESENT = "present"
    CORRECT = "correct"
