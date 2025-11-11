"""
Gunicorn configuration file for Racker production deployment
"""
import os
import multiprocessing
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv(dotenv_path=Path(__file__).resolve().parent / '.env')

# Server socket
bind = f"{os.getenv('BIND_ADDRESS', '127.0.0.1')}:{os.getenv('SERVER_PORT', '8000')}"

# Worker processes
workers_env = os.getenv('GUNICORN_WORKERS', '')
if workers_env:
    workers = int(workers_env)
else:
    # Auto-calculate: 2-4 x CPU cores (recommended)
    workers = multiprocessing.cpu_count() * 2 + 1

# Worker class - use uvicorn for async support
worker_class = 'uvicorn.workers.UvicornWorker'

# Worker connections
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50

# Timeout
timeout = 120
graceful_timeout = 30
keepalive = 5

# Logging
accesslog = os.getenv('GUNICORN_ACCESS_LOG', '-')  # - means stdout
errorlog = os.getenv('GUNICORN_ERROR_LOG', '-')    # - means stderr
loglevel = os.getenv('GUNICORN_LOG_LEVEL', 'info')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'racker'

# Server mechanics
daemon = False  # We'll use systemd for daemonization
pidfile = None  # Let systemd handle PID
umask = 0
user = None     # Set by systemd
group = None    # Set by systemd
tmp_upload_dir = None

# SSL (if needed)
keyfile = os.getenv('SSL_KEYFILE', None)
certfile = os.getenv('SSL_CERTFILE', None)

# Preload app for better performance
preload_app = True

# Django WSGI application path
wsgi_app = 'backend.wsgi:application'

def when_ready(server):
    """Called just after the server is started."""
    server.log.info("Gunicorn server is ready. Spawning workers")

def on_starting(server):
    """Called just before the master process is initialized."""
    server.log.info("Starting Gunicorn server")

def on_reload(server):
    """Called to recycle workers during a reload via SIGHUP."""
    server.log.info("Reloading Gunicorn server")

def worker_int(worker):
    """Called just after a worker exited on SIGINT or SIGQUIT."""
    worker.log.info("Worker received INT or QUIT signal")

def worker_abort(worker):
    """Called when a worker receives the SIGABRT signal."""
    worker.log.info("Worker received SIGABRT signal")
