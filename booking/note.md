# Booking API
This shows Redis in infrastructure services in a microservice architecture.

## Get Booking Details

- [GET] /eats/order/{order_id}

## Get Active Created Booking

- [GET] /eats/stores/{store_id}/created-orders

## Get Get Latest Canceled Booking

- [GET] /eats/stores/{store_id}/canceled-orders

## Accept Booking

- [POST] /eats/orders/{order_id}/accept_pos_order

## Deny Booking

- [POST] /eats/orders/{order_id}/deny_pos_order

## Cancel Booking

- [POST] /eats/orders/{order_id}/cancel

## Patch Cart

- [PATCH] /eats/orders/{order_id}/cart
