# === Variables and Types ===
#Variables store data.  Python figures out the type automatically. 
name = "SRE Practice App" # string
version = 1 # int - whole number
uptime = 99.99 # float - decimal number
is_healthy = True # boolean - True or False

# Print shows output in the terminal
print(f"App Name: {name}, Version: {version}, Uptime: {uptime}%, Healthy: {is_healthy}")
# The f"..." syntax lets you embed variables inside strings
# This is called an "f-string"

# === Lists ===
alerts = ["high CPU", "disk full", "service down"]
print(alerts[0]) # Accesses the first alert. "High CPU" - list starts at index 0, not 1
alerts.append("memory leak") # Adds a new alert to the list
print(len(alerts)) # Shows how many alerts are in the list. len() tells you how many items are in a list

# === Dictionaries ===
# Dicts store key-value pairs.  You can look up values by their keys. Think of them like a config file.
# This is the most improtant data structure for SRE work.
server = {
    "hostname": "web-01",
    "cpu_percent": 72.5,
    "status": "healthy"
}
print(server["hostname"]) # Accesses the hostname value. "web-01"
server["memory_percent"] = 45 # Adds a new key-value pair to the dict

# === Conditional Statements ===
cpu = server["cpu_percent"]
if cpu > 90:
    print("Critical: CPU over 90%")
elif cpu > 70:
    print("Warning: CPU over 70%")
else:
    print("Okay: CPU normal")

# === Loops ===
# For loops iterate over collections like lists.  They let you do something for each item in the list.
for alert in alerts:
    print(f"Processing alert: {alert}")

# While loops repeat as long as a condition is true.  Be careful to avoid infinite loops!
retry_count = 0
while retry_count < 3:
    print(f"Retry attempt {retry_count + 1}")
    retry_count += 1 # += means "add to itself"

# === Functions === 
# Functions are reusable blocks of code that perform a specific task.  
# They can take inputs (called "arguments") and return outputs.
# SREs write functions for health checks, metrics calculations, alert logging, and more.
def check_health(cpu_percent, memory_percent):
    if cpu_percent > 90 or memory_percent > 90:
        return "unhealthy"
    elif cpu_percent > 70 or memory_percent > 70:
        return "degraded"
    else:
        return "healthy"
    
status = check_health(72.5, 45.0)
print(f"Server status: {status}") # degraded

# === Try/Except ===
# Try/Except blocks let you handle errors gracefully instead of crashing your program.
try:
    result = 10 / 0 # This will cause a ZeroDivisionError
except ZeroDivisionError:
    print("Error: Cannot divide by zero!")
    result = 0 # Provide a safe default value
print(f"Result: {result}") # Result: 0