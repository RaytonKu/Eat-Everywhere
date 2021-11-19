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

@app.route('/customers', methods=['GET'])
def get_customer():
    if len(db.hget('customers'))==0:
        return {"error": "The database has no customers."},204
        
    else:
        datas=db.hkeys("customers")
        data= {"customers":[]}
        for data in datas:
            data = json.loads(db.hget("customers",data))
            datas['customers'].append(data) 
        return datas, 200
        
@app.route('/customer/<customer_id>', methods=['GET'])
def get_customer_by_id(customer_id):
    if db.hexists("customers", customer_id):
        return json.loads(db.hget("customers",customer_id)), 200
    else:
        return {"Error": "Customer could not be located."},404
