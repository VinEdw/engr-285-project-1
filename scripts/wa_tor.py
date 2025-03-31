# A program implementing and measuring a Wa-Tor (water torus) Simulation

import numpy as np              # Library needed for numerical functions
import matplotlib.pyplot as plt # Library needed to plot results
import imageio.v2 as io         # Library for converting a collection of image files to a gif
import copy                     # Library for copying objects
import random as rand           # Library for generating random numbers

# Classes to hold the creatures (fish and sharks)

class Creature:
    def __init__(self, i: int, j: int, active: bool = True) -> None:
        self.i = i
        self.j = j
        self.active = active

    def __repr__(self) -> str:
        return f"Creature({self.i}, {self.j})"

class Fish(Creature):
    def __init__(self, i: int, j: int, time: int, active: bool = True) -> None:
        super().__init__(i, j, active=active)
        self.time = time

    def __repr__(self) -> str:
        return f"Fish({self.i}, {self.j}, {self.time})"

    def can_breed(self, breed_time: int) -> bool:
        """
        Return whether the fish has enough time to breed.
        """
        return self.time > breed_time

class Shark(Creature):
    def __init__(self, i: int, j: int, energy: int, active: bool = True) -> None:
        super().__init__(i, j, active=active)
        self.energy = energy

    def __repr__(self) -> str:
        return f"Shark({self.i}, {self.j}, {self.energy})"

    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, new_energy):
        """
        Set the energy of the shark.
        If the energy of a shark reaches 0, deactivate the shark.
        """
        self._energy = new_energy
        if new_energy <= 0:
            self.active = False

    @energy.deleter
    def energy(self):
        del self._energy

    def can_breed(self, breed_energy: int) -> bool:
        """
        Return whether the shark has enough energy to breed.
        """
        return self.energy > breed_energy

# Class to store the board

class Board:
    def __init__(self, dims: tuple[int, int], creatures: list[Creature]|None = None):
        self.dims = dims
        if creatures is None:
            creatures = []
        self.creatures = creatures

    def size(self):
        return self.dims[0] * self.dims[1]

    def __repr__(self) -> str:
        return f"Board({self.dims}, {self.creatures})"

    def creature_count(self, creature_type) -> int:
        """
        Return the number of the given creature in the game board.
        """
        count = 0
        for creature in self.creatures:
            if isinstance(creature, creature_type):
                count += 1
        return count

    def fish_count(self) -> int:
        """
        Return the number of fish in the game board.
        """
        return self.creature_count(Fish)

    def shark_count(self) -> int:
        """
        Return the number of sharks in the game board.
        """
        return self.creature_count(Shark)

    def everything_extinct(self) -> bool:
        """
        Return whether all creatures in the game board have gone died.
        In other words, whether the fish and sharks are both extinct.
        This happens shortly after the sharks eat all the fish.
        """
        return len(self.creatures) == 0

    def fish_fill_board(self) -> bool:
        """
        Return whether all creatures in the game board are fish.
        In other words, whether the fish have filled the board.
        This happens shortly after the sharks go extinct.
        """
        return self.fish_count() == self.size()

    def get_active_creature_at_location(self, i: int, j: int) -> Creature|None:
        """
        Return the first active creature found at the given location in the board.
        If no creature could be found, return None.
        """
        for creature in self.creatures:
            if creature.active and (creature.i == i) and (creature.j == j):
                return creature
        return None

    def remove_inactive_creatures(self) -> None:
        """
        Remove the creatures that are not active from the board.
        """
        i = len(self.creatures) - 1
        while i >= 0:
            creature = self.creatures[i]
            if not creature.active:
                self.creatures.pop(i)
            i -= 1

    def get_empty_adjacent_locations(self, i: int, j: int) -> list[tuple[int, int]]:
        """
        Return a list of locations in the game board adjacent to the given location that are empty.
        Locations are considered empty if they do not have an active creature.
        """
        locs = get_adjacent_locations(self.dims, i, j)
        empty_locs = []
        for loc in locs:
            creature = self.get_active_creature_at_location(loc[0], loc[1])
            if creature is None:
                empty_locs.append(loc)
        return empty_locs

    def get_fish_occupied_adjacent_locations(self, i: int, j: int) -> list[tuple[int, int]]:
        """
        Return a list of locations in the game board adjacent to the given location that are occupied by fish.
        Locations are considered empty if they do not have an active creature.
        """
        locs = get_adjacent_locations(self.dims, i, j)
        fish_occupied_locs = []
        for loc in locs:
            creature = self.get_active_creature_at_location(loc[0], loc[1])
            if isinstance(creature, Fish):
                fish_occupied_locs.append(loc)
        return fish_occupied_locs

