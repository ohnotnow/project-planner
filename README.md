# Project Planner

A command-line tool that automates the generation of project artifacts—Business Requirement Document (BRD), Product Requirement Document (PRD), User Stories, and Coding Instructions—using lightweight LLM agents. Given a specification file, it orchestrates multiple agents to produce structured outputs in a timestamped directory under `output/`.

## Features

- Generates BRD, PRD, user stories, and coding instructions  
- Uses [litellm](https://github.com/astral-sh/litellm) for model inference  
- Template-driven output with Jinja2  
- Pydantic-based validation  
- Timestamped, unique output directories  

## Repository

```bash
git clone https://github.com/ohnotnow/project-planner.git
cd project-planner
```

## Prerequisites

- Git
- Python 3.8 or later
- `uv` (Astral’s modern CLI tool; see https://docs.astral.sh/uv/)
- (Optional) Set your OpenAI API key if using OpenAI backends:
  ```bash
  export OPENAI_API_KEY="your_api_key_here"   # macOS / Linux
  setx OPENAI_API_KEY "your_api_key_here"     # Windows PowerShell
  ```

## Installation

Install dependencies and prepare the environment via `uv`:

macOS / Ubuntu / Windows (PowerShell / CMD):

```bash
# From project root
uv sync
```

This installs all Python packages defined in `pyproject.toml` (including litellm, jinja2, pydantic, etc.).

## Usage

Run the main script to generate project artifacts. By default it reads `spec.md` in the project root.

```bash
# Basic usage (uses spec.md)
uv run main.py

# Specify a custom spec file
uv run main.py -- --spec path/to/your_spec.md
```

Options and flags:

  • `--spec`  
    Path to the Markdown specification file.  
    Default: `spec.md`

Outputs are saved under `output/<generated_name>_<YYYY-MM-DD_HH-MM-SS>/`.  
At the end of execution you’ll see total cost and runtime.

## Project Structure

```
.
├── agents/
│   ├── brd.py
│   ├── prd.py
│   ├── user_stories.py
│   └── coding_instructions.py
├── output/             # Generated outputs
├── spec.md             # Sample spec file (optional)
├── main.py             # Entry point
├── pyproject.toml      # Python project manifest
└── README.md
```

## License

This project is licensed under the MIT License.  
See [LICENSE](LICENSE) for details.
