from threading import Lock
from typing import Any
import socket


messages = {
    "power_on": 'power "on"\r\n',
    "power_off": 'power "off"\r\n'
}


class ADCPHelper:
    _instance: Any = None
    _lock: Lock = Lock()
    ip: str = None
    port: int = None
    connected: bool = False
    socket: socket = None

    def __new__(cls) -> Any:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def init(self, ip: str, port: int) -> None:
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, message: str):
        try:
            self.socket.connect((self.ip, self.port))
            self.socket.sendall(message.encode())
            response = self.socket.recv(1024)
            response_parsed = response.decode()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.socket.close()


# Usage
singleton1 = ADCPHelper()
singleton2 = ADCPHelper()

singleton1.init("192.168.1.93", 53595)
singleton1.send(messages["power_off"])