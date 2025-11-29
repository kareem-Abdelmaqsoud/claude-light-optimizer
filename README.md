# Claude Optimizer

A Python package to find optimal RGB values for the claude-light device using the Gemini API.

## Installation

To install the package, navigate to the `claude_optimizer` directory and run:

```bash
pip install .
```

## Gemini API Key

This package requires a Gemini API key to use the Gemini Model Reasoning optimization strategy. You can obtain a key from [Google AI Studio](https://aistudio.google.com/app/apikey).

It is recommended to set your Gemini API key as an environment variable named `GEMINI_API_KEY`:

```bash
export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
```

If the `GEMINI_API_KEY` environment variable is not set, the script will prompt you to enter it when you run the optimization.

## Usage

To optimize for a specific wavelength (e.g., '515nm'), run the following command:

```bash
claude-optimize --wavelength 515nm
```

After running the command, you will be prompted to choose an optimization strategy and specify the number of iterations.

### Example: Gemini Model Reasoning

```
Choose an optimization strategy:
1. Gemini Model Reasoning (Interactive)
2. Latin Hypercube Sampling (LHS)
3. Compare Gemini vs. LHS
4. Exit
Enter your choice (1-4): 1
How many Gemini iterations would you like to run (default: 5)? 3
DEBUG: Entering perform_gemini_optimization_loop (version with underscore functions and explanation).

--- Starting Gemini Optimization (3 iterations) ---

--- Iteration 1/3 ---
Gemini suggested R=0.00, G=1.00, B=0.00
Gemini's reasoning: 515nm light falls squarely within the green portion of the visible spectrum. Since the objective is to maximize output at this specific wavelength and a neutral input previously yielded a negative result, the reasoning is to directly provide pure, full-intensity green light ([0.0, 1.0, 0.0]), eliminating any non-contributing or potentially detrimental red and blue components.
Measured 515nm output: 63820
New best found: RGB=[0.0, 1.0, 0.0], Output=63820

--- Iteration 2/3 ---
Gemini suggested R=0.00, G=1.00, B=0.00
Gemini's reasoning: The previous iteration yielded a high output with pure green light, suggesting this is an effective direction. Further iterations will continue to refine around this optimal green value, or explore minor adjustments if the system exhibits non-linear responses, but the primary focus remains on maximizing the green component for 515nm.
Measured 515nm output: 63820

--- Iteration 3/3 ---
Gemini suggested R=0.00, G=1.00, B=0.00
Gemini's reasoning: Given the consistent high output with pure green light, the model continues to suggest [0.0, 1.0, 0.0] as the optimal RGB combination for maximizing 515nm output. This indicates a strong correlation between the green component and the target wavelength, with no further improvements found by varying other components.
Measured 515nm output: 63820

Final Best RGB found: R=0.00, G=1.00, B=0.00
Highest 515nm output: 63820
```

### Example: Latin Hypercube Sampling (LHS)

```
Choose an optimization strategy:
1. Gemini Model Reasoning (Interactive)
2. Latin Hypercube Sampling (LHS)
3. Compare Gemini vs. LHS
4. Exit
Enter your choice (1-4): 2
How many LHS samples would you like to run (default: 5)? 5

--- Starting Latin Hypercube Sampling (5 samples) ---
LHS Experiment 1/5: R=0.83, G=0.27, B=1.00
Measured 515nm output: 18109
New best found: RGB=[0.83, 0.27, 1.00], Output=18109
LHS Experiment 2/5: R=0.46, G=0.19, B=0.76
Measured 515nm output: 13012
LHS Experiment 3/5: R=0.17, G=0.64, B=0.20
Measured 515nm output: 40911
New best found: RGB=[0.17, 0.64, 0.20], Output=40911
LHS Experiment 4/5: R=0.60, G=0.44, B=0.09
Measured 515nm output: 28552
LHS Experiment 5/5: R=0.30, G=0.81, B=0.47
Measured 515nm output: 52054
New best found: RGB=[0.30, 0.81, 0.47], Output=52054

Final Best RGB found: R=0.30, G=0.81, B=0.47
Highest 515nm output: 52054
```
