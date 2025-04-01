import test_outcome_chances as tst

trials = 25
target_parameter = "energy_gain"
start_value = 2
end_value = 18

tst.plot_and_test_extinction_chances(f"media/outcome_chances_{target_parameter}.svg", target_parameter, range(start_value, end_value + 1), trials)
