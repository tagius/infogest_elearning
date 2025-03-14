import streamlit as st
import pandas as pd
import json

st.set_page_config(
    layout="wide"
)

# Define the function to load json data file for easier editing
def load_json_data(json_file):
    try:
        with open(json_file, "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return []

# Define the formula for calculating Powder amount
def update_powder(df):
    c = df["Concentration stock (mol/L)"]
    V = df["Desired Vol. (mL) (editable)"]
    M = df["Molecular Weight (g/mol)"]
    df["Powder mass (g)"] = ((c / 1000) * V * M)
    return df

# Function triggered on change
def df_on_change():
    state = st.session_state["df_editor"]
    for index, updates in state["edited_rows"].items():
        #st.session_state["df"].loc[st.session_state["df"].index == index, "edited"] = True
        for key, value in updates.items():
            st.session_state["df"].loc[st.session_state["df"].index == index, key] = value
        # Update the result column based on the input column
        c = st.session_state["df"].loc[st.session_state["df"].index == index, "Concentration stock (mol/L)"]
        V = st.session_state["df"].loc[st.session_state["df"].index == index, "Desired Vol. (mL) (editable)"]
        M = st.session_state["df"].loc[st.session_state["df"].index == index, "Molecular Weight (g/mol)"]
        st.session_state["df"].loc[st.session_state["df"].index == index, "Powder mass (g)"] = ((c/1000)*V*M)


st.title("️:material/experiment: Preparation of the Stock Solutions")

st.write("""
This protocol is adapted from the nature INFOGEST Simulated Digestive Fluids Protocol (Brodkorb et al., 2019).

It provides step-by-step instructions and tables to guide you through:

↳**Preparing the working stock solutions.**

↳**Preparing acids and bases for pH adjustment.**

---
""")

# ======================
# 1. Stock Solutions
# ======================
st.header("⚗️ Stock Solutions")

st.markdown("""
**⚠️ Before You Begin**  
1. **Check the LFO walk-in fridge to see if existing stock solutions are available.**
2. Check the chemical availability and location in the [ETHZ Chemical Database](https://vtchemicals.ethz.ch/login)
    1. *(Optional) If your ETH account doesn't have access, please ask your supervisor a.s.a.p.*    
3. Check that you have the chemicals with the correct molecular weight (MW)
4. Stock concentration has been taken from the INFOGEST protocol

### 🧪 Preparation Instructions 
1. Gather all needed chemical from the table below.

**Table 1.** Stock solution preparation:
> You can write the desired volume of the stock solution to prepare by changing values in `Desired Vol. (mL) (editable)`. The mass of powder will be calculated automatically.
""")

# Add table here
# Load data from the JSON file
data_stock_sol = load_json_data("utils/assets/stock_solution.json")
df_stock_sol = pd.DataFrame(data_stock_sol)

# Ensure Powder (g) is calculated before display
df_stock_sol = update_powder(df_stock_sol)

# Editable DataFrame as main editor
def editor():
    if "df" not in st.session_state:
        st.session_state["df"] = df_stock_sol
    st.data_editor(
    st.session_state["df"],
    hide_index=True,
    column_config={
        "Desired Vol. (mL) (editable)": st.column_config.NumberColumn("Desired Vol. (mL) (editable)", step=1),
        "Powder mass (g)": st.column_config.NumberColumn(step=0.01)
    },
    disabled=["", "Powder mass (g)", "Concentration stock (mol/L)", "Molecular Weight (g/mol)","last location"],  # Make only "Volume (mL)" editable
    key="df_editor",  # Store in session state
    on_change=df_on_change
    )

#Run editor
editor()

st.write("""
2. Depending on the required volume, prepare and label a clean bottle, Falcon tube, or Eppendorf container according to the guidelines on chemical labeling *(check P: drive)*.  
3. Prepare clean graduated cylinders for accurate volume measurement when preparing and mixing solutions.  
4. Use the precision balances (LFV D28) to **weigh** the required amount of chemical from the table and transfer it into the graduated cylinder.  
5. Add MilliQ water until reaching the desired volume.  
6. Mix well.  

**After Preparation**  
1. Aliquot **50 mL** portions of the stock solution into Falcon tubes and store them in the freezer.  
   1. To ensure clean aliquots, **all solutions must be filtered using a 0.25 µm filter**.  
   2. Use a **vacuum bottle filter** or a **syringe with an appropriate filter**.  
2. Store all prepared stock solutions in the **LFO walk-in fridge** (LFO, -1 floor).

---
""")

st.header("🔬 Acids & Bases for pH Adjustment")

st.write("""
To properly adjust the pH during the experiment, acids and bases must be prepared in advance.

**⚠️ Before You Begin**
1. **Check in LFV D28** to see if pre-prepared acid and base solutions are already available.  
2. **Verify chemical availability and location** in the [ETHZ Chemical Database](https://vtchemicals.ethz.ch/login).  
3. Prepare the following solutions in a **plastic container**:  
   - **NaOH 1M**  
   - **NaOH 6M**  
   - **HCl 1M**  
   - **HCl 6M**  


> **🛑 Safety Precautions**
> - Always **wear personal protective equipment** (lab coat, safety glasses, gloves).  
> - Work **under a fume/laminar flow hood** to ensure safe handling of corrosive chemicals.  
> - **Exothermic reactions**: Mixing acids and bases with water generates heat.  
>   - If the solution becomes too hot, **prepare an ice bucket** to cool the container.  
> - **Always add water first, then slowly add the acid** to avoid dangerous splashing or explosions.  
>   - ❌ **Never pour water into concentrated acid!**  


### 🧪 Preparation Instructions  
1.	Calculate the required NaOH mass using the formula:

> *Mass (g) = Molarity (M) * Volume (L) * Molar Mass of NaOH (40 g/mol)*

- For 1M NaOH, dissolve 40 g of NaOH per 1L of water.
- For 6M NaOH, dissolve 240 g of NaOH per 1L of water.
	
2. Measure the appropriate amount of distilled water (about 80% of the final volume) and pour it into a plastic beaker.
3. Slowly add NaOH pellets to the water while stirring continuously with a magnetic stirrer.
4. Allow the solution to dissolve completely before adding more NaOH. The solution will become hot—place the container in an ice bucket if necessary.
5. Once fully dissolved, adjust the volume to 1L with additional distilled water.
6. Transfer the solution to a labeled storage bottle and store in LFV D28.
7. **Repeat the same step for HCl.**

---

### 📦 **Storage Guidelines**  
- **Label all prepared solutions** clearly with concentration, date, and your initials.
- Stock solutions can be prepared and **stored at−20 °C for 1 year**.
- **Store all acid and base solutions in LFV D28** after preparation.  
- **CaCl₂ stock solution** is typically added just before the actual digestion experiment and not in the stock solutions.  

--- 
""")
if st.button(":material/experiment: Continue here -> Preparation of Simulated Digestive Fluids", type="primary"):
    st.switch_page("pages/sdf_prep.py")