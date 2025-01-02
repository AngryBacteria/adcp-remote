# Sony ADCP Remote Control

A web application built with Streamlit to control Sony VPL-PHZ10 projectors through the ADCP interface. While specifically designed and tested for the VPL-PHZ10 model, it may work with other Sony projectors that support ADCP. This app will only work for a single projector in your local network!

## Features

- Power control (on/off)
- Input source selection (HDMI1, HDMI2)
- Picture mode adjustment (Dynamic, Standard, Presentation)
- Brightness control (High, Mid, Low)
- Screen blank control
- Custom command support with direct ADCP protocol access

## Prerequisites

- Python 3.12 or higher
- Network connectivity to the projector
- Projector's IP address
- ADCP port (default: 53595)

## Installation

### Standard Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sony-adcp-remote.git
   cd sony-adcp-remote
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   export ADCP_HOST="192.168.1.93"  # Replace with your projector's IP
   export ADCP_PORT="53595"         # Default ADCP port
   export ADCP_TIMEOUT="5.0"        # Connection timeout in seconds
   ```

5. Run the application:
   ```bash
   streamlit run app.py
   ```

### Docker Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sony-adcp-remote.git
   cd sony-adcp-remote
   ```

2. Build the Docker image:
   ```bash
   docker build -t sony-adcp-remote .
   ```

3. Run the container:
   ```bash
   docker run -p 8501:8501 \
     -e ADCP_HOST="192.168.1.93" \
     -e ADCP_PORT="53595" \
     -e ADCP_TIMEOUT="5.0" \
     sony-adcp-remote
   ```

## Usage

1. Access the web interface at `http://localhost:8501`
2. Use the buttons and dropdowns to control the projector:
   - Power controls
   - Input selection
   - Picture mode adjustment
   - Brightness control
   - Screen blank control
3. For advanced users, custom ADCP commands can be sent through the Custom Command section

## Troubleshooting

1. Connection Issues:
   - Verify the projector's IP address is correct
   - Ensure the projector is connected to the network
   - Check if the ADCP port (default: 53595) is accessible

2. Command Failures:
   - Verify the command syntax matches the Sony ADCP protocol
   - Check if the projector supports the specific command
   - Ensure the projector is powered on and responsive

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Built using Streamlit framework
- Implements Sony's ADCP protocol for projector control
- Inspired by the need for a simple, web-based projector control interface