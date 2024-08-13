import os
import speedtest
import sys
import time
import json
from datetime import datetime
from scapy.all import conf
import subprocess
import ipaddress
import platform
import re
import nmap # dun dun dunnnn

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
        f.write("This has been saved to 'speed_test_records.txt'")

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

def get_ip_address():
    clear_screen()
    # Find the Operating System
    system = platform.system()

    if system == "Windows":
        command = "ipconfig"
        pattern = r"IPv4 Address.*: ([\d\.]+)"  # Adjusted Regex
    else:
        command = "ifconfig"
        pattern = r"inet\s([\d\.]+)\s"  # Adjusted Regex

    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout

    matches = re.findall(pattern, output)
    if matches:
        if len(matches) > 1:
            print("Multiple Addresses Found:")
            for idx, match in enumerate(matches):
                print(f"{idx + 1}: {match}")
            while True:
                choice = input("Please Select the Addr you would like to Use > ")
                try:
                    selected_ip = matches[int(choice) - 1]
                    # print(f"Selected IP Address: {selected_ip}")
                    return selected_ip
                    break
                except(IndexError, ValueError):
                    print("Invalid Selection")
        else:
            selected_ip = match[0]
            # print(f"Automatically Select Ip Addr: {selected_ip}")
            return selected_ip
    else:
        print("No Addresses Found")

def get_network_address(ip_address):
    ip_interface = ipaddress.ip_interface(f"{ip_address}/24")
    return ip_interface.network

def get_default_interface():
    """Finds what Network Interface is Being Used"""
    default_iface = conf.route.route("0.0.0.0")[0]
    return default_iface

def scan_network(network):
    """Scans Given Network"""
    nm = nmap.PortScanner()
    nm.scan(hosts=network, arguments='-sn')

    # Initalize empty table
    devices = []

    for host in nm.all_hosts():
        if 'mac' in nm[host]['addresses']:
            devices.append({
                'ip': nm[host]['addresses']['ipv4'],
                'mac': nm[host]['addresses']['mac']
            })

    return devices

def save_to_csv(devices, filename="network_devices.csv"):
    # CSV Name
    print("Nice")

def connected_devices():
    ip_address = get_ip_address()
    network_address = get_network_address(ip_address)
    clear_screen()
    print(f"Device IP Address: {ip_address}")
    print(f"Network Interface: {network_address}")

    devices = scan_network(network=network_address)
    print(devices)
    option = input("Would you like to save the output to a CSV file? (y/n) > ").lower()

    if option == "y":
        save_to_csv(devices=devices)
    else:
        input("No Problem! Press Enter to Continue...")
        main_menu()

def port_scan(target):
    nm = nmap.PortScanner()
    nm.scan(target, '1-1024')
    
    for host in nm.all_hosts():
        # Prints the item that was scanned, as well as the hostname
        print(f'Host: {host} ({nm[host].hostname()})')
        print(f'State: {nm[host].state()}')

        for proto in nm[host].all_protocols():
            print('----------')
            print(f'Protocol: {proto}')

            lport = nm[host][proto].keys()
            for port in sorted(lport):
                print(f'Port: {port}\tState: {nm[host][proto][port]["state"]}')

def port_scan_menu():
    clear_screen()
    option = input("What would you like to scan?\n1) Host Machine\n2) Network Devices\n\n> ")
    
    if option == '1':
        host = '127.0.0.1'
        port_scan(host)
    elif option == '2':
        ip_address = get_ip_address()
        network_address = get_network_address(ip_address=ip_address)
        port_scan(network_address)

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
        port_scan_menu()
    elif option == '4':
        vuln_assessment()
    elif option == '5':
        log_analysis()
    else:
        input("Invalid Input, Press Enter to Continuee...")
        main_menu()
    
main_menu()