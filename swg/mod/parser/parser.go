package parser

import (
	"bufio"
	"os"
	"strconv"
	"strings"
	"time"

	"sockshop/mod/apispec"
	"sockshop/mod/model"
)

func panic_cmd(err error) {
	if err != nil {
		panic(err)
	}
}

func getRateType(rateString string) time.Duration {
	if rateString == "sec" {
		return time.Second
	} else if rateString == "min" {
		return time.Minute
	} else if rateString == "hr" {
		return time.Hour
	} else {
		panic("Illegal rate")
	}
}

func parseLineData(data string) (string, uint32, time.Duration, string) {
	line := strings.Split(data, ";")

	requestName := line[0]

	rate, err := strconv.Atoi(line[1])
	panic_cmd(err)

	rateType := line[2]

	param := line[3]

	return requestName, uint32(rate), getRateType(rateType), param
}

// read all workload from the workload file and return map[day] = simAPI
func ReadWorkloadFromFile(fileName string) (map[uint32][]model.SimAPI, error) {
	workload := make(map[uint32][]model.SimAPI)
	var day uint32 = 0

	file, err := os.Open(fileName)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		line := scanner.Text()
		if strings.HasPrefix(line, "#") {
			// The line is a comment
			continue
		}
		if line == "---" {
			day++
			continue
		}
		requestName, rate, rateType, param := parseLineData(line)
		requestSim := apispec.RequestSimMap[requestName]
		requestSim.Rate = rate
		requestSim.RateType = rateType
		if param != "" {
			requestSim.TargetApi.SetParam(param)
		}
		workload[day] = append(workload[day], requestSim)
	}

	return workload, nil
}
