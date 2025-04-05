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

.PHONY: clean
clean: 
	rm -r $(OUTPUT_DIR)
