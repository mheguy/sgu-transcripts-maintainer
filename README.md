# sgu-transcripts-maintainer

<!-- Cronitor badge ![sgu-transcripts-maintainer]() -->

This tool helps maintain the transcriptions within <https://www.sgutranscripts.org><br>
This tool is a fan creation and is neither endorsed by nor associated with the creators of the podcast.<br>

## How it works

This explanation is targeted toward those who have no experience writing or reading code.<br>

## Development

The project uses Python 3.13.<br>
UV is used to manage dependencies.<br>
Ruff and Pyright should be used for linting and type checking, respectively.<br>
Install, run linting, type checking, and tests: `uv sync --locked --all-extras --dev && uv run ruff check && uv run pyright && uv run ruff format && uv run pytest`<br>
