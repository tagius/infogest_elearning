import streamlit as st
import streamlit.components.v1 as components
import time
import base64
from streamlit_autorefresh import st_autorefresh
import os

st.set_page_config(
    layout="wide"
)


# Inject CSS for blinking effect
st.markdown("""
<style>
@keyframes blink {
  0% { opacity: 1; }
  50% { opacity: 0; }
  100% { opacity: 1; }
}
</style>
""", unsafe_allow_html=True)


# ------------------------------
# Utility: Load an MP3 file and encode it as base64.
# ------------------------------
def get_audio_file_as_base64(filepath):
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode("utf-8")
    else:
        return None


# Path to the MP3 file
mp3_path = "utils/assets/sencha.mp3"
mp3_b64 = get_audio_file_as_base64(mp3_path)

# Prepare the alarm audio HTML element using the MP3 file
if mp3_b64:
    alarm_audio_html = f"""
    <audio autoplay loop>
      <source src="data:audio/mp3;base64,{mp3_b64}" type="audio/mp3">
      Your browser does not support the audio element.
    </audio>
    """
else:
    alarm_audio_html = "<p><em>MP3 file not found.</em></p>"

# ------------------------------
# Session state initialization
# ------------------------------
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "remaining" not in st.session_state:
    st.session_state.remaining = 0
if "alarm_active" not in st.session_state:
    st.session_state.alarm_active = False
if "last_update" not in st.session_state:
    st.session_state.last_update = None
if "paused" not in st.session_state:
    st.session_state.paused = False


# ------------------------------
# Callback functions
# ------------------------------
def start_timer():
    h = st.session_state.get("input_hours", 0)
    m = st.session_state.get("input_minutes", 0)
    s = st.session_state.get("input_seconds", 0)
    total = h * 3600 + m * 60 + s
    if total > 0:
        st.session_state.remaining = total
        st.session_state.timer_running = True
        st.session_state.paused = False
        st.session_state.alarm_active = False
        st.session_state.last_update = time.time()


def pause_timer():
    if not st.session_state.remaining == 0:
        st.session_state.timer_running = False
        st.session_state.paused = True
        st.session_state.alarm_active = False


def resume_timer():
    st.session_state.timer_running = True
    st.session_state.paused = False
    st.session_state.last_update = time.time()


def reset_timer():
    st.session_state.timer_running = False
    st.session_state.paused = False
    st.session_state.alarm_active = False
    st.session_state.remaining = 0


# ------------------------------
# Sidebar: Timer UI (no title)
# ------------------------------
with st.sidebar:
    if st.session_state.timer_running:
        # Timer running state: update remaining time as currently done
        now = time.time()
        elapsed = int(now - st.session_state.last_update)
        if elapsed > 0:
            st.session_state.remaining = max(0, st.session_state.remaining - elapsed)
            st.session_state.last_update = now
        if st.session_state.remaining == 0:
            st.session_state.alarm_active = True

        rem = st.session_state.remaining
        hours = rem // 3600
        minutes = (rem % 3600) // 60
        seconds = rem % 60
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        if st.session_state.alarm_active:
            st.markdown(
                f'<div style="font-size: 3em; font-weight: bold; color: red; animation: blink 1s linear infinite;">{time_str}</div>',
                unsafe_allow_html=True
            )
            st.markdown(alarm_audio_html, unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div style="font-size: 3em; font-weight: bold;">{time_str}</div>',
                unsafe_allow_html=True
            )

        # Replace the Stop button with a Pause button
        btn_cols = st.columns(2)
        btn_cols[0].button("Pause", on_click=pause_timer)
        btn_cols[1].button("Reset", on_click=reset_timer)

    elif st.session_state.paused:
        # Paused state: display the paused time with Resume and Reset buttons
        rem = st.session_state.remaining
        hours = rem // 3600
        minutes = (rem % 3600) // 60
        seconds = rem % 60
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        st.markdown(f'<div style="font-size: 3em; font-weight: bold;">{time_str}</div>', unsafe_allow_html=True)
        btn_cols = st.columns(2)
        btn_cols[0].button("Resume", on_click=resume_timer)
        btn_cols[1].button("Reset", on_click=reset_timer)

    else:
        # Idle state: show timer inputs and the Start button
        # init values
        hours = 0
        minutes = 0
        seconds = 0

        # Preset pills row
        option = ["2 min", "120 min"]
        selection = st.pills("Duration", option, selection_mode="single")
        if selection == "2 min":
            hours = 0
            minutes = 2
            seconds = 0
        if selection == "120 min":
            hours = 2
            minutes = 0
            seconds = 0

        cols = st.columns([1, 1, 1])
        cols[0].number_input("Hours", min_value=0, max_value=99, key="input_hours", value=hours, step=1)
        cols[1].number_input("Minutes", min_value=0, max_value=59, key="input_minutes", value=minutes, step=1)
        cols[2].number_input("Seconds", min_value=0, max_value=59, key="input_seconds", value=seconds, step=1)
        if st.button("Start", on_click=start_timer, type="primary"):
            pass

    # Auto-refresh sidebar every second while timer or alarm is active.
    if st.session_state.timer_running or st.session_state.alarm_active:
        st_autorefresh(interval=1000, key="timer_refresh")

# ------------------------------

# Read the content of your local index.html file
with open('utils/infogest/index.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Read the CSS content
with open('utils/infogest/design.css', 'r', encoding='utf-8') as css_file:
    css_content = css_file.read()

# Inject the CSS into the HTML head section
html_content = html_content.replace(
    "<head>",
    f"<head><style>{css_content}</style>"
)

st.title("📋 Template for the harmonized *in vitro* digestion method from Infogest 2.0")

# Embed the HTML content in your Streamlit app
components.html(html_content, height=3300, scrolling=True)
