import os
import speedtest

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def speedtestp():
    clear_screen()
    print("Loading...")

    st = speedtest.Speedtest()

    best_server = st.get_best_server()

    print(f"Found Best Server!\n- Name: {best_server['name']}\n- Country: {best_server['country']}")

    download_speed = st.download()
    print("Testing Download Speed")

    upload_speed = st.upload()
    print("Testing Upload Speed")

    dspeed_mbps = download_speed / 1_000_000
    uspeed_mbps = upload_speed / 1_000_000

    print(f"\nDownload speed: {dspeed_mbps:.2f} mbps")
    print(f"Upload Speed: {uspeed_mbps:.2f} mbps")

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