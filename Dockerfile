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
# CMD ["python", "app.py"]

# Replace the CMD line with:
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
# --bind: what address/port to listen on
# --workers 2: run 2 worker processes to handle concurrent requests
# "app:app": first "app" = the filename (app.py), second "app" = the Flask variable name