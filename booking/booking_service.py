import sys
import redis
import prometheus_client
import json

from flask import Flask, Response, request
from prometheus_client import Counter
from prometheus_flask_exporter import PrometheusMetrics

#port = int(sys.argv[1])
db_port = 6379
app = Flask(__name__)
db = redis.Redis(host='db', port=db_port)
metrics = PrometheusMetrics(app)

total_requests = Counter('request_count', 'Total webapp request count')

# static information as metric
metrics.info('app_info', 'Application info', version='1.0.3')

@app.route('/booking/<booking_id>', methods=['GET'])
def get_booking(booking_id):
    if db.hexists("bookings", booking_id):
        return json.loads(db.hget("bookings",booking_id)), 200
    else:
        return {"error": "No bookings were found."},404

@app.route('/restaurants/<restaurant_id>/created-bookings', methods=['GET'])
def get_created_bookings(restaurant_id):
    bookings_records=db.hkeys("bookings")
    created_bookings= {"bookings":[]}
    count = 0
    
    for bookings_record in bookings_records:    
        booking = json.loads(db.hget("bookings",bookings_record))
        if booking["state"] == "Created" and booking["restaurant"]["id"] == restaurant_id:
            created_bookings["bookings"].append({"id":bookings_record, "state":booking["state"]})
            count += 1
    return created_bookings,200

@app.route('/restaurants/<restaurant_id>/canceled-bookings', methods=['GET'])
def get_canceled_bookings(restaurant_id):
    bookings_records=db.hkeys("bookings")
    canceled_bookings= {"bookings":[]}

    for bookings_record in bookings_records:    
        booking = json.loads(db.hget("bookings",bookings_record))
        if booking["state"] == "Canceled" and booking["restaurant"]["id"] == restaurant_id:
            canceled_bookings["bookings"].append({"id":bookings_record, "state":booking["state"]})
    return canceled_bookings,200

@app.route('/bookings/<booking_id>/accept_pos_booking', methods=['POST'])
def accept_booking(booking_id):
    if db.hexists("bookings", booking_id):
        booking = json.loads(db.hget("bookings",booking_id))
        if booking["state"]=="Created" or booking["state"]=="Denied":
            booking["state"] = "Accepted"
            db.hset("bookings",booking_id,json.dumps(booking))
            return '',204
        else:
            return {"error":"The status of the reservation is: " + booking["state"]},409
    else:
        return {"error": "No bookings were found."},404


@app.route('/bookings/<booking_id>/deny_pos_booking', methods=['POST'])
def deny_booking(booking_id):
    if db.hexists("bookings", booking_id):
        booking = json.loads(db.hget("bookings",booking_id))
        if booking["state"]=="Created" or booking["state"]=="Accepted":
            booking["state"] = "Denied"
            db.hset("bookings",booking_id,json.dumps(booking))
            return '',204
        else:
            return {"error":"The status of the reservation is: " + booking["state"]},409
    else:
        return {"error": "No bookings were found."},404

@app.route('/bookings/<booking_id>/cancel', methods=['POST'])
def cancel_booking(booking_id):
    if db.hexists("bookings", booking_id):
        booking = json.loads(db.hget("bookings",booking_id))
        if booking["state"]!="Denied" and booking["state"]!="Completed" and booking["state"]!="Canceled":
            booking = json.loads(db.hget("bookings",booking_id))
            booking["state"] = "Canceled"
            db.hset("bookings",booking_id,json.dumps(booking))
            return '',204
        else:
            return {"error":"The status of the reservation is: " + booking["state"]},409
    else:
        return {"error": "No bookings were found."},404
