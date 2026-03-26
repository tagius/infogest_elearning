import streamlit as st
import streamlit.components.v1 as components
import time

from streamlit_autorefresh import st_autorefresh

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
            st.audio("utils/assets/Sencha.mp3", format="audio/mpeg", loop=True, autoplay=True)
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

st.title("🟢 INFOGEST 2.0 Static in-vitro calculator")

# LogBook reminder
logbook_cols = st.columns([5, 1], vertical_alignment="center")

with logbook_cols[0]:
    st.markdown("📓 **Reminder:** Don't forget to log your experiment setup and observations.")
with logbook_cols[1]:
    if st.button(":material/menu_book: Open LogBook"):
        st.switch_page("pages/logbook.py")

# Embed the static calculator page in an iframe
components.iframe(
    "https://tagius.github.io/INFOGEST-2.0-Static-In-Vitro-Digestion-Calculator/",
    height=800,
    scrolling=True,
)
