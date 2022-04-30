package printer

import (
	"time"

	"sockshop/mod/logger"
	"sockshop/mod/model"
)

func PrintDayInfo(day uint32, dayDuration uint32) {
	logger.InfoMessage("- Day %d: (duration: %d seconds)\n", day, dayDuration)
}

func PrintTargetInfo(target model.SimAPI, dayDuration uint32) {
	if target.RateType == time.Second {
		logger.InfoMessage("\t> %s: %d request per sec - %d total requests\n", target.TargetApi.GetAbsoluteUrl(), target.Rate, target.Rate*dayDuration)
	} else if target.RateType == time.Minute {
		logger.InfoMessage("\t> %s: %d request per min - %d total requests\n", target.TargetApi.GetAbsoluteUrl(), target.Rate, target.Rate*(dayDuration/60))
	} else if target.RateType == time.Hour {
		logger.InfoMessage("\t> %s: %d request per hour - %d total requests\n", target.TargetApi.GetAbsoluteUrl(), target.Rate, target.Rate*(dayDuration/(60*60)))
	}

}

func PrintAttackPendingInfo(target model.SimAPI) {
	if target.RateType == time.Second {
		logger.PendingMessage("\t> attacking: %s - rate: %d per seconds\n", target.TargetApi.GetAbsoluteUrl(), target.Rate)
	} else if target.RateType == time.Minute {
		logger.PendingMessage("\t> attacking: %s - rate: %d per minutes\n", target.TargetApi.GetAbsoluteUrl(), target.Rate)
	} else if target.RateType == time.Hour {
		logger.PendingMessage("\t> attacking: %s - rate: %d per hours\n", target.TargetApi.GetAbsoluteUrl(), target.Rate)
	}
}

func PrintAttackErrorInfo(target model.SimAPI) {
	logger.ErrorMessage("\t> skipping : %s - time rate attack > length of a day\n", target.TargetApi.GetAbsoluteUrl())
}

func PrintAttackCompletedInfo(target model.SimAPI, attackDuration time.Duration, successRate float64) {
	logger.CompletedMessage("\t> finished : %s - took: %fs - non-error responses: %.2f%%\n", target.TargetApi.GetAbsoluteUrl(), attackDuration.Seconds(), successRate)
}
