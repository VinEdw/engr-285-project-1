import test_outcome_chances as tst

trials = 25
target_parameter = "initial_sharks"
step_size = 50
start_value = 200
end_value = 1000

tst.plot_and_test_extinction_chances(f"media/outcome_chances_{target_parameter}.svg", target_parameter, range(start_value, end_value + step_size, step_size), trials)
