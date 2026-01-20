# Sloth Python 🦥

[![Python Version](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Sloth Python is a comprehensive automation and algorithm playground. Designed for the "efficiently lazy," this
repository contains a variety of tools ranging from network security scanners to machine learning implementations and
automated testing suites.

## 🚀 Key Features

- **Network Security:** Built-in Nmap integration for port scanning and host discovery.
- **Algorithms:** Extensive library of algorithms covering machine learning (K-Means), data structures, and more.
- **Automation:** Support for Robot Framework and various automation protocols:
    - **Web:** HTTP/HTTPS testing
    - **Services:** SOAP & REST API automation
    - **Databases:** JDBC connectivity
- **Performance Testing:** Utilities for load testing many server/protocol types.

## 🛠️ Requirements

- **Python 3.14+**
- **Nmap** (Required for the `nmapscanner.py` utility)
- **PyCharm** (Recommended IDE)

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/sloth-python.git
   cd sloth-python
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   python -m pip install -r requirements.txt
   ```

## 🖥️ Usage

### Running the Nmap Scanner

Navigate to the tutorial directory and provide a target IP:

```bash
python tutorial/nmapscanner.py 127.0.0.1
```

### Running Robot Framework Tests

You can execute automated tests using the `python -m robot` command. For example, to run the calculator demo:

```bash
python -m robot interview\RobotDemos\calculator-demo-test\keyword_driven.robot
```

Or run all tests in a directory:

```bash
python -m robot interview\RobotDemos\
```

> **💡 Tip:** If you want to use the `robot` command directly, ensure your Python `Scripts` directory is in your system's
`PATH`. On your system, this is likely:
> `C:\Users\weipe\AppData\Local\Python\pythoncore-3.14-64\Scripts`
