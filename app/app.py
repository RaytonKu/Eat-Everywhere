#! /usr/bin/python

import sys
import redis
import prometheus_client
from flask import Flask, Response
from prometheus_client import Counter

#port = int(sys.argv[1])
db_port = 6379
app = Flask(__name__)
db = redis.Redis(host='db', port=db_port)

# TEST: try to insert some data to db
'''
db.set('foo', 'bar3')
msg = db.get('foo')
print(msg)
'''

total_requests = Counter('request_count', 'Total webapp request count')

@app.route('/metrics')
def requests_count():
    total_requests.inc()
    return Response(prometheus_client.generate_latest(total_requests), mimetype='text/plain')

# API Gateway
@app.route('/')
def main():
    return 'hello'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
