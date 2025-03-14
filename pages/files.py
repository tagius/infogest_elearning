import streamlit as st
from streamlit_extras.grid import grid

# Set wide layout for the app
st.set_page_config(layout="wide", page_title="Dashboard Test - Oral Phase")

st.title("📥 File to download")

# Main grid to download the different files
grid = grid(2, vertical_align="bottom")

# Display the protocol file uploaded

with grid.container(border=True):
    st.write("""
                #### Download the latest SFP Standard protocol
                
                *Last update: 2025.03.15*
                
                You can also download the full protocol document here:
                """)

    with open("utils/assets/s41596-018-0119-1.pdf", "rb") as file:
        st.download_button(
            label="📄 Download Standard Protocol (PDF)",
            data=file,
            file_name="s41596-018-0119-1.pdf",
            mime="application/pdf",
        )

with grid.container(border=True):
    st.write("""
                #### Download the latest excel calculation template

                *Last update: 2025.03.15*

                This file is an excel file based on the dashboard app to calculate volumes and enzyme quantity for each phases.
                You can also download the excel file here:
                """)

    with open("utils/assets/s41596-018-0119-1.pdf", "rb") as file:
        st.download_button(
            label="📄 Download calculation Template (Excel)",
            data=file,
            file_name="s41596-018-0119-1.pdf",
            mime="application/pdf",
        )

