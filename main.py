"""Run the full content pipeline end to end.

Usage:
    uv run python main.py [steps]

Steps (default: parse generate):
    parse       Parse dennet.txt -> tools.json (process_dennet.main)
    generate    Generate markdown via Ollama (generate_content.main)
    references  Append References sections (add_references.main)
    clean       Strip References sections (remove_references.main)

Examples:
    uv run python main.py                 # parse + generate
    uv run python main.py parse           # just (re)build tools.json
    uv run python main.py parse generate references
"""

import sys

import process_dennet
import generate_content
import add_references
import remove_references

STEPS = {
    "parse": process_dennet.main,
    "generate": generate_content.main,
    "references": add_references.main,
    "clean": remove_references.main,
}

DEFAULT_STEPS = ["parse", "generate"]


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    steps = argv or DEFAULT_STEPS

    unknown = [s for s in steps if s not in STEPS]
    if unknown:
        print(f"Unknown step(s): {', '.join(unknown)}")
        print(f"Available steps: {', '.join(STEPS)}")
        return 1

    for step in steps:
        print(f"\n=== Running step: {step} ===")
        STEPS[step]()

    print("\nDone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
