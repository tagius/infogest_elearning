import streamlit as st

st.set_page_config(
    layout="centered"
)

# Title and introductory message
st.title("Welcome to the INFOGEST Protocol E-Learning App")
st.write(
    """
    This app introduces you to the INFOGEST in vitro digestion protocol as described by [(Brodkorb et al. in Nature Protocols)](https://www.nature.com/articles/s41596-018-0119-1).
    
    The INFOGEST 2.0 protocol is a **standardised way to simulate digestion in a lab**, mimicking how food is broken down in the upper part of the human digestive system (mouth, stomach, and small intestine). It allows for a consistent method to compare results across different labs.
     """
)
# Display a representative figure from the article
st.image(
    "utils/assets/41596_2018_119_Fig1_HTML.webp",
    caption="Figure 1: Overview of the INFOGEST Protocol",
    use_container_width=True
)

# Provide more detailed points and tips
st.write(
    """
    ## **Key Idea**
    The protocol uses **constant conditions** (ratios of food to fluids and pH) within each phase of digestion. This makes it simpler to perform but not suitable for studying how fast digestion occurs.
    
    ## **Three Main Stages**
    The digestion process is divided into three phases:
    
    - **Oral Phase:** Mix the food with a **simulated saliva fluid (SSF)**. If the food is solid or semi-solid, mimic chewing. This stage lasts **2 minutes**.
    - **Gastric Phase:** Mix the oral bolus with **simulated gastric fluid (SGF)** and enzymes (**pepsin and gastric lipase**), and incubate for **2 hours**. Adjust the **pH to 3**.
    - **Intestinal Phase:** Combine the gastric mixture with **simulated intestinal fluid (SIF)**, bile salts, and pancreatic enzymes (or **pancreatin, based on trypsin activity**). Incubate for **2 hours**. Adjust the **pH to 7**.
    
    ## **Enzyme Preparation**
    Before starting the digestion, you need to prepare the digestive enzymes:
    
    - Prepare **fresh enzyme solutions** just before use and **keep them cold** until needed.
    - Use **Tris buffer** for pepsin activity assays to improve reproducibility.
    
    ### Enzyme Activity Assays
    Prior to the digestion experiment, it is **crucial to determine the activities of all digestive enzymes** using recommended standardised assays. These assays include:
    
    - **α-amylase**
    - **Pepsin**
    - **Gastric and pancreatic lipase**
    - **Trypsin**
    - **Chymotrypsin**
    - The assay for gastric lipase has been adapted from Carrière et al and merged with that for pancreatic lipase.
    - **Bile salt concentrations** should also be determined.
    
    > *Remark: Enzyme activity determination is recommended for each new batch of enzyme or after prolonged storage.*
    
    ## **Using Gastric Lipase**
    - The protocol recommends using **gastric lipase**.
    - A good source is **rabbit gastric extract (RGE)**.
    - RGE also contains **pepsin**, which make it a good alternative to **gastric lipase**.
    
    ## **Digestion Fluids**
    - You will need to prepare **simulated digestive fluids** for the **oral, gastric, and intestinal phases** (**SSF, SGF, and SIF**, respectively).
    - These solutions are made with a mix of salts and other compounds, which mimic the conditions of the digestive tract.
    - The solutions are made as a **concentrate**, then **diluted before use**.
    - Add **calcium chloride (CaCl₂)** immediately before the experiment to each of the simulated digestive fluids.
    - **Warm the fluids** to **37°C** before using them for the experiment.
    
    ## **Running the Digestion**
    - **Mix the food** with the fluids and enzymes in the correct sequence.
    - **Adjust the pH** at each stage using acid or base as required.
    - Perform a **pH test adjustment** to determine how much acid or base is needed.
    - Make sure to **record all volumes and times carefully**.
    - Incubate the samples at **37°C while mixing**.
    - Include a **blank tube** (without food but with all enzymes) to help identify enzyme-derived peptides that may be detected in the digesta.
    
    ## **After Digestion**
    - You should stop enzyme activity at the end of digestion by using an **inhibitor** or by **heat shocking the sample**.
    - Centrifuge the samples to separate the hard pellet from the digested supernatant.
    - Snap freeze and **freeze-dry the sample**.
    - Analyse the samples to determine digestion products, such as **peptides, fatty acids, or sugars**.
    
    ---
    """
)
if st.button(":material/sort: Continue here -> First steps"):
    st.switch_page("pages/first_steps.py")