import telnetlib


class ADCPHelper:
    def __init__(self, host: str, port=53595, timeout: int | float = 5):
        self.host: str = host
        self.port: int = port
        self.timeout = timeout
        self.tn: telnetlib.Telnet | None = None
        print("ADCP-Client initialized")

    def connect(self):
        self.tn = telnetlib.Telnet(self.host, self.port, self.timeout)
        response = (
            self.tn.read_until(b"NOKEY\r\n", self.timeout).decode("ascii").strip()
        )
        if response == "NOKEY":
            print(f"Connected to projector [{self.host}:{self.port}]")
        else:
            raise Exception(
                f"Connection to projector [{self.host}:{self.port}] could not be established: {response}"
            )

    def disconnect(self):
        if not self.tn:
            raise Exception(
                f"Cannot disconnect from projector [${self.host}:{self.port}] if not connected"
            )
        if self.tn:
            self.tn.close()
            print(f"Disconnected from projector [${self.host}:{self.port}]")
            self.tn = None

    def send_command(self, command: str):
        print(f"Sending command to projector [{self.host}:{self.port}]: {command}")
        if not self.tn:
            raise Exception("Not connected to projector, cannot send command")
        self.tn.write(command.encode("ascii") + b"\r\n")
        response = self.tn.read_until(b"\r\n", self.timeout).decode("ascii").strip()
        if "err_" not in response:
            return response
        else:
            raise Exception(
                "ADCP Message could not be transmitted, received error: ", response
            )


if __name__ == "__main__":
    adcp_helper = ADCPHelper("192.168.1.93", timeout=5)
    adcp_helper.connect()
    print(adcp_helper.send_command('input "hdmi2"'))
    adcp_helper.disconnect()
