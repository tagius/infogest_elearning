import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

st.title("📓 LogBook")
st.write(
    """
    Use this LogBook to record your INFOGEST digestion experiments.
    Fill in the form below to log your setup, parameters, and observations.
    """
)

# Embed Notion form
components.html(
    '''
    <iframe
        src="https://sfp-apnh.notion.site/ebd//310fe013d6a1800b9db3d59c99556871"
        width="100%"
        height="800"
        frameborder="0"
        allowfullscreen
        style="border: none; border-radius: 8px;">
    </iframe>
    ''',
    height=820,
    scrolling=False
)

# Browser tab close/navigate warning
components.html(
    """
    <script>
    window.parent.addEventListener('beforeunload', function(e) {
        e.preventDefault();
        e.returnValue = '';
    });
    </script>
    """,
    height=0
)
