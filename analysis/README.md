# Analyze pipe benchmark data with uv

This folder is a small [uv](https://docs.astral.sh/uv/) project for the CSV
analysis script. `uv` creates a local `analysis/.venv` and installs the Python
packages listed in `pyproject.toml`. You do not need to activate the environment
or install those packages globally.

## Install uv

On Linux or macOS, use the [official installation instructions](https://docs.astral.sh/uv/getting-started/installation/).
One supported installation command is:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Open a new terminal, then check `uv --version`. If `curl` is unavailable, the
official installation page also gives a `wget` command. The analysis project
requires Python 3.12 or newer; `uv` can install a compatible Python if your
system does not have one.

## Run the analysis

From the **repository root**, after producing `bench-results/pipe.csv` with
`bench_pipe` or receiving a fallback CSV from the instructor:

```bash
uv sync --project analysis --locked
uv run --project analysis --locked python analysis/analyze.py bench-results/pipe.csv \
  --plot bench-results/throughput.png
```

`uv sync` downloads the locked dependencies into `analysis/.venv`. `uv run`
uses that environment and runs the script. Inspect the printed summary, the
raw CSV, and the saved plot. If the instructor gave you a fallback CSV, replace
`bench-results/pipe.csv` with its actual path and record its provenance in your
notes. Results from different machines are not directly comparable.

The lock file belongs in Git so the same dependency versions are used across
teams. Keep `.venv` and generated benchmark results local.
