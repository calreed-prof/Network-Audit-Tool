# Network Scanner

## Overview

This project is a **Network Device Scanner** designed to challenge and demonstrate security and programming skills. The scanner identifies devices connected to the local network, collecting their IP and MAC addresses and saving the information to a CSV file for easy reference.

## Features

- **Device Scanning**: The scanner identifies devices on the local network, capturing both IP and MAC addresses.
- **CSV Export**: The scanned device information is saved to a CSV file, allowing for easy data analysis and storage.
- **Error Handling**: The program includes error handling to manage potential I/O issues when writing to the file.

## Requirements

- **Python 3.x**
- **scapy** library (for network scanning)
- **csv** module (standard library, no installation required)

## Installation

- Ensure you have Python 3 installed on your system.

   ```bash
   pip install -r requirements.txt
