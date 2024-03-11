bind = '0.0.0.0:8001'
workers = 4
worker_class = 'uvicorn.workers.UvicornWorker'

errorlog = '-'
loglevel = 'debug'
accesslog = '-'
proxy_protocol = True
