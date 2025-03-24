SCRIPTS := $(wildcard scripts/*.py)
OUTPUT := $(SCRIPTS:scripts/%.py=output/%.output)

project-1.pdf: project-1.typ engr-conf.typ $(OUTPUT)
	typst compile $<

output/%.output: scripts/%.py
	mkdir -p output
	mkdir -p media
	python $< > $@

.PHONY: clean
clean: 
	rm output/*.output
