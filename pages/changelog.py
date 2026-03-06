import streamlit as st

# Set wide layout for the app
st.set_page_config(layout="centered", page_title="Changelog")

st.title("🧑🏽‍💻 Changelog")

st.markdown("### Changelog for March 2026")
st.markdown("""
*Update March 6th*
- Added **Dashboard v2** in the Tools navigation section.
- Dashboard v2 embeds the modular INFOGEST calculator from static assets.
- The pH Adjustment tab and timer behavior remain available in Dashboard v2.
""")

st.markdown("### Changelog for February 2026")
st.markdown("""
*Update February 23rd*
- Addition of the **LogBook** page:
    - Embedded Notion form for logging INFOGEST digestion experiments.
    - Standalone section in the navigation menu for visibility.
    - Browser warning when leaving the page with unsaved entries.
    - Reminder banner added to the Dashboard with a direct link to the LogBook.
    - LogBook button added to the Dashboard calculation top bar.
""")

st.markdown("### Changelog for September 2025")
st.markdown(""" 
*Update September 12th*
- **v.2.3** Enhanced enzyme panels with purity and solution options:
    - Added **powder purity** input fields (0.1-100%) for all enzyme types to account for non-100% pure enzyme powders
    - Added **powder/solution toggle switches** for flexible enzyme preparation methods
    - Added **stock concentration** inputs for enzyme solutions with automatic volume-based calculations  
    - Enhanced calculation logic to support both powder purity adjustments and direct solution concentration calculations
    - Implemented for salivary amylase, RGE, pepsin, lipase, pancreatin, bile, and individual intestinal enzymes
    - Users can now accurately calculate enzyme amounts whether using impure powders or pre-made solutions
""")

st.markdown("### Changelog for April 2025")
st.markdown(""" 
*Update April 25th*
- Fix pH adjustment when sample number is changed. Now Update correctly the Total volume and the water volume to add
- ⚠️ pH value will be reset if tab is reloaded. I am working on a solution to fix this.
""")
st.markdown(""" 
*Update April 10th*
- Fix alarm on Safari. Please be sure to have your autoplay allowed in the safari settings (Safari > Settings > Websites > allow autoplay = always.).
- **v.2.2** Update of the dashboard:
    - Added a guided tour to the dashboard. support light and dark theme preferences.
    - Use only RGE is checked by default.
    - Icon CDN updated after unpck error.
""")

st.markdown("### Changelog for March 2025")
st.markdown(""" 
*Update March 31th*
- Fix pH Adjustment row generation when sample number is changed.

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
