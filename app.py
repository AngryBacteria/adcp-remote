import streamlit as st
from ADCPHelper import ADCPHelper


def setup_adcp_client() -> ADCPHelper | None:
    try:
        if not st.session_state.get("adcp"):
            adcp_helper = ADCPHelper("192.168.1.93", timeout=1)
            st.session_state["adcp"] = adcp_helper
            adcp_helper.connect()
            st.toast("Successfully connected to the projector.")
            return adcp_helper
        else:
            return st.session_state["adcp"]
    except Exception as error:
        st.toast(f"Failed to connect to the projector. Error: {error}")
        return None


def send_command_wrapper(command):
    projector = setup_adcp_client()
    if projector:
        try:
            result = projector.send_command(command)
            st.toast(f"Command '{command}' sent successfully. Response: {result}")
        except Exception as e:
            st.toast(f"Failed to send command '{command}'. Error: {str(e)}")
    else:
        st.toast(
            "No active projector connection. Please check the connection and try again."
        )


st.title("Sony ADCP Remote")
col1, col2 = st.columns(2)


def select_brightness():
    if "brightness" in st.session_state and st.session_state["brightness"]:
        send_command_wrapper(f'light_output_mode "{st.session_state.brightness}"')


def select_picture_mode():
    if "picture_mode" in st.session_state and st.session_state["picture_mode"]:
        send_command_wrapper(f'picture_mode "{st.session_state.picture_mode}"')


def select_input():
    if "input" in st.session_state and st.session_state["input"]:
        send_command_wrapper(f'input "{st.session_state.input}"')


def execute_custom_command():
    if (
        "custom_command" in st.session_state
        and len(st.session_state["custom_command"]) > 2
    ):
        result = send_command_wrapper(st.session_state["custom_command"])
        st.session_state["command_result"] = result
    else:
        st.toast("Please enter a valid custom command (at least 3 characters long).")


# Buttons for power and blank
with col1:
    st.button(
        "Turn on",
        type="primary",
        icon=":material/power:",
        on_click=send_command_wrapper,
        args=('power "on"',),
    )
    st.button(
        "Turn on Blank",
        type="primary",
        icon=":material/visibility_off:",
        on_click=send_command_wrapper,
        args=('blank "on"',),
    )

with col2:
    st.button(
        "Turn off",
        type="primary",
        icon=":material/cancel:",
        on_click=send_command_wrapper,
        args=('power "off"',),
    )
    st.button(
        "Turn off Blank",
        type="primary",
        icon=":material/visibility:",
        on_click=send_command_wrapper,
        args=('blank "off"',),
    )

# Multi selects for input, picture_mode and brightness
st.selectbox(
    "Select Input",
    ("hdmi1", "hdmi2"),
    key="input",
    on_change=select_input,
    index=None,
)
st.selectbox(
    "Picture mode",
    ("dynamic", "standard", "presentation"),
    key="picture_mode",
    on_change=select_picture_mode,
    index=None,
)
st.selectbox(
    "Brightness",
    ("high", "mid", "low"),
    key="brightness",
    on_change=select_brightness,
    index=None,
)

col1, col2 = st.columns(2)
# Custom commands
st.subheader("Custom Command")
custom_command = st.text_input("Enter custom command", key="custom_command")
st.button("Execute Custom Command", on_click=execute_custom_command)
if "command_result" in st.session_state:
    st.text(f"Command Result: {st.session_state['command_result']}")
st.link_button(
    "List of custom commands",
    "https://static1.squarespace.com/static/614f1245001113494b94be1e/t/63626bf8b87e1c10f59c3b74/1667394553509/Sony_Protocol-Manual_Supported-Command-List_1st-Edition.pdf",
)
