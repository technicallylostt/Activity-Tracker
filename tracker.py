import csv
import psutil
import platform
import socket
import speedtest
import os
import subprocess
import time
from datetime import datetime
from AppKit import NSWorkspace

# File info
date_str = datetime.now().strftime("%Y-%m-%d")
os.makedirs("logs", exist_ok=True)
csv_file = os.path.join("logs", f"activity_log_{date_str}.csv")

# header if file doesn't exist
write_header = not os.path.exists(csv_file)

if write_header:
    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Device", "App Type", "App Name", "Host", "IP",
                             "Start Time", "End Time", "Network", "ISP", "Source URL"])

# Detect if system is a laptop or desktop
def get_device_type():
    battery = psutil.sensors_battery()
    if battery is not None:
        return "Laptop"
    else:
        return "Desktop"

device_type = get_device_type()

# Host name of system
hostname = socket.gethostname()

# Active tab type and name
def get_active_app_info():
    system = platform.system()

    known_browsers = {
        ["Safari", "Google Chrome", "Firefox", "Brave Browser", "Microsoft Edge"]
    }
    try:
            from AppKit import NSWorkspace
            app = NSWorkspace.sharedWorkspace().activeApplication()
            app_name = app['NSApplicationName']
            app_type = "Browser" if app_name in known_browsers else "Application"
            return app_type, app_name
    except Exception as e:
            return "Unknown", "Unknown" + str(e)

app_type, app_name = get_active_app_info()

# Determine source of url if browser
def get_browser_url(app_name):
    try:
        if app_name == "Google Chrome":
            script = 'tell application "Google Chrome" to get URL of active tab of front window'
        elif app_name == "Safari":
            script = 'tell application "Safari" to get URL of front document'
        else:
            return ""
        url = subprocess.check_output(
            ['osascript', '-e', script]).decode().strip()
        return url
    except:
        return ""

# Local IP address
ip_address = socket.gethostbyname(hostname)


# Network type
def get_network_type():
    try:
        output = subprocess.check_output(
            ["networksetup", "-getinfo", "Wi-Fi"]).decode()
        if "IP address" in output and "None" not in output:
            return "WiFi"
    except:
        pass
    return "Ethernet"  # fallback

network = get_network_type()

# ISP info
st = speedtest.Speedtest()
isp = st.get_best_server()['sponsor']


# Create a CSV file to log activity daywise
def log_activity(app_type, app_name, start_time, end_time):
    source_url = get_browser_url(app_name) if app_type == "Browser" else ""    
    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            device_type, app_type, app_name,
            hostname, ip_address,
            start_time.strftime("%H:%M:%S"),
            end_time.strftime("%H:%M:%S"),
            network, isp, source_url
        ])

# Time Tracking
print("Monitoring activity. Press Ctrl+C to stop.")
previous_app_type, previous_app_name = get_active_app_info()
start_time = datetime.now()

try:
    while True:
        time.sleep(1)
        current_app_type, current_app_name = get_active_app_info()

        if (current_app_name != previous_app_name or current_app_type != previous_app_type):
            end_time = datetime.now()
            log_activity(previous_app_type, previous_app_name,
                         start_time, end_time)
            previous_app_type, previous_app_name = current_app_type, current_app_name
            start_time = datetime.now()

except KeyboardInterrupt:
    print("Stopped by user. Logging final entry.")
    end_time = datetime.now()
    log_activity(previous_app_type, previous_app_name, start_time, end_time)
