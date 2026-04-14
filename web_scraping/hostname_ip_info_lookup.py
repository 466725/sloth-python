import socket
import requests
from typing import Dict

IPINFO_URL = "https://ipinfo.io/{ip}/json"
WEATHER_URL = "www.theweathernetwork.com"
REQUEST_TIMEOUT = 5


def get_headers(host: str) -> None:
    url = f"https://{host}"
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    print("\nHTTP Response Headers:")
    for k, v in response.headers.items():
        print(f"{k}: {v}")


def resolve_ip(host: str) -> str:
    ip = socket.gethostbyname(host)
    print(f"\nResolved IP address for {host}: {ip}")
    return ip


def get_ip_location(ip: str) -> Dict[str, str]:
    response = requests.get(
        IPINFO_URL.format(ip=ip),
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def main() -> None:
    host = WEATHER_URL.strip()

    try:
        print("#" * 96)
        print("#" * 96)
        get_headers(host)
        print("#" * 96)
        print("#" * 96)
        ip = resolve_ip(host)
        print("#" * 96)
        print("#" * 96)
        location = get_ip_location(ip)

        print("\nIP Location Info:")
        print(f"City: {location.get('city', 'N/A')}")
        print(f"Region: {location.get('region', 'N/A')}")
        print(f"Country: {location.get('country', 'N/A')}")
        print(f"Coordinates: {location.get('loc', 'N/A')}")

    except socket.gaierror:
        print("Error: Failed to resolve hostname.")
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
