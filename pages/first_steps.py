import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

st.set_page_config(
    layout="wide"
)

st.title("⚙️INFOGEST Protocol Steps")

tab1, tab2 = st.tabs(["INFOGEST nature Protocol", "Video protocol"])

with tab1:
    with st.container():
        col1, col2 = st.columns(2, gap="medium")
        with col1:
            st.write("""
            ### Step 1: Save and Read the Original Published Protocol
            
            Before simulating digestion in the laboratory, it is essential to carefully read and understand the [standard INFOGEST protocol.](https://www.nature.com/articles/s41596-018-0119-1)
                
            This protocol provides a standardized method for simulating gastrointestinal digestion in vitro, ensuring reproducibility and physiological relevance.
            """)
        with col2:
            # Display the protocol file uploaded
            st.write("""
            ### Download the Original Protocol
            
            You can also download the full protocol PDF here:
            """)

            with open("utils/assets/s41596-018-0119-1.pdf", "rb") as file:
                st.download_button(
                    label="📄 Download INFOGEST Protocol (PDF)",
                    data=file,
                    file_name="s41596-018-0119-1.pdf",
                    mime="application/pdf",
                )

            st.write("**Make sure to read through the entire document before proceeding to the next steps.**")

    st.markdown("---")
    pdf_viewer("utils/assets/s41596-018-0119-1.pdf", width="100%", render_text=True)

with tab2:
    # Step 2: Video Demonstration of INFOGEST Protocol
    st.write("""
    ## INFOGEST In Vitro Digestion Learning Module
    ### Step 2: Watch the In-House Protocol Demonstration 🎥
    Now that you've read the INFOGEST protocol, it's time to see it in action!
    This video demonstrates the **step-by-step execution** of the protocol, including only the sample digestion and storage.
    """)

    # Video demonstration. URL: https://youtu.be/bd7A1_sKZ_g
    VIDEO_URL = "https://youtu.be/bd7A1_sKZ_g"
    if VIDEO_URL == "":
        video_file = open("utils/assets/infogest protocol video.mp4", "rb")
        video_bytes = video_file.read()
        try:
            with video_file as video:
                st.video(video)
        except FileNotFoundError:
            st.warning("⚠️ The in-house protocol video is not available yet. Please upload or record it.")
    else:
        st.video(VIDEO_URL)

    st.write("""
    👉 **Make sure to pay attention to pH adjustments, and digestion conditions in the video.**
    
    *⚠️ The actual instrument setup may differ from what is shown in the video. However, the underlying principle remains the same!*
    
    ---
    """)
    if st.button(":material/experiment: Continue here -> Preparation of the Stock Solutions", type="primary"):
        st.switch_page("pages/solution_prep.py")
