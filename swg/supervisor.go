package main

import (
	"errors"
        "flag"

	"sockshop/mod/parser"
	"sockshop/mod/simulator"
	"sockshop/mod/model"
)

var targetUrl string

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

func parseArgs() (string, uint32, string) {
        workloadArg := flag.String("w", "", "path to the workload configuration file")

        dayLengthArg := flag.Uint("d", 0, "simulated day length (in seconds)")

		targetUrl := flag.String("t", "", "target endpoint to attack")

        flag.Parse()

        if !requiredFlags("w") {
            panic_cmd(errors.New("-w arg is required\n\nSYNOPSIS: <swg> -w </path/to/workload_config_file.txt> -d <simulated_day_length (in seconds)> -t <target_url>"))
        }

        if !requiredFlags("d") {
            panic_cmd(errors.New("-d arg is required\n\nSYNOPSIS: <swg> -w </path/to/workload_config_file.txt> -d <simulated_day_length (in seconds)> -t <target_url>"))
        }

		if !requiredFlags("t") {
            panic_cmd(errors.New("-t arg is required\n\nSYNOPSIS: <swg> -w </path/to/workload_config_file.txt> -d <simulated_day_length (in seconds)> -t <target_url>"))
        }

	return *workloadArg, uint32(*dayLengthArg), *targetUrl
}

func main() {
	// fileName: path of the workload file
	// simDayLength: day length (in seconds)
	fileName, simDayLength, targetUrl := parseArgs()
	workload, err := parser.ReadWorkloadFromFile(fileName)
	panic_cmd(err)

	// Set up url
	model.SetTargetUrl(targetUrl)

	// Simulate the workload with a chosen day's length
	simulator.Simulate(workload, simDayLength)
}
