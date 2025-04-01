import test_outcome_chances as tst

trials = 25
target_parameter = "side_length"
step_size = 10
start_value = 40
end_value = 120

tst.plot_and_test_extinction_chances(f"media/outcome_chances_{target_parameter}.svg", target_parameter, range(start_value, end_value + step_size, step_size), trials)
