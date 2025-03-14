import streamlit as st

st.set_page_config(
    layout="centered"
)

st.title("🧑‍🎓 INFOGEST Protocol E-Learning App")
st.write(
    """
    Welcome to the INFOGEST Protocol E-Learning App.

    This platform is designed as an e-learning resource for understanding the in vitro digestion protocol from INFOGEST.

    Use the sidebar to navigate between sections such as:
    - Introduction
    - Protocol Steps
    - Quiz and more!
    
    **To get started, please select a page from the sidebar.**
    
    ---
    """
)
st.image("utils/assets/Bandeau-general_inra_bandeau_nh.jpg", use_container_width=True)
st.header("ℹ️ About INFOGEST")
st.write(
    """
    Understanding the **effect of food on human health** is a current research priority in Europe but it is also a strong consumer demand. People want to be aware of the effects on their body of the food they eat. After ingestion, food will be broken down in the gut releasing components (peptides, amino acids, minerals, fatty acids…) that, beside their nutritional properties, may have a biological action.
    
    INFOGEST aims at improving the current scientific knowledge on **how foods are disintegrated during digestion**. This improved knowledge will help the scientific community and the industry to design new foods with improved nutritional and functional properties.
    
    INFOGEST was created under a cost Action [FA1005] with the aim to fulfil the need for developing a trans-European network to improve dissemination of critical research findings, develop truly multidisciplinary collaborations and harmonise approaches between groups and discipline areas spanning the main stages of food digestion.
    
    After the success of the European action [2011-2015], INFOGEST members has continue working together.
    
    INFOGEST is now an international network. The specific objectives of the network are to:
    
    - compare the existing digestion models, harmonize the methodologies, validate them towards in vivo data and propose guidelines for performing new experiments
    - identify the bioactive components that are released in the gut during food digestion
    - demonstrate the effect of these compounds on human health
    - determine the effect of the matrix structure on the bioavailability of food nutrients and bioactive molecules.
    """
)
st.write("---")
if st.button(":material/123: Continue here -> Fundamentals", type="primary"):
    st.switch_page("pages/fundamentals.py")