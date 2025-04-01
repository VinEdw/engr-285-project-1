import test_outcome_chances as tst

trials = 25
target_parameter = "aspect_ratio"
test_values = [i/8 for i in range(8, 16 + 1)]

tst.plot_and_test_extinction_chances(f"media/outcome_chances_{target_parameter}.svg", target_parameter, test_values, trials)
