import streamlit as st

from ADCPHelper import ADCPHelper


# TODO implement error handling


def get_adcp_client() -> ADCPHelper:
    if not st.session_state.get("adcp"):
        adcp_helper = ADCPHelper("192.168.1.93", timeout=1)
        st.session_state["adcp"] = adcp_helper
        adcp_helper.connect()
        return adcp_helper
    else:
        return st.session_state["adcp"]


try:
    projector = get_adcp_client()
    st.title("Sony ADCP Remote")
    col1, col2 = st.columns(2)

    def select_brightness():
        if "brightness" in st.session_state and st.session_state["brightness"]:
            projector.send_command(f'light_output_mode "{st.session_state.brightness}"')

    def select_picture_mode():
        if "picture_mode" in st.session_state and st.session_state["picture_mode"]:
            projector.send_command(f'picture_mode "{st.session_state.picture_mode}"')

    def select_input():
        if "input" in st.session_state and st.session_state["input"]:
            projector.send_command(f'input "{st.session_state.input}"')

    def execute_custom_command():
        if (
            "custom_command" in st.session_state
            and len(st.session_state["custom_command"]) > 2
        ):
            result = projector.send_command(st.session_state["custom_command"])
            st.session_state["command_result"] = result

    # Buttons for power and blank
    with col1:
        st.button(
            "Turn on",
            type="primary",
            icon=":material/power:",
            on_click=projector.send_command,
            args=('power "on"',),
        )
        st.button(
            "Turn on Blank",
            type="primary",
            icon=":material/visibility_off:",
            on_click=projector.send_command,
            args=('blank "on"',),
        )

    with col2:
        st.button(
            "Turn off",
            type="primary",
            icon=":material/cancel:",
            on_click=projector.send_command,
            args=('power "off"',),
        )
        st.button(
            "Turn off Blank",
            type="primary",
            icon=":material/visibility:",
            on_click=projector.send_command,
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

except Exception as e:
    st.title(f"Could not connect to projector, try reloading your browser window: {e}")
