package model

import (
	"encoding/json"
	"fmt"
	"strings"
)

var SitePrefix string 

func SetTargetUrl(targetUrl string) {
	SitePrefix = targetUrl
}

type API struct {
	RelativeUrl  string
	Method       string
	JSONParam    string
	ExtParamName string
}

func (api API) GetAbsoluteUrl() string {
	if strings.Contains(api.RelativeUrl, "%s") {
		if (!json.Valid([]byte(api.JSONParam))) || api.JSONParam == "" {
			panic("must set a JSONParam")
		}
		var param map[string]string
		json.Unmarshal([]byte(api.JSONParam), &param)
		return SitePrefix + fmt.Sprintf(api.RelativeUrl, param["id"])
	}
	return SitePrefix + api.RelativeUrl
}

func (api *API) SetParam(jsonParam string) {
	if !json.Valid([]byte(jsonParam)) {
		panic("Not a valid param json string")
	}
	api.JSONParam = jsonParam
}
