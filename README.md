# Dennett's Thinking Tools

A web app listing 77 thinking tools from Daniel Dennett's "Intuition Pumps and Other Tools for Thinking".

## Project Structure

- `dennet.txt`: Source text.
- `slugify.py`: Single source of truth for turning a tool name into a URL slug (kept in sync with `site/src/lib/tools.ts`).
- `process_dennet.py`: Parses `dennet.txt` into `tools.json`, computing the canonical `slug` for each tool.
- `generate_content.py`: Generates detailed markdown content using Ollama (with retries, validation, and atomic writes).
- `add_references.py`: Appends a `## References` section to each tool's markdown, sourced from the "Works cited" list in `dennet.txt`.
- `remove_references.py`: Strips `## References` sections back out of the markdown.
- `main.py`: Pipeline runner that ties the above scripts together (see below).
- `sync_content.sh`: Copies `tools.json` and `content/` into `site/` so the app can read them.
- `content/`: Generated markdown files (one per tool, named `<slug>.md`).
- `site/`: Next.js web application.

## Setup

1. **Install Python dependencies**:
   ```bash
   uv sync
   ```
   (Or prefix commands with `uv run ...`.)

2. **Run the content pipeline**:
   `main.py` orchestrates the Python steps. The default (no args) runs `parse` then `generate`.
   ```bash
   uv run python main.py                 # parse + generate (default)
   uv run python main.py parse           # rebuild tools.json only (fast, no Ollama)
   uv run python main.py generate        # generate markdown via Ollama
   uv run python main.py references      # append References sections
   uv run python main.py clean           # strip References sections
   uv run python main.py parse generate references   # chain steps
   ```
   *Notes:*
   - Content generation uses a local Ollama instance (`mistral:latest` model), so Ollama must be running for the `generate` step.
   - Generation takes time. You can stop and resume it; it skips tools whose `content/<slug>.md` already exists. Failed/invalid responses are retried and are not written, so they will be retried on the next run.

3. **Build the site**:
   The site needs `tools.json` and `content/` copied into `site/`. Use the sync script:
   ```bash
   ./sync_content.sh
   cd site
   npm install
   npm run dev     # local preview at http://localhost:3000
   # or
   npm run build   # production build (static export of all 77 tool pages)
   ```

## Deployment

The project is deployed to **Netlify** and configured via `netlify.toml` (these settings come from the file, not the dashboard):

- **Base directory**: `.` (repo root, so the build can run `sync_content.sh`)
- **Build command**: `chmod +x sync_content.sh && ./sync_content.sh && cd site && npm install && npm run build`
- **Publish directory**: `site/.next`
- **Plugin**: `@netlify/plugin-nextjs`

Pushing to the `main` branch on GitHub triggers an automatic build and deploy.

## Notes

- The canonical tool slug is computed once in `process_dennet.py` and stored in `tools.json` (the `slug` field). All downstream code (content generation, references, the site) reads that field rather than recomputing it. `slugify.py` and `slugify()` in `site/src/lib/tools.ts` exist only as fallbacks and must be kept in sync.
- The app uses **Vanilla CSS** (CSS Modules) for styling.
- It features a "Rich Aesthetic" with dark mode, gradients, and glassmorphism.
- The homepage supports **live search** and **category filtering** (client-side, in `site/src/app/ToolBrowser.tsx`).
- Each tool page generates its own SEO metadata (`generateMetadata`) from the tool's name and short description.
- If content for a tool is missing, the tool page displays a "Content Generating..." placeholder with the base description. (With all 77 files generated, this is a fallback that is not normally shown.)
