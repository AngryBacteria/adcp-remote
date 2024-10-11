import telnetlib


class ADCPHelper:
    def __init__(self, host: str, port=53595, timeout: int | float = 5):
        self.host: str = host
        self.port: int = port
        self.timeout = timeout
        self.tn: telnetlib.Telnet | None = None
        print(f"ADCP-Client initialized for {host}:{port}")

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
