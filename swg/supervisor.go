package main

import (
	"errors"
        "flag"

	"sockshop/mod/parser"
	"sockshop/mod/simulator"
)

func panic_cmd(err error) {
	if err != nil {
		panic(err)
	}
}

func requiredFlags(flagName string) bool {
	res := false
	flag.Visit(func(f *flag.Flag) {
		if f.Name == flagName {
			res = true
		}
	})
	return res
}

func parseArgs() (string, uint32) {
        workloadArg := flag.String("w", "", "path to the workload configuration file")

        dayLengthArg := flag.Uint("d", 0, "simulated day length (in seconds)")

        flag.Parse()

        if !requiredFlags("w") {
            panic_cmd(errors.New("-w arg is required\n\nSYNOPSIS: <swg> -w </path/to/workload_config_file.txt> -d <simulated_day_length (in seconds)>"))
        }

        if !requiredFlags("d") {
            panic_cmd(errors.New("-d arg is required\n\nSYNOPSIS: <swg> -w </path/to/workload_config_file.txt> -d <simulated_day_length (in seconds)>"))
        }

	return *workloadArg, uint32(*dayLengthArg)
}

func main() {
	// fileName: path of the workload file
	// simDayLength: day length (in seconds)
	fileName, simDayLength := parseArgs()
	workload, err := parser.ReadWorkloadFromFile(fileName)
	panic_cmd(err)

	// Simulate the workload with a chosen day's length
	simulator.Simulate(workload, simDayLength)
}
