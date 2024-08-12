import os
import speedtest
import sys
import itertools
import time
import threading
import json
from datetime import datetime

s = sys.stdout

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def clear_line():
    sys.stdout.write('\r\033[K')
    sys.stdout.flush()

# Saves Cached Servers to a JSON
def save_cached_server(server_info):
    with open('cached_server.json', 'w')as f:
        json.dump(server_info, f)

# Tries to Load Cached server
def load_cached_server():
    try:
        with open('cached_server.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def save_test(dspeed, uspeed):
    current_time = datetime.now()
    with open('speed_test_records.txt', 'a') as f:
        f.write(f"{current_time} - Download Speed {dspeed:.2f} mbps - Upload Speed: {uspeed:.2f} mbps\n")

# Made my own best server function to cache servers
def get_best_server():
    st = speedtest.Speedtest()
    cached_server = load_cached_server()

    # Checks if cached server is empty or not
    if cached_server:
        print(f"Using cached server: {cached_server['host']} located in {cached_server['country']}")
        return cached_server
    else:
        print("Please note: The initial run may take longer than usual.")
        best_server = st.get_best_server()
        save_cached_server(best_server)
        print(f"Cached new server: {best_server['host']} located in {best_server['country']}")
        return best_server

def speedtestp():
    clear_screen()
    st = speedtest.Speedtest()

    # Get best server
    best_server = get_best_server()
    clear_line()

    # Test Download Speed
    s.write("Testing Download Speed...")
    s.flush()
    dspeed = st.download() / 1_000_000 # Convert to mbps
    clear_line()

    # Test Upload Speed
    s.write("Testing Upload Speed...")
    s.flush()
    uspeed = st.upload() / 1_000_000 # Convert to mbps
    clear_line()

    # print(f"Server Used: {best_server['host']} located in {best_server['country']}") - This is Redundant
    save_test(dspeed, uspeed)
    print(f"Download Speed: {dspeed:.2f} mbps")
    print(f"Upload Speed: {uspeed:.2f} mbps")

def main_menu():
    # Clears Screen
    clear_screen()
    option = input("""Welcome to the Network Auditer!\n
1. Test Network Speed
2. Scan for Connected Devices
3. Scan Ports
4. Vulnerability Assessment
5. Log Analysis\n
> """)
    
    if option == '1':
        speedtestp()
    elif option == '2':
        connected_devices()
    elif option == '3':
        portscan()
    elif option == '4':
        vuln_assessment()
    elif option == '5':
        log_analysis()
    else:
        input("Invalid Input, Press Enter to Continuee...")
        main_menu()
    
main_menu()