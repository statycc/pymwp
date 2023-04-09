SHELL := /bin/bash

SRC_DIR = guide/
OUT_DIR = web/

MARKDOWN = $(shell find $(SRC_DIR) -name '*.md')
IN_FILES :=  $(addprefix $(SRC_DIR), $(addsuffix .md,  $(basename $(notdir $(MARKDOWN)))))
OPTIONS = -f markdown -t html --mathjax --template=$(SRC_DIR)_template.html

all: clean main

.PHONY: clean
clean:
	rm -rf $(OUT_DIR)

.PHONY: main
main:
	 mkdir -p $(OUT_DIR) && $(foreach file, $(IN_FILES),  \
	 pandoc $(OPTIONS) -s $(file) -o $(addprefix $(OUT_DIR), \
	 $(addsuffix .html, $(basename $(notdir $(file)))));)
