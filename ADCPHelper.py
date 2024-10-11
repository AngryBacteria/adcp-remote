import telnetlib


class ADCPHelper:
    def __init__(self, host: str, port=53595, timeout=5):
        self.host: str = host
        self.port: int = port
        self.timeout: int = timeout
        self.tn: telnetlib.Telnet | None = None

    def connect(self):
        self.tn = telnetlib.Telnet(self.host, self.port, self.timeout)
        response = self.tn.read_until(b"NOKEY\r\n", self.timeout).decode("ascii").strip()
        if response == "NOKEY":
            print(f"Connected to projector [{self.host}:{self.port}]")
        else:
            raise Exception(f"Connection to projector [{self.host}:{self.port}] could not be established: {response}")

    def disconnect(self):
        if not self.tn:
            raise Exception(f"Not connected to projector [${self.host}:{self.port}]")
        if self.tn:
            self.tn.close()
            print(f"Disconnected from projector [${self.host}:{self.port}]")
            self.tn = None

    def send_command(self, command: str):
        if not self.tn:
            raise Exception("Not connected to projector")
        self.tn.write(command.encode("ascii") + b"\r\n")
        response = self.tn.read_until(b"\r\n", self.timeout).decode("ascii").strip()
        if response.lower() == "ok":
            return response
        else:
            raise Exception("ADCP Message could not be transmitted, received error: ", response)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()


# Example usage:
if __name__ == "__main__":
    projector_ip = "192.168.1.93"
    try:
        with ADCPHelper(projector_ip) as projector:
            print(projector.send_command('input "hdmi1"'))
    except Exception as e:
        print(f"An error occurred: {str(e)}")
