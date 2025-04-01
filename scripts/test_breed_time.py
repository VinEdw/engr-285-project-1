import test_outcome_chances as tst

trials = 25
target_parameter = "breed_time"
start_value = 1
end_value = 15

tst.plot_and_test_extinction_chances(f"media/outcome_chances_{target_parameter}.svg", target_parameter, range(start_value, end_value + 1), trials)
