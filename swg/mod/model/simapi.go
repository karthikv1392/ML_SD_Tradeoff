package model

import (
	"time"
)

type SimAPI struct {
	TargetApi API
	RateType  time.Duration
	Rate      uint32
}
