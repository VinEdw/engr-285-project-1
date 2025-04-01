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

# Initialize the game board
initial_game_board = wa_tor.Board(dims)
if use_basic_setup:
    wa_tor.initialize_game_board_randomly(initial_game_board, initial_fish, initial_sharks, breed_time, breed_energy)
else:
    wa_tor.initialize_game_board_circular(initial_game_board, initial_fish, initial_sharks, breed_time, breed_energy)

# Run the Simulation
print("Playing game...")
game_board_list = wa_tor.run_simulation(initial_game_board, steps, breed_time, energy_gain, breed_energy, start_energy, print_progress=True)
print("\nSimulation finished")

# Create an animation and plots
actual_steps = len(game_board_list)
paramater_str = wa_tor.create_simulation_paramater_str(dims, breed_time, energy_gain, breed_energy, start_energy, initial_fish, initial_sharks)
animation_fname = f"media/TestAnimation{paramater_str}_{actual_steps}.gif"
plot_fname = f"media/TestPlot_{paramater_str}_{actual_steps}.png"
wa_tor.create_simulation_animation(game_board_list, animation_fname)
wa_tor.create_simulation_plots(game_board_list, plot_fname)
