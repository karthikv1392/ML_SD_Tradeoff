package attacker

import (
	"encoding/json"
	"fmt"
	"net/http"
	"sync"
	"time"

	"sockshop/mod/model"
	"sockshop/mod/printer"

	vegeta "github.com/tsenart/vegeta/v12/lib"
)

func panic_cmd(err error) {
	if err != nil {
		panic(err)
	}
}

func Attack(waitGroup *sync.WaitGroup, attackDuration uint32, target model.SimAPI) {
	timeDuration, err := time.ParseDuration(fmt.Sprintf("%ds", attackDuration))
	panic_cmd(err)

	if (1 * target.RateType) > timeDuration {
		printer.PrintAttackErrorInfo(target)
	} else {
		call_attacker(timeDuration, target)
	}
	waitGroup.Done()
}

func POSTTargeter(targetRequest model.SimAPI) vegeta.Targeter {
	return func(target *vegeta.Target) error {
		if target == nil {
			return vegeta.ErrNilTarget
		}

		target.Method = targetRequest.TargetApi.Method
		target.URL = targetRequest.TargetApi.GetAbsoluteUrl()

		if json.Valid([]byte(targetRequest.TargetApi.JSONParam)) {
			payload, err := json.Marshal(targetRequest.TargetApi.JSONParam)
			if err != nil {
				return err
			}
			target.Body = payload

			header := http.Header{}
			header.Add("Accept", "application/json")
			header.Add("Content-Type", "application/json")
			target.Header = header
		}

		return nil
	}
}

// Use module vegeta to probe the site (for now, maybe later we can build an attacker)
func call_attacker(attackDuration time.Duration, target model.SimAPI) {
	printer.PrintAttackPendingInfo(target)

	vegetaRate := vegeta.Rate{Freq: int(target.Rate), Per: target.RateType}
	var vegetaTargeter vegeta.Targeter

	if target.TargetApi.Method == "POST" {
		vegetaTargeter = POSTTargeter(target)

	} else if target.TargetApi.Method == "GET" || target.TargetApi.Method == "DELETE" {
		vegetaTargeter = vegeta.NewStaticTargeter(vegeta.Target{
			Method: target.TargetApi.Method,
			URL:    target.TargetApi.GetAbsoluteUrl(),
		})
	} else {
		panic("Illegal method")
	}

	vegetaAttacker := vegeta.NewAttacker()

	var metrics vegeta.Metrics
	start := time.Now()
	for res := range vegetaAttacker.Attack(vegetaTargeter, vegetaRate, attackDuration, "test_"+target.TargetApi.GetAbsoluteUrl()) {
		metrics.Add(res)
	}
	metrics.Close()
	elapsed := time.Since(start)
	printer.PrintAttackCompletedInfo(target, elapsed, metrics.Success)
}
