import streamlit as st
import pandas as pd
import json

# Configure Streamlit page
st.set_page_config(layout="wide")

def load_json_data(json_file):
    try:
        with open(json_file, "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return []

# Define the formula for calculating Powder amount
# (conc*volume)/(stock conc*1000)*1.25
def update_table(cdf, vdf):
    def compute_volume(working, stock, volume):
        try:
            working_num = float(working)
            stock_num = float(stock)
            return round(((working_num * volume) / (stock_num * 1000)) * 1.25, 2)
        except (ValueError, TypeError):
            # Return the original text (e.g., "until pH 7") if conversion fails
            return working

    volume = st.session_state.volume_slider  # get the updated slider value

    vdf["SSF (for 1.25×)"] = cdf.apply(
        lambda row: compute_volume(row["SSF Working conc. (mM)"], row["Stock conc. (M)"], volume),
        axis=1,
    )
    vdf["SGF (for 1.25×)"] = cdf.apply(
        lambda row: compute_volume(row["SGF Working conc. (mM)"], row["Stock conc. (M)"], volume),
        axis=1,
    )
    vdf["SIF (for 1.25×)"] = cdf.apply(
        lambda row: compute_volume(row["SIF Working conc. (mM)"], row["Stock conc. (M)"], volume),
        axis=1,
    )
    return vdf

def update_cacl2_table(cdf, vdf):
    # Get the updated reaction tube volume from the number input (in mL)
    tube_volume = st.session_state.cacl2_volume_slider

    # Update the first row ("Reaction tube volume (mL)") in the CaCl2 DataFrame for each solution.
    # We assume the columns in vdf are: "SSF", "SGF", "SIF".
    vdf.loc["Reaction tube volume (mL)"] = [tube_volume, tube_volume*2, tube_volume*4]

    # Extract the row corresponding to CaCl2(H2O)2 from conc_df.
    # It is assumed that the reagent name is stored in the column "".
    try:
        cacl2_row = cdf[cdf[""] == "CaCl2(H2O)2"].iloc[0]
    except IndexError:
        st.error("CaCl2(H2O)2 entry not found in the concentration data.")
        return vdf

    # Extract the working concentration factors for each fluid.
    # These values represent the µL per mL factor.
    try:
        ssf_factor = float(cacl2_row["SSF Working conc. (mM)"])
    except (ValueError, TypeError):
        ssf_factor = cacl2_row["SSF Working conc. (mM)"]
    try:
        sgf_factor = float(cacl2_row["SGF Working conc. (mM)"])
    except (ValueError, TypeError):
        sgf_factor = cacl2_row["SGF Working conc. (mM)"]
    try:
        sif_factor = float(cacl2_row["SIF Working conc. (mM)"])
    except (ValueError, TypeError):
        sif_factor = cacl2_row["SIF Working conc. (mM)"]
    try:
        stock_conc = float(cacl2_row["Stock conc. (M)"])
    except (ValueError, TypeError):
        stock_conc = cacl2_row["Stock conc. (M)"]

    # Calculate the CaCl2(H2O)2 addition (in µL) for each fluid.
    ssf_add = round((tube_volume * ssf_factor)/stock_conc, 3)
    sgf_add = round((tube_volume * sgf_factor)/stock_conc, 3)
    sif_add = round((tube_volume * sif_factor)/stock_conc, 3)

    # Update the second row ("CaCl2(H2O)2 to add (µL)") in the DataFrame.
    vdf.loc["CaCl2(H2O)2 to add (µL)"] = [ssf_add, sgf_add, sif_add]

    return vdf



st.title(":material/experiment: Preparation of Simulated Digestive Fluids")

st.write("""
This protocol is adapted from the nature INFOGEST Simulated Digestive Fluids Protocol (Brodkorb et al., 2019).

It provides step-by-step instructions and tables to guide you through:

↳**Preparing the working Simulated Digestive Fluid solutions (SDF).**

---
""")

# ======================
# 2. Simulated Digestive Fluids (SDF)
# ======================
st.header("🍵 Preparing Simulated Digestive Fluids (SDF)")

st.markdown("""
**⚠️ Before You Begin**  
1. **Check the LFO walk-in fridge to see if existing SDF solutions are available.**
2. Check LFO walk-in fridge to ensure that all the necessary stock solutions are available.    
3. These instructions assume you are preparing 1 L of each fluid.
4. **Use appropriate measuring devices** (Pasteur pipette, measuring cylinder, etc.).


### 🧪 Preparation Instructions 

> *The following instructions will guide you to prepare the simulated digestive fluid solutions: SSF (Salivary), SGF (Gastric) and SIF (Intestinal).*

1. **⚠️NaHCO3 (1M) need to be replaced by NaCl (use 2M stock solution). Volumes below already consider this change.**
2. Check the table below to see the electrolyte stock solutions final working concentrations:

**Table 2:** Working SDF concentration of electrolytes.
""")

## add table here
# Load data from the JSON file
conc_data = load_json_data("utils/assets/sdf_conc.json")
conc_df = pd.DataFrame(conc_data)
st.dataframe(conc_data,
             hide_index=True)

st.write("""
3. Stock SDF solutions **must be 1.25x concentrated** compare to the working SDF solution.
4. **In a 1 L graduated cylinder**, place a magnetic stir bar.
5. **Add the required volumes of each stock solution** (see tables below).

**Table 3:** Volumes of electrolyte stock solutions to prepare **1.25x stock** SDF.
*Select the volume you want to prepare (Default is 1000 mL):*
""")
## add table here
vol_data = load_json_data("utils/assets/sdf_vol.json")
vol_df = pd.DataFrame(vol_data)

col1, col2, col3 = st.columns(3)
with col1:
    volume = st.slider(
        "Volume to prepare (mL):",
        100, 10000, 1000,
        step=50,
        key="volume_slider",  # add a key so you can access the value
        on_change=update_table,
        args=(conc_df, vol_df)  # swap the order here
    )
## add table here of SDF calculation
vol_df = update_table(conc_df, vol_df)

st.dataframe(vol_df,
             hide_index=True)

st.write("""
6. Add MilliQ water until 90% of the final volume (~900mL for 1L) and mix well.
7. Adjust the pH of each SSF. SGF and SIF solutions:
   - **pH = 7** for SSF
   - **pH = 3** for SGF
   - **pH = 7** for SIF
   Use either HCl or NaOH as needed.
   

8. **Top up** the volume to 1 L with dH₂O after pH adjustment.
9. Transfer in a clean glass bottle.
10. Store all prepared stock solutions in the **LFO walk-in fridge** (LFO, -1 floor). Stock solutions can be prepared and **stored at−20 °C for 1 year**.

---

### 🧑‍🔬 Addition of CaCl2(H2O)2
CaCl₂ is *not* added into the SDF directly. Instead, add the required CaCl₂ volume right before performing the digestion experiment. 
It can also be added directly into the reaction tube.

**The volumes to add depends of the reaction volume**. 
To calculate the amount of salts added during in-vitro digestion, 
write the volume of digestive fluid added during each phase and the volume you need to add will be calculated below.

**Table 4:** Volumes of CaCl₂ to add to the reaction tube.
*Select the volume you want to prepare (Default is 3.2 mL):*
""")
## add tab le here
cacl2_data = {
    "SSF": [3.2, 20],
    "SGF": [6.4, 4],
    "SIF": [12.8, 32],
}
index = ["Reaction tube volume (mL)", "CaCl2(H2O)2 to add (µL)"]
cacl2_df = pd.DataFrame(cacl2_data, index=index)

col4, col5, col6 = st.columns(3)
with col4:
    cacl2_volume = st.number_input(
        "Volume in the reaction tube (mL):",
        min_value=0.001,
        value=3.200,
        step=0.001,
        format="%0.3f",
        key="cacl2_volume_slider",  # add a key so you can access the value
        on_change=update_cacl2_table,
        args=(conc_df, cacl2_df)  # swap the order here
    )
## add table here of SDF calculation
cacl2_df = update_cacl2_table(conc_df, cacl2_df)

st.dataframe(cacl2_df)

st.markdown("""
**Notes**  
- Values in the final columns refer to the final (working) concentrations in the **1×** solution.  
- **NaHCO₃** is replaced by additional **NaCl** in these protocols.  
- Refer to the protocol steps for proper volume measurement from each stock solution.  
- After adjusting the pH, remember to top up to 1L with deionized water (unless you are preparing different volumes).

---
""")
if st.button(":material/rocket_launch: Continue here -> Quick Start Protocol"):
    st.switch_page("pages/quick_start.py")