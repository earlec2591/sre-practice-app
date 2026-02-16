# SRE Practice Application — Complete Project Roadmap

> **Your goal:** Build a Python web application from scratch, deploy it to AWS, and layer on professional SRE tooling (CI/CD, monitoring, alerting, infrastructure-as-code). By the end, you'll have a portfolio-ready project that demonstrates real SRE skills to employers.

---

## How This Roadmap Works

This plan is broken into **6 phases**, designed to be completed in order. Each phase builds on the previous one. At ~1 hour/day, expect each phase to take 1–2 weeks.

**Every step includes:**
- Exactly what to do (commands, code, config)
- **Why** you're doing it (the SRE reasoning)
- What to verify before moving on

**Tools you'll use (all free tier):**

| Tool | What It Does | Why SREs Use It |
|------|-------------|-----------------|
| Python + Flask | Your application | Simple, widely used for microservices |
| Git + GitHub | Version control & code hosting | Every SRE team uses Git daily |
| Docker | Containerization | Standard way to package & ship apps |
| GitHub Actions | CI/CD pipelines | Automates testing & deployment |
| Terraform | Infrastructure as Code | Defines infrastructure in reviewable, repeatable files |
| AWS (Free Tier) | Cloud hosting | Most common cloud platform in SRE roles |
| Prometheus | Metrics collection | Industry standard for collecting app & infra metrics |
| Grafana | Dashboards & alerting | Industry standard for visualizing metrics & setting alerts |

---

## Phase 0: Environment Setup (Days 1–2)

### Why this matters
Before writing any code, SREs need a clean, reproducible development environment. This is a habit you'll carry into every job — "works on my machine" is the enemy of reliability.

### Step 0.1 — Install Homebrew (if you don't have it)
Homebrew is macOS's package manager. It lets you install developer tools with one command instead of hunting for downloads.

```bash
# Open Terminal (Applications > Utilities > Terminal)
# Paste this command and press Enter:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Verify it works:
brew --version
```
**You should see** a version number like `Homebrew 4.x.x`.

### Step 0.2 — Install Python 3
macOS comes with an older Python. We want a modern version we control.

```bash
brew install python@3.12

# Verify:
python3 --version
```
**You should see** `Python 3.12.x`.

**Why Python 3.12?** It's a stable, well-supported version. In SRE, you generally avoid bleeding-edge versions because stability matters more than new features.

### Step 0.3 — Install Git (and configure it)
```bash
brew install git

# Tell Git who you are (used in commit history):
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"

# Verify:
git --version
```

### Step 0.4 — Install Docker Desktop
1. Go to https://www.docker.com/products/docker-desktop/
2. Download the **Mac with Apple chip** or **Mac with Intel chip** version (depending on your Mac)
3. Install and open it
4. Verify in Terminal:
```bash
docker --version
docker run hello-world
```
**You should see** a "Hello from Docker!" message.

**Why Docker?** Containers are how modern apps get deployed. They package your app + its dependencies into a single unit that runs the same everywhere. This eliminates "it works on my machine" problems.

### Step 0.5 — Install Terraform
```bash
brew tap hashicorp/tap
brew install hashicorp/tap/terraform

# Verify:
terraform --version
```

### Step 0.6 — Install VS Code (recommended editor)
1. Download from https://code.visualstudio.com/
2. Install the **Python extension** (search "Python" in the Extensions sidebar)

### Step 0.7 — Create your project directory
```bash
mkdir -p ~/projects/sre-practice-app
cd ~/projects/sre-practice-app
```

### ✅ Phase 0 Checkpoint
Run these and confirm all succeed:
```bash
python3 --version    # 3.12.x
git --version        # 2.x.x
docker --version     # 24.x or 27.x
terraform --version  # 1.x.x
```

---

## Phase 1: Python Fundamentals + Your First App (Days 3–9)

### Why this matters
You don't need to become a Python expert to be a great SRE. But you DO need to understand enough Python to: read application code during incidents, write automation scripts, and understand what the apps you support are actually doing.

### Step 1.1 — Python Basics (spend 2–3 days here)

