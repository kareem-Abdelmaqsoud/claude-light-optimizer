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
3. Bayesian Optimization
4. Compare Gemini, LHS, and Bayesian
5. Exit
Enter your choice (1-5): 1
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
3. Bayesian Optimization
4. Compare Gemini, LHS, and Bayesian
5. Exit
Enter your choice (1-5): 2
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

### Example: Bayesian Optimization

```
Choose an optimization strategy:
1. Gemini Model Reasoning (Interactive)
2. Latin Hypercube Sampling (LHS)
3. Bayesian Optimization
4. Compare Gemini, LHS, and Bayesian
5. Exit
Enter your choice (1-5): 3
How many Bayesian optimization iterations would you like to run (minimum: 10, default: 5)? 10

--- Starting Bayesian Optimization (10 iterations) ---
Bayesian Optimization finished. Best RGB: [0.0, 1.0, 0.0], Best Output: 63820

Final Best RGB found: R=0.00, G=1.00, B=0.00
Highest 515nm output: 63820
```

### Example: Compare Gemini, LHS, and Bayesian

```
Choose an optimization strategy:
1. Gemini Model Reasoning (Interactive)
2. Latin Hypercube Sampling (LHS)
3. Bayesian Optimization
4. Compare Gemini, LHS, and Bayesian
5. Exit
Enter your choice (1-5): 4
How many iterations/samples for the comparison (default: 10)? 10

--- Comparing Gemini vs. LHS vs. Bayesian Optimization (10 iterations/samples each) ---
DEBUG: Entering perform_gemini_optimization_loop (version with underscore functions and explanation).

--- Starting Gemini Optimization (10 iterations) ---

--- Iteration 1/10 ---
Gemini suggested R=1.00, G=0.00, B=0.00
Gemini's reasoning: My reasoning for suggesting [1.0, 0.0, 0.0] is that 630nm corresponds to deep red light. Given the objective to maximize this output, and that the current best output is a negative value indicating extremely poor or non-existent performance, applying the maximum pure red stimulus is the most direct and aggressive initial step to attempt to elicit a positive 630nm response by heavily biasing the input towards the target wavelength.
Measured 630nmnm output: 29356
New best found: RGB=[1.0, 0.0, 0.0], Output=29356

--- Iteration 2/10 ---
Gemini suggested R=1.00, G=0.00, B=0.00
Gemini's reasoning: The suggested values of [1.0, 0.0, 0.0] correspond to pure red light. Given that 630nm falls squarely within the red spectrum, maximizing output at this specific wavelength inherently favors an absence of green and blue light, as these would either shift the dominant wavelength or dilute the red intensity. The fact that the current best output was already achieved with [1.0, 0.0, 0.0] confirms that this configuration is currently the most effective, making it the logical choice to reiterate for maximizing 630nm production.
Measured 630nmnm output: 29362
New best found: RGB=[1.0, 0.0, 0.0], Output=29362

--- Iteration 3/10 ---
Gemini suggested R=1.00, G=0.00, B=0.00
Gemini's reasoning: The suggested values introduce a minute amount of green to the previously optimized pure red output. This is an exploratory step to determine if a slight spectral perturbation or a subtle synergistic effect between red and a minimal green component could further enhance the 630nm output beyond what pure red alone provides, searching for an optimal blend without significantly diluting the primary red contribution.
Measured 630nmnm output: 29389
New best found: RGB=[1.0, 0.001, 0.0], Output=29389

--- Iteration 4/10 ---
Gemini suggested R=1.00, G=0.00, B=0.00
Gemini's reasoning: Given that 630nm falls squarely in the red spectrum, my reasoning is to eliminate any potentially non-contributory or counterproductive light inputs. The current best value has a minute green component (0.001). Since green light does not typically enhance red output and could potentially dilute or interfere with the desired red light production, setting the green value to 0.0 aims to provide an even purer red stimulus, thereby optimizing the system solely for 630nm output and maximizing efficiency.
Measured 630nmnm output: 29375

--- Iteration 5/10 ---
Gemini suggested R=1.00, G=0.00, B=0.00
Gemini's reasoning: To maximize 630nm output, which is squarely in the red spectrum, the proposed values maintain maximum red (1.0) and zero blue, while eliminating the minuscule trace of green (0.001) present in the previous best. This change is based on the assumption that any non-red light, even in tiny amounts, is either neutral or potentially detrimental to the highly specific 630nm output, thus purifying the light source to focus solely on the most relevant color component.
Measured 630nmnm output: 29384

--- Iteration 6/10 ---
Gemini suggested R=1.00, G=0.00, B=0.00
Gemini's reasoning: Given that 630nm light falls squarely within the red spectrum, the suggested RGB values of [1.0, 0.0, 0.0] aim to maximize this output by exclusively driving the red LED channel. The previous best of [1.0, 0.001, 0.0] was already extremely close to pure red, so reducing the minute 0.001 green component to zero is a logical refinement, as any green light would not contribute to (and could potentially dilute the purity or efficiency of) the desired 630nm red output.
Measured 630nmnm output: 29406
New best found: RGB=[1.0, 0.0, 0.0], Output=29406

--- Iteration 7/10 ---
Gemini suggested R=1.00, G=0.00, B=0.00
Gemini's reasoning: The suggestion `[1.0, 0.001, 0.0]` is a minimal perturbation from the current best `[1.0, 0.0, 0.0]`. With red already maximized as the dominant contributor to 630nm output and blue assumed unhelpful, this slight increment of green is introduced to probe for a subtle synergistic effect or a more efficient spectral balance that could further optimize the overall system's 630nm emission, testing if the current peak is a true global maximum or if a slight modification can yield higher output.
Measured 630nmnm output: 29391

--- Iteration 8/10 ---
Gemini suggested R=1.00, G=1.00, B=1.00
Gemini's reasoning: My reasoning is to test if the combined spectral output of all three LEDs at full intensity, or any non-linear system interaction, can yield a higher 630nm measurement than relying solely on the red channel. This explores if the previous `[1.0, 0.0, 0.0]` was a local maximum and if the green and blue components contribute to the target wavelength, even indirectly, within the system.
Measured 630nmnm output: 31416
New best found: RGB=[1.0, 1.0, 1.0], Output=31416

--- Iteration 9/10 ---
Gemini suggested R=1.00, G=1.00, B=1.00
Gemini's reasoning: My suggestion of `[1.0, 1.0, 1.0]` is based on the fact that these values represent the maximum possible intensity for all Red, Green, and Blue channels. Given that the current best output of 31416 for 630nm was already achieved at this maximum setting, it indicates that we've reached the upper limit of what can be produced by simply increasing the RGB input values.
Measured 630nmnm output: 31428
New best found: RGB=[1.0, 1.0, 1.0], Output=31428

--- Iteration 10/10 ---
Gemini suggested R=1.00, G=0.00, B=0.00
Gemini's reasoning: The suggestion of `[1.0, 0.0, 0.0]` (pure red) is based on the fact that 630 nanometers falls squarely within the red light spectrum. To maximize output at this specific wavelength, it is logical to activate only the red LED component at its highest intensity (1.0), while setting the green and blue components to zero (0.0), as their wavelengths are significantly shorter and would not contribute to, or could even dilute, the desired 630nm output.
Measured 630nmnm output: 29387

Gemini Final Best RGB: [1.0, 1.0, 1.0], Output: 31428

--- Starting Latin Hypercube Sampling (10 samples) ---
LHS Experiment 1/10: R=0.95, G=0.29, B=0.45
Measured 630nmnm output: 28334
New best found: RGB=[np.float64(0.9471139065809467), np.float64(0.29357749469746613), np.float64(0.4533897014179164)], Output=28334
LHS Experiment 2/10: R=0.35, G=0.53, B=0.39
Measured 630nmnm output: 11309
LHS Experiment 3/10: R=0.59, G=0.68, B=0.52
Measured 630nmnm output: 18547
LHS Experiment 4/10: R=0.10, G=0.90, B=0.03
Measured 630nmnm output: 4520
LHS Experiment 5/10: R=0.04, G=0.16, B=0.13
Measured 630nmnm output: 1662
LHS Experiment 6/10: R=0.88, G=0.34, B=0.22
Measured 630nmnm output: 26371
LHS Experiment 7/10: R=0.60, G=0.08, B=0.66
Measured 630nmnm output: 18162
LHS Experiment 8/10: R=0.42, G=0.89, B=0.82
Measured 630nmnm output: 14054
LHS Experiment 9/10: R=0.27, G=0.72, B=0.76
Measured 630nmnm output: 9738
LHS Experiment 10/10: R=0.73, G=0.47, B=0.97
Measured 630nmnm output: 22414

LHS Final Best RGB: [np.float64(0.9471139065809467), np.float64(0.29357749469746613), np.float64(0.4533897014179164)], Output: 28334

--- Starting Bayesian Optimization (10 iterations) ---
Bayesian Optimization finished. Best RGB: [0.8472517387841256, 0.6235636967859725, 0.38438170729269994], Best Output: 25853

Bayesian Final Best RGB: [0.8472517387841256, 0.6235636967859725, 0.38438170729269994], Output: 25853

--- Comparison Results ---
The winning strategy is Gemini with highest 630nmnm output: 31428

Overall Best RGB found: R=1.00, G=1.00, B=1.00
Overall Highest 630nmnm output: 31428
Winning Strategy: Gemini
```
