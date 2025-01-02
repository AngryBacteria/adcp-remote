import os
import telnetlib


class ADCPHelper:
    def __init__(self):
        self.host: str = os.environ.get("ADCP_HOST", "192.168.1.93")
        self.port: int = int(os.environ.get("ADCP_PORT", "53595"))
        self.timeout = float(os.environ.get("ADCP_TIMEOUT", "5.0"))
        self.tn: telnetlib.Telnet | None = None
        print(f"ADCP-Client initialized for {self.host}:{self.port}")

    def connect(self):
        self.tn = telnetlib.Telnet(self.host, self.port, self.timeout)
        response = (
            self.tn.read_until(b"NOKEY\r\n", self.timeout).decode("ascii").strip()
        )
        if response == "NOKEY":
            print(f"Successfully connected to projector [{self.host}:{self.port}]")
        else:
            raise Exception(
                f"Connection to projector [{self.host}:{self.port}] failed. Response: {response}"
            )

    def disconnect(self):
        if not self.tn:
            print(
                f"No active connection to projector [{self.host}:{self.port}], cannot disconnect."
            )
            return
        self.tn.close()
        print(f"Disconnected from projector [{self.host}:{self.port}]")
        self.tn = None

    def send_command(self, command: str):
        print(f"Sending command to projector [{self.host}:{self.port}]: {command}")
        if not self.tn:
            raise Exception(
                "Not connected to projector. Please connect before sending commands."
            )
        self.tn.write(command.encode("ascii") + b"\r\n")
        response = self.tn.read_until(b"\r\n", self.timeout).decode("ascii").strip()
        if "err_" not in response:
            print(f"Command '{command}' executed successfully. Response: {response}")
            return response
        else:
            raise Exception(f"Command '{command}' failed. Error: {response}")
