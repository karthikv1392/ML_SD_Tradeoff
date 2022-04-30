package apispec

import (
	"sockshop/mod/model"
)

// Association between the name of the request and the SimAPI object
var RequestSimMap map[string]model.SimAPI = map[string]model.SimAPI{
	// All GET methods
	"health_get":                             HealthGetSim,
	"orders_get_all":                         OrdersGetAllSim,
	"catalogue_get_all":                      CatalogueGetAllSim,
	"catalogue_get_by_id":                    CatalogueGetByIdSim,
	"catalogue_size_get":                     CatalogueSizeGetSim,
	"tags_get_all":                           TagsGetAllSim,
	"login_get":                              LoginGetSim,
	"customers_get_all":                      CustomersGetAllSim,
	"customers_get_by_id":                    CustomersGetByIdSim,
	"customers_get_cards_by_id":              CustomersGetCardsByIdSim,
	"customers_get_addresses_by_customer_id": CustomersGetAddressesByCustomerIdSim,
	"cards_get_all":                          CardsGetAllSim,
	"cards_get_by_id":                        CardsGetByIdSim,
	"addresses_get_all":                      AddressesGetAllSim,
	"addresses_get_by_id":                    AddressesGetByIdSim,
	// All POST methods
	"paymentauth_post":      PaymentAuthPostSim,
	"orders_create_post":    OrdersCreateSim,
	"register_post":         RegisterPostSim,
	"cards_create_post":     CardsCreateSim,
	"addresses_create_post": AddressesCreateSim,
	// All DELETE methods
	"customers_delete_by_id": CustomersDeleteByIdSim,
	"cards_delete_by_id":     CardsDeleteByIdSim,
	"addresses_delete_by_id": AddressesDeleteByIdSim,
}
