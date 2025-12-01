# Advanced Penetration Testing Framework

A comprehensive, modular penetration testing framework written in Python, designed to rival commercial tools like Cobalt Strike in functionality and sophistication.

## Features

### Reconnaissance
- **Advanced Port Scanner**: Multi-threaded port scanning with service detection
- **Service Banner Grabbing**: Identify running services and versions
- **Network Mapping**: Comprehensive target enumeration

### Vulnerability Assessment
- **Automated Vulnerability Scanning**: Detect common vulnerabilities
- **Web Application Testing**: SQL injection, XSS, and other web vulnerabilities
- **Service-Specific Checks**: Targeted vulnerability detection for known services

### Exploitation Framework
- **Modular Exploit System**: Pluggable exploit modules
- **Common Exploits**: FTP anonymous, Telnet default creds, SMTP relay, web vulnerabilities
- **Custom Exploit Development**: Framework for adding new exploits

### Command & Control (C2)
- **Encrypted C2 Server**: Secure communication with implants
- **Beacon Management**: Handle multiple compromised systems
- **Real-time Command Execution**: Interactive shell access
- **File Transfer**: Upload/download capabilities

### Payload Generation
- **Multiple Payload Types**: Reverse shells, bind shells, Meterpreter-like payloads
- **Obfuscation**: Base64 encoding and junk code insertion
- **Cross-Platform**: Windows and Unix/Linux support

### Post-Exploitation
- **Persistence Mechanisms**: Registry, scheduled tasks, services, cron jobs
- **Lateral Movement**: PsExec, WMI, SMB, SSH, RDP techniques
- **Privilege Escalation**: Automated privilege escalation attempts

### Reporting & Logging
- **Comprehensive Reports**: JSON, HTML, and PDF formats
- **Detailed Logging**: Timestamped activity logs
- **Evidence Collection**: Screenshots, file dumps, and session data

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation

1. **Clone or download the framework**:
   ```bash
   cd pen_test_tool
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python main.py --help
   ```

### Directory Structure
```
pen_test_tool/
├── main.py                 # Main CLI entry point
├── requirements.txt        # Python dependencies
├── modules/                # Core modules
│   ├── recon/             # Reconnaissance tools
│   ├── vuln/              # Vulnerability scanning
│   ├── exploit/           # Exploitation framework
│   ├── c2/                # Command & Control
│   ├── payloads/          # Payload generation
│   └── post/              # Post-exploitation
├── utils/                 # Utilities
│   ├── logging_config.py  # Logging configuration
│   └── reporting.py       # Report generation
├── logs/                  # Generated log files (auto-created)
└── reports/               # Generated reports (auto-created)
```

## Usage Guide

### Command Structure
```bash
python main.py <module> <subcommand> [options]
```

### Getting Help
```bash
# General help
python main.py --help

# Module-specific help
python main.py recon --help
python main.py recon port_scan --help
```

---

## Reconnaissance Module

### Port Scanning
Scan for open ports on a target:

```bash
# Scan default ports (1-1024)
python main.py recon port_scan example.com

# Scan specific ports
python main.py recon port_scan example.com -p 80 443 3389 8080

# Scan port range
python main.py recon port_scan example.com -p 1 2 3 4 5 6 7 8 9 10
```

### Service Detection
Identify running services and grab banners:

```bash
# Detect services on common ports
python main.py recon service_detect example.com

# Detect services on specific ports
python main.py recon service_detect example.com -p 21 22 80 443 3306
```

---

## Vulnerability Scanning

### Basic Vulnerability Scan
Perform automated vulnerability checks:

```bash
# Basic scan (open ports and common vulnerabilities)
python main.py vuln example.com

# Deep scan (includes web application testing)
python main.py vuln example.com -s deep
```

**Note**: Deep scans may take longer and generate more network traffic.

---

## Exploitation Framework

### Available Exploits
- `ftp_anonymous`: Test for anonymous FTP login
- `telnet_default`: Try default Telnet credentials
- `smtp_relay`: Test for SMTP open relay
- `sql_injection`: Test for SQL injection vulnerabilities
- `xss`: Test for Cross-Site Scripting vulnerabilities

### Running Exploits

```bash
# FTP anonymous login test
python main.py exploit example.com ftp_anonymous

# SQL injection test (requires URL)
python main.py exploit example.com sql_injection -o url=http://example.com/search.php?q=test

# XSS test (requires URL)
python main.py exploit example.com xss -o url=http://example.com/comment.php
```

---

## Command & Control (C2)

### Starting C2 Server
```bash
# Start server on default port (8080)
python main.py c2 server

# Start server on custom port
python main.py c2 server -p 9999
```

### Connecting C2 Client
```bash
# Connect to C2 server
python main.py c2 client 192.168.1.100

# Connect to custom port
python main.py c2 client 192.168.1.100 -p 9999
```

