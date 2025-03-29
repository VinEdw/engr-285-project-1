parameters = {
    "breed_time": 3,
    "energy_gain": 4,
    "breed_energy": 10,
    "dims": (50, 50),
    "initial_fish": 300,
    "initial_sharks": 100,
    "steps": 500,
    "start_energy": 9,
    "use_basic_setup": True,
}

def get_initialization_parameters(params):
    """
    Return a dictionary with just the parameters needed to initialize the game array.
    """
    result = {}
    desired_keys = ["initial_fish", "initial_sharks", "breed_time", "breed_energy"]
    for key in desired_keys:
        result[key] = params[key]
    return result

def get_simulation_parameters(params):
    """
    Return a dictionary with just the parameters needed to run the simulation.
    """
    result = {}
    desired_keys = ["steps", "breed_time", "energy_gain", "breed_energy", "start_energy"]
    for key in desired_keys:
        result[key] = params[key]
    return result
