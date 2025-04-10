import streamlit as st
import streamlit.components.v1 as components
import time
import base64

from streamlit_autorefresh import st_autorefresh
import os
import pandas as pd

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
tabs = st.tabs(["Calculation", "pH Adjustment"])
with tabs[0]:
    components.html(html_content, height=3300, scrolling=True)

# Function triggered on change
def df_on_change():
    for idx, df in st.session_state.phdf.items():
        state = st.session_state[f'q{idx}']
        for index, updates in state["edited_rows"].items():
            #st.session_state["phdf"].loc[st.session_state["phdf"].index == index, "edited"] = True
            for key, value in updates.items():
                st.session_state.phdf[idx].loc[st.session_state.phdf[idx].index == index, key] = value

            # Update the result column based on the input columns by summing numeric values
            def to_float(val):
                try:
                    return float(val) if val not in [None, ""] else 0.0
                except ValueError:
                    return 0.0

            v1_val = st.session_state.phdf[idx].loc[st.session_state.phdf[idx].index == index, "6M HCl (µL)"].iloc[0]
            v2_val = st.session_state.phdf[idx].loc[st.session_state.phdf[idx].index == index, "1M HCl (µL)"].iloc[0]
            v3_val = st.session_state.phdf[idx].loc[st.session_state.phdf[idx].index == index, "6M NaOH (µL)"].iloc[0]
            v4_val = st.session_state.phdf[idx].loc[st.session_state.phdf[idx].index == index, "1M NaOH (µL)"].iloc[0]

            v1_num = to_float(v1_val)
            v2_num = to_float(v2_val)
            v3_num = to_float(v3_val)
            v4_num = to_float(v4_val)

            Vtot_sum = v1_num + v2_num + v3_num + v4_num
            st.session_state.phdf[idx].loc[st.session_state.phdf[idx].index == index, "Added V(total) (µL)"] = Vtot_sum
            st.session_state.phdf[idx].loc[st.session_state.phdf[idx].index == index, "V(water) to add (ml)"] = st.session_state.finalVolGastricPhase - (Vtot_sum/1000)

def update_on_change():
    # Recalculate the final volume of the gastric phase based on the new food value
    totalVolumeGastricPhase = 4 * st.session_state.food
    VolSGF = 1.6 * st.session_state.food
    VolRGE = (200 / 1000) * st.session_state.food
    VolOralPhase = 2 * st.session_state.food
    VolCaCl2 = (1 / 1000) * st.session_state.food
    sumVol = VolSGF + VolRGE + VolOralPhase + VolCaCl2
    st.session_state.finalVolGastricPhase = totalVolumeGastricPhase - sumVol

    # Helper function to safely convert values to float
    def to_float(val):
        try:
            return float(val) if val not in [None, ""] else 0.0
        except ValueError:
            return 0.0

    # Check if the dictionary of dataframes exists
    if 'phdf' in st.session_state:
        # Loop through each dataframe stored in st.session_state.phdf
        for idx, df in st.session_state.phdf.items():
            # Update every row in the "V(water) to add (ml)" column based on the new final volume
            for i in df.index:
                v1 = to_float(df.loc[i, "6M HCl (µL)"])
                v2 = to_float(df.loc[i, "1M HCl (µL)"])
                v3 = to_float(df.loc[i, "6M NaOH (µL)"])
                v4 = to_float(df.loc[i, "1M NaOH (µL)"])
                acid_base_total = v1 + v2 + v3 + v4
                # Calculate the updated water volume (assumes acid/base volumes are in µL, hence division by 1000)
                st.session_state.phdf[idx].loc[i, "V(water) to add (ml)"] = st.session_state.finalVolGastricPhase - (acid_base_total / 1000)

with tabs[1]:
    if 'sample_number' not in st.session_state:
        st.session_state.sample_number = 7
    if 'food' not in st.session_state:
        st.session_state.food = 0.5

    totalVolumeGastricPhase = 4 * st.session_state.food
    VolSGF = 1.6 * st.session_state.food
    VolRGE = 200 / 1000 * st.session_state.food
    VolOralPhase = 2 * st.session_state.food
    VolCaCl2 = 1 / 1000 * st.session_state.food
    sumVol = VolSGF + VolRGE + VolOralPhase + VolCaCl2
    st.session_state.finalVolGastricPhase = totalVolumeGastricPhase - sumVol


    cols = st.columns(6)
    with cols[0]:
        st.number_input("Sample Number", key="sample_number", step=1)
    with cols[1]:
        st.number_input("Initial Quantity of food", key="food", step=0.1, on_change=update_on_change)
    # Create an editable dataframe with a row for each sample
    # num_samples = st.session_state.sample_number

    columns = [
        "Sample Number",
        "pH at start",
        "6M HCl (µL)",
        "1M HCl (µL)",
        "6M NaOH (µL)",
        "1M NaOH (µL)",
        "pH at end",
        "Added V(total) (µL)",
        "V(water) to add (ml)"
    ]

    if 'phdf' not in st.session_state:
        st.session_state.phdf = {}

    elements = ["pH adjustment to 3: between oral and gastric phase", "pH adjustment to 3: during gastric phase (after 10 minutes)", "pH adjustment to 3: during gastric phase (after 60 minutes)", "pH adjustment to 7: between gastric and intestinal phase", "pH adjustment to 7: during intestinal phase (after 10 minutes)", "pH adjustment to 7: during intestinal phase (after 60 minutes)"]

    for idx, tables in enumerate(elements):
        st.header(tables)

        # Initialize the dataframe with current sample number
        st.session_state.phdf[idx] = pd.DataFrame({
            "Sample Number": list(range(1, st.session_state.sample_number + 1)),
            "pH at start": [None] * st.session_state.sample_number,
            "6M HCl (µL)": [None] * st.session_state.sample_number,
            "1M HCl (µL)": [None] * st.session_state.sample_number,
            "6M NaOH (µL)": [None] * st.session_state.sample_number,
            "1M NaOH (µL)": [None] * st.session_state.sample_number,
            "pH at end": [None] * st.session_state.sample_number,
            "Added V(total) (µL)": [None] * st.session_state.sample_number,
            "V(water) to add (ml)": [st.session_state.finalVolGastricPhase] * st.session_state.sample_number
        })

        # Display an editable dataframe
        # Editable DataFrame as main editor
        def editor():
            st.data_editor(
                st.session_state.phdf[idx],
                hide_index=True,
                column_config={
                    "V(water) to add (ml)": st.column_config.NumberColumn(format="%.10g")
                },
                disabled=["", "Added V(total) (µL)", "V(water) to add (ml)", "Sample Number"],  # lock some columns
                key=f"q{idx}",  # Store in session state
                on_change=df_on_change
            )


        # Run editor
        editor()
        if idx == 2:
            st.divider()
