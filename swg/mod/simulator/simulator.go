package simulator

import (
	"fmt"
	"sort"
	"sync"

	"sockshop/mod/attacker"
	"sockshop/mod/model"
	"sockshop/mod/printer"
)

func perform_attack(attackDuration uint32, targets []model.SimAPI) {
	var waitGroup sync.WaitGroup

	// launch an Attacker for every target
	for _, target := range targets {
		waitGroup.Add(1)
		go attacker.Attack(&waitGroup, attackDuration, target)
	}
	waitGroup.Wait()
}

// given the workload (request map structure) and the length of a day (in seconds) this function attempts to simulate the requests
func Simulate(workload map[uint32][]model.SimAPI, dayLength uint32) {
	var days []uint32

	for day := range workload {
		days = append(days, day)
	}

	sort.Slice(days, func(i, j int) bool { return days[i] < days[j] })

	for _, day := range days {
		targets := workload[day]

		printer.PrintDayInfo(day, dayLength)

		// overview of targets
		for _, target := range targets {
			printer.PrintTargetInfo(target, dayLength)
		}
		// launch attack to all targets
		perform_attack(dayLength, targets)
		fmt.Println()
	}
}
