import socket
import logging
import re

class ServiceDetector:
    def __init__(self, target, ports=None):
        self.target = target
        self.ports = ports or [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 3389]
        self.services = {}
        self.logger = logging.getLogger(__name__)

    def grab_banner(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((self.target, port))

            if port in [80, 443]:
                # HTTP/HTTPS banner grabbing
                request = f"GET / HTTP/1.1\r\nHost: {self.target}\r\n\r\n"
                sock.send(request.encode())
                banner = sock.recv(1024).decode('utf-8', errors='ignore')
            else:
                banner = sock.recv(1024).decode('utf-8', errors='ignore')

            sock.close()
            return banner.strip()
        except Exception as e:
            self.logger.debug(f"Error grabbing banner for port {port}: {e}")
            return None

    def identify_service(self, port, banner):
        service_map = {
            21: 'FTP',
            22: 'SSH',
            23: 'Telnet',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            143: 'IMAP',
            443: 'HTTPS',
            993: 'IMAPS',
            995: 'POP3S',
            3306: 'MySQL',
            3389: 'RDP'
        }

        service = service_map.get(port, 'Unknown')

        if banner:
            if 'SSH' in banner.upper():
                service = 'SSH'
            elif 'HTTP' in banner.upper():
                service = 'HTTP'
            elif 'FTP' in banner.upper():
                service = 'FTP'
            elif 'SMTP' in banner.upper():
                service = 'SMTP'
            elif 'MySQL' in banner.upper():
                service = 'MySQL'

        return service, banner

    def detect(self):
        self.logger.info(f"Starting service detection on {self.target}")
        for port in self.ports:
            banner = self.grab_banner(port)
            if banner:
                service, banner = self.identify_service(port, banner)
                self.services[port] = {'service': service, 'banner': banner}
                self.logger.info(f"Port {port}: {service} - {banner[:50]}...")
            else:
                self.services[port] = {'service': 'Unknown', 'banner': None}

        return self.services