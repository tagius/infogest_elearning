import streamlit as st

# Set wide layout for the app
st.set_page_config(layout="centered", page_title="Changelog")

st.title("🧑🏽‍💻 Changelog")
st.markdown("### Changelog for March 2025")
st.markdown(""" 
*Update March 27th*
- **v.2.1** Update of the dashboard:
    - Hiding Amylase related panels and does the sum of the water volumes in algae mode.
    - Add tabs with Calculation sheet and pH Adjustments.
    - Creation of the ***v.1.0*** of pH Adjustments tables similar to the excel file.


- Improvement of the quiz questions:
    - Question 20 is now valid even if answer order is random.
    
---
- **v.2.0** Update of the dashboard:
    - Add support for light and dark mode
    - Add option for Lipase solution to add extra lipase
    - Improvement of the overall design
    - Better readability. 


- Addition of a basic countdown timer with start, stop, reset, and blinking red alarm in the dashboard:
    - Added marimba-inspired alarm synthesis.
    - Added preset pills for quick duration selection (2 min & 120 min).
   
""")

st.markdown("### Changelog for February 2025")
st.markdown(""" 
- **v.1.0** Creation of the dashboard:
    - Integration of the original template for the harmonized in vitro digestion method.
    - Update and enhancement of the original template for INFOGEST 2.0.


- Addition of the page:
    - Preparation stock solution
    - Preparation Simulated Digestion Fluids
    - Quick protocol
    - Download File page
""")

st.markdown("### Changelog for January 2025")
st.markdown(""" 
- First release of the changelog.
- Creation of the pages:
    - Introduction
    - Fundamentals
    - First steps
    - Quiz

""")