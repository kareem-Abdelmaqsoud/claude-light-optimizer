import requests
import os
import google.generativeai as genai
import numpy as np
import argparse
from scipy.stats.qmc import LatinHypercube

CLAUDE_LIGHT_URL = "https://claude-light.cheme.cmu.edu"

def get_gemini_api_key():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        api_key = input("Please enter your Gemini API Key: ")
        os.environ["GEMINI_API_KEY"] = api_key
    return api_key

def list_available_gemini_models():
    """Lists and prints available Gemini models."""
    print("\n--- Listing Available Gemini Models ---")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Model: {m.name}, Supported methods: {m.supported_generation_methods}")
    except Exception as e:
        print(f"Error listing models: {e}")
    print("---------------------------------------")

def claude_light_measure(r, g, b):
    """Performs a measurement with claude-light for given RGB values."""
    try:
        response = requests.get(f"{CLAUDE_LIGHT_URL}/api", params={"R": r, "G": g, "B": b})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Claude-light API Call Failed: {e}")
        return None

def _gemini_suggest_rgb(model, best_rgb, best_output, target_wavelength):
    """Prompts Gemini for new RGB values."""
    prompt = f"""
    Current best RGB for {target_wavelength}nm is {best_rgb} with output {best_output}.
    Suggest new R, G, B values (between 0.0 and 1.0, inclusive, as floats) to maximize the {target_wavelength}nm output.
    Provide the values as a comma-separated string, e.g., "0.1,0.2,0.3".
    Do not include any other text in your response.
    """
    response = model.generate_content(prompt)
    suggested_rgb_str = response.text.strip()
    suggested_rgb = [float(x) for x in suggested_rgb_str.split(',')]
    return [max(0.0, min(1.0, val)) for val in suggested_rgb]

def _gemini_explain_choice(model, suggested_rgb, best_rgb, best_output, target_wavelength):
    """Prompts Gemini for an explanation of its choice."""
    explanation_prompt = f"""
    You just suggested RGB values {suggested_rgb} to maximize {target_wavelength}nm output, given the current best RGB was {best_rgb} with output {best_output}.
    Explain your reasoning for these suggested values in one concise paragraph.
    """
    explanation_response = model.generate_content(explanation_prompt)
    return explanation_response.text.strip()

def perform_gemini_optimization_loop(model, target_wavelength, initial_rgb, initial_best_output, iterations):
    print("DEBUG: Entering perform_gemini_optimization_loop (version with underscore functions and explanation).")
    """
    Performs a set of optimization iterations using Gemini.
    """
    best_rgb = list(initial_rgb) # Ensure it's a mutable list
    best_output = initial_best_output
    current_rgb = list(initial_rgb)

    print(f"\n--- Starting Gemini Optimization ({iterations} iterations) ---")

    for i in range(iterations):
        print(f"\n--- Iteration {i+1}/{iterations} ---")
        
        try:
            suggested_rgb = _gemini_suggest_rgb(model, best_rgb, best_output, target_wavelength)
            r, g, b = suggested_rgb
            print(f"Gemini suggested R={r:.2f}, G={g:.2f}, B={b:.2f}")

            explanation = _gemini_explain_choice(model, suggested_rgb, best_rgb, best_output, target_wavelength)
            print(f"Gemini's reasoning: {explanation}")

            measurement = claude_light_measure(r, g, b)

            if measurement and target_wavelength in measurement['out']:
                current_output = measurement['out'][target_wavelength]
                print(f"Measured {target_wavelength}nm output: {current_output}")

                if current_output > best_output:
                    best_output = current_output
                    best_rgb = suggested_rgb
                    print(f"New best found: RGB={best_rgb}, Output={best_output}")
            else:
                print("Measurement failed or target wavelength not found in output.")

        except Exception as e:
            print(f"Error during Gemini interaction or parsing: {e}")
            current_rgb = [max(0.0, min(1.0, val + np.random.uniform(-0.1, 0.1))) for val in current_rgb]
            best_rgb = current_rgb
            best_output = -1

    return best_rgb, best_output

