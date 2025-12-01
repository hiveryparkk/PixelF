import socket
import threading
import logging
import json
import base64
from cryptography.fernet import Fernet

class C2Server:
    def __init__(self, port=8080, host='0.0.0.0'):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = {}
        self.logger = logging.getLogger(__name__)
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt_message(self, message):
        return self.cipher.encrypt(message.encode())

    def decrypt_message(self, encrypted_message):
        return self.cipher.decrypt(encrypted_message).decode()

    def handle_client(self, client_socket, client_address):
        client_id = f"{client_address[0]}:{client_address[1]}"
        self.clients[client_id] = client_socket
        self.logger.info(f"New client connected: {client_id}")

        try:
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break

                try:
                    decrypted_data = self.decrypt_message(data)
                    command = json.loads(decrypted_data)
                    self.logger.info(f"Received command from {client_id}: {command}")

                    # Process command
                    response = self.process_command(command, client_id)

                    # Send response
                    encrypted_response = self.encrypt_message(json.dumps(response))
                    client_socket.send(encrypted_response)

                except Exception as e:
                    self.logger.error(f"Error processing command from {client_id}: {e}")

        except Exception as e:
            self.logger.error(f"Client {client_id} disconnected: {e}")
        finally:
            if client_id in self.clients:
                del self.clients[client_id]
            client_socket.close()

    def process_command(self, command, client_id):
        cmd_type = command.get('type', 'unknown')

        if cmd_type == 'heartbeat':
            return {'status': 'ok', 'message': 'Heartbeat received'}
        elif cmd_type == 'execute':
            # Simulate command execution
            result = f"Executed: {command.get('command', 'unknown')}"
            return {'status': 'success', 'result': result}
        elif cmd_type == 'upload':
            # Simulate file upload
            filename = command.get('filename', 'unknown')
            return {'status': 'success', 'message': f'File {filename} uploaded'}
        elif cmd_type == 'download':
            # Simulate file download
            filename = command.get('filename', 'unknown')
            return {'status': 'success', 'data': base64.b64encode(b'fake file data').decode()}
        else:
            return {'status': 'error', 'message': f'Unknown command type: {cmd_type}'}

    def broadcast_command(self, command):
        """Send command to all connected clients"""
        encrypted_command = self.encrypt_message(json.dumps(command))
        disconnected_clients = []

        for client_id, client_socket in self.clients.items():
            try:
                client_socket.send(encrypted_command)
            except:
                disconnected_clients.append(client_id)

        # Clean up disconnected clients
        for client_id in disconnected_clients:
            del self.clients[client_id]

        return len(self.clients)

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        self.logger.info(f"C2 Server started on {self.host}:{self.port}")

        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.daemon = True
                client_thread.start()
        except KeyboardInterrupt:
            self.logger.info("C2 Server shutting down")
        finally:
            if self.server_socket:
                self.server_socket.close()