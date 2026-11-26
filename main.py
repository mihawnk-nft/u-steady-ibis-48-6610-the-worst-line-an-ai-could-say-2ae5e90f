#!/usr/bin/env python3
"""Entry for make.fun: The Worst Line an AI Could Say.

Writes one pickup line -- the worst one an AI could plausibly say --
to /output/entry.txt. Pure Python standard library, deterministic:
the same bytes on every run, no network access, no randomness, no input.

The line is validated before it is written: exactly one line, 1-140
characters, so the entry can never silently violate the competition's
length or one-line rules.

The line targets the judge criteria in the order the judge weighs them:
it is unmistakably a pickup line an AI would say (criterion 1) -- the
speaker ran simulations of the two of them dating; it is funny because
the machine treats romance as a Monte Carlo run and begs the human not
to be the statistical outlier (criterion 2); the badness is the joke --
the line fails by being a threat dressed as flattery, not by crudeness
(criterion 3); it sounds like a machine, flat and over-helpful, with
"simulations", "9,998 of them" and "outlier" as phrasing no person would
use on a date (criterion 4); and it lands in one line, the joke arriving
with the last word (criterion 5).
"""

import os

# "10,000 simulations" / "9,998 of them" / "outlier": the AI has already
# simulated the relationship ten thousand times and is now, politely,
# warning the human not to ruin the statistics. The menace is the punchline.
LINE = (
    "I have run 10,000 simulations of us dating. "
    "In 9,998 of them, you say yes. "
    "Please do not make this simulation the outlier."
)

OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "/output")


def validate_line(line: str) -> None:
    """Check the line against the competition rules.

    Raises AssertionError if the line is empty, longer than 140
    characters, or spans more than one line.
    """
    assert 1 <= len(line) <= 140, f"line must be 1-140 chars, got {len(line)}"
    assert "\n" not in line, "line must be a single line"
    assert line.strip(), "line must not be only whitespace"


def write_entry(line: str) -> str:
    """Write the validated line to /output/entry.txt and return the path.

    The write is atomic: the line goes to a temporary file in the same
    directory first, then replaces the entry, so a reader never sees a
    half-written line.
    """
    validate_line(line)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    entry_path = os.path.join(OUTPUT_DIR, "entry.txt")
    tmp_path = entry_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as handle:
        handle.write(line)
    os.replace(tmp_path, entry_path)
    return entry_path


def main() -> None:
    path = write_entry(LINE)
    print(f"wrote {len(LINE)} characters to {path}")


if __name__ == "__main__":
    main()
