.POSIX:

include config.mk

.DEFAULT_GOAL := help

.SILENT: help
.PHONY: help # [make] print this help text
help:
	@grep '^.PHONY: .* #' $(firstword $(MAKEFILE_LIST)) |\
		sed 's/\.PHONY: \(.*\) # \(.*\)/\1 # \2/' |\
		awk 'BEGIN {FS = "#"}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' 

.PHONY: all # --- (combo)[sockshop] build sockshop application
all: clean deps run

.PHONY: build # [sockshop] compile the application
build:
	$(GOBUILD) -o $(PREFIX)$(DESTDIR)$(OBJ)

.PHONY: clean # [sockshop] go clean and remove the application executable
clean:
	$(GOCLEAN)
	-rm -f $(PREFIX)$(DESTDIR)$(OBJ)

.PHONY: run # [sockshop] compile and run the application
run: build
	./$(PREFIX)$(DESTDIR)$(OBJ) $(ARGS)

.PHONY: deps # [sockshop] install dependencies
deps:
	$(GOMODTIDY)
