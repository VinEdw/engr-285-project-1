import wa_tor
import default_parameters
import matplotlib.pyplot as plt

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
        # Extract the needed parameters for later steps
        init_params = default_parameters.get_initialization_parameters(params)
        sim_params = default_parameters.get_simulation_parameters(params)
        # Keep track of the counts for the possible outcomes
        everything_extinct_count = 0
        fish_fill_count = 0

        for _ in range(trials):
            # Initialize the game array
            initial_game_array = wa_tor.create_empty_game_array(params["dims"])
            if params["use_basic_setup"]:
                wa_tor.initialize_game_array_randomly(initial_game_array, **init_params)
            else:
                wa_tor.initialize_game_array_circular(initial_game_array, **init_params)

            # Run the simulation
            fish_counts, shark_counts = wa_tor.run_simulation_minimal(initial_game_array, **sim_params)

            # Check whether fish filled the board or if sharks and fish both went extinct
            # Update the counts for these events
            size = params["dims"][0] * params["dims"][1]
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

def plot_and_test_extinction_chances(fname, target_param, test_values, trials, params=None):
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
