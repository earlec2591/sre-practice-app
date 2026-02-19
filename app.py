import time
import random
from flask import Flask, jsonify, Response
from flask import request as flask_request
import time as time_module
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

# Create the Flask application
# __name__ tells Flask where to find your app's files
app = Flask(__name__)

# Track when the app started (we'll use this for uptime)
START_TIME = time.time()

# Simulated metrics storage (in a real app, this would be a database)
request_count = 0

# === PROMETHEUS METRICS ===
# These are the "instruments" that Prometheus will read.
# There are 3 main types:

# COUNTER: A number that only goes UP (like a car's odometer)
# Use for: total requests, total errors, total bytes sent
REQUEST_COUNTER = Counter(
    "http_requests_total",           # Metric name (Prometheus convention: snake_case)
    "Total number of HTTP requests",  # Description
    ["method", "endpoint", "status"]  # Labels let you filter (e.g., show only errors)
)

# HISTOGRAM: Tracks the DISTRIBUTION of values (not just the average)
# Use for: request duration, response size
# WHY histogram over average? If 99 requests take 50ms and 1 takes 10s,
# the average is 149ms — that hides the terrible experience of that 1 user.
# Histograms give you percentiles (p50, p95, p99) which are much more useful.
REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "Time spent processing request",
    ["endpoint"]
)

# GAUGE: A number that can go UP or DOWN (like a speedometer)
# Use for: current CPU %, active connections, queue depth
APP_UPTIME = Gauge(
    "app_uptime_seconds",
    "Application uptime in seconds"
)

# === REQUEST HOOKS ===
# These functions run before and after every request

@app.before_request
def before_request_func():
    """Record the start time of each request."""
    flask_request.start_time = time_module.time()

@app.after_request
def after_request_func(response):
    """Record metrics for each request after it completes."""
    # Calculate how long the request took
    duration = time_module.time() - flask_request.start_time
    
    # Record the request in our counter
    REQUEST_COUNTER.labels(
        method=flask_request.method,
        endpoint=flask_request.path,
        status=response.status_code
    ).inc()  # inc() adds 1 to the counter
    
    # Record the duration in our histogram
    REQUEST_DURATION.labels(
        endpoint=flask_request.path
    ).observe(duration)  # observe() records the value
    
    # Update the uptime gauge
    APP_UPTIME.set(time_module.time() - START_TIME)
    
    return response

# === ROUTES ===
# Routes map URLs to Python functions.
# When someone visits the URL, Flask runs the function and returns the result.

@app.route("/")
def home():
    """Root endpoint — returns basic app info."""
    return jsonify({
        "app": "SRE Practice App",
        "version": "1.0.0",
        "status": "running"
    })
    # jsonify() converts a Python dict into JSON (the standard format for APIs)


@app.route("/health")
def health_check():
    """Health check endpoint.
    
    WHY THIS MATTERS: Every production service needs a health endpoint.
    Load balancers, Kubernetes, and monitoring tools hit this endpoint
    to decide if your app is alive and able to serve traffic.
    If this returns unhealthy, traffic gets routed away from this instance.
    """
    global request_count
    request_count += 1
    
    uptime_seconds = time.time() - START_TIME
    
    return jsonify({
        "status": "healthy",
        "uptime_seconds": round(uptime_seconds, 2),
        "total_requests": request_count
    })


@app.route("/metrics")
def metrics():
    """Metrics endpoint — exposes data for Prometheus to scrape.
    
    WHY THIS MATTERS: Prometheus (our monitoring tool) needs a place to
    collect numbers from your app. This endpoint gives it CPU, memory,
    and request data in a format Prometheus understands.
    We'll connect this to Prometheus and Grafana in Phase 4.
    """
    uptime_seconds = time.time() - START_TIME
    
    # Simulate some varying metrics
    # In a real app, you'd use the `psutil` library to get actual system stats
    simulated_cpu = random.uniform(10, 80)
    simulated_memory = random.uniform(30, 70)
    
    return jsonify({
        "cpu_percent": round(simulated_cpu, 2),
        "memory_percent": round(simulated_memory, 2),
        "uptime_seconds": round(uptime_seconds, 2),
        "request_count": request_count
    })


@app.route("/prometheus")
def prometheus_metrics():
    """Expose metrics in Prometheus format.
    
    WHY a separate endpoint? Prometheus has its own text format.
    The generate_latest() function converts our Python metric objects
    into that format. Prometheus will hit this endpoint every 15 seconds
    (configurable) to collect fresh data.
    """
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.route("/simulate/error")
def simulate_error():
    """Simulates a 500 error for incident response practice.
    
    WHY THIS MATTERS: SREs need to practice responding to errors.
    This endpoint deliberately fails so you can see what errors look like
    in your logs, metrics, and dashboards.
    """
    # Randomly decide if this request "fails"
    if random.random() < 0.5:
        return jsonify({"error": "Internal server error", "code": 500}), 500
    return jsonify({"status": "ok", "message": "No error this time"})


@app.route("/simulate/slow")
def simulate_slow():
    """Simulates a slow response (latency).
    
    WHY THIS MATTERS: Slow responses are one of the most common issues
    SREs deal with. This endpoint lets you practice detecting and
    alerting on high latency.
    """
    delay = random.uniform(0.1, 3.0)  # Random delay between 100ms and 3s
    time.sleep(delay)
    return jsonify({
        "status": "ok",
        "response_time_seconds": round(delay, 3)
    })


# Run the app
if __name__ == "__main__":
    # debug=True auto-reloads when you change code (NEVER use in production)
    # host="0.0.0.0" makes it accessible outside the container (needed for Docker)
    app.run(host="0.0.0.0", port=5000, debug=True)