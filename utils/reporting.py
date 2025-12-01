import json
import csv
import os
from datetime import datetime
import logging

class Reporter:
    def __init__(self, format_type, output_file=None):
        self.format_type = format_type.lower()
        self.output_file = output_file
        self.logger = logging.getLogger(__name__)
        self.data = {
            'timestamp': datetime.now().isoformat(),
            'scan_results': [],
            'vulnerabilities': [],
            'exploits_attempted': [],
            'post_exploitation': []
        }

    def add_scan_result(self, target, ports, services):
        """Add port scan results"""
        self.data['scan_results'].append({
            'target': target,
            'open_ports': ports,
            'services': services
        })

    def add_vulnerability(self, vuln_data):
        """Add vulnerability finding"""
        self.data['vulnerabilities'].append(vuln_data)

    def add_exploit_attempt(self, exploit_name, target, success, result=None):
        """Add exploit attempt result"""
        self.data['exploits_attempted'].append({
            'exploit': exploit_name,
            'target': target,
            'success': success,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })

    def add_post_exploitation(self, action, target, success, details=None):
        """Add post-exploitation action"""
        self.data['post_exploitation'].append({
            'action': action,
            'target': target,
            'success': success,
            'details': details,
            'timestamp': datetime.now().isoformat()
        })

    def generate(self):
        """Generate the report in specified format"""
        if not self.output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            self.output_file = f'report_{timestamp}.{self.format_type}'

        # Create reports directory if it doesn't exist
        os.makedirs('reports', exist_ok=True)
        filepath = os.path.join('reports', self.output_file)

        try:
            if self.format_type == 'json':
                self._generate_json(filepath)
            elif self.format_type == 'html':
                self._generate_html(filepath)
            elif self.format_type == 'pdf':
                self._generate_pdf(filepath)
            else:
                self.logger.error(f"Unsupported report format: {self.format_type}")
                return False

            self.logger.info(f"Report generated: {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to generate report: {e}")
            return False

    def _generate_json(self, filepath):
        """Generate JSON report"""
        with open(filepath, 'w') as f:
            json.dump(self.data, f, indent=2)

    def _generate_html(self, filepath):
        """Generate HTML report"""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Penetration Testing Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1, h2 {{ color: #333; }}
        table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .success {{ color: green; }}
        .failure {{ color: red; }}
        .warning {{ color: orange; }}
    </style>
</head>
<body>
    <h1>Penetration Testing Report</h1>
    <p><strong>Generated:</strong> {self.data['timestamp']}</p>

    <h2>Scan Results</h2>
    {self._html_scan_results()}

    <h2>Vulnerabilities Found</h2>
    {self._html_vulnerabilities()}

    <h2>Exploits Attempted</h2>
    {self._html_exploits()}

    <h2>Post-Exploitation Actions</h2>
    {self._html_post_exploitation()}
</body>
</html>
"""
        with open(filepath, 'w') as f:
            f.write(html_content)

    def _html_scan_results(self):
        if not self.data['scan_results']:
            return "<p>No scan results available.</p>"

        html = "<table><tr><th>Target</th><th>Open Ports</th><th>Services</th></tr>"
        for result in self.data['scan_results']:
            services = ", ".join([f"{k}:{v['service']}" for k, v in result['services'].items()])
            html += f"<tr><td>{result['target']}</td><td>{', '.join(map(str, result['open_ports']))}</td><td>{services}</td></tr>"
        html += "</table>"
        return html

    def _html_vulnerabilities(self):
        if not self.data['vulnerabilities']:
            return "<p>No vulnerabilities found.</p>"

        html = "<table><tr><th>Port</th><th>Service</th><th>Severity</th><th>Description</th></tr>"
        for vuln in self.data['vulnerabilities']:
            severity_class = vuln['severity'].lower()
            html += f"<tr><td>{vuln['port']}</td><td>{vuln['service']}</td><td class='{severity_class}'>{vuln['severity']}</td><td>{vuln['description']}</td></tr>"
        html += "</table>"
        return html

    def _html_exploits(self):
        if not self.data['exploits_attempted']:
            return "<p>No exploits attempted.</p>"

        html = "<table><tr><th>Exploit</th><th>Target</th><th>Success</th><th>Result</th><th>Timestamp</th></tr>"
        for exploit in self.data['exploits_attempted']:
            success_class = "success" if exploit['success'] else "failure"
            html += f"<tr><td>{exploit['exploit']}</td><td>{exploit['target']}</td><td class='{success_class}'>{exploit['success']}</td><td>{exploit.get('result', 'N/A')}</td><td>{exploit['timestamp']}</td></tr>"
        html += "</table>"
        return html

    def _html_post_exploitation(self):
        if not self.data['post_exploitation']:
            return "<p>No post-exploitation actions performed.</p>"

        html = "<table><tr><th>Action</th><th>Target</th><th>Success</th><th>Details</th><th>Timestamp</th></tr>"
        for action in self.data['post_exploitation']:
            success_class = "success" if action['success'] else "failure"
            html += f"<tr><td>{action['action']}</td><td>{action['target']}</td><td class='{success_class}'>{action['success']}</td><td>{action.get('details', 'N/A')}</td><td>{action['timestamp']}</td></tr>"
        html += "</table>"
        return html

    def _generate_pdf(self, filepath):
        """Generate PDF report (simplified - would require reportlab or similar)"""
        # For now, just create a text file that could be converted to PDF
        text_content = f"""
Penetration Testing Report
Generated: {self.data['timestamp']}

SCAN RESULTS:
{self._text_scan_results()}

VULNERABILITIES:
{self._text_vulnerabilities()}

EXPLOITS ATTEMPTED:
{self._text_exploits()}

POST-EXPLOITATION:
{self._text_post_exploitation()}
"""
        with open(filepath.replace('.pdf', '.txt'), 'w') as f:
            f.write(text_content)

    def _text_scan_results(self):
        if not self.data['scan_results']:
            return "No scan results available."

        text = ""
        for result in self.data['scan_results']:
            text += f"Target: {result['target']}\n"
            text += f"Open Ports: {', '.join(map(str, result['open_ports']))}\n"
            text += "Services:\n"
            for port, service in result['services'].items():
                text += f"  {port}: {service['service']}\n"
            text += "\n"
        return text

    def _text_vulnerabilities(self):
        if not self.data['vulnerabilities']:
            return "No vulnerabilities found."

        text = ""
        for vuln in self.data['vulnerabilities']:
            text += f"Port {vuln['port']} ({vuln['service']}): {vuln['severity']} - {vuln['description']}\n"
        return text

    def _text_exploits(self):
        if not self.data['exploits_attempted']:
            return "No exploits attempted."

        text = ""
        for exploit in self.data['exploits_attempted']:
            status = "SUCCESS" if exploit['success'] else "FAILED"
            text += f"{exploit['exploit']} on {exploit['target']}: {status}\n"
        return text

    def _text_post_exploitation(self):
        if not self.data['post_exploitation']:
            return "No post-exploitation actions performed."

        text = ""
        for action in self.data['post_exploitation']:
            status = "SUCCESS" if action['success'] else "FAILED"
            text += f"{action['action']} on {action['target']}: {status}\n"
        return text