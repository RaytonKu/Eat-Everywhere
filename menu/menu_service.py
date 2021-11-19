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

@app.route('/<restaurant_id>/menus', methods=['GET'])
def get_menu(restaurant_id):
    if db.hexists("menus", restaurant_id):
        return json.loads(db.hget("menus",restaurant_id)), 200
    else:
        return {"Error": "The menu for this restaurant is unavailable."},404

@app.route('/<restaurant_id>/menus', methods=['PUT'])
def upload_menu(restaurant_id):
    items = request.get_json()
    try:
        db.hset("menus",restaurant_id,json.dumps(items))
        return items, 200
    except Exception as e:
        return {"message":str(e)},200

@app.route('/<restaurant_id>/menus/dishes', methods=['POST'])
def update_menu(restaurant_id):
    items = request.get_json()
    try:
        db.hset("menus",restaurant_id,json.dumps(items))
        return items, 200
    except Exception as e:
        return {"message":str(e)},200
