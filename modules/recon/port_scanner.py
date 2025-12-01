import socket
import threading
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

class PortScanner:
    def __init__(self, target, ports=None, timeout=1, max_threads=100):
        self.target = target
        self.ports = ports or range(1, 1025)
        self.timeout = timeout
        self.max_threads = max_threads
        self.open_ports = []
        self.logger = logging.getLogger(__name__)

    def scan_port(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((self.target, port))
            sock.close()
            if result == 0:
                self.open_ports.append(port)
                self.logger.info(f"Port {port} is open")
                return port
        except Exception as e:
            self.logger.debug(f"Error scanning port {port}: {e}")
        return None

    def scan(self):
        self.logger.info(f"Starting port scan on {self.target}")
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = [executor.submit(self.scan_port, port) for port in self.ports]
            for future in as_completed(futures):
                future.result()  # Just to handle exceptions if any

        if self.open_ports:
            self.logger.info(f"Open ports found: {sorted(self.open_ports)}")
        else:
            self.logger.info("No open ports found")

        return sorted(self.open_ports)