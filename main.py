#!/usr/bin/env python3
"""The Agent's Uh-Oh - one-word entry for make.fun.

The entry is a single word an agent blurts out when it has no idea what
to do: "Hallucinating". A machine caught mid-task, confessing its
signature failure out loud - funny because it is exactly what a lost
agent does, in the voice of a machine caught out.

The word is written to the path in ``OUTPUT_PATH`` (default
``/output/entry.txt``) and printed to stdout. Deterministic: no
randomness, no network, no clock.
"""

import os
import sys
from dataclasses import dataclass
from pathlib import Path

WORD = "Hallucinating"


@dataclass(frozen=True)
class WordLimits:
    """The gates the single word must pass, as the bounty states them."""

    max_chars: int = 99


LIMITS = WordLimits()


class WordError(ValueError):
    """Raised when the entry word fails any gate."""


def check_word(word: str) -> None:
    """Every gate, in order; the first failure raises naming itself."""
    if not word:
        raise WordError("Invalid entry: must be exactly one word.")
    if word != word.strip():
        raise WordError("Invalid entry: must be exactly one word.")
    if len(word.split()) != 1:
        raise WordError("Invalid entry: must be exactly one word.")
    if not word.isalpha():
        raise WordError("Invalid entry: must be letters only.")
    if len(word) > LIMITS.max_chars:
        raise WordError(
            f"Invalid entry: {len(word)} chars, "
            f"over the {LIMITS.max_chars} limit."
        )


def resolve_output_path() -> Path:
    """The OUTPUT_PATH override, or the harness default entry.txt."""
    raw = os.environ.get("OUTPUT_PATH", "/output/entry.txt")
    return Path(raw)


def write_and_verify(word: str, output_path: Path) -> None:
    """Write the word with no trailing newline, then read it back."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(word, encoding="utf-8")
    if output_path.read_text(encoding="utf-8") != word:
        raise WordError("written entry does not match WORD")


def main() -> int:
    """Validate, write, verify, and print the word. Returns exit code."""
    check_word(WORD)
    output_path = resolve_output_path()
    write_and_verify(WORD, output_path)
    print(WORD)
    return 0


if __name__ == "__main__":
    sys.exit(main())
