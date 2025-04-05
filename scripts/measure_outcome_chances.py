import wa_tor
import default_parameters
import matplotlib.pyplot as plt

# Specify the test values to use when testing each parameter
test_ranges = {
    "breed_time": range(1, 15 + 1),
    "energy_gain": range(2, 18 + 1),
    "breed_energy": range(default_parameters.parameters["start_energy"] + 1, 25 + 1),
    "side_length": range(40, 120 + 10, 10),
    "aspect_ratio": [i/8 for i in range(8, 16 + 1)],
    "initial_fish": range(200, 1000 + 50, 50),
    "initial_sharks": range(200, 1000 + 50, 50),
    "start_energy": range(1, default_parameters.parameters["breed_energy"] - 1),
}

def test_outcome_chances(target_param, test_values, trials, params=None):
    """
    Vary the target parameter to have the given test values.
    For each value, run the simulation for the specified number of trials and calculate the chance of each of the possible outcomes.
    - Everything went extinct
    - Fish fill the board
    - Simulation could keep going

    Return a dictionary containing three lists of chances, one list for each outcome.
    Each list contains the chances found using each test value of the target parameter.
    """
    # Set the parameters to the default if not specified
    if params is None:
        params = default_parameters.parameters.copy()

    overall_chances = {
        "everything_extinct": [],
        "fish_fill_board": [],
        "still_going": [],
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
        # Keep track of the counts for the possible outcomes
        everything_extinct_count = 0
        fish_fill_count = 0

        for _ in range(trials):
            # Initialize the game array
            initial_game_array = wa_tor.create_empty_game_array(dims)
            if params["use_basic_setup"]:
                wa_tor.initialize_game_array_randomly(initial_game_array, **init_params)
            else:
                wa_tor.initialize_game_array_circular(initial_game_array, **init_params)

            # Run the simulation
            fish_counts, shark_counts = wa_tor.run_simulation_minimal(initial_game_array, **sim_params)

            # Check whether fish filled the board or if sharks and fish both went extinct
            # Update the counts for these events
            size = dims[0] * dims[1]
            if fish_counts[-1] + shark_counts[-1] < 0:
                everything_extinct_count += 1
            elif fish_counts[-1] == size:
                fish_fill_count += 1

        # Store the chances of each possible outcome
        still_going_count = trials - everything_extinct_count - fish_fill_count
        overall_chances["everything_extinct"].append(everything_extinct_count / trials)
        overall_chances["fish_fill_board"].append(fish_fill_count / trials)
        overall_chances["still_going"].append(still_going_count / trials)

    return overall_chances

def plot_and_test_outcome_chances(fname, target_param, test_values, trials, params=None):
    """
    Run the function test_outcome_chances() with the given arguments, then plot the results.
    Save the figure at the given file name.
    """
    outcome_chances = test_outcome_chances(target_param, test_values, trials, params)

    fig, ax = plt.subplots()
    ax.plot(test_values, outcome_chances["everything_extinct"], "o", label="Both Extinct")
    ax.plot(test_values, outcome_chances["fish_fill_board"], "^", label="Sharks Extinct")
    ax.plot(test_values, outcome_chances["still_going"], ".", label="Neither Extinct")
    ax.set(xlabel=target_param, ylabel="Chance")
    ax.legend()
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
        fname = f"media/outcome_chances_{target_parameter}.svg"
    else:
        fname = f"media/outcome_chances_{target_parameter}_circular.svg"

    plot_and_test_outcome_chances(fname, target_parameter, test_values, trials, params)
