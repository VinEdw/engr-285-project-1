# A program implementing and measuring a Wa-Tor (water torus) Simulation

import numpy as np              # Library needed for numerical functions
import matplotlib.pyplot as plt # Library needed to plot results
import imageio.v2 as io         # Library for converting a collection of image files to a gif
rng = np.random.default_rng()   # Random number generator

# Classes to hold the creatures (fish and sharks)

class Creature:
    def __init__(self, i: int, j: int) -> None:
        self.i = i
        self.j = j

class Fish(Creature):
    def __init__(self, i: int, j: int, time: int) -> None:
        super().__init__(i, j)
        self.time = time

class Shark(Creature):
    def __init__(self, i: int, j: int, energy: int) -> None:
        super().__init__(i, j)
        self.energy = energy

# Class to store the board

class Board:
    def __init__(self, dims: list[int], creatures: None|list[Creature] = None):
        self.dims = dims
        if creatures is None:
            creatures = []
        self.creatures = creatures

    def size(self):
        return self.dims[0] * self.dims[1]

# Functions for running the simulation

def run_simulation(game_array, steps, breed_time, energy_gain, breed_energy, start_energy, print_progress=False):
    """
    Run the simulation for the given number of steps, performing all the movements, hunts, breedings, and deaths.
    If the fish population fills the board or all the sharks and fish die, terminate early.
    Pass in the relevant simulation parameters.
    Return a list containing the game_array at each step.
    """
    game_array_list = [game_array]
    percent = 0

    for k in range(steps):
        game_array = step_game(game_array, breed_time, energy_gain, breed_energy, start_energy)
        game_array_list.append(game_array)

        # Print the current progress if the percentage has changed
        if print_progress:
            new_percent = np.floor((k + 1) / steps * 100).astype(int)
            if new_percent > percent:
                percent = new_percent
                print(f"{percent:3}%", end="\r")

        # If the array is full of fish or both species have gone extinct, stop simulating early
        if check_if_fish_fill_board(game_array) or check_if_everything_extinct(game_array):
            break

    return game_array_list

def step_game(old_array, breed_time, energy_gain, breed_energy, start_energy):
    """
    Increment the simulation by 1 step, performing all the movements, hunts, breedings, and deaths.
    Pass in the relevant simulation parameters.
    Return a new game array with the updates.
    """
    # Copy the old array to avoid overwriting the original
    old_array = old_array.copy()
    # Create a new array to return with the updates
    new_array = create_empty_game_array(old_array.shape)

    # Visit each cell in the array in a random order
    locs = create_random_location_sequence(old_array)
    for loc in locs:
        cell_value = old_array[loc]

        # Handle fish behavior
        if cell_value > 0:
            # Find the adjacent cells that are open in both arrays
            old_locs = get_empty_adjacent_locations(old_array, *loc)
            new_locs = get_empty_adjacent_locations(new_array, *loc)
            available_locs = list_intersection(old_locs, new_locs)
            # If there are open adjacent cells, randomly move the fish into one
            if len(available_locs) > 0:
                chosen_loc = choose_random_location(available_locs)
                # Check the fish is eligible to breed
                if cell_value > breed_time:
                    # Place the fish in the new location, reset, and place a new fish in the old location
                    new_array[chosen_loc] = 1
                    new_array[loc] = 1
                else:
                    # Place the fish in the new location, incrementing its time by 1
                    new_array[chosen_loc] = cell_value + 1
            # If there are no open cells, the fish stays in place
            else:
                new_array[loc] = cell_value

        # Handle shark behavior
        elif cell_value < 0:
            # Find the adjacent cells that contain fish in either array
            old_locs = get_fish_occupied_adjacent_locations(old_array, *loc)
            new_locs = get_fish_occupied_adjacent_locations(new_array, *loc)
            available_locs = list_union(old_locs, new_locs)
            # If there are fish occupied adjacent cells, randomly move the shark into one
            if len(available_locs) > 0:
                chosen_loc = choose_random_location(available_locs)
                # Check the shark is eligible to breed
                if cell_value < -breed_energy:
                    # Place the shark in the new location, and place a new shark at the old location
                    # Share the energy from the eating the fish
                    new_array[chosen_loc] = cell_value + start_energy - round(energy_gain / 2) + 1
                    new_array[loc] = -start_energy - round(energy_gain / 2)
                else:
                    # Place the shark in the new location
                    # Give it all the energy from eating the fish
                    new_array[chosen_loc] = cell_value - energy_gain + 1
                # Clear the eaten fish from the old array, if it came from there
                if old_array[chosen_loc] > 0:
                    old_array[chosen_loc] = 0
            # Try to move the shark randomly into an empty adjacent cell
            else:
                # Find the adjacent cells that are open in both arrays
                old_locs = get_empty_adjacent_locations(old_array, *loc)
                new_locs = get_empty_adjacent_locations(new_array, *loc)
                available_locs = list_intersection(old_locs, new_locs)
                # If there are open adjacent cells, randomly move the shark into one
                if len(available_locs) > 0:
                    chosen_loc = choose_random_location(available_locs)
                    # Check the shark is eligible to breed
                    if cell_value < -breed_energy:
                        # Place the shark in the new location, and place a new shark at the old location
                        new_array[chosen_loc] = cell_value + start_energy + 1
                        new_array[loc] = -start_energy
                    else:
                        # Place the shark in the new location
                        new_array[chosen_loc] = cell_value + 1
                # The shark can't move and stays in place
                else:
                    new_array[loc] = cell_value + 1

        # Remove the creature from the old array
        old_array[loc] = 0

    return new_array

