import wa_tor

# Main parameters of the simulation
breed_time = 3          # Number of steps before a fish is capable of duplicating
energy_gain = 4         # Additional steps granted to a shark after eating a fish
breed_energy = 10       # Number of stored steps before a shark is capable of duplicating

# Other simulation parameters
dims = (30, 40)         # Size of the simulation window
initial_fish = 300      # Starting number of fish
initial_sharks = 100    # Starting number of sharks
steps = 500             # Time duration of the simulation
start_energy = 9        # Number of moves a child shark begins with
use_basic_setup = True  # Whether to use a random initial distribution (or not)

# Initialize the game array
initial_game_array = wa_tor.create_empty_game_array(dims)
if use_basic_setup:
    wa_tor.initialize_game_array_randomly(initial_game_array, initial_fish, initial_sharks, breed_time, breed_energy)
else:
    wa_tor.initialize_game_array_circular(initial_game_array, initial_fish, initial_sharks, breed_time, breed_energy)

# Run the Simulation
print("Playing game...")
game_array_list = wa_tor.run_simulation(initial_game_array, steps, breed_time, energy_gain, breed_energy, start_energy, print_progress=True)
print("\nSimulation finished")

# Create an animation and plots
actual_steps = len(game_array_list)
fish_counts = [wa_tor.count_fish(game_array) for game_array in game_array_list]
shark_counts = [wa_tor.count_sharks(game_array) for game_array in game_array_list]

paramater_str = wa_tor.create_simulation_paramater_str(dims, breed_time, energy_gain, breed_energy, start_energy, initial_fish, initial_sharks)
animation_fname = f"media/TestAnimation_{paramater_str}_{actual_steps}.gif"
plot_fname = f"media/TestPlot_{paramater_str}_{actual_steps}.png"

wa_tor.create_simulation_animation(game_array_list, animation_fname)
wa_tor.create_simulation_plots(fish_counts, shark_counts, plot_fname)
