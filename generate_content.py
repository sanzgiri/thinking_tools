import json
import os
import tempfile
import time

import requests

from slugify import slugify

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL = "mistral:latest"
CONTENT_DIR = "content"
MAX_RETRIES = 3
RETRY_BACKOFF = 2  # seconds, multiplied by attempt number


def build_prompt(tool):
    return f"""
    You are an expert on Daniel Dennett's philosophy and his book "Intuition Pumps and Other Tools for Thinking".

    Your task is to write a detailed guide for the thinking tool: "{tool['name']}".

    Here is the base information provided:

    Category: {tool.get('category', 'N/A')}
    Short Description: {tool.get('short_description', 'N/A')}
    Base Description: {tool.get('detailed_description', 'N/A')}
    Base Exercise/App Idea: {tool.get('implementation_strategy', 'N/A')}

    Please expand on this to create a comprehensive guide (around 500 words).
    Consult your internal knowledge about this tool and Dennett's work.

    The output must be in Markdown format with the following sections:

    # {tool['name']}

    ## Brief Description
    (A concise summary, based on the short description but slightly expanded)

    ## Detailed Description
    (Elaborate on the base description. Explain the philosophical concept, the problem it solves, and why it is important. Use examples.)

    ## Exercise / How to Apply
    (Describe how a user can practice this tool. Use the "Base Exercise" provided as a starting point but make it a practical, actionable exercise for a human, not just an app feature.)

    ## Suggestion for Creating an App
    (Elaborate on the "Base App Idea". Describe how this could be built as a web or mobile app, what the features would be, and how it would gamify the concept.)

    Note: Do not include a "References" section unless you have specific citations.
    """


def is_valid_content(content, tool):
    """Reject obviously broken/truncated responses so we don't persist garbage.

    A valid response must be non-trivially long and contain the expected
    section structure produced by the prompt.
    """
    if not content or len(content.strip()) < 200:
        return False
    # The prompt asks for these markdown section headers.
    required_markers = ["## Brief Description", "## Detailed Description"]
    return all(marker in content for marker in required_markers)


def generate_content(tool):
    """Call Ollama with retries. Returns valid markdown or None."""
    payload = {
        "model": MODEL,
        "prompt": build_prompt(tool),
        "stream": False,
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
            response.raise_for_status()
            content = response.json().get("response", "")

            if is_valid_content(content, tool):
                return content

            print(
                f"  - Attempt {attempt}/{MAX_RETRIES}: response failed validation "
                f"(len={len(content.strip())}), retrying..."
            )
        except Exception as e:
            print(
                f"  - Attempt {attempt}/{MAX_RETRIES}: error generating content "
                f"for {tool['name']}: {e}"
            )

        if attempt < MAX_RETRIES:
            time.sleep(RETRY_BACKOFF * attempt)

    return None


def write_atomic(filename, content):
    """Write to a temp file in the same dir, then rename.

    This guarantees the resume logic never sees a half-written file: a file
    either exists complete or not at all.
    """
    directory = os.path.dirname(filename) or "."
    fd, tmp_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(content)
        os.replace(tmp_path, filename)
    except Exception:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


def main():
    if not os.path.exists(CONTENT_DIR):
        os.makedirs(CONTENT_DIR)

    with open("tools.json", "r") as f:
        tools = json.load(f)

    print(f"Found {len(tools)} tools. Starting generation...")

    failures = []
    for i, tool in enumerate(tools):
        # Prefer the canonical slug baked into tools.json; fall back for
        # backwards compatibility with older data files.
        slug = tool.get("slug") or slugify(tool["name"])
        filename = os.path.join(CONTENT_DIR, f"{slug}.md")

        if os.path.exists(filename):
            print(f"[{i + 1}/{len(tools)}] Skipping {tool['name']} (already exists)")
            continue

        print(f"[{i + 1}/{len(tools)}] Generating {tool['name']}...")
        content = generate_content(tool)

        if content:
            write_atomic(filename, content)
            print(f"  - Saved to {filename}")
        else:
            print(f"  - Failed to generate after {MAX_RETRIES} attempts.")
            failures.append(tool["name"])

        # small delay
        time.sleep(0.1)

    if failures:
        print(f"\n{len(failures)} tool(s) failed and can be retried on next run:")
        for name in failures:
            print(f"  - {name}")
    else:
        print("\nAll tools generated successfully.")


if __name__ == "__main__":
    main()
