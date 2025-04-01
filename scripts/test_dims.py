import test_outcome_chances as tst
import default_parameters

trials = 25
target_parameter = "dims"
step_size = 10

offset = 10
vary_size = [(length, length + offset) for length in range(40, 120 + step_size, step_size)]

initial_length = default_parameters.parameters["dims"][0]
vary_aspect_ratio = [(initial_length, initial_length + offset) for offset in range(0, initial_length + step_size, step_size)]

tst.plot_and_test_extinction_chances(f"media/outcome_chances_{target_parameter}_vary_size.svg", target_parameter, vary_size, trials)
tst.plot_and_test_extinction_chances(f"media/outcome_chances_{target_parameter}_vary_aspect_ratio.svg", target_parameter, vary_size, trials)