**Security Note**: C2 communications are encrypted using AES. In production, use proper key exchange.

---

## Payload Generation

### Available Payload Types
- `reverse_shell`: Connect back to attacker
- `bind_shell`: Listen for attacker connection
- `meterpreter`: Advanced Meterpreter-like shell

### Generating Payloads

```bash
# Generate reverse shell payload
python main.py payload reverse_shell -o reverse_shell.py

# Generate obfuscated payload (AV evasion)
python main.py payload meterpreter -o meterpreter.py -e

# Generate bind shell
python main.py payload bind_shell -o bind_shell.py
```

**Customization**: Edit the generated Python files to modify host, port, and other parameters.

---

## Post-Exploitation

### Persistence
Establish persistence on compromised systems:

```bash
# Windows registry persistence
python main.py post persist registry

# Windows scheduled task persistence
python main.py post persist scheduled_task

# Windows service persistence
python main.py post persist service

# Linux/Unix cron job persistence
python main.py post persist cron

# Linux systemd service persistence
python main.py post persist systemd
```

### Lateral Movement
Move between systems in the network:

```bash
# PsExec lateral movement
python main.py post lateral 192.168.1.101 -t psexec

# WMI lateral movement
python main.py post lateral 192.168.1.101 -t wmi

# SMB lateral movement
python main.py post lateral 192.168.1.101 -t smb

# SSH lateral movement
python main.py post lateral 192.168.1.101 -t ssh

# RDP lateral movement
python main.py post lateral 192.168.1.101 -t rdp
```

---

## Reporting

### Generate Reports

```bash
# Generate HTML report
python main.py report html -o assessment_report.html

# Generate JSON report
python main.py report json -o assessment_report.json

# Generate PDF report (text-based)
python main.py report pdf -o assessment_report.pdf
```

Reports are saved in the `reports/` directory.

---

## Configuration & Logging

### Logging
- Logs are automatically created in `logs/` directory
- Log levels: DEBUG, INFO, WARNING, ERROR
- File format: `pen_test_YYYYMMDD_HHMMSS.log`

### Environment Variables
```bash
# Set log level (optional)
export LOG_LEVEL=DEBUG

# Custom log directory (optional)
export LOG_DIR=/path/to/custom/logs
```

---

## Advanced Usage

### Chaining Operations
Combine multiple tools in sequence:

```bash
# Recon -> Vulnerability Scan -> Report
python main.py recon port_scan example.com
python main.py vuln example.com -s deep
python main.py report html -o full_assessment.html
```

### Custom Scripts
Extend functionality by creating custom modules in the `modules/` directory.

### Integration
The framework can be integrated with other tools via:
- API endpoints (future feature)
- Custom scripts
- External tool output parsing

---

## Important Security & Legal Notes

### **LEGAL WARNING**
- **This framework is for EDUCATIONAL and AUTHORIZED TESTING purposes ONLY.**
- **Never use on systems you do not own or have explicit permission to test.**
- **Comply with all applicable laws and regulations.**
- **Unauthorized use may result in criminal charges.**

### **Ethical Use Guidelines**
1. **Obtain Written Permission**: Always get written authorization before testing
2. **Scope Definition**: Clearly define testing scope and boundaries
3. **Responsible Disclosure**: Report vulnerabilities through proper channels
4. **Data Protection**: Handle sensitive data appropriately
5. **Cleanup**: Remove all tools and restore systems after testing

### **Security Best Practices**
- Use encrypted connections (HTTPS, SSH, etc.)
- Implement proper access controls
- Keep systems updated and patched
- Monitor for unauthorized access
- Use strong, unique passwords

---

## Troubleshooting

### Common Issues

**Module Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Permission Errors**
```bash
# Run with appropriate permissions
sudo python main.py ...  # Linux/Mac
# Run as Administrator  # Windows
```

**Network Connectivity**
- Ensure target is reachable
- Check firewall settings
- Verify DNS resolution

**C2 Connection Issues**
- Verify server is running
- Check port availability
- Confirm encryption keys match

### Debug Mode
Enable debug logging for troubleshooting:
```bash
export LOG_LEVEL=DEBUG
python main.py <command>
```

---

## Additional Resources

- [Penetration Testing Methodology](https://owasp.org/www-project-web-security-testing-guide/)
- [Ethical Hacking Guidelines](https://www.eccouncil.org/ethical-hacking/)
- [Python Security Best Practices](https://owasp.org/www-pdf-archive/Python_Security_Best_Practices.pdf)

---

## Contributing

The framework is designed to be extensible:

1. **Add New Modules**: Create directories under `modules/`
2. **Implement Classes**: Follow existing patterns
3. **Update CLI**: Add integration in `main.py`
4. **Test Thoroughly**: Ensure compatibility and security

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest

# Code formatting
black .
```