# Functions for running the simulation

def run_simulation(game_board: Board, steps: int, breed_time: int, energy_gain: int, breed_energy: int, start_energy: int, print_progress: bool = False):
    """
    Run the simulation for the given number of steps, performing all the movements, hunts, breedings, and deaths.
    If the fish population fills the board or all the sharks and fish die, terminate early.
    Pass in the relevant simulation parameters.
    Return a list containing the game board at each step.
    """
    game_board_list = [game_board]
    percent = 0

    for k in range(steps):
        game_board = step_game(game_board, breed_time, energy_gain, breed_energy, start_energy)
        game_board_list.append(game_board)

        # Print the current progress if the percentage has changed
        if print_progress:
            new_percent = np.floor((k + 1) / steps * 100).astype(int)
            if new_percent > percent:
                percent = new_percent
                print(f"{percent:3}%", end="\r")

        # If the board is full of fish or both species have gone extinct, stop simulating early
        if game_board.fish_fill_board() or game_board.everything_extinct():
            break

    return game_board_list

def step_game(old_board: Board, breed_time: int, energy_gain: int, breed_energy: int, start_energy: int):
    """
    Increment the simulation by 1 step, performing all the movements, hunts, breedings, and deaths.
    Pass in the relevant simulation parameters.
    Return a new game board with the updates.
    """
    # Copy the old board to avoid overwriting the original
    old_board = copy.deepcopy(old_board)
    # Create a new board to return with the updates
    new_board = Board(old_board.dims)

    # Shuffle the creature list before looping through
    rand.shuffle(old_board.creatures)
    for creature in old_board.creatures:
        i = creature.i
        j = creature.j

        # Skip the loop iteration if the creature is not active
        if not creature.active:
            continue

        # Handle fish behavior
        if isinstance(creature, Fish):
            # Find the adjacent cells that are open in both boards
            available_locs = get_valid_fish_moves(old_board, new_board, i, j)

            # If there are open adjacent cells, randomly move the fish into one
            if len(available_locs) > 0:
                chosen_loc = rand.choice(available_locs)
                chosen_i = chosen_loc[0]
                chosen_j = chosen_loc[1]
                # Check the fish is eligible to breed
                if creature.can_breed(breed_time):
                    # Place a reset fish at the new location
                    new_board.creatures.append(Fish(chosen_i, chosen_j, 1))
                    # Place a child fish at the old location
                    new_board.creatures.append(Fish(i, j, 1))
                else:
                    # Place the fish in the new location, incrementing its time by 1
                    new_board.creatures.append(Fish(chosen_i, chosen_j, creature.time + 1))

            # If there are no open cells, the fish stays in place
            else:
                new_board.creatures.append(Fish(i, j, creature.time))


        # Handle shark behavior
        elif isinstance(creature, Shark):
            # Find the adjacent cells that are open in both boards
            available_locs = get_valid_fish_moves(old_board, new_board, i, j)
            # Find the adjacent cells that contain fish in either board
            preferred_locs = get_preferred_shark_moves(old_board, new_board, i, j)

            # If there are fish occupied adjacent cells, randomly move the shark into one
            if len(preferred_locs) > 0:
                chosen_loc = rand.choice(preferred_locs)
                chosen_i = chosen_loc[0]
                chosen_j = chosen_loc[1]
                # Check the shark is eligible to breed
                if creature.can_breed(breed_energy):
                    # Share the energy from the eating the fish
                    shared_energy_gain = round(energy_gain / 2)
                    # Place the shark in the new location
                    new_energy = creature.energy + shared_energy_gain - start_energy - 1
                    new_board.creatures.append(Shark(chosen_i, chosen_j, new_energy))
                    # Place a new shark at the old location
                    new_board.creatures.append(Shark(i, j, start_energy + shared_energy_gain))
                else:
                    # Place the shark in the new location, and give it all the energy from eating the food
                    new_energy = creature.energy + energy_gain - 1
                    new_board.creatures.append(Shark(chosen_i, chosen_j, new_energy))
                # Deactivate the fish that was eaten
                fish_eaten = old_board.get_active_creature_at_location(chosen_i, chosen_j) or new_board.get_active_creature_at_location(chosen_i, chosen_j)
                assert fish_eaten is not None
                fish_eaten.active = False

            # If there are open adjacent cells, randomly move the shark into one
            elif len(available_locs) > 0:
                chosen_loc = rand.choice(available_locs)
                chosen_i = chosen_loc[0]
                chosen_j = chosen_loc[1]
                # Check the shark is eligible to breed
                if creature.can_breed(breed_energy):
                    # Place the shark in the new location
                    new_energy = creature.energy - start_energy - 1
                    new_board.creatures.append(Shark(chosen_i, chosen_j, new_energy))
                    # Place a new shark at the old location
                    new_board.creatures.append(Shark(i, j, start_energy))
                else:
                    # Place the shark in the new location
                    new_board.creatures.append(Shark(chosen_i, chosen_j, creature.energy - 1))

            # If there are no open cells, the shark can't move and stays in place
            else:
                new_board.creatures.append(Shark(i, j, creature.energy - 1))

        # Deactivate the creature in the old board
        creature.active = False

    # Remove inactive creatures from the new board, then return it
    new_board.remove_inactive_creatures()
    return new_board

