import socket
import logging
import re
import requests
from urllib.parse import urljoin

class VulnScanner:
    def __init__(self, target, scan_type='basic'):
        self.target = target
        self.scan_type = scan_type
        self.vulnerabilities = []
        self.logger = logging.getLogger(__name__)

    def check_open_ports(self):
        """Check for common vulnerable ports"""
        vulnerable_ports = {
            21: 'FTP - Check for anonymous login',
            23: 'Telnet - Unencrypted protocol',
            80: 'HTTP - Check for common web vulnerabilities',
            443: 'HTTPS - Check for SSL/TLS issues',
            3389: 'RDP - Check for BlueKeep vulnerability',
            5900: 'VNC - Check for weak authentication'
        }

        open_ports = []
        for port in vulnerable_ports.keys():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((self.target, port))
                sock.close()
                if result == 0:
                    open_ports.append(port)
                    self.vulnerabilities.append({
                        'port': port,
                        'service': vulnerable_ports[port],
                        'severity': 'Medium',
                        'description': f'Potentially vulnerable service running on port {port}'
                    })
            except:
                pass

        return open_ports

    def check_web_vulnerabilities(self, ports):
        """Check for common web vulnerabilities"""
        web_ports = [p for p in ports if p in [80, 443, 8080, 8443]]

        for port in web_ports:
            protocol = 'https' if port in [443, 8443] else 'http'
            base_url = f"{protocol}://{self.target}:{port}"

            try:
                response = requests.get(base_url, timeout=5, verify=False)
                server = response.headers.get('Server', '')

                # Check for outdated server software
                if 'Apache/2.2' in server or 'Apache/2.4.1' in server:
                    self.vulnerabilities.append({
                        'port': port,
                        'service': f'Web Server ({server})',
                        'severity': 'High',
                        'description': f'Outdated web server version: {server}'
                    })

                # Check for common paths
                common_paths = ['/admin', '/login', '/phpmyadmin', '/wp-admin']
                for path in common_paths:
                    try:
                        resp = requests.get(urljoin(base_url, path), timeout=3, verify=False)
                        if resp.status_code == 200:
                            self.vulnerabilities.append({
                                'port': port,
                                'service': 'Web Application',
                                'severity': 'Low',
                                'description': f'Common admin path accessible: {path}'
                            })
                    except:
                        pass

            except requests.exceptions.RequestException:
                pass

    def check_ssl_vulnerabilities(self):
        """Check for SSL/TLS vulnerabilities"""
        try:
            import ssl
            context = ssl.create_default_context()
            with socket.create_connection((self.target, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=self.target) as ssock:
                    cert = ssock.getpeercert()
                    # Check certificate validity
                    if ssl.cert_time_to_seconds(cert['notAfter']) < time.time():
                        self.vulnerabilities.append({
                            'port': 443,
                            'service': 'SSL/TLS',
                            'severity': 'High',
                            'description': 'SSL certificate has expired'
                        })
        except:
            pass

    def scan(self):
        self.logger.info(f"Starting vulnerability scan on {self.target}")

        open_ports = self.check_open_ports()

        if self.scan_type == 'deep':
            self.check_web_vulnerabilities(open_ports)
            self.check_ssl_vulnerabilities()

        if self.vulnerabilities:
            self.logger.info(f"Found {len(self.vulnerabilities)} potential vulnerabilities")
            for vuln in self.vulnerabilities:
                self.logger.info(f"[{vuln['severity']}] {vuln['description']}")
        else:
            self.logger.info("No obvious vulnerabilities found")

        return self.vulnerabilities