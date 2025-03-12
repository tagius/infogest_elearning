import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    layout="wide"
)

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

st.title("📋 Template for the harmonized *in vitro* digestion method from COST Infogest")

# Embed the HTML content in your Streamlit app
components.html(html_content, height=3300, scrolling=True)
