#! /usr/bin/python

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

# TEST
#db.hmset('test_store', {'store_addr':'test_addr', 'store_tel':'test_tel', 'store_dishes1':'test_dishes1', 'store_dishes2':'test_dishes2', 'store_dishes3':'test_dishes3'})
#db.hset('test_store', 'store_addr', 'test_addr')
#db.hset('test_store', 'store_tel', 'test_tel')
#db.hset('test_store', 'store_dishes1', 'test_dishes1')
#db.hset('test_store', 'store_dishes2', 'test_dishes2')
#db.hset('test_store', 'store_dishes3', 'test_dishes3')

#db.hset('23456789', 'store_name', 'test_store')
#db.hset('23456789', 'order_time', '2021-11-20 19:00')

# Gateway
@app.route('/')
def main():
    return 'hello'

@app.route('/eats/stores')
def get_stores():
    return 'stores'

@app.route('/eats/stores/get_store/<store_name>', methods=['GET'])
def get_stores_by_name(store_name):
	store_addr = db.hget(store_name, 'store_addr').decode()
	store_tel = db.hget(store_name, 'store_tel').decode()
	store_dishes1 = db.hget(store_name, 'store_dishes1').decode()
	store_dishes2 = db.hget(store_name, 'store_dishes2').decode()
	store_dishes3 = db.hget(store_name, 'store_dishes3').decode()
	store = {'store_name':store_name, 'store_addr':store_addr, 'store_tel':store_tel, 'store_dishes1':store_dishes1, 'store_dishes2':store_dishes2, 'store_dishes3':store_dishes3}
	return json.dumps(store)

@app.route('/eats/stores/add_store', methods=['POST'])
def add_store():
    store_name = request.values.get('store_name')
    store_addr = request.values.get('store_addr')
    store_tel = request.values.get('store_tel')
    store_dishes1 = request.values.get('store_dishes1')
    store_dishes2 = request.values.get('store_dishes2')
    store_dishes3 = request.values.get('store_dishes3')
    db.hset(store_name, 'store_addr', store_addr)
    db.hset(store_name, 'store_tel', store_tel)
    db.hset(store_name, 'store_dishes1', store_dishes1)
    db.hset(store_name, 'store_dishes2', store_dishes2)
    db.hset(store_name, 'store_dishes3', store_dishes3)
    return 'store added'

@app.route('/eats/stores/del_store/<store_name>', methods=['POST'])
def del_store():
	pass

@app.route('/eats/orders/get_order/<customer_tel>', methods=['GET'])
def get_order(customer_tel):
    store_name = db.hget(customer_tel, 'store_name').decode()
    order_time = db.hget(customer_tel, 'order_time').decode()
    order = {'customer_tel':customer_tel, 'store_name':store_name, 'order_time': order_time}
    return json.dumps(order)

@app.route('/eats/orders/add_order', methods=['POST'])
def add_order():
    customer_tel = request.values.get('customer_tel')
    store_name = request.values.get('store_name')
    order_time = request.values.get('order_time')
    db.hset(customer_tel, 'store_name', store_name)
    db.hset(customer_tel, 'order_time', order_time)
    return 'order added'

@app.route('/eats/orders/del_order/<customer_tel>', methods=['POST'])
def del_order():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
