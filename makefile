SCRIPT_DIR := ./scripts
OUTPUT_DIR := ./output

SCRIPTS := $(shell find $(SCRIPT_DIR) -type f -name '*.py')
OUTPUTS := $(SCRIPTS:$(SCRIPT_DIR)/%.py=$(OUTPUT_DIR)/%.output)

project-1.pdf: project-1.typ engr-conf.typ $(OUTPUTS)
	typst compile $<

$(OUTPUT_DIR)/%.output: $(SCRIPT_DIR)/%.py
	@mkdir -p $(dir $@)
	@mkdir -p media
	python $< > $@

SIMULATION_SCRIPT := $(SCRIPT_DIR)/wa_tor.py
TEST_SCRIPTS := $(filter $(OUTPUT_DIR)/test%.output,$(OUTPUTS))
RATIO_TEST_SCRIPTS := $(filter $(OUTPUT_DIR)/test_%_ratios.output $(OUTPUT_DIR)/test_%_ratios_circular.output,$(TEST_SCRIPTS))
OUTCOME_CHANCE_TEST_SCRIPTS := $(filter-out $(RATIO_TEST_SCRIPTS),$(TEST_SCRIPTS))

$(filter $(OUTPUT_DIR)/lvm%stream_plot.output,$(OUTPUTS)): $(SCRIPT_DIR)/stream_plotter.py
$(filter $(OUTPUT_DIR)/measure%.output,$(OUTPUTS)): $(SIMULATION_SCRIPT) $(SCRIPT_DIR)/default_parameters.py
$(OUTPUT_DIR)/simulation_playground.output: $(SIMULATION_SCRIPT)
$(RATIO_TEST_SCRIPTS): $(SCRIPT_DIR)/measure_ratios.py
$(OUTCOME_CHANCE_TEST_SCRIPTS): $(SCRIPT_DIR)/measure_outcome_chances.py

.PHONY: clean
clean: 
	rm -r $(OUTPUT_DIR)
