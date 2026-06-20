"""Single source of truth for turning a tool name into a URL slug.

This MUST stay in sync with the TypeScript implementation in
`site/src/lib/tools.ts`. Both derive the slug as:

    lowercase -> replace runs of non-word chars with "-" -> trim leading/trailing "-"

The canonical slug is also written into tools.json (the `slug` field) by
process_dennet.py, so downstream code should prefer reading that field rather
than recomputing it.
"""

import re


def slugify(text: str) -> str:
    """Convert a tool name to a filesystem/URL-safe slug."""
    return re.sub(r"[\W_]+", "-", text.lower()).strip("-")
