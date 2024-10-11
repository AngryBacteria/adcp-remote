import streamlit as st

from ADCPHelper import ADCPHelper


def get_adcp_client() -> ADCPHelper:
    if not st.session_state.get("adcp"):
        adcp_helper = ADCPHelper("192.168.1.93", timeout=1)
        st.session_state["adcp"] = adcp_helper
        return adcp_helper
    else:
        return st.session_state["adcp"]


try:
    with get_adcp_client() as projector:
        st.title("Sony ADCP Remote")
        st.button(
            "Turn on",
            type="primary",
            icon=":material/power:",
            on_click=projector.send_command,
            args=('power "on"',),
        )
        st.button(
            "Turn off",
            type="primary",
            icon=":material/cancel:",
            on_click=projector.send_command,
            args=('power "off"',),
        )

        st.button(
            "Input HDMI 1",
            type="primary",
            icon=":material/input:",
            on_click=projector.send_command,
            args=('input "hdmi1"',),
        )
        st.button(
            "Input HDMI 2",
            type="primary",
            icon=":material/input:",
            on_click=projector.send_command,
            args=('input "hdmi2"',),
        )

        st.button(
            "Turn on Blank",
            type="primary",
            icon=":material/visibility_off:",
            on_click=projector.send_command,
            args=('blank "on"',),
        )
        st.button(
            "Turn off Blank",
            type="primary",
            icon=":material/visibility:",
            on_click=projector.send_command,
            args=('input "off"',),
        )

except Exception as e:
    st.title(f"Could not connect to projector, try reloading your browser window: {e}")
