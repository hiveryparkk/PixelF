#!/usr/bin/env python3
"""
Advanced Penetration Testing Framework
Main CLI entry point for the pen testing tool suite.
"""

import argparse
import sys
import logging
from modules.recon.port_scanner import PortScanner
from modules.recon.service_detector import ServiceDetector
from modules.vuln.vuln_scanner import VulnScanner
from modules.exploit.exploit_framework import ExploitFramework
from modules.c2.server import C2Server
from modules.c2.client import C2Client
from modules.post.persistence import Persistence
from modules.post.lateral_movement import LateralMovement
from modules.payloads.generator import PayloadGenerator
from utils.reporting import Reporter
from utils.logging_config import setup_logging

def main():
    parser = argparse.ArgumentParser(description='Advanced Penetration Testing Framework')
    subparsers = parser.add_subparsers(dest='module', help='Available modules')

    # Recon module
    recon_parser = subparsers.add_parser('recon', help='Reconnaissance tools')
    recon_sub = recon_parser.add_subparsers(dest='recon_tool')

    port_scan = recon_sub.add_parser('port_scan', help='Port scanning')
    port_scan.add_argument('target', help='Target IP or domain')
    port_scan.add_argument('-p', '--ports', nargs='+', type=int, default=range(1, 1025), help='Ports to scan')

    service_detect = recon_sub.add_parser('service_detect', help='Service detection')
    service_detect.add_argument('target', help='Target IP or domain')
    service_detect.add_argument('-p', '--ports', nargs='+', type=int, help='Specific ports to check')

    # Vuln module
    vuln_parser = subparsers.add_parser('vuln', help='Vulnerability scanning')
    vuln_parser.add_argument('target', help='Target IP or domain')
    vuln_parser.add_argument('-s', '--scan_type', choices=['basic', 'deep'], default='basic', help='Scan depth')

    # Exploit module
    exploit_parser = subparsers.add_parser('exploit', help='Exploitation framework')
    exploit_parser.add_argument('target', help='Target IP or domain')
    exploit_parser.add_argument('exploit_name', help='Name of the exploit to use')
    exploit_parser.add_argument('-o', '--options', nargs='*', help='Exploit options')

    # C2 module
    c2_parser = subparsers.add_parser('c2', help='Command and Control')
    c2_sub = c2_parser.add_subparsers(dest='c2_action')

    server_start = c2_sub.add_parser('server', help='Start C2 server')
    server_start.add_argument('-p', '--port', type=int, default=8080, help='Server port')

    client_connect = c2_sub.add_parser('client', help='Connect C2 client')
    client_connect.add_argument('server_ip', help='C2 server IP')
    client_connect.add_argument('-p', '--port', type=int, default=8080, help='Server port')

    # Post module
    post_parser = subparsers.add_parser('post', help='Post-exploitation tools')
    post_sub = post_parser.add_subparsers(dest='post_tool')

    persist = post_sub.add_parser('persist', help='Establish persistence')
    persist.add_argument('method', choices=['registry', 'scheduled_task', 'service'], help='Persistence method')

    lateral = post_sub.add_parser('lateral', help='Lateral movement')
    lateral.add_argument('target', help='Target for lateral movement')
    lateral.add_argument('technique', choices=['psexec', 'wmi', 'smb'], help='Lateral movement technique')

    # Payload module
    payload_parser = subparsers.add_parser('payload', help='Payload generation')
    payload_parser.add_argument('type', choices=['reverse_shell', 'bind_shell', 'meterpreter'], help='Payload type')
    payload_parser.add_argument('-o', '--output', help='Output file')
    payload_parser.add_argument('-e', '--encode', action='store_true', help='Encode payload')

    # Report module
    report_parser = subparsers.add_parser('report', help='Generate reports')
    report_parser.add_argument('format', choices=['json', 'html', 'pdf'], help='Report format')
    report_parser.add_argument('-o', '--output', help='Output file')

    args = parser.parse_args()

    if not args.module:
        parser.print_help()
        sys.exit(1)

    setup_logging()

    try:
        if args.module == 'recon':
            if args.recon_tool == 'port_scan':
                scanner = PortScanner(args.target, args.ports)
                scanner.scan()
            elif args.recon_tool == 'service_detect':
                detector = ServiceDetector(args.target, args.ports)
                detector.detect()
        elif args.module == 'vuln':
            scanner = VulnScanner(args.target, args.scan_type)
            scanner.scan()
        elif args.module == 'exploit':
            framework = ExploitFramework(args.target, args.exploit_name, args.options)
            framework.exploit()
        elif args.module == 'c2':
            if args.c2_action == 'server':
                server = C2Server(args.port)
                server.start()
            elif args.c2_action == 'client':
                client = C2Client(args.server_ip, args.port)
                client.connect()
        elif args.module == 'post':
            if args.post_tool == 'persist':
                persist_tool = Persistence(args.method)
                persist_tool.establish()
            elif args.post_tool == 'lateral':
                lateral_tool = LateralMovement(args.target, args.technique)
                lateral_tool.move()
        elif args.module == 'payload':
            generator = PayloadGenerator(args.type, args.output, args.encode)
            generator.generate()
        elif args.module == 'report':
            reporter = Reporter(args.format, args.output)
            reporter.generate()
    except Exception as e:
        logging.error(f"Error executing {args.module}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()