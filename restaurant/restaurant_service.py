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

@app.route('/restaurants', methods=['GET'])
def get_restaurant():
    if len(db.hget('restaurants'))==0:
        return {"error": "Empty list"},204        
    else:
        datas=db.hkeys("restaurants")
        data= {"restaurants":[]}
        for data in datas:
            data = json.loads(db.hget("restaurants",data))
            datas['restaurants'].append(data) 
        return datas, 200
        
@app.route('/restaurant/<restaurant_id>', methods=['GET'])
def get_restaurant_by_id(restaurant_id):
    if db.hexists("restaurants", restaurant_id):
        return json.loads(db.hget("restaurants",restaurant_id)), 200
    else:
        return {"Error": "restaurant not found"},404

@app.route('/restaurant/<restaurant_id>/holiday-hours', methods=['GET'])
def get_holiday_hours(restaurant_id):
    if db.hexists("holidayHours", restaurant_id):
        return json.loads(db.hget("holidayHours",restaurant_id)), 200
    else:
        return {"Error": "restaurant not found"},404

@app.route('/restaurant/<restaurant_id>/setHoliday-hours', methods=['POST', 'GET'])
def set_holiday_hours(store_id):
    url = request.args.get('jsonInputString')
    jsonInputString = unquote(url)
   
    if db.hexists("holidayHours", restaurant_id):
        db.hset("holidayHours",restaurant_id, json.dumps(jsonInputString))
        return {"Success": "Holiday-hours updated"}, 200
    else:
        return {"Error": "restaurant not found"},404
