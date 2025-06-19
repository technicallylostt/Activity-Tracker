# Activity-Tracker

A Python-based system activity tracker that logs active applications or browser tabs with start and end times into a CSV file — all without using any external APIs.

## 🔧 Features

- Detects whether system is Laptop or Desktop
- Logs:
  - App type (Browser/Application)
  - App name
  - Start and End times
  - IP, Hostname, ISP
  - Network type (WiFi/Cellular)
  - Source URL (if browser)
- Saves logs daily into CSV files

## 📦 Dependencies

This project uses the following Python modules:

### 🐍 Standard Library Modules (No Installation Required)
- `csv` – for writing logs to CSV files
- `os` – for creating folders and handling file paths
- `datetime` – to get current date and time
- `platform` – to detect OS type
- `socket` – to get host and IP address
- `subprocess` – to execute macOS system commands
- `time` – for loop delay and time measurement

### 📦 Third-Party Modules (Install via pip)

| Module                    | Purpose                                | Install Command                             |
|---------------------------|----------------------------------------|---------------------------------------------|
| `psutil`                  | Check battery status and process info  | `pip install psutil`                        |
| `speedtest-cli`           | Get ISP name using speedtest           | `pip install speedtest-cli`                 |
| `pyobjc-framework-AppKit` | Get active app on macOS                | `pip install pyobjc-framework-AppKit`       |

> You can install all dependencies at once using:

```bash
pip install -r requirements.txt