# Functions for game array initialization

    """
def initialize_game_array_randomly(game_array, initial_fish, initial_sharks, breed_time, breed_energy):
    """
    Randomly fill the game array with the given number of fish and sharks.
    Each fish will be given a random time.
    Each shark will be given a random amount of energy.
    """
    # Check that there are enough spaces to fit all the fish and sharks
    initial_creatures = initial_fish + initial_sharks
    assert game_array.size >= initial_creatures
    # Randomly place fish then sharks into the game array
    locs = create_random_location_sequence(game_array)
    for i in range(initial_creatures):
        loc = locs[i]
        if i < initial_fish:
            # Generate a random initial time for fish
            initial_value = generate_random_fish_time(breed_time)
        else:
            # Generate a random initial energy for sharks
            initial_value = generate_random_shark_energy(breed_energy)
        # Place the creature in the game array
        game_array[loc] = initial_value

def initialize_game_array_circular(game_array, initial_fish, initial_sharks, breed_time, breed_energy):
    """
    Fill the game array with the given number of fish and sharks in a circular pattern.
    Populate a central disk with sharks, and surround them with a ring of fish.
    Each fish will be given a random time.
    Each shark will be given a random amount of energy.
    """
    rows = game_array.shape[0]
    cols = game_array.shape[1]
    row_center = rows / 2
    col_center = cols / 2
    for i in range(rows):
        for j in range(cols):
            y = i - row_center
            x = j - col_center
            # Check if the position is within the central shark disk
            if x**2 + y**2 < initial_sharks / np.pi:
                # Place a shark in the game array with a random energy
                game_array[i, j] = generate_random_shark_energy(breed_energy)
            # Check if the position is within the surrounding fish ring
            elif x**2 + y**2 < (initial_sharks + initial_fish) / np.pi:
                # Place a fish in the game array with a random time
                game_array[i, j] = generate_random_fish_time(breed_time)

# Functions for randomization

def create_random_location_sequence(board: Board) -> list[tuple[int]]:
    """
    Create a list of (i, j) indices for each location in the board with given dimensions.
    Return them in a random order.
    """
    # Randomly generate a sequence of positions in the array
    # Cells are numbered starting at 0 in the upper left corner, increasing by 1 as you move right then down
    N = board.size()
    positions = rng.choice(N, N, replace=False)
    # Map each position to an (i, j) pair
    coordinates = []
    cols = board.dims[1]
    for pos in positions:
        i = pos // cols
        j = pos % cols
        coordinates.append((i, j))
    return coordinates

def choose_random_location(locs: list[tuple[int]]) -> tuple[int]:
    """
    Return a random location (i, j) in the given list of locations.
    """
    return tuple(rng.choice(locs))

def generate_random_fish_time(breed_time):
    """
    Return a random initial time for a fish.
    """
    return rng.integers(1, breed_time, endpoint=True)

def generate_random_shark_energy(breed_energy):
    """
    Return a random initial energy for a shark.
    """
    return rng.integers(-breed_energy, -1, endpoint=True)

# Functions for getting useful information out of the game array

def count_fish(game_array):
    """
    Return the fish count for the given game array.
    Fish are represented by positive values, sharks by negative values, and empty spaces by 0.
    """
    fish_count = (game_array > 0).sum()
    return fish_count

def count_sharks(game_array):
    """
    Return the shark count for the given game array.
    Fish are represented by positive values, sharks by negative values, and empty spaces by 0.
    """
    shark_count = (game_array < 0).sum()
    return shark_count

def check_if_everything_extinct(game_array):
    """
    Return whether all creatures in the game array have gone died.
    In other words, whether the fish and sharks are both extinct.
    """
    empty_spaces = (game_array == 0).sum()
    return empty_spaces == game_array.size

def check_if_fish_fill_board(game_array):
    """
    Return whether all creatures in the game array are fish.
    In other words, whether the fish have filled the board.
    This happens when the sharks go extinct.
    """
    fish_count = count_fish(game_array)
    return fish_count == game_array.size

def get_adjacent_locations(game_array, i, j):
    """
    Return a list of locations in the game array adjacent to the given location.
    Cells are adjacent if they can be reached by moving up, down, left, or right.
    Moves at the edges of the array wrap around to the other side.
    """
    locs = []
    for nudge in [+1, -1]:
        for axis in [0, 1]:
            loc = [i, j]
            loc[axis] = (loc[axis] + nudge) % game_array.shape[axis]
            locs.append(tuple(loc))
    return locs

def get_empty_adjacent_locations(game_array, i, j):
    """
    Return a list of locations in the game array adjacent to the given location that are empty.
    """
    locs = get_adjacent_locations(game_array, i, j)
    empty_locs = []
    for loc in locs:
        if game_array[loc] == 0:
            empty_locs.append(loc)
    return empty_locs

def get_fish_occupied_adjacent_locations(game_array, i, j):
    """
    Return a list of locations in the game array adjacent to the given location that are occupied by fish.
    """
    locs = get_adjacent_locations(game_array, i, j)
    fish_occupied_locs = []
    for loc in locs:
        if game_array[loc] > 0:
            fish_occupied_locs.append(loc)
    return fish_occupied_locs

def find_local_maxima(x_values, y_values):
    """
    Return the x values where y is at a local maximum.
    To deal with noise, chunk the data into sections.
    A section starts once values go above some threshold of the range, and it ends when values go below another threshold of the range.
    Return the list of critical x values.
    """
    y_range = np.ptp(y_values)
    x_crit_list = []

    y_chunk_start = y_range / 4
    y_chunk_end = y_range / 5
    inside_y_chunk = False
    y_max = 0
    x_crit = 0

    # Walk through each (x, y) pair
    for x, y in zip(x_values, y_values):
        # Check if we are inside a y chunk
        if inside_y_chunk:
            # If we are still above the end threshold, keep going
            if y > y_chunk_end:
                # Check if this y value is the biggest we have seen so far
                if y > y_max:
                    y_max = y
                    x_crit = x
            # Otherwise, we need to save the critical value and leave the chunk
            else:
                x_crit_list.append(x_crit)
                inside_y_chunk = False
                # Reset the max y value
                y_max = 0
                x_crit = 0
        # Otherwise, check if we have entered a y chunk
        elif y > y_chunk_start:
            inside_y_chunk = True

    return x_crit_list

def calculate_critical_points(game_array_list):
    """
    Calculate the critical points (x = a/b, y = d/c) given a list of game arrays.
    When x is at a local maximum, y = d/c.
    When y is at a local maximum, x = a/b.
    To estimate the ratios, average the x or y values found at each local maxima.
    Return the estimates for (a/b, d/c).
    """
    fish_counts = [count_fish(game_array) for game_array in game_array_list]
    shark_counts = [count_sharks(game_array) for game_array in game_array_list]

    x_crit_list = find_local_maxima(fish_counts, shark_counts)
    y_crit_list = find_local_maxima(shark_counts, fish_counts)

    return np.mean(x_crit_list), np.mean(y_crit_list)

# Functions to help with comparing/combining lists

def list_intersection(list_1, list_2):
    """
    Return the common elements of two lists without repeats.
    """
    result = []
    for item in list_1:
        if item in list_2:
            result.append(item)
    return result

def list_union(list_1, list_2):
    """
    Return the combined elements of two lists without repeats.
    """
    result = []
    for item in list_1 + list_2:
        if item not in result:
            result.append(item)
    return result

# Functions for creating visualizations

def create_simulation_paramater_str(dims: list[int], breed_time: int, energy_gain: int, breed_energy: int, start_energy: int, initial_fish: int, initial_sharks: int) -> str:
    """
    Return a standardized string summarizing the simulation parameters.
    This is useful for creating file names that describe the setup.
    """
    dimensions = f"{dims[0]}x{dims[1]}"
    paramaters = f"{breed_time},{energy_gain},{breed_energy},{start_energy}"
    initial_conditions = f"{initial_sharks},{initial_fish}"
    return f"{dimensions}_({paramaters})_({initial_conditions})"

def create_image_array(game_array):
    """
    Return the game array converted into a format for visual display.
    Each cell is given a different color:
    - empty: white
    - fish: red
    - sharks: blue
    The cell is translated into a 16x16 square of the RGB value for its color.
    """
    square_width = 16
    rows = game_array.shape[0] * square_width
    cols = game_array.shape[1] * square_width
    result = np.zeros((rows, cols, 3), dtype="uint8")
    empty_color = np.array([255, 255, 255], dtype="uint8")
    fish_color = np.array([255, 0, 0], dtype="uint8")
    shark_color = np.array([0, 0, 255], dtype="uint8")

    for i, row in enumerate(game_array):
        row_range = slice(i*square_width, (i + 1)*square_width)
        for j, cell_value in enumerate(row):
            col_range = slice(j*square_width, (j + 1)*square_width)
            if cell_value > 0:
                color = fish_color  # Fish are positive
            elif cell_value < 0:
                color = shark_color # Sharks are negative
            else:
                color = empty_color # Empty spaces are 0
            result[row_range, col_range, :] = color

    return result

def create_simulation_animation(game_array_list, fname, fps=20):
    """
    Create a gif file animating the simulation.
    Pass in a list of game arrays and the desired file name.
    """
    img_data = [create_image_array(game_array) for game_array in game_array_list]
    io.mimwrite(fname, img_data, format=".gif", fps=fps)

def create_simulation_plots(game_array_list, fname):
    """
    Create plots describing the simulation 
    """
    actual_steps = len(game_array_list)
    fish_counts = [count_fish(game_array) for game_array in game_array_list]
    shark_counts = [count_sharks(game_array) for game_array in game_array_list]

    fig, axes = plt.subplots(2, 1)
    fig.suptitle("Wa-Tor Populations")

    # Plot each population over time
    axes[0].plot(range(actual_steps), fish_counts, label="fish")
    axes[0].plot(range(actual_steps), shark_counts, label="sharks")
    axes[0].legend()
    axes[0].set(xlabel="", ylabel="Population")

    # Plot each population against the other
    axes[1].plot(fish_counts, shark_counts, marker=".")
    axes[1].set(xlabel="Fish Population", ylabel="Shark Population")

    fig.savefig(fname)

