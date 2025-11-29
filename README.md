# Claude Optimizer

A Python package to find optimal RGB values for the claude-light device using the Gemini API.

## Installation

To install the package, navigate to the `claude_optimizer` directory and run:

```bash
pip install .
```

## Usage

To optimize for a specific wavelength (e.g., '515nm'), run the following command:

```bash
claude-optimize --wavelength 515nm
```

The script will prompt you for your Gemini API key if it's not set as an environment variable (`GEMINI_API_KEY`).
