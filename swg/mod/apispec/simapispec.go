package apispec

import (
	"sockshop/mod/model"
)

// Payment
var HealthGetSim model.SimAPI = model.SimAPI{TargetApi: HealthGet}
var PaymentAuthPostSim model.SimAPI = model.SimAPI{TargetApi: PaymentAuthPost}

// Orders
var OrdersGetAllSim model.SimAPI = model.SimAPI{TargetApi: OrdersGetAll}
var OrdersCreateSim model.SimAPI = model.SimAPI{TargetApi: OrdersCreate}

var CatalogueGetAllSim model.SimAPI = model.SimAPI{TargetApi: CatalogueGetAll}
var CatalogueGetByIdSim model.SimAPI = model.SimAPI{TargetApi: CatalogueGetById}
var CatalogueSizeGetSim model.SimAPI = model.SimAPI{TargetApi: CatalogueSizeGet}
var TagsGetAllSim model.SimAPI = model.SimAPI{TargetApi: TagsGetAll}

// Users
var LoginGetSim model.SimAPI = model.SimAPI{TargetApi: LoginGet}

var RegisterPostSim model.SimAPI = model.SimAPI{TargetApi: RegisterPost}

var CustomersGetAllSim model.SimAPI = model.SimAPI{TargetApi: CustomersGetAll}
var CustomersDeleteByIdSim model.SimAPI = model.SimAPI{TargetApi: CustomersDeleteById}
var CustomersGetByIdSim model.SimAPI = model.SimAPI{TargetApi: CustomersGetById}
var CustomersGetCardsByIdSim model.SimAPI = model.SimAPI{TargetApi: CustomersGetCardsById}
var CustomersGetAddressesByCustomerIdSim model.SimAPI = model.SimAPI{TargetApi: CustomersGetAddressesByCustomerId}

var CardsGetAllSim model.SimAPI = model.SimAPI{TargetApi: CardsGetAll}
var CardsCreateSim model.SimAPI = model.SimAPI{TargetApi: CardsCreate}
var CardsDeleteByIdSim model.SimAPI = model.SimAPI{TargetApi: CardsDeleteById}
var CardsGetByIdSim model.SimAPI = model.SimAPI{TargetApi: CardsGetById}

var AddressesGetAllSim model.SimAPI = model.SimAPI{TargetApi: AddressesGetAll}
var AddressesCreateSim model.SimAPI = model.SimAPI{TargetApi: AddressesCreate}
var AddressesDeleteByIdSim model.SimAPI = model.SimAPI{TargetApi: AddressesDeleteById}
var AddressesGetByIdSim model.SimAPI = model.SimAPI{TargetApi: AddressesGetById}

// Carts
var CartGetSim model.SimAPI = model.SimAPI{TargetApi: CartGet}

// Shipping
var ShippingGetAllSim model.SimAPI = model.SimAPI{TargetApi: ShippingGetAll}
