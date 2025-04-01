import test_outcome_chances as tst
import default_parameters

trials = 25
target_parameter = "breed_energy"
start_value = default_parameters.parameters["start_energy"] + 1
end_value = 25

tst.plot_and_test_extinction_chances(f"media/outcome_chances_{target_parameter}.svg", target_parameter, range(start_value, end_value + 1), trials)