Create a file called `learn_python.py` in your project folder. Work through each concept by typing it out (don't copy-paste — typing builds muscle memory).

```python
# === VARIABLES AND TYPES ===
# Variables store data. Python figures out the type automatically.
name = "SRE Practice App"    # str (text)
version = 1                   # int (whole number)
uptime = 99.99                # float (decimal number)
is_healthy = True             # bool (true/false)

# Print shows output in your terminal
print(f"App: {name}, Version: {version}")
# The f"..." syntax lets you embed variables inside strings.
# This is called an "f-string" — you'll use it constantly.

# === LISTS ===
# Lists hold multiple items in order. Think of them like a queue of alerts.
alerts = ["high CPU", "disk full", "service down"]
print(alerts[0])       # "high CPU" — lists start at index 0, not 1
alerts.append("memory leak")  # Add to the end
print(len(alerts))     # 4 — len() tells you how many items

# === DICTIONARIES ===
# Dicts store key-value pairs. Think of them like a config file.
# This is the most important data structure for SRE work.
server = {
    "hostname": "web-01",
    "cpu_percent": 72.5,
    "status": "healthy"
}
print(server["hostname"])  # "web-01"
server["memory_percent"] = 45.0  # Add a new key

# === CONDITIONALS ===
# if/elif/else let you make decisions in code
cpu = server["cpu_percent"]
if cpu > 90:
    print("CRITICAL: CPU over 90%")
elif cpu > 70:
    print("WARNING: CPU over 70%")
else:
    print("OK: CPU normal")

# === LOOPS ===
# For loops iterate over collections
for alert in alerts:
    print(f"Processing alert: {alert}")

# While loops keep going until a condition is false
retry_count = 0
while retry_count < 3:
    print(f"Retry attempt {retry_count + 1}")
    retry_count += 1  # += means "add to itself"

# === FUNCTIONS ===
# Functions are reusable blocks of code. They take inputs and return outputs.
# Why? So you don't repeat yourself. SREs write functions for health checks,
# metric calculations, alert logic, etc.
def check_health(cpu_percent, memory_percent):
    """Check if a server is healthy based on CPU and memory."""
    if cpu_percent > 90 or memory_percent > 90:
        return "unhealthy"
    elif cpu_percent > 70 or memory_percent > 70:
        return "degraded"
    else:
        return "healthy"

status = check_health(72.5, 45.0)
print(f"Server status: {status}")  # "degraded"

# === TRY/EXCEPT (Error Handling) ===
# In SRE, things WILL go wrong. try/except prevents your code from crashing.
try:
    result = 10 / 0  # This would normally crash
except ZeroDivisionError:
    print("Error: Can't divide by zero")
    result = 0  # Provide a safe default
print(f"Result: {result}")
```

**Run it:**
```bash
cd ~/projects/sre-practice-app
python3 learn_python.py
```

**Practice exercise:** Modify `check_health` to also check disk usage. Add a `disk_percent` parameter and include it in the logic.

### Step 1.2 — Build Your Flask Application (Days 5–7)

Flask is a Python web framework. It turns your Python code into a web server that responds to HTTP requests. Most microservices you'll support as an SRE are built on frameworks like this.

**First, set up a virtual environment:**
```bash
cd ~/projects/sre-practice-app

# Create a virtual environment (an isolated space for this project's packages)
python3 -m venv venv

# Activate it (you'll do this every time you work on the project)
source venv/bin/activate

# Your prompt should now show (venv) at the beginning
```

**Why virtual environments?** They keep each project's dependencies separate. Without them, installing a package for one project could break another. SREs deal with dependency conflicts constantly — this is your first taste of that.

**Install Flask:**
```bash
pip install flask
```

**Create the app — `app.py`:**
```python
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
```

**Run it:**
```bash
python3 app.py
```

**Test it (open a NEW terminal tab):**
```bash
curl http://localhost:5000/
curl http://localhost:5000/health
curl http://localhost:5000/metrics
curl http://localhost:5000/simulate/error
curl http://localhost:5000/simulate/slow
```

**What to look for:** Each `curl` command sends an HTTP request to your app and shows the JSON response. You should see different data each time you hit `/metrics` (because the values are simulated).

### Step 1.3 — Add Requirements File
```bash
# Make sure your venv is activated, then:
pip freeze > requirements.txt
```

**Why?** `requirements.txt` lists every package your app needs. When someone else (or a Docker container) needs to run your app, they run `pip install -r requirements.txt` to get the exact same packages. Reproducibility is a core SRE principle.

### Step 1.4 — Initialize Git and Push to GitHub (Days 8–9)

**Create a `.gitignore` file** (tells Git which files to NOT track):
```bash
cat > .gitignore << 'EOF'
venv/
__pycache__/
*.pyc
.env
.DS_Store
EOF
```

**Why .gitignore?** Your virtual environment (`venv/`) contains thousands of files that can be recreated from `requirements.txt`. Tracking them would bloat your repo and cause merge conflicts. Same with `__pycache__` (Python's auto-generated cache files).

**Initialize Git and make your first commit:**
```bash
cd ~/projects/sre-practice-app
git init
git add .
git commit -m "Initial commit: Flask app with health, metrics, and simulation endpoints"
```

**Push to GitHub:**
1. Go to https://github.com/new
2. Name it `sre-practice-app`
3. Leave it **Public** (good for your portfolio)
4. Do NOT initialize with README (you already have files)
5. Click "Create repository"
6. Run the commands GitHub shows you:
```bash
git remote add origin https://github.com/YOUR-USERNAME/sre-practice-app.git
git branch -M main
git push -u origin main
```

### ✅ Phase 1 Checkpoint
- [ ] `python3 app.py` starts the server
- [ ] `curl http://localhost:5000/health` returns JSON with status "healthy"
- [ ] Your code is on GitHub
- [ ] You can explain what a route, a function, and a JSON response are

---

## Phase 2: Dockerize the Application (Days 10–13)

### Why this matters
Containers solve one of SRE's biggest headaches: **environment inconsistency**. When your app runs in Docker, it runs the same way on your laptop, on a coworker's laptop, in CI/CD, and in production. "Works on my machine" becomes "works everywhere."

### Step 2.1 — Create a Dockerfile

A Dockerfile is a recipe that tells Docker how to build an image of your app. Think of it like a checklist: start with a base OS, copy files, install dependencies, run the app.

Create `Dockerfile` in your project root:
```dockerfile
# Start from the official Python 3.12 image
# "slim" means it's a minimal version (smaller = faster to build and deploy)
# WHY: SREs prefer slim images because they have fewer packages,
# which means fewer security vulnerabilities and faster deploy times.
FROM python:3.12-slim

# Set the working directory inside the container
# All following commands will run relative to /app
WORKDIR /app

# Copy requirements first, THEN install them
# WHY: Docker caches each step. If your requirements haven't changed,
# Docker skips the install step. This makes rebuilds much faster.
# This is called "layer caching" — understanding it will save you
# tons of time in CI/CD pipelines.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of your application
COPY . .

# Tell Docker this container listens on port 5000
# This is documentation — it doesn't actually publish the port
EXPOSE 5000

# The command to run when the container starts
# WHY we use gunicorn instead of flask's built-in server:
# Flask's dev server handles one request at a time. Gunicorn is a
# production-grade server that handles multiple requests concurrently.
# Every SRE should know: never run Flask's dev server in production.
CMD ["python", "app.py"]
```

### Step 2.2 — Add gunicorn (production server)

```bash
source venv/bin/activate
pip install gunicorn
pip freeze > requirements.txt
```

Now update the last line of your Dockerfile:
```dockerfile
# Replace the CMD line with:
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
# --bind: what address/port to listen on
# --workers 2: run 2 worker processes to handle concurrent requests
# "app:app": first "app" = the filename (app.py), second "app" = the Flask variable name
```

### Step 2.3 — Build and Run the Container

```bash
# Build the Docker image (the -t flag gives it a name/tag)
docker build -t sre-practice-app:v1 .

# Run it
docker run -d -p 5000:5000 --name sre-app sre-practice-app:v1
# -d: run in background (detached)
# -p 5000:5000: map port 5000 on your Mac to port 5000 in the container
# --name: give the container a human-readable name
```

**Test it:**
```bash
curl http://localhost:5000/health
```

**Useful Docker commands you'll use constantly as an SRE:**
```bash
docker ps                    # See running containers
docker logs sre-app          # View container logs (like checking app logs during an incident)
docker exec -it sre-app sh   # Open a shell INSIDE the container (for debugging)
docker stop sre-app          # Stop the container
docker rm sre-app            # Remove the container
```

### Step 2.4 — Create docker-compose.yml

Docker Compose lets you define multi-container setups in a single file. We'll need this when we add Prometheus and Grafana later.

Create `docker-compose.yml`:
```yaml
# docker-compose.yml
version: "3.8"

services:
  app:
    build: .
    ports:
      - "5000:5000"
    # Restart automatically if the container crashes
    # WHY: In production, you want services to self-heal from transient failures.
    # "unless-stopped" means: always restart, unless I manually stopped it.
    restart: unless-stopped
```

**Run with Compose:**
```bash
docker compose up -d --build
# --build: rebuild the image if files changed
# -d: detached mode (background)

# Verify:
docker compose ps
curl http://localhost:5000/health

# Stop everything:
docker compose down
```

### Step 2.5 — Commit and Push
```bash
git add .
git commit -m "Add Docker support with Dockerfile and docker-compose"
git push
```

### ✅ Phase 2 Checkpoint
- [ ] `docker compose up -d --build` starts your app
- [ ] `curl http://localhost:5000/health` returns healthy
- [ ] `docker logs <container>` shows request logs
- [ ] You can explain why containers matter for reliability

---

## Phase 3: CI/CD with GitHub Actions (Days 14–20)

### Why this matters
CI/CD (Continuous Integration / Continuous Delivery) is the automated pipeline that tests and deploys your code every time you push a change. Without CI/CD, deployments are manual, error-prone, and scary. With it, they're automatic, tested, and routine. **Every SRE job description mentions CI/CD.**

### Step 3.1 — Add a Simple Test

First, let's add something for CI to actually test. Install pytest:
```bash
source venv/bin/activate
pip install pytest
pip freeze > requirements.txt
```

Create `test_app.py`:
```python
"""Tests for the SRE Practice App.

WHY TESTS MATTER FOR SREs:
Tests are your safety net. They catch bugs BEFORE code reaches production.
In CI/CD, tests run automatically on every push. If a test fails,
the pipeline stops and the bad code never gets deployed.
This is how you prevent incidents.
"""
import json
from app import app


def test_home():
    """Test that the home endpoint returns expected data."""
    # Flask provides a test client so you don't need a running server
    client = app.test_client()
    response = client.get("/")
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data["app"] == "SRE Practice App"
    assert "version" in data


def test_health():
    """Test the health check endpoint."""
    client = app.test_client()
    response = client.get("/health")
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data["status"] == "healthy"
    assert "uptime_seconds" in data


def test_metrics():
    """Test that metrics endpoint returns expected fields."""
    client = app.test_client()
    response = client.get("/metrics")
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert "cpu_percent" in data
    assert "memory_percent" in data
    assert isinstance(data["cpu_percent"], float)
```

**Run tests locally:**
```bash
pytest test_app.py -v
# -v = verbose (shows each test name and result)
```

### Step 3.2 — Create GitHub Actions Workflow

GitHub Actions is GitHub's built-in CI/CD system. It runs your pipeline in the cloud for free (2,000 minutes/month on free tier).

Create the directory structure:
```bash
mkdir -p .github/workflows
```

Create `.github/workflows/ci.yml`:
```yaml
# This file tells GitHub Actions WHAT to do and WHEN to do it.
# It lives in your repo, so it's version-controlled just like your code.
# WHY: "Pipeline as code" means your CI/CD config is reviewable,
# auditable, and reproducible — core SRE principles.

name: CI Pipeline

# WHEN to run this pipeline:
on:
  push:
    branches: [main]       # Run on every push to main
  pull_request:
    branches: [main]       # Run on PRs targeting main

jobs:
  test:
    # WHERE to run: a fresh Ubuntu virtual machine provided by GitHub
    runs-on: ubuntu-latest
    
    steps:
      # Step 1: Check out your code
      - name: Checkout code
        uses: actions/checkout@v4
        # WHY: The runner starts empty. This copies your repo into it.
      
      # Step 2: Set up Python
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      
      # Step 3: Install dependencies
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest
      
      # Step 4: Run tests
      - name: Run tests
        run: pytest test_app.py -v
  
  build-docker:
    # This job runs AFTER tests pass
    needs: test  # "needs" creates a dependency between jobs
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      # Verify the Docker image builds successfully
      - name: Build Docker image
        run: docker build -t sre-practice-app:${{ github.sha }} .
        # ${{ github.sha }} tags the image with the commit hash
        # WHY: Tagging with the commit hash means you can always trace
        # a running container back to the exact code that built it.
        # This is critical during incidents when you need to know
        # "what version is actually running?"
```

### Step 3.3 — Push and Watch It Run

```bash
git add .
git commit -m "Add CI pipeline with tests and Docker build"
git push
```

**Now go to GitHub:**
1. Navigate to your repo
2. Click the **Actions** tab
3. You should see your pipeline running!
4. Click into it to watch each step execute in real-time

**If it passes:** You'll see green checkmarks. Congratulations — you have CI!

**If it fails:** Click the failed step to read the error logs. This is exactly what you'd do as an SRE when a deployment pipeline fails. Debug it, fix it, push again.

### Step 3.4 — Add a Branch Protection Rule (Optional but Recommended)

1. Go to your repo → Settings → Branches
2. Click "Add rule"
3. Branch name pattern: `main`
4. Check "Require status checks to pass before merging"
5. Select your CI jobs

**Why?** This prevents anyone (including you) from pushing broken code directly to main. All changes must go through a pull request and pass CI first. This is how professional teams protect production.

### ✅ Phase 3 Checkpoint
- [ ] Pushing to main triggers the CI pipeline
- [ ] Tests pass in GitHub Actions
- [ ] Docker image builds in the pipeline
- [ ] You can read the Actions logs to diagnose a failure

---

## Phase 4: Monitoring & Alerting with Prometheus + Grafana (Days 21–30)

### Why this matters
**Monitoring is the heart of SRE.** You can't keep a system reliable if you can't see what it's doing. Prometheus collects metrics (numbers like CPU %, request count, error rate). Grafana turns those numbers into dashboards and alerts. Together, they're the industry standard.

### Step 4.1 — Add Prometheus Metrics to Your App

Install the Prometheus client library:
```bash
source venv/bin/activate
pip install prometheus-client
pip freeze > requirements.txt
```

Update your `app.py` — add these imports at the top:
```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
```

Add these metric definitions right after `request_count = 0`:
```python
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
```

Add a `before_request` and `after_request` hook to automatically track every request:
```python
from flask import request as flask_request
import time as time_module

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
```

Add a `/prometheus` endpoint that Prometheus will scrape:
```python
@app.route("/prometheus")
def prometheus_metrics():
    """Expose metrics in Prometheus format.
    
    WHY a separate endpoint? Prometheus has its own text format.
    The generate_latest() function converts our Python metric objects
    into that format. Prometheus will hit this endpoint every 15 seconds
    (configurable) to collect fresh data.
    """
    from flask import Response
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
```

### Step 4.2 — Add Prometheus to Docker Compose

Create `prometheus.yml` (Prometheus configuration):
```yaml
# prometheus.yml
# This tells Prometheus WHERE to collect metrics FROM and HOW OFTEN.

global:
  scrape_interval: 15s  # Collect metrics every 15 seconds
  # WHY 15s? It's a balance between freshness and overhead.
  # Too frequent = too much load on your app. Too infrequent = you miss short spikes.

scrape_configs:
  # Each "job" is a group of targets to scrape
  - job_name: "sre-practice-app"
    # Where is the metrics endpoint?
    static_configs:
      - targets: ["app:5000"]
        # "app" = the service name from docker-compose.yml
        # Docker Compose creates a network where services can find each other by name
    metrics_path: "/prometheus"  # The endpoint we created in Step 4.1
```

Update `docker-compose.yml` to add Prometheus and Grafana:
```yaml
version: "3.8"

services:
  app:
    build: .
    ports:
      - "5000:5000"
    restart: unless-stopped

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      # Mount our config file into the container
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    restart: unless-stopped
    # WHY volumes? Volumes let you share files between your Mac and the container.
    # We're saying "take our local prometheus.yml and put it inside the container
    # at /etc/prometheus/prometheus.yml"

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      # Default login will be admin/admin
      # In production, you'd NEVER put passwords in docker-compose.
      # You'd use secrets management. For learning, this is fine.
    restart: unless-stopped
```

### Step 4.3 — Start Everything and Verify

```bash
docker compose up -d --build

# Verify all 3 services are running:
docker compose ps

# Check your app:
curl http://localhost:5000/health

# Check Prometheus can reach your app:
# Open in browser: http://localhost:9090
# Go to Status > Targets — you should see your app listed as "UP"

# Check your metrics exist in Prometheus:
# In the Prometheus query box, type: http_requests_total
# Click "Execute" — you should see data
```

### Step 4.4 — Set Up Grafana Dashboard

1. Open http://localhost:3000 in your browser
2. Login with `admin` / `admin` (skip the password change for now)
3. **Add Prometheus as a data source:**
   - Go to Connections → Data Sources → Add data source
   - Select Prometheus
   - URL: `http://prometheus:9090` (container-to-container networking)
   - Click "Save & Test" — should say "Data source is working"

4. **Create your first dashboard:**
   - Click Dashboards → New Dashboard → Add Visualization
   - Select Prometheus as the data source
   
5. **Add these panels (one at a time):**

**Panel 1: Request Rate**
- Query: `rate(http_requests_total[5m])`
- Title: "Requests Per Second"
- **Why rate()?** `http_requests_total` only goes up. `rate()` calculates how fast it's increasing, giving you requests per second. The `[5m]` means "calculate the rate over 5-minute windows."

**Panel 2: Error Rate**
- Query: `rate(http_requests_total{status="500"}[5m])`
- Title: "Error Rate (5xx)"
- **Why this matters:** Error rate is one of the "Four Golden Signals" that Google SRE recommends monitoring for every service.

**Panel 3: Request Duration (p95)**
- Query: `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))`
- Title: "Request Duration (p95)"
- **Why p95?** "95% of requests complete faster than this value." If your p95 is 2 seconds, that means 5% of your users are waiting more than 2 seconds. This is more useful than average because it shows worst-case experience.

**Panel 4: Uptime**
- Query: `app_uptime_seconds`
- Title: "App Uptime"

6. **Save the dashboard** as "SRE Practice App"

### Step 4.5 — Generate Some Traffic for Your Dashboard

Create a simple load generator script — `load_test.sh`:
```bash
#!/bin/bash
# Sends random requests to your app to generate dashboard data
echo "Generating traffic... Press Ctrl+C to stop"
while true; do
    curl -s http://localhost:5000/health > /dev/null
    curl -s http://localhost:5000/metrics > /dev/null
    curl -s http://localhost:5000/simulate/error > /dev/null
    curl -s http://localhost:5000/simulate/slow > /dev/null
    sleep 0.5
done
```

```bash
chmod +x load_test.sh
./load_test.sh
```

Now watch your Grafana dashboard update in real-time! You should see request rates climbing, occasional errors spiking, and latency variations.

### Step 4.6 — Commit and Push
```bash
git add .
git commit -m "Add Prometheus metrics and Grafana monitoring"
git push
```

### ✅ Phase 4 Checkpoint
- [ ] Prometheus shows your app as "UP" in targets
- [ ] You have a Grafana dashboard with at least 4 panels
- [ ] Running the load test makes your graphs move
- [ ] You can explain what a counter, histogram, and gauge are

---

## Phase 5: Infrastructure as Code with Terraform + AWS (Days 31–42)

### Why this matters
Manually clicking through the AWS console to create resources is slow, error-prone, and impossible to reproduce. Terraform lets you define your infrastructure in code files. Need the same setup in a new region? Run `terraform apply`. Need to know what changed? Check the Git log. **IaC is a non-negotiable SRE skill.**

### Step 5.1 — Configure AWS CLI

```bash
brew install awscli

aws configure
# Enter your AWS Access Key ID
# Enter your Secret Access Key
# Default region: us-east-1 (cheapest, most services available)
# Default output: json
```

**Where to find your keys:** AWS Console → IAM → Users → Your user → Security credentials → Create access key

⚠️ **IMPORTANT:** Never commit AWS keys to Git. They're stored in `~/.aws/credentials` on your machine.

### Step 5.2 — Your First Terraform Config

Create a `terraform/` directory:
```bash
mkdir -p terraform
cd terraform
```

Create `terraform/main.tf`:
```hcl
# main.tf
# This file defines WHAT infrastructure you want.

# Tell Terraform we're using AWS
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"  # Use version 5.x
    }
  }
}

# Configure the AWS provider
provider "aws" {
  region = "us-east-1"
}

# === VPC (Virtual Private Cloud) ===
# A VPC is your own private network inside AWS.
# WHY: You never put servers on the public internet directly.
# A VPC gives you control over who can access what.
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "sre-practice-vpc"
  }
}

# === Public Subnet ===
# A subnet is a section of your VPC.
# "Public" means it can reach the internet (for your web app).
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "us-east-1a"

  tags = {
    Name = "sre-practice-public-subnet"
  }
}

# === Internet Gateway ===
# Connects your VPC to the internet
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "sre-practice-igw"
  }
}

# === Route Table ===
# Tells traffic where to go. This route says:
# "For any address not in our VPC (0.0.0.0/0 = everywhere), 
#  send traffic to the internet gateway."
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "sre-practice-public-rt"
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

# === Security Group ===
# Acts like a firewall. Defines what traffic is allowed in and out.
resource "aws_security_group" "app" {
  name        = "sre-practice-app-sg"
  description = "Allow HTTP and SSH access"
  vpc_id      = aws_vpc.main.id

  # Allow HTTP (port 80) from anywhere
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow your app (port 5000) from anywhere
  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow SSH (port 22) from anywhere
  # NOTE: In production, you'd restrict this to your IP only!
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "sre-practice-app-sg"
  }
}

# === EC2 Instance ===
# This is your actual server in the cloud.
resource "aws_instance" "app" {
  ami                    = "ami-0c7217cdde317cfec"  # Ubuntu 22.04 in us-east-1
  instance_type          = "t2.micro"                # Free tier eligible!
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.app.id]

  # Script that runs when the instance first boots
  user_data = <<-EOF
              #!/bin/bash
              apt-get update
              apt-get install -y docker.io docker-compose
              systemctl start docker
              systemctl enable docker
              EOF

  tags = {
    Name = "sre-practice-app"
  }
}

# === Outputs ===
# Print useful info after terraform apply
output "instance_public_ip" {
  value       = aws_instance.app.public_ip
  description = "Public IP of the EC2 instance"
}
```

### Step 5.3 — Run Terraform

```bash
cd terraform

# Initialize Terraform (downloads the AWS provider plugin)
terraform init

# See what Terraform WOULD do (without actually doing it)
terraform plan
# Read this output carefully! It shows exactly what will be created.
# WHY: Always review the plan. In production, a wrong `terraform apply`
# could delete a database or expose a service to the internet.

# Actually create the infrastructure
terraform apply
# Type "yes" when prompted

# Note the public IP it outputs — you'll need it!
```

**After it completes,** go to the AWS Console → EC2 → Instances and you'll see your server running!

### Step 5.4 — Clean Up to Avoid Charges

When you're done practicing for the day:
```bash
terraform destroy
# Type "yes" when prompted
# This deletes EVERYTHING Terraform created — no surprise bills
```

**WHY `terraform destroy` is important:** EC2 instances cost money when running. The t2.micro is free-tier eligible (750 hours/month for 12 months), but it's a good habit to destroy resources you're not using. SREs are often responsible for cloud costs.

### Step 5.5 — Commit Terraform Config
```bash
cd ~/projects/sre-practice-app

# Add a .gitignore for Terraform
cat >> .gitignore << 'EOF'

# Terraform
.terraform/
*.tfstate
*.tfstate.backup
*.tfvars
EOF

git add .
git commit -m "Add Terraform IaC for AWS infrastructure"
git push
```

**Why ignore .tfstate?** The state file contains your real infrastructure's details. In a team, you'd store it in a shared backend (like S3). For a solo project, keeping it local is fine, but never commit it — it can contain secrets.

### ✅ Phase 5 Checkpoint
- [ ] `terraform plan` shows resources to create
- [ ] `terraform apply` creates resources in AWS
- [ ] You can see the EC2 instance in the AWS console
- [ ] `terraform destroy` removes everything
- [ ] You can explain what a VPC, subnet, and security group are

---

## Phase 6: Putting It All Together (Days 43–50+)

### Why this matters
Real SRE work isn't about using tools in isolation — it's about how they connect. This phase ties everything together into a workflow that mirrors a real job.

### Step 6.1 — The Complete Workflow

Here's the loop you should practice until it feels natural:

1. **Write code** → Make a change to `app.py` (add a new endpoint, fix a bug)
2. **Test locally** → Run `pytest` to make sure nothing broke
3. **Commit & push** → `git add . && git commit -m "message" && git push`
4. **CI runs automatically** → Watch GitHub Actions run tests and build Docker
5. **Deploy** → Use `terraform apply` to update infrastructure if needed
6. **Monitor** → Watch Grafana dashboards for the impact of your change
7. **Alert** → When something breaks, notice it in Grafana and respond

### Step 6.2 — Practice Scenarios

These simulate real SRE situations. Try one per day:

**Scenario 1: Deploy a Bad Change**
- Add a bug to `app.py` (e.g., make `/health` return status 500)
- Push it. Watch CI. Does it catch the bug?
- If not, add a test that WOULD catch it, then fix the bug

**Scenario 2: Capacity Alert**
- Modify `load_test.sh` to send 10x more traffic
- Watch Grafana — what happens to latency and error rate?
- Add a Grafana alert that fires when p95 latency > 2 seconds

**Scenario 3: Infrastructure Change**
- Modify `main.tf` to change the instance type
- Run `terraform plan` — understand what will change
- Apply it and verify the app still works

**Scenario 4: Write a Runbook**
Create a `runbooks/high-latency.md` file:
```markdown
# Runbook: High Latency Alert

## Trigger
p95 latency > 2 seconds for 5 minutes

## Steps
1. Check Grafana dashboard for affected endpoints
2. Check if traffic increased (request rate panel)
3. SSH into the server: check CPU, memory, disk
4. Check application logs for errors
5. If caused by load: scale up or add caching
6. If caused by a deploy: roll back to previous version

## Escalation
If not resolved in 15 minutes, page the on-call engineer.
```

**Why runbooks?** During an incident at 3 AM, you won't remember the right steps. Runbooks remove the need to think under pressure. Every good SRE team has them.

---

## What to Add to Your Resume

Once you've completed this project, you can honestly claim experience with:

- **Python** — built a REST API with Flask, including health checks and metrics endpoints
- **Docker** — containerized an application with multi-stage compose setup
- **CI/CD** — built automated test and build pipelines with GitHub Actions
- **Monitoring & Observability** — implemented Prometheus metrics (counters, histograms, gauges) with Grafana dashboards
- **Infrastructure as Code** — provisioned AWS infrastructure (VPC, EC2, security groups) with Terraform
- **SRE Practices** — health checks, SLI/SLO concepts, runbooks, incident simulation

---

## Quick Reference: Daily Commands

```bash
# Start your dev environment
cd ~/projects/sre-practice-app
source venv/bin/activate

# Start all services (app + Prometheus + Grafana)
docker compose up -d --build

# Run tests
pytest test_app.py -v

# View logs
docker compose logs -f app

# Push a change
git add .
git commit -m "your message"
git push

# Terraform
cd terraform
terraform plan
terraform apply
terraform destroy  # When done for the day!

# Stop everything
docker compose down
```

---

> **Remember:** The goal isn't to rush through this. Spend time with each phase. Break things on purpose and fix them. That's how real SRE skills are built. Every incident you cause and resolve in your practice environment is one you'll handle better in production.
