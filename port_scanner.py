import socket
import sys
import argparse
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def scan_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except socket.error as e:
        print(f"Error scanning port {port}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error scanning port {port}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Simple Port Scanner')
    parser.add_argument('host', help='Target host IP or domain')
    parser.add_argument('-p', '--ports', nargs='+', type=int, default=[21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995],
                        help='Ports to scan (default: common ports)')
    args = parser.parse_args()

    try:
        # Validate host
        socket.gethostbyname(args.host)
    except socket.gaierror:
        print(f"Error: Unable to resolve host '{args.host}'")
        sys.exit(1)

    print(f"Scanning {args.host} for open ports...")
    open_ports = []
    for port in args.ports:
        if port < 1 or port > 65535:
            print(f"Warning: Port {port} is out of range (1-65535). Skipping.")
            continue
        if scan_port(args.host, port):
            open_ports.append(port)
            print(f"Port {port} is open")

    if not open_ports:
        print("No open ports found.")
    else:
        print(f"Open ports: {open_ports}")

if __name__ == "__main__":
    main()