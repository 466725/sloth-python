import sys
import nmap  # Requires Nmap to be installed on the system


def get_target() -> str:
    """
    Get the target host from command-line arguments or prompt the user.
    """
    if len(sys.argv) > 1:
        return sys.argv[1]
    return input("Please enter the target IP or hostname to scan: ").strip()


def scan_ports(target: str, ports: list[int]) -> None:
    """
    Scan the specified ports on the target host and print results.
    """
    scanner = nmap.PortScanner()
    ports_str = ",".join(map(str, ports))

    print(f"\nScanning {target} for ports {ports_str}...\n")

    try:
        scan_result = scanner.scan(
            hosts=target,
            ports=ports_str,
            arguments="-Pn"
        )

        if target not in scan_result.get("scan", {}):
            print(f"Host {target} is down or unreachable.")
            return

        host_data = scan_result["scan"][target]

        for port in ports:
            port_info = host_data.get("tcp", {}).get(port)
            if port_info:
                print(f"Port {port} is {port_info['state']}")
            else:
                print(f"Port {port} was not scanned or not available")

        print(f"\nHost {target} is {host_data['status']['state']}")

    except nmap.PortScannerError as err:
        print(f"Nmap execution error: {err}")
    except Exception as err:
        print(f"Unexpected error during scan: {err}")


if __name__ == "__main__":
    TARGET_PORTS = [21, 22, 80, 129, 443, 8080]
    target_host = get_target()
    scan_ports(target_host, TARGET_PORTS)