def run_lhs_optimization(target_wavelength, num_samples):
    """
    Performs Latin Hypercube Sampling optimization.
    """
    print(f"\n--- Starting Latin Hypercube Sampling ({num_samples} samples) ---")
    sampler = LatinHypercube(d=3) # 3 dimensions for R, G, B
    lhs_samples = sampler.random(n=num_samples) # Samples between 0 and 1

    best_rgb = [0.0, 0.0, 0.0]
    best_output = -1
    all_results = [] # Not used for returning, but good for internal tracking

    for i, sample in enumerate(lhs_samples):
        r, g, b = sample
        print(f"LHS Experiment {i+1}/{num_samples}: R={r:.2f}, G={g:.2f}, B={b:.2f}")
        measurement = claude_light_measure(r, g, b)

        if measurement and target_wavelength in measurement['out']:
            current_output = measurement['out'][target_wavelength]
            print(f"Measured {target_wavelength}nm output: {current_output}")
            all_results.append({'R': r, 'G': g, 'B': b, 'Output': current_output})

            if current_output > best_output:
                best_output = current_output
                best_rgb = [r, g, b]
                print(f"New best found: RGB={best_rgb}, Output={best_output}")
        else:
            print("Measurement failed or target wavelength not found in output.")

    return best_rgb, best_output

def compare_optimization_methods(model, target_wavelength, iterations):
    """
    Compares Gemini and LHS optimization methods.
    """
    print(f"\n--- Comparing Gemini vs. LHS Optimization ({iterations} iterations/samples each) ---")

    # Run Gemini Optimization
    gemini_best_rgb, gemini_best_output = perform_gemini_optimization_loop(
        model, target_wavelength, [0.5, 0.5, 0.5], -1, iterations
    )
    print(f"\nGemini Final Best RGB: {gemini_best_rgb}, Output: {gemini_best_output}")

    # Run LHS Optimization
    lhs_best_rgb, lhs_best_output = run_lhs_optimization(
        target_wavelength, iterations
    )
    print(f"\nLHS Final Best RGB: {lhs_best_rgb}, Output: {lhs_best_output}")

    print("\n--- Comparison Results ---")
    if gemini_best_output > lhs_best_output:
        print(f"Gemini performed better! Highest {target_wavelength}nm output: {gemini_best_output}")
        return gemini_best_rgb, gemini_best_output, "gemini"
    elif lhs_best_output > gemini_best_output:
        print(f"LHS performed better! Highest {target_wavelength}nm output: {lhs_best_output}")
        return lhs_best_rgb, lhs_best_output, "lhs"
    else:
        print(f"Both methods achieved the same highest {target_wavelength}nm output: {gemini_best_output}")
        return gemini_best_rgb, gemini_best_output, "tie"

from skopt import gp_minimize
from skopt.space import Real

def run_bayesian_optimization(target_wavelength, num_iterations):
    """
    Performs Bayesian optimization using scikit-optimize.
    """
    print(f"\n--- Starting Bayesian Optimization ({num_iterations} iterations) ---")

    # Define the search space for R, G, B
    space = [Real(0.0, 1.0, name='R'),
             Real(0.0, 1.0, name='G'),
             Real(0.0, 1.0, name='B')]

    def objective_function(rgb):
        r, g, b = rgb
        measurement = claude_light_measure(r, g, b)
        if measurement and target_wavelength in measurement['out']:
            # gp_minimize minimizes, so we return the negative of the output
            return -measurement['out'][target_wavelength]
        return 0.0 # Return a neutral value if measurement fails

    res = gp_minimize(objective_function,
                      space,
                      n_calls=num_iterations,
                      random_state=0,
                      verbose=False)

    best_rgb = res.x
    best_output = -res.fun # Convert back to positive for actual output

    print(f"Bayesian Optimization finished. Best RGB: {best_rgb}, Best Output: {best_output}")
    return best_rgb, best_output