# Functions for game array initialization

def initialize_game_board_randomly(game_board: Board, initial_fish: int, initial_sharks: int, breed_time: int, breed_energy: int):
    """
    Randomly fill the game board with the given number of fish and sharks.
    Each fish will be given a random time.
    Each shark will be given a random amount of energy.
    """
    # Check that there are enough spaces to fit all the fish and sharks
    initial_creatures = initial_fish + initial_sharks
    assert game_board.size() >= initial_creatures
    # Randomly place fish then sharks into the game board
    locs = create_random_location_sequence(game_board)
    for i in range(initial_creatures):
        loc = locs[i]
        if i < initial_fish:
            # Generate a random initial time for fish
            initial_time = generate_random_fish_time(breed_time)
            creature = Fish(loc[0], loc[1], initial_time)
        else:
            # Generate a random initial energy for sharks
            initial_energy = generate_random_shark_energy(breed_energy)
            creature = Shark(loc[0], loc[1], initial_energy)
        # Place the creature in the game board
        game_board.creatures.append(creature)

def initialize_game_board_circular(game_board: Board, initial_fish: int, initial_sharks: int, breed_time: int, breed_energy: int):
    """
    Fill the game board with the given number of fish and sharks in a circular pattern.
    Populate a central disk with sharks, and surround them with a ring of fish.
    Each fish will be given a random time.
    Each shark will be given a random amount of energy.
    """
    # Check that there are enough spaces to fit all the fish and sharks
    initial_creatures = initial_fish + initial_sharks
    assert game_board.size() >= initial_creatures
    # Calculate where the board center is
    rows = game_board.dims[0]
    cols = game_board.dims[1]
    row_center = rows / 2
    col_center = cols / 2
    for i in range(rows):
        for j in range(cols):
            y = i - row_center
            x = j - col_center
            # Check if the position is within the central shark disk
            if x**2 + y**2 < initial_sharks / np.pi:
                # Place a shark in the game board with a random energy
                initial_energy = generate_random_shark_energy(breed_energy)
                game_board.creatures.append(Shark(i, j, initial_energy))
            # Check if the position is within the surrounding fish ring
            elif x**2 + y**2 < (initial_sharks + initial_fish) / np.pi:
                # Place a fish in the game array with a random time
                initial_time = generate_random_fish_time(breed_time)
                game_board.creatures.append(Fish(i, j, initial_time))

# Functions for randomization

def create_random_location_sequence(board: Board) -> list[tuple[int, int]]:
    """
    Create a list of (i, j) indices for each location in the board with given dimensions.
    Return them in a random order.
    """
    # Randomly generate a sequence of positions in the array
    # Cells are numbered starting at 0 in the upper left corner, increasing by 1 as you move right then down
    N = board.size()
    positions = rand.sample(range(N), N)
    # Map each position to an (i, j) pair
    coordinates = []
    cols = board.dims[1]
    for pos in positions:
        i = pos // cols
        j = pos % cols
        coordinates.append((i, j))
    return coordinates

def choose_random_location(locs: list[tuple[int, int]]) -> tuple[int, int]:
    """
    Return a random location (i, j) in the given list of locations.
    """
    return rand.choice(locs)

def generate_random_fish_time(breed_time: int) -> int:
    """
    Return a random initial time for a fish.
    """
    return rand.randint(1, breed_time)

def generate_random_shark_energy(breed_energy: int) -> int:
    """
    Return a random initial energy for a shark.
    """
    return rand.randint(1, breed_energy)

# Functions for getting useful information out of the game array

    """
def get_adjacent_locations(game_array, i, j):
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

def create_simulation_paramater_str(dims: tuple[int, int], breed_time: int, energy_gain: int, breed_energy: int, start_energy: int, initial_fish: int, initial_sharks: int) -> str:
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

