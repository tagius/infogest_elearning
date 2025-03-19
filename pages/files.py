import streamlit as st
import base64

# Set wide layout for the app
st.set_page_config(layout="centered", page_title="Files to download")

st.title("📥 File to download")

# Display the protocol file uploaded
link = "https://polybox.ethz.ch/index.php/s/DInobqGaX03EkBH"
pwd = "sfp2025"

with st.container(border=True):
    st.write("""
                #### Download the latest files
                
                *Last update: 2025.03.15*
                
                You can download the latest documents from the ETHZ Polybox:
                """)
    with st.expander("Show password", expanded=False, icon=":material/lock:"):
        st.write(pwd)

    # Display a clickable markdown link with a styled button appearance
    with open("utils/assets/polybox.png", "rb") as image_file:
        img_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    html_content = f'''
    <a href="{link}" target="_blank" style="text-decoration: none;">
        <div style="background-color: #ff4b4b; border-radius: 10px; overflow: hidden; text-align: center;">
            <img src="data:image/png;base64,{img_base64}" alt="Go to Polybox" style="width: 95%; border-radius: 10px; display: block; margin: 10px auto 0;">
            <div style="padding: 10px;">
                <span style="color: #ffffff; font-weight: bold;">Go to Polybox</span>
            </div>
        </div>
        </br>
    </a>
    '''

    st.markdown(html_content, unsafe_allow_html=True)

    st.write("""
    
    :orange-background[*Files are updated regularly, please check last update date.*]
    
    """)
