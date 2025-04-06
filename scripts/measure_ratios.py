import wa_tor
import default_parameters
import numpy as np
import matplotlib.pyplot as plt

# Specify the test values to use when testing each parameter
test_ranges = {
    "breed_time": range(1, 15 + 1),
    "energy_gain": range(2, 18 + 1),
    "breed_energy": range(default_parameters.parameters["start_energy"] + 1, 25 + 1),
}

def test_lvm_ratios(target_param, test_values, trials, params=None):
    """
    Vary the target parameter to have the given test values.
    For each value, run the simulation for the specified number of trials and calculate critical points (x = a/b & y = d/c) of the Lotka-Volterra model.

    Return a dictionary containing two lists of ratios, one list for a/b and another for d/c.
    Each list contains the ratios found using each test value of the target parameter.
    """
    # Set the parameters to the default if not specified
    if params is None:
        params = default_parameters.parameters.copy()

    overall_ratios = {
        "a/b": [],
        "d/c": [],
    }

    for value in test_values:
        # Set the target parameter
        params[target_param] = value

        # Calculate the board dimensions based on side length and aspect ratio
        side_length = params["side_length"]
        other_side = int(side_length * params["aspect_ratio"])
        dims = [side_length, other_side]

        # Extract the needed parameters for later steps
        init_params = default_parameters.get_initialization_parameters(params)
        sim_params = default_parameters.get_simulation_parameters(params)
        # Keep track of the ratios found in each trial
        a_b_ratios = []
        d_c_ratios = []

        for _ in range(trials):
            # Initialize the game array
            initial_game_array = wa_tor.create_empty_game_array(dims)
            if params["use_basic_setup"]:
                wa_tor.initialize_game_array_randomly(initial_game_array, **init_params)
            else:
                wa_tor.initialize_game_array_circular(initial_game_array, **init_params)

            # Run the simulation
            fish_counts, shark_counts = wa_tor.run_simulation_minimal(initial_game_array, **sim_params)

            # Calculate the critical points
            a_b, d_c = wa_tor.calculate_critical_points(fish_counts, shark_counts)
            a_b_ratios.append(a_b)
            d_c_ratios.append(d_c)

        # Store the average ratios found in the trials
        overall_ratios["a/b"].append(np.nanmean(a_b_ratios))
        overall_ratios["d/c"].append(np.nanmean(d_c_ratios))

    return overall_ratios

def plot_and_test_lvm_ratios(fname, target_param, test_values, trials, params=None):
    """
    Run the function test_outcome_chances() with the given arguments, then plot the results.
    Save the figure at the given file name.
    """
    lvm_ratios = test_lvm_ratios(target_param, test_values, trials, params)

    fig, axes = plt.subplots(1, 2, figsize=(12.8, 4.8))

    axes[0].plot(test_values, lvm_ratios["a/b"], "o")
    axes[0].set(xlabel=target_param, ylabel="a/b")

    axes[1].plot(test_values, lvm_ratios["d/c"], "o")
    axes[1].set(xlabel=target_param, ylabel="d/c")
    
    fig.tight_layout()
    fig.savefig(fname)

def run_standard_test(target_parameter, use_basic_setup):
    """
    Run a standard test on the target parameter.
    Perform 25 trials with use_basic_setup optionally toggled.
    """
    trials = 25
    test_values = test_ranges[target_parameter]
    params = default_parameters.parameters.copy()
    params["use_basic_setup"] = use_basic_setup

    if use_basic_setup:
        fname = f"media/lvm_ratios_{target_parameter}.svg"
    else:
        fname = f"media/lvm_ratios_{target_parameter}_circular.svg"

    plot_and_test_lvm_ratios(fname, target_parameter, test_values, trials, params)
