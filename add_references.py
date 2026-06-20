"""Append a References section to each tool's markdown file.

Scans each tool's `detailed_description` for footnote-style citation markers
(a number attached to the end of a word, e.g. "mistakes.6") and matches them
against the "Works cited" list parsed from dennet.txt. Only citation numbers
that actually exist in that list are emitted.

Idempotent: skips files that already contain a References section.
"""

import json
import os
import re

from slugify import slugify

SOURCE_FILE = "dennet.txt"
CONTENT_DIR = "content"
TOOLS_FILE = "tools.json"


def parse_citations(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    citations = {}
    in_works_cited = False

    for line in lines:
        if "Works cited" in line:
            in_works_cited = True
            continue

        if in_works_cited:
            line = line.strip()
            if not line:
                continue

            # Format: "1. Title - Author ..."
            match = re.match(r"^(\d+)\.\s+(.+)", line)
            if match:
                citations[match.group(1)] = match.group(2)

    return citations


def find_citation_numbers(description):
    """Return the set of footnote numbers referenced in the description text.

    Footnotes appear as a number attached to the end of a word, e.g.
    "mistakes.6" or "parody.2". We deliberately only match the
    `<word-char>.<digits>` pattern to avoid sweeping up ordinary numbers.
    """
    return set(re.findall(r"\w\.(\d+)", description))


def build_references_section(numbers, citations):
    lines = ["\n\n## References\n"]
    for num in sorted(numbers, key=int):
        ref_text = citations[num]
        url_match = re.search(r"(https?://\S+)", ref_text)
        if url_match:
            url = url_match.group(1)
            text_display = ref_text.replace(url, "").strip().strip(",").strip("-").strip()
            # Guard against empty link text producing "[]( ... )".
            if not text_display:
                text_display = url
            lines.append(f"- [{text_display}]({url})\n")
        else:
            lines.append(f"- {ref_text}\n")
    return "".join(lines)


def main():
    citations = parse_citations(SOURCE_FILE)
    print(f"Found {len(citations)} citations.")

    with open(TOOLS_FILE, "r") as f:
        tools = json.load(f)

    for tool in tools:
        slug = tool.get("slug") or slugify(tool["name"])
        filename = os.path.join(CONTENT_DIR, f"{slug}.md")

        if not os.path.exists(filename):
            print(f"File not found: {filename}")
            continue

        with open(filename, "r") as f:
            content = f.read()

        if "## References" in content:
            print(f"References already in {slug}")
            continue

        numbers = find_citation_numbers(tool.get("detailed_description", ""))
        valid_numbers = [n for n in numbers if n in citations]

        if not valid_numbers:
            continue

        ref_section = build_references_section(valid_numbers, citations)
        with open(filename, "w") as f:
            f.write(content + ref_section)
        print(f"Added references to {slug}")


if __name__ == "__main__":
    main()