def compare_optimization_methods(model, target_wavelength, iterations):
    """
    Compares Gemini, LHS, and Bayesian optimization methods.
    """
    print(f"\n--- Comparing Gemini vs. LHS vs. Bayesian Optimization ({iterations} iterations/samples each) ---")

    # Run Gemini Optimization
    gemini_best_rgb, gemini_best_output = perform_gemini_optimization_loop(
        model, target_wavelength, [0.5, 0.5, 0.5], -1, iterations
    )
    print(f"\nGemini Final Best RGB: {gemini_best_rgb}, Output: {gemini_best_output}")

    # Run LHS Optimization
    lhs_best_rgb, lhs_best_output = run_lhs_optimization(
        target_wavelength, iterations
    )
    print(f"\nLHS Final Best RGB: {lhs_best_rgb}, Output: {lhs_best_output}")

    # Run Bayesian Optimization
    bayesian_best_rgb, bayesian_best_output = run_bayesian_optimization(
        target_wavelength, iterations
    )
    print(f"\nBayesian Final Best RGB: {bayesian_best_rgb}, Output: {bayesian_best_output}")

    print("\n--- Comparison Results ---")
    
    # Determine the best among all three
    all_results = {
        "gemini": {"rgb": gemini_best_rgb, "output": gemini_best_output},
        "lhs": {"rgb": lhs_best_rgb, "output": lhs_best_output},
        "bayesian": {"rgb": bayesian_best_rgb, "output": bayesian_best_output}
    }

    winning_strategy = "gemini"
    highest_output = gemini_best_output
    best_rgb = gemini_best_rgb

    if lhs_best_output > highest_output:
        highest_output = lhs_best_output
        best_rgb = lhs_best_rgb
        winning_strategy = "lhs"
    
    if bayesian_best_output > highest_output:
        highest_output = bayesian_best_output
        best_rgb = bayesian_best_rgb
        winning_strategy = "bayesian"

    print(f"The winning strategy is {winning_strategy.capitalize()} with highest {target_wavelength}nm output: {highest_output}")
    return best_rgb, highest_output, winning_strategy

