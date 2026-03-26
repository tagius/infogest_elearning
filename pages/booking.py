import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

st.title("📅 Booking Calendar")

components.iframe(
    "https://teamup.com/ks2z77nnri9vjnxswv?tz=Calendar%20default&showHeader=0&showProfileAndInfo=0&showSidepanel=1&showMenu=1&showViewHeader=1&showAgendaDetails=0&showDateControls=1&showDateRange=1",
    height=700,
    scrolling=True,
)
