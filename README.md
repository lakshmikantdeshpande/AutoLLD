# LLDGen: Automated Low-Level Design Generator

LLDGen is a Python tool that automates the generation of Low-Level Design (LLD) documents for code repositories. It leverages LLMs (such as Gemini or OpenAI models) to analyze code, generate detailed HTML LLDs, and ensure all diagrams (especially Mermaid diagrams) are valid and renderable.

## Features
- **Automated LLD Generation:** Parses source code and generates detailed, well-structured HTML LLDs.
- **Chunked Processing:** Processes large codebases in configurable chunks for scalability.
- **Parallel Execution:** Utilizes multi-threading for efficient LLD generation and merging.
- **Recursive Merging:** Merges LLDs recursively until a single, comprehensive document remains.
- **Mermaid Diagram Fixes:** Automatically fixes and validates all Mermaid diagrams in the final LLD using LLMs.
- **Configurable:** All key parameters (API keys, chunk size, model, etc.) are set in `config.py`.

## Requirements
- Python 3.8+
- See `requirements.txt` for dependencies:
  - `openai`
  - `backoff`
  - `gitpython`
  - `pyyaml`

Install dependencies with:
```sh
pip install -r requirements.txt
```

## Configuration
Edit `config.py` to set:
- `OPENAI_API_KEY_ENV`: Name of the environment variable holding your LLM API key.
- `OPENAI_BASE_URL`: Base URL for the LLM API (e.g., Gemini or OpenAI endpoint).
- `MODEL_NAME`: The LLM model to use (e.g., `gemini-2.0-flash`).
- `API_RATE_LIMIT_PER_MINUTE`: Requests per minute to respect API throttling.
- `CHUNK_SIZE`: Number of files per chunk for LLD generation/merging.

## Usage
```sh
python cli.py <repo_url> [--output <output_dir>]
```
- `<repo_url>`: URL of the git repository to process.
- `--output`: (Optional) Output directory for results (default: `./output`).

### Example
```sh
python cli.py https://github.com/example/repo.git --output ./my_lld_output
```

## Output
- The final LLD HTML is saved as `output/component-lld.html` (or your chosen output directory).
- Intermediate debug files and merged LLDs are stored in `output/debug/`.

## How It Works
1. **Clone & Parse:** Clones the repo and parses all project files.
2. **Chunk & Generate:** Splits files into chunks and generates LLDs for each chunk using the LLM.
3. **Recursive Merge:** Merges LLDs recursively until one remains.
4. **Fix Mermaid Diagrams:** Calls the LLM to fix and validate all Mermaid diagrams in the final HTML.
5. **Document Config:** Documents configuration properties found in the codebase.

## Notes
- Ensure your API key is set in your environment as specified in `config.py`.
- The tool is designed for extensibility and can be adapted for other LLM providers or custom prompts.

## License
MIT License
