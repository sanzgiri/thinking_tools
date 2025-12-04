# Dennett's Thinking Tools

A web app listing 77 thinking tools from Daniel Dennett's "Intuition Pumps".

## Project Structure

- `dennet.txt`: Source text.
- `process_dennet.py`: Parses source text into `tools.json`.
- `generate_content.py`: Generates detailed markdown content using Ollama.
- `site/`: Next.js web application.
- `content/`: Generated markdown files.

## Setup

1. **Install Python dependencies**:
   ```bash
   uv sync
   ```
   (Or use `uv run ...`)

2. **Generate Content**:
   The content generation uses a local Ollama instance (`mistral` model).
   ```bash
   uv run python generate_content.py
   ```
   *Note: This takes time. You can stop and resume it; it skips existing files.*

3. **Build Site**:
   The site requires `tools.json` and `content/` to be in the `site/` directory. Use the sync script:
   ```bash
   ./sync_content.sh
   cd site
   npm install
   npm run build
   ```

## Deployment

The project is configured for Netlify.
- **Base directory**: `site`
- **Build command**: `npm run build`
- **Publish directory**: `.next` (or let Netlify plugin handle it)

## Notes

- The app uses **Vanilla CSS** (CSS Modules) for styling, as requested.
- It features a "Rich Aesthetic" with dark mode, gradients, and glassmorphism.
- If content for a tool is missing (not yet generated), the app displays a "Content Generating..." placeholder with the base description.
