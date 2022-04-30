package apispec

import (
	"sockshop/mod/model"
)

//
// Sockshop API general definition
//

// Payment
var HealthGet model.API = model.API{RelativeUrl: "/health", Method: "GET"}
var PaymentAuthPost model.API = model.API{RelativeUrl: "/paymentAuth", Method: "POST"}

// Orders
var OrdersGetAll model.API = model.API{RelativeUrl: "/orders", Method: "GET"}
var OrdersCreate model.API = model.API{RelativeUrl: "/orders", Method: "POST"}

var CatalogueGetAll model.API = model.API{RelativeUrl: "/catalogue", Method: "GET"}
var CatalogueGetById model.API = model.API{RelativeUrl: "/catalogue/%s", Method: "GET", ExtParamName: "id"}
var CatalogueSizeGet model.API = model.API{RelativeUrl: "/catalogue/size", Method: "GET"}
var TagsGetAll model.API = model.API{RelativeUrl: "/tags", Method: "GET"}

// Users
var LoginGet model.API = model.API{RelativeUrl: "/login", Method: "GET"}

var RegisterPost model.API = model.API{RelativeUrl: "/register", Method: "POST", ExtParamName: "register"}

var CustomersGetAll model.API = model.API{RelativeUrl: "/customers", Method: "GET"}
var CustomersDeleteById model.API = model.API{RelativeUrl: "/customers/%s", Method: "DELETE", ExtParamName: "id"}
var CustomersGetById model.API = model.API{RelativeUrl: "/customers/%s", Method: "GET", ExtParamName: "id"}
var CustomersGetCardsById model.API = model.API{RelativeUrl: "/customers/%s/cards", Method: "GET", ExtParamName: "id"}
var CustomersGetAddressesByCustomerId model.API = model.API{RelativeUrl: "/customers/%s/addresses", Method: "GET", ExtParamName: "id"}

var CardsGetAll model.API = model.API{RelativeUrl: "/cards", Method: "GET"}
var CardsCreate model.API = model.API{RelativeUrl: "/cards", Method: "POST", ExtParamName: "card"}
var CardsDeleteById model.API = model.API{RelativeUrl: "/cards/%s", Method: "DELETE", ExtParamName: "id"}
var CardsGetById model.API = model.API{RelativeUrl: "/cards/%s", Method: "GET", ExtParamName: "id"}

var AddressesGetAll model.API = model.API{RelativeUrl: "/addresses", Method: "GET"}
var AddressesCreate model.API = model.API{RelativeUrl: "/addresses", Method: "POST", ExtParamName: "address"}
var AddressesDeleteById model.API = model.API{RelativeUrl: "/addresses/%s", Method: "DELETE", ExtParamName: "id"}
var AddressesGetById model.API = model.API{RelativeUrl: "/addresses/%s", Method: "GET", ExtParamName: "id"}