def optimize_wavelength_cli():
    parser = argparse.ArgumentParser(description='Optimize Claude-light RGB values for a target wavelength using Gemini API, LHS, or Bayesian Optimization.')
    parser.add_argument('--wavelength', type=str, required=True, help='The target wavelength to optimize (e.g., 515nm).')
    parser.add_argument('--iterations', type=int, default=10, help='Number of optimization iterations for Gemini/Bayesian or samples for LHS.')
    parser.add_argument('--strategy', type=int, choices=[1, 2, 3, 4, 5], help='Optimization strategy: 1=Gemini, 2=LHS, 3=Bayesian, 4=Compare, 5=Exit')
    args = parser.parse_args()

    gemini_api_key = get_gemini_api_key()
    genai.configure(api_key=gemini_api_key)
    
    model_name = 'models/gemini-2.5-flash'
    gemini_model = None
    try:
        gemini_model = genai.GenerativeModel(model_name)
    except Exception as e:
        print(f"Error initializing Gemini model '{model_name}': {e}")
        list_available_gemini_models()
        print("Please check the available models and update the script with a valid model name if you wish to use Gemini.")
        # Do not return here, allow other options to proceed if Gemini fails

    target_wavelength = args.wavelength
    initial_iterations = args.iterations

    best_rgb = [0.5, 0.5, 0.5]
    best_output = -1

    if args.strategy:
        strategy_choice = str(args.strategy)
    else:
        print("\nChoose an optimization strategy:")
        print("1. Gemini Model Reasoning (Interactive)")
        print("2. Latin Hypercube Sampling (LHS)")
        print("3. Bayesian Optimization")
        print("4. Compare Gemini, LHS, and Bayesian")
        print("5. Exit")
        strategy_choice = input("Enter your choice (1-5): ").strip()

    if strategy_choice == '1':
        if gemini_model is None:
            print("Gemini model not initialized. Cannot perform Gemini optimization.")
        else:
            try:
                num_iterations = int(input(f"How many Gemini iterations would you like to run (default: {initial_iterations})? ") or initial_iterations)
                if num_iterations <= 0:
                    print("Number of iterations must be positive. Using default.")
                    num_iterations = initial_iterations
            except ValueError:
                print("Invalid input. Using default number of iterations.")
                num_iterations = initial_iterations
            best_rgb, best_output = perform_gemini_optimization_loop(gemini_model, target_wavelength, best_rgb, best_output, num_iterations)
            print(f"\nFinal Best RGB found: R={best_rgb[0]:.2f}, G={best_rgb[1]:.2f}, B={best_rgb[2]:.2f}")
            print(f"Highest {target_wavelength}nm output: {best_output}")
    elif strategy_choice == '2':
        try:
            num_samples = int(input(f"How many LHS samples would you like to run (default: {initial_iterations})? ") or initial_iterations)
            if num_samples <= 0:
                print("Number of samples must be positive. Using default.")
                num_samples = initial_iterations
        except ValueError:
            print("Invalid input. Using default number of samples.")
            num_samples = initial_iterations
        best_rgb, best_output = run_lhs_optimization(target_wavelength, num_samples)
        print(f"\nFinal Best RGB found: R={best_rgb[0]:.2f}, G={best_rgb[1]:.2f}, B={best_rgb[2]:.2f}")
        print(f"Highest {target_wavelength}nm output: {best_output}")
    elif strategy_choice == '3': # Bayesian Optimization
        min_bayesian_iterations = 10
        try:
            num_iterations = int(input(f"How many Bayesian optimization iterations would you like to run (minimum: {min_bayesian_iterations}, default: {initial_iterations})? ") or initial_iterations)
            if num_iterations < min_bayesian_iterations:
                print(f"Number of iterations must be at least {min_bayesian_iterations}. Setting to {min_bayesian_iterations}.")
                num_iterations = min_bayesian_iterations
        except ValueError:
            print(f"Invalid input. Using default number of iterations: {initial_iterations}.")
            num_iterations = initial_iterations
            if num_iterations < min_bayesian_iterations:
                num_iterations = min_bayesian_iterations
        best_rgb, best_output = run_bayesian_optimization(target_wavelength, num_iterations)
        print(f"\nFinal Best RGB found: R={best_rgb[0]:.2f}, G={best_rgb[1]:.2f}, B={best_rgb[2]:.2f}")
        print(f"Highest {target_wavelength}nm output: {best_output}")
    elif strategy_choice == '4': # Comparison option
        if gemini_model is None:
            print("Gemini model not initialized. Cannot perform comparison with Gemini.")
        else:
            try:
                compare_iterations = int(input(f"How many iterations/samples for the comparison (default: {initial_iterations})? ") or initial_iterations)
                if compare_iterations <= 0:
                    print("Number of iterations/samples must be positive. Using default.")
                    compare_iterations = initial_iterations
            except ValueError:
                print("Invalid input. Using default number of iterations/samples.")
                compare_iterations = initial_iterations
            best_rgb, best_output, winning_strategy = compare_optimization_methods(gemini_model, target_wavelength, compare_iterations)
            print(f"\nOverall Best RGB found: R={best_rgb[0]:.2f}, G={best_rgb[1]:.2f}, B={best_rgb[2]:.2f}")
            print(f"Overall Highest {target_wavelength}nm output: {best_output}")
            print(f"Winning Strategy: {winning_strategy.capitalize()}")
    elif strategy_choice == '5':
        print("Exiting optimizer. Goodbye!")
    else:
        print("Invalid strategy choice. Please enter a number between 1 and 5.")
