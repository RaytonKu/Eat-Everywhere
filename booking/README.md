# Booking API
This shows Redis in infrastructure services in a microservice architecture.

## Get Booking Details
- [GET] /booking/{booking_id}

## Get Active Created Booking
- [GET] /restaurant/{restaurant_id}/created-bookings

## Get Get Latest Canceled Booking
- [GET] /restaurant/{restaurant_id}/canceled-bookings

## Accept Booking
- [POST] /booking/{booking_id}/accept_pos_bookings

## Deny Booking
- [POST] /booking/{booking_id}/deny_pos_bookings

## Cancel Booking
- [POST] /booking/{booking_id}/cancel
