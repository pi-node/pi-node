from flask import Flask, request
from gunicorn.workers.gthread import ThreadWorker

app = Flask(__name__)

@app.route('/')
def index():
    # Distribute requests to different instances of pi-supernode
    if request.headers.get('X-Forwarded-For'):
        return f'Instance 1'
    else:
        return f'Instance 2'

if __name__ == '__main__':
    worker_class = ThreadWorker
    num_workers = 2
    app.run(host='0.0.0.0', port=8080, threaded=True, processes=num_workers)
