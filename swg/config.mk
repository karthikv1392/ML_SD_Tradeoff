GOCMD ?= go
GOBUILD ?= $(GOCMD) build
GOCLEAN ?= $(GOCMD) clean
GOGET ?= $(GOCMD) get
GOMOD ?= $(GOCMD) mod
GOMODTIDY ?= $(GOMOD) tidy
GORUN ?= $(GOCMD) run

SRC ?= supervisor.go
OBJ ?= swg
PREFIX ?= bin/

ARGS ?= -w workload/workload.txt -d 60
