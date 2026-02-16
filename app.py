import time
import random
from flask import Flask, jsonify

# Create the Flask application
# __name__ tells Flask where to find your app's files
app = Flask(__name__)

# Track when the app started (we'll use this for uptime)
START_TIME = time.time()

# Simulated metrics storage (in a real app, this would be a database)
request_count = 0


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