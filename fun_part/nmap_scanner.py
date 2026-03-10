import sys

import nmap  # Requires NMap to be installed locally

# Check if the target argument was provided via command line
if len(sys.argv) > 1:
    target = str(sys.argv[1])
else:
    # If not provided, ask the user for input so the program doesn't crash
    target = input("Please enter the target IP or hostname to scan: ")

ports = [21, 22, 80, 129, 443, 8080]
scan_v = nmap.PortScanner()

print(f"\nScanning {target} for ports {', '.join(map(str, ports))}...\n")

try:
    for port in ports:
        portscan = scan_v.scan(target, str(port))
        # Ensure the host was actually found in the scan results to avoid KeyErrors
        if target in portscan["scan"]:
            state = portscan["scan"][target]["tcp"][port]["state"]
            print(f"Port {port} is {state}")
        else:
            print(f"Port {port} could not be scanned (Host down or unreachable)")

    if target in portscan["scan"]:
        print(f"\nHost {target} is {portscan['scan'][target]['status']['state']}")
except Exception as e:
    print(f"An error occurred during the scan: {e}")
