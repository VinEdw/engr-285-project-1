import test_outcome_chances as tst
import default_parameters

trials = 25
target_parameter = "start_energy"
start_value = 1
end_value = default_parameters.parameters["breed_energy"] - 1

tst.plot_and_test_extinction_chances(f"media/outcome_chances_{target_parameter}.svg", target_parameter, range(start_value, end_value + 1), trials)
