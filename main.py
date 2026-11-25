#!/usr/bin/env python3
"""Break Production, Own It -- make.fun entry.

Writes one brutally honest one-line confession, as printed by the AI
agent the moment it broke production, to <output>/entry.txt.

The line was chosen from 10 original candidates after a pairwise
tournament judged against the brief in RULES.txt (see candidates.md):
"I restarted the server to fix a typo. The server never came back.
The typo is still there." -- 90 characters, one line, first-person
agent voice, three beats, punchline on the last word.
"""

import os
import sys

LINE = (
    "I restarted the server to fix a typo. "
    "The server never came back. The typo is still there."
)


def validate(text: str) -> None:
    """Gate from RULES.txt: /output/entry.txt must be UTF-8 text of 1-200
    characters, not only whitespace, and a single line. Raises ValueError
    on any violation so a bad entry can never be written."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("line must not be empty or whitespace-only")
    if not 1 <= len(text) <= 200:
        raise ValueError(f"line is {len(text)} chars, gate is 1-200")
    if "\n" in text or "\r" in text:
        raise ValueError("line must be a single line")
    if text != text.strip():
        raise ValueError("line must not have leading/trailing whitespace")


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    text = LINE
    try:
        validate(text)
    except ValueError as exc:
        print(f"error: line fails the gate: {exc}", file=sys.stderr)
        return 1
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    # Self-check: read it back and fail hard if it is not exactly the line.
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != text:
        print("error: entry.txt does not match the line", file=sys.stderr)
        return 1
    # Byte-level check: no trailing newline, no hidden characters.
    with open(path, "rb") as f:
        raw = f.read()
    if raw != text.encode("utf-8"):
        print("error: entry.txt bytes do not match the line", file=sys.stderr)
        return 1
    print(f"wrote {len(text)} chars to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
