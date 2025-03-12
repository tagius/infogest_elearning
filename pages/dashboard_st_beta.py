import streamlit as st
from streamlit_extras.grid import grid
from streamlit_extras.row import row

st.set_page_config(
    layout="wide"
)

# Default input values (from original tool) for initialization
defaults = {
    "amount": 9,                  # Number of samples (excluding master mix)
    "food1": 5.0,                 # Quantity of food (g or ml)
    "sampling1": 0.0,             # Oral phase sampling volume (ml)
    "acid2": 0.1,                 # Gastric phase acid volume (ml)
    "sampling2": 0.0,             # Gastric phase sampling volume (ml)
    "base3": 0.2,                 # Intestinal phase base (NaOH) volume (ml) for pancreatin mode
    "sampling3": 0.0,             # Intestinal phase sampling volume (ml) for pancreatin mode
    "base4": 0.2,                 # Intestinal phase base volume (ml) for individual enzyme mode
    "sampling4": 0.0,             # Intestinal phase sampling volume (ml) for individual enzyme mode
    # Enzyme measurements and required units (defaults from tool)
    "finalu1": 75.0,   # Final amylase units (U/ml) required in oral phase  
    "measured1": 1000.0,  # Measured amylase activity (U/mg) 
    "effective1": 1.0,    # Amylase powder weight per sample (mg) 
    "Meffective1": 10.0,  # Amylase powder weight for master mix (mg)
    "finallu2": 60.0,   # Final lipase units required in gastric (U/ml) 
    "measuredl2": 200.0, # Measured lipase activity of RGE (U/mg) 
    "measuredlp2": 0.0,  # Measured pepsin activity of RGE (U/mg) 
    "effectivel2": 6.0,  # RGE powder weight per sample (mg) 
    "Meffectivel2": 60.0, # RGE powder weight for master mix (mg)
    "finalpu2": 2000.0,  # Final pepsin units required (U/ml) 
    "measuredp2": 2500.0,# Measured pepsin activity (U/mg) 
    "effectivep2": 16.0, # Pepsin powder weight per sample (mg) 
    "Meffectivep2": 160.0,# Pepsin powder weight for master mix (mg)
    "finalu3a": 100.0,   # Final pancreatin trypsin units (U/ml) 
    "measured3a": 200.0, # Measured pancreatin activity (U/mg) 
    "effective3a": 20.0, # Pancreatin weight per sample (mg) 
    "Meffective3a": 200.0,# Pancreatin weight for master mix (mg)
    "finalu3b": 10.0,    # Final bile concentration (mM) 
    "measured3b": 100.0, # Measured bile content (mmol/g) 
    "effective3b": 4.0,  # Bile powder weight per sample (mg) 
    "Meffective3b": 40.0,# Bile powder weight for master mix (mg)
    "finalu4a": 100.0,   # Final trypsin units (U/ml) 
    "measured4a": 200.0, # Measured trypsin activity (U/mg) 
    "effective4a": 20.0, # Trypsin weight per sample (mg) 
    "Meffective4a": 200.0,# Trypsin weight for stock solution (mg)
    "finalu4b": 25.0,    # Final chymotrypsin units (U/ml) 
    "measured4b": 50.0,  # Measured chymotrypsin activity (U/mg) 
    "effective4b": 20.0, # Chymotrypsin weight per sample (mg) 
    "Meffective4b": 200.0,# Chymotrypsin weight for stock (mg)
    "finalu4c": 2000.0,  # Final lipase units (U/ml) 
    "measured4c": 1000.0,# Measured lipase activity (U/mg) 
    "effective4c": 80.0, # Lipase weight per sample (mg) 
    "Meffective4c": 800.0,# Lipase weight for stock (mg)
    "finalu4d": 6000.0,  # Colipase activity (U/mg) – measured activity 
    "effective4d": 6.0,  # Colipase weight per sample (mg) 
    "Meffective4d": 54.0,# Colipase weight for stock (mg)
    "finalu4e": 200.0,   # Final pancreatic amylase units (U/ml) 
    "measured4e": 100.0, # Measured pancreatic amylase activity (U/mg) 
    "effective4e": 80.0, # Pancreatic amylase weight per sample (mg) 
    "Meffective4e": 800.0,# Pancreatic amylase weight for stock (mg)
    "finalu4f": 10.0,    # Final bile concentration (mM) 
    "measured4f": 100.0, # Measured bile content (mmol/g) 
    "effective4f": 4.0,  # Bile powder weight per sample (mg) 
    "Meffective4f": 40.0 # Bile powder weight for stock (mg)
}
# Initialize session state with defaults on first load
if "food1" not in st.session_state:
    for k,v in defaults.items():
        st.session_state[k] = v

## Page title -------------------
st.title("Template for the harmonized in vitro digestion method from COST Infogest")
help = st.empty()

## Side menu -------------------
# Intestinal phase mode toggle (pancreatin vs individual enzymes)
with st.sidebar:
    mode = st.radio(
        "Intestinal enzyme mix:",
        options=["Pancreatin (combined enzymes)", "Individual enzymes"],
        index=1 if st.session_state.get("indi") else 0
    )
    use_individual = (mode == "Individual enzymes")
    st.session_state["indi"] = use_individual  # track mode in session state

    # Reset button to restore defaults
    if st.button("Reset all"):
        for k,v in defaults.items():
            st.session_state[k] = v
        st.rerun()

    if st.toggle("Help"):
        help.write("""
        This is a support for the setup of an in vitro digestion (IVD) of food according to the harmonized Infogest method.
        
        The light yellow input fields need to be changed according to your needs and measured enzyme activities. "Food" can be liquid, solid or dissolved food. The enzyme activities should be measured as described in the harmonized IVD method.
        
        Press the "Intestinal step..." button to switch between intestinal phase with pancreatin or individual enzymes.
        
        Input is stored in the browser cache until you clear your browser memory. Press "Reset all" to go back to the presettings.
        
        Print as pdf to have a printout for your records. 
        """)

## -------------------
main_grid = grid(2,1, vertical_align="bottom")
main_grid.header("Digestion phase recipes")
main_grid.header("Solutions recipes")
main_grid.divider()

# --- Oral phase composition ---
with main_grid.expander("Oral Phase Composition", expanded=True):
    # Calculations for oral phase composition
    food1 = st.session_state.food1
    sampling1 = st.session_state.sampling1
    ssf1 = food1 * 4.0 / 5.0  # Simulated Salivary Fluid volume
    amylase1 = food1 / 10.0  # Salivary amylase solution volume
    cacl1 = food1 * 5.0  # CaCl2 volume in µL (0.3 M, 5 µL per mL food)
    h2o1 = food1 - ssf1 - amylase1 - (
            cacl1 / 1000)  # Water to add (ml)
    total1 = food1 * 2.0  # Total volume = 2 × food volume
    final1 = total1 - sampling1  # Final volume after removing sample

    #Row 1
    opc_row = row([3,2,1,2,1], vertical_align="center", gap="small")
    opc_row.write(" ")
    opc_row.write("Individual addition")
    opc_row.write(" ")
    opc_row.write("Using Oral mastermix")
    opc_row.write(" ")

    #Row 2
    opc_row.write("Quantity of food")
    opc_row.number_input("Amount of food (g or ml)", min_value=0.1, key="food1", label_visibility="collapsed")
    opc_row.write("g")
    opc_row.number_input("Using Oral mastermix", min_value=0.1, value=food1, label_visibility="collapsed", disabled=True)
    opc_row.write("g")

    #Row 3
    opc_row.write("Simulated salivary fluid (SSF)")
    opc_row.write(f"<p style='text-align: right;'>{ssf1:.3f}</p>", unsafe_allow_html=True)
    opc_row.write("ml")
    opc_row.write("")
    opc_row.write("")

    # Row 4
    opc_row.write("Salivary amylase solution")
    opc_row.write(f"<p style='text-align: right;'>{amylase1:.3f}</p>", unsafe_allow_html=True)
    opc_row.write("ml")
    opc_row.write("")
    opc_row.write("")

    # Row 5
    opc_row.write("0.3 M CaCl2")
    opc_row.write(f"<p style='text-align: right;'>{cacl1:.1f}</p>", unsafe_allow_html=True)
    opc_row.write("µl")
    opc_row.write("")
    opc_row.write("")

    # Row 6
    opc_row.write("Water")
    opc_row.write(f"<p style='text-align: right;'>{h2o1:.3f}</p>", unsafe_allow_html=True)
    opc_row.write("ml")
    opc_row.write("")
    opc_row.write("")

    # Row 7
    opc_row.write("<p style=' background-color: lightblue;'>Oral mastermix</p>", unsafe_allow_html=True)
    opc_row.write("<p style=' background-color: lightblue;'> </div>", unsafe_allow_html=True)
    opc_row.write("<p style=' background-color: lightblue;'> </p>", unsafe_allow_html=True)
    opc_row.write(f"<p style='text-align: right; background-color: lightblue;'>{food1:.3f}</p>", unsafe_allow_html=True)
    opc_row.write("<p style=' background-color: lightblue;'>g</p>", unsafe_allow_html=True)
    st.markdown("<hr style='margin-top: 0px; margin-bottom: 0px; border: none; border-top: 1px solid #ccc;'/>", unsafe_allow_html=True)

    # Row 8
    opc_row2 = row([3,2,1,2,1], vertical_align="center", gap="small")
    opc_row2.write("Total digest volume")
    opc_row2.write(f"<p style='text-align: right;'>{total1:.3f}</p>", unsafe_allow_html=True)
    opc_row2.write("ml")
    opc_row2.write(f"<p style='text-align: right;'>{total1:.3f}</p>", unsafe_allow_html=True)
    opc_row2.write("ml")
    st.markdown("<hr style='margin-top: 0px; margin-bottom: 0px; border: none; border-top: 1px solid #ccc;'/>", unsafe_allow_html=True)

    # Row 9
    opc_row3 = row([3, 2, 1, 2, 1], vertical_align="center", gap="small")
    opc_row3.write("Sampling volume after oral phase (if any)")
    opc_row3.number_input("Sampling volume after oral phase (ml", min_value=0.0, key="sampling1", label_visibility="collapsed")
    opc_row3.write("ml")
    opc_row3.write(f"<p style='text-align: right;'>{sampling1:.3f}</p>", unsafe_allow_html=True)
    opc_row3.write("ml")

    # Row 10
    opc_row3.write("Final volume")
    opc_row3.write(f"<p style='text-align: right;'>{final1:.3f}</p>", unsafe_allow_html=True)
    opc_row3.write("ml")
    opc_row3.write(f"<p style='text-align: right;'>{final1:.3f}</p>", unsafe_allow_html=True)
    opc_row3.write("ml")
    st.markdown("<hr style='margin-top: 0px; margin-bottom: 0px; border: none; border-top: 1px solid #ccc;'/>", unsafe_allow_html=True)

    # Row 12
    opc_row4 = row([3, 2, 1, 2, 1], vertical_align="center", gap="small")
    opc_row4.write("Digestion duration")
    opc_row4.write("<p style='text-align: right;'>2</p>", unsafe_allow_html=True)
    opc_row4.write("min")
    opc_row4.write("<p style='text-align: right;'>2</p>", unsafe_allow_html=True)
    opc_row4.write("min")

## -------------------
# --- Oral phase Mastermix ---
with main_grid.expander("Oral Phase Mastermix", expanded=True):
    st.number_input("Number of samples (excluding master mix)", min_value=0, step=1, key="amount")
    st.markdown("<hr style='margin-top: 0px; margin-bottom: 0px; border: none; border-top: 1px solid #ccc;'/>",
                unsafe_allow_html=True)

    sample_count = int(st.session_state.amount)
    total_samples = sample_count + 1  # include master mix sample
    M_ssf1 = ssf1 * total_samples
    M_amylase1 = amylase1 * total_samples
    M_cacl1 = cacl1 * total_samples
    M_h2o1 = h2o1 * total_samples
    M_volume1 = food1 * total_samples

    # Header rows (translated from HTML)
    st.markdown("<h3>Oral mastermix</h3>", unsafe_allow_html=True)
    st.markdown(f"<h4>Stock solution for {sample_count}+1 samples</h4>", unsafe_allow_html=True)

    # Row 1: Simulated salivary fluid (SSF)
    mastermix_row = row([3, 2, 1], vertical_align="center", gap="small")
    mastermix_row.write("Simulated salivary fluid (SSF)")
    mastermix_row.write(f"<p style='text-align: right;'>{M_ssf1:.3f}</p>", unsafe_allow_html=True)
    mastermix_row.write("ml")

    # Row 2: Salivary amylase stock solution (HTML row has a special color; you could add styling if desired)
    mastermix_row = row([3, 2, 1], vertical_align="center", gap="small")
    mastermix_row.write("<p style=' background-color: #ffbb96;'>Salivary amylase stock solution</p>", unsafe_allow_html=True)
    mastermix_row.write(f"<p style='text-align: right; background-color: #ffbb96;'>{M_amylase1:.3f}</p>", unsafe_allow_html=True)
    mastermix_row.write("<p style=' background-color: #ffbb96;'>ml</p>", unsafe_allow_html=True)

    # Row 3: 0.3 M CaCl₂
    mastermix_row = row([3, 2, 1], vertical_align="center", gap="small")
    mastermix_row.write("0.3 M CaCl₂")
    mastermix_row.write(f"<p style='text-align: right;'>{M_cacl1:.1f}</p>", unsafe_allow_html=True)
    mastermix_row.write("µl")

    # Row 4: Water
    mastermix_row = row([3, 2, 1], vertical_align="center", gap="small")
    mastermix_row.write("Water")
    mastermix_row.write(f"<p style='text-align: right;'>{M_h2o1:.3f}</p>", unsafe_allow_html=True)
    mastermix_row.write("ml")

    # Divider row (converted from HTML <hr>)
    st.markdown("<hr style='margin-top: 0px; margin-bottom: 0px; border: none; border-top: 1px solid #ccc;'/>",
                unsafe_allow_html=True)

    # Row 5: Total volume (the HTML row had a background color class "color9" – you can add styling as needed)
    mastermix_row = row([3, 2, 1], vertical_align="center", gap="small")
    mastermix_row.write("<p style=' background-color: lightblue;'>Total volume</p>", unsafe_allow_html=True)
    mastermix_row.write(f"<p style='text-align: right; background-color: lightblue;'>{M_volume1:.3f}</p>", unsafe_allow_html=True)
    mastermix_row.write("<p style=' background-color: lightblue;'>ml</p>", unsafe_allow_html=True)

## -------------------
main_grid.write("")

# --- Salivary Amylase Solution ---
main_grid.write("")
with main_grid.expander("Salivary Amylase Solution", expanded=True):
    # Calculations
    finalu1 = st.session_state.finalu1
    measured1 = st.session_state.measured1
    effective1 = st.session_state.effective1
    Meffective1 = st.session_state.Meffective1

    # Calculate minimal required enzyme weight
    minimal1 = (total1 * finalu1) / measured1 if measured1 > 0 else 0.0  # mg needed per sample
    M_minimal1 = minimal1 * total_samples  # mg needed for all samples
    dissolve1 = (effective1 * amylase1) / minimal1 if minimal1 > 0 else 0.0  # ml to dissolve per sample
    M_dissolve1 = total_samples * ((Meffective1 * amylase1) / M_minimal1) if M_minimal1 > 0 else 0.0  # ml to dissolve for stock

    # Row for Product
    prod_row = row([3, 9], vertical_align="center", gap="small")
    prod_row.write("Product")
    prod_row.text_input("", key="product1", value=st.session_state.get("product1", "Sigma Amylase A1031"),
                        label_visibility="collapsed")

    # Row for Lot number
    lot_row = row([3, 9], vertical_align="center", gap="small")
    lot_row.write("Lot number")
    lot_row.text_input("", key="lot1", value=st.session_state.get("lot1", ""), label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    # Row for Final units (3-column layout)
    final_units_row = row([3, 2, 1], vertical_align="center", gap="small")
    final_units_row.write("Final units")
    final_units_row.number_input("", min_value=0.0, key="finalu1",
                                 value=st.session_state.get("finalu1", 75.0),
                                 disabled=True, label_visibility="collapsed")
    final_units_row.write("U/ml")

    # Row for Measured activity
    measured_row = row([3, 2, 1], vertical_align="center", gap="small")
    measured_row.write("Measured activity")
    measured_row.number_input("", min_value=0.0, key="measured1",
                              value=st.session_state.get("measured1", 1000.0),
                              label_visibility="collapsed")
    measured_row.write("U/mg")

    st.markdown("<br>", unsafe_allow_html=True)

    # Header row for Per sample and Stock solution values (5 columns)
    header_row = row([3, 2, 1, 2, 1], vertical_align="center", gap="small")
    header_row.write("")  # Empty first cell
    header_row.write("**Per sample**", unsafe_allow_html=True)
    header_row.write("")  # Empty third cell
    # Use the number of individual samples from session state (key "amount")
    sample_count = int(st.session_state.get("amount", 9))
    header_row.write(f"**Stock solution for {sample_count}+1 samples**", unsafe_allow_html=True)
    header_row.write("")  # Empty fifth cell

    # Row for Minimal weight out
    minimal_row = row([3, 2, 1, 2, 1], vertical_align="center", gap="small")
    minimal_row.write("Minimal weight out")
    minimal_row.number_input("wo1", min_value=0.0,
                             value=minimal1,
                             disabled=True, label_visibility="collapsed")
    minimal_row.write("mg")
    minimal_row.number_input("wo2", min_value=0.0,
                             value=M_minimal1,
                             disabled=True, label_visibility="collapsed")
    minimal_row.write("mg")

    # Row for Effective weighed
    effective_row = row([3, 2, 1, 2, 1], vertical_align="center", gap="small")
    effective_row.write("Effective weighed")
    effective_row.number_input("Effective weighed 1", min_value=0.0, key="effective1",
                               value=st.session_state.get("effective1", 1.0),
                               label_visibility="collapsed")
    effective_row.write("mg")
    effective_row.number_input("Effective weighed 2", min_value=0.0, key="Meffective1",
                               value=st.session_state.get("Meffective1", 10.0),
                               label_visibility="collapsed")
    effective_row.write("mg")

    # Row for Dissolve in water
    dissolve_row = row([3, 2, 1, 2, 1], vertical_align="center", gap="small")
    dissolve_row.write("Dissolve in water")
    dissolve_row.number_input("water1", min_value=0.0,
                              value=dissolve1,
                              format="%0.3f",
                              disabled=True, label_visibility="collapsed")
    dissolve_row.write("ml")
    dissolve_row.number_input("water2", min_value=0.0,
                              value=M_dissolve1,
                              format="%0.3f",
                              disabled=True, label_visibility="collapsed")
    dissolve_row.write("ml")

    # Display warnings based on the computed values
    warnings = []
    if measured1 < 1:
        warnings.append("⚠️ Please provide the measured activity of the amylase powder.")
    else:
        if minimal1 > effective1:
            warnings.append("⚠️ Not enough amylase weighed per sample to reach the required activity.")
        if effective1 > 0 and dissolve1 > 0 and (effective1 / dissolve1 > 10):
            warnings.append("⚠️ High enzyme concentration per sample (dissolution may be difficult).")
        if total_samples > 2:
            if M_minimal1 > Meffective1:
                warnings.append("⚠️ Not enough amylase weighed for the stock solution.")
            if Meffective1 > 0 and M_dissolve1 > 0 and (Meffective1 / M_dissolve1 > 10):
                warnings.append("⚠️ High enzyme concentration in stock solution.")

    for w in warnings:
        st.markdown(f"<span style='color:red;'>{w}</span>", unsafe_allow_html=True)

## -------------------
main_grid.divider()

# --- Gastric phase composition ---
with main_grid.expander("Gastric Phase Composition", expanded=True):

    # Determine volumes for gastric phase
    oral2 = final1  # volume entering gastric phase (ml)
    acid2 = st.session_state.acid2
    sampling2 = st.session_state.sampling2
    use_rge = st.session_state.get("use_rge", False)

    sgf2 = oral2 * 4.0 / 5.0  # Simulated Gastric Fluid volume 
    cacl2 = oral2 / 2.0  # CaCl2 volume (µL) 
    enzyme_vol = oral2 / 20.0  # Volume of pepsin solution (ml) 
    pepsin_vol = enzyme_vol
    rabbit_vol = enzyme_vol if use_rge else 0.0  # If RGE is used, it has the same volume as pepsin 

    # Water to add (ml), adjusted for whether RGE is added  
    h2o2 = oral2 - sgf2 - acid2 - (cacl2 / 1000.0) - pepsin_vol - rabbit_vol
    total2 = oral2 * 2.0  # Total gastric phase volume (ml) 
    final2 = total2 - sampling2  # Final volume after gastric sampling 

    # Save enzyme volumes in session (to display or use in next sections)
    st.session_state.pepsin2 = pepsin_vol
    st.session_state.rabbit2 = rabbit_vol

    # Row 1: Volume of oral phase
    r1 = row([3, 2, 1, 2, 1], vertical_align="center", gap="small")
    r1.write("Volume of oral phase")
    r1.number_input("oral2_input", value=oral2, disabled=True, format="%0.3f", label_visibility="collapsed")
    r1.write("ml")
    r1.number_input("Moral2_input", value=oral2, disabled=True, format="%0.3f", label_visibility="collapsed")
    r1.write("ml")

    # Row 2: Simulated gastric fluid (SGF) – 3-column layout
    r2 = row([3, 2, 1], vertical_align="center", gap="small")
    r2.write("Simulated gastric fluid (SGF)")
    r2.number_input("sgf2_input", value=sgf2, disabled=True, format="%0.3f", label_visibility="collapsed")
    r2.write("ml")

    # Row 3: 0.3 M CaCl₂ – 3-column layout
    r3 = row([3, 2, 1], vertical_align="center", gap="small")
    r3.write("0.3 M CaCl₂")
    r3.number_input("cacl2_input", value=cacl2, disabled=True, format="%0.1f", label_visibility="collapsed")
    r3.write("µl")

    # Row 4: Acid/base for pH3.0 – 3-column layout (editable)
    r4 = row([3, 2, 1], vertical_align="center", gap="small")
    r4.write("Acid/base for pH3.0")
    r4.number_input("acid2", value=acid2, key="acid2", format="%0.3f", label_visibility="collapsed")
    r4.write("ml")

    # Row 5: Water – 3-column layout
    r5 = row([3, 2, 1], vertical_align="center", gap="small")
    r5.write("Water")
    r5.number_input("h2o2_input", value=h2o2, disabled=True, format="%0.3f", label_visibility="collapsed")
    r5.write("ml")

    # Row 6: Gastric mastermix – 5-column layout; only the stock solution column is filled
    # For example, we compute gmm as the remaining volume after subtracting 2×pepsin_vol:
    gmm = oral2 - (2 * pepsin_vol)
    r6 = row([3, 2, 1, 2, 1], vertical_align="center", gap="small")
    r6.write("Gastric mastermix")
    r6.write("")  # empty cell for individual addition
    r6.write("")  # empty unit cell
    r6.number_input("gmm_input", value=gmm, disabled=True, format="%0.3f", label_visibility="collapsed")
    r6.write("ml")

    # Row 7: Rabbit gastric extract solution – 5-column layout
    r7 = row([3, 2, 1, 2, 1], vertical_align="center", gap="small")
    r7.write("Rabbit gastric extract solution")
    r7.number_input("rabbit2_input", value=rabbit_vol, disabled=True, format="%0.3f", label_visibility="collapsed")
    r7.write("ml")
    r7.number_input("Mrabbit2_input", value=rabbit_vol * total_samples, disabled=True, format="%0.3f",
                    label_visibility="collapsed")
    r7.write("ml")

    # Row 8: Pepsin solution – 5-column layout
    r8 = row([3, 2, 1, 2, 1], vertical_align="center", gap="small")
    r8.write("Pepsin solution")
    r8.number_input("pepsin2_input", value=pepsin_vol, disabled=True, format="%0.3f", label_visibility="collapsed")
    r8.write("ml")
    r8.number_input("Mpepsin2_input", value=pepsin_vol * total_samples, disabled=True, format="%0.3f",
                    label_visibility="collapsed")
    r8.write("ml")

    # Divider row
    st.markdown("<hr style='margin-top: 0px; margin-bottom: 0px; border: none; border-top: 1px solid #ccc;'/>",
                unsafe_allow_html=True)

    # Row 9: Total volume – 5-column layout
    r9 = row([3, 2, 1, 2, 1], vertical_align="center", gap="small")
    r9.write("Total volume")
    r9.number_input("total2_input", value=total2, disabled=True, format="%0.3f", label_visibility="collapsed")
    r9.write("ml")
    r9.number_input("Mtotal2_input", value=total2 * total_samples, disabled=True, format="%0.3f",
                    label_visibility="collapsed")
    r9.write("ml")

    # Divider row
    st.markdown("<hr style='margin-top: 0px; margin-bottom: 0px; border: none; border-top: 1px solid #ccc;'/>",
                unsafe_allow_html=True)

    # Row 10: Sampling volume (if any) – 5-column layout (editable)
    r10 = row([3, 2, 1, 2, 1], vertical_align="center", gap="small")
    r10.write("Sampling volume (if any)")
    r10.number_input("sampling2", value=sampling2, key="sampling2", format="%0.3f", label_visibility="collapsed")
    r10.write("ml")
    r10.number_input("Msampling2_input", value=sampling2 * total_samples, disabled=True, format="%0.3f",
                     label_visibility="collapsed")
    r10.write("ml")

    # Row 11: Final volume – 5-column layout
    r11 = row([3, 2, 1, 2, 1], vertical_align="center", gap="small")
    r11.write("Final volume")
    r11.number_input("final2_input", value=final2, disabled=True, format="%0.3f", label_visibility="collapsed")
    r11.write("ml")
    r11.number_input("Mfinal2_input", value=final2 * total_samples, disabled=True, format="%0.3f",
                     label_visibility="collapsed")
    r11.write("ml")

    # Divider row
    st.markdown("<hr style='margin-top: 0px; margin-bottom: 0px; border: none; border-top: 1px solid #ccc;'/>",
                unsafe_allow_html=True)

    # Row 12: Digestion duration – 5-column layout (fixed value: 120 min)
    r12 = row([3, 2, 1, 2, 1], vertical_align="center", gap="small")
    r12.write("Digestion duration")
    r12.number_input("duration2", value=120, disabled=True, format="%0.0f", label_visibility="collapsed")
    r12.write("min")
    r12.number_input("Mduration2", value=120, disabled=True, format="%0.0f", label_visibility="collapsed")
    r12.write("min")


    st.write(f"**Simulated gastric fluid (SGF):** {sgf2:.3f} ml")
    st.write(f"**0.3 M CaCl₂:** {cacl2:.1f} µl")
    st.write(f"**Pepsin solution:** {pepsin_vol:.3f} ml")
    st.write(f"**Rabbit gastric extract solution:** {rabbit_vol:.3f} ml")
    st.write(f"**Acid:** {acid2:.3f} ml")
    st.write(f"**Water:** {h2o2:.3f} ml")
    st.write(f"**Total gastric phase volume:** {total2:.3f} ml")
    st.write(f"**Final volume after gastric sampling:** {final2:.3f} ml")

## -------------------
# --- Gastric phase Mastermix ---
with st.expander("Gastric Mastermix", expanded=False):
    # Mastermix volumes for gastric phase (scale per-sample values by total_samples)
    M_sgf2 = sgf2 * total_samples
    M_cacl2 = cacl2 * total_samples
    M_acid2 = acid2 * total_samples
    # Water in mastermix depends on RGE usage (match formula used for h2o2 then multiply) 
    if use_rge:
        M_h2o2 = (oral2 - sgf2 - acid2 - (cacl2 / 1000.0) - pepsin_vol - rabbit_vol) * total_samples
    else:
        M_h2o2 = (oral2 - sgf2 - acid2 - (cacl2 / 1000.0) - pepsin_vol) * total_samples
    M_volume2 = (sgf2 + acid2 + (cacl2 / 1000.0) + h2o2) * total_samples  # total volume for all samples

    st.write(f"**SGF for {total_samples} samples:** {M_sgf2:.3f} ml")
    st.write(f"**0.3 M CaCl₂ for {total_samples} samples:** {M_cacl2:.1f} µl")
    st.write(f"**Acid for {total_samples} samples:** {M_acid2:.3f} ml")
    st.write(f"**Water for {total_samples} samples:** {M_h2o2:.3f} ml")
    st.write(f"**Total gastric phase volume (mastermix):** {M_volume2:.3f} ml")

## -------------------
# --- Rabbit Gastric Extract Solution (if used) ---
with st.expander("Rabbit Gastric Extract Solution", expanded=False):
    st.number_input("Final lipase activity in gastric phase (U/ml)", min_value=0.0, key="finallu2")
    st.number_input("Measured RGE lipase activity (U/mg)", min_value=0.0, key="measuredl2")
    st.number_input("Effective RGE weighed per sample (mg)", min_value=0.0, key="effectivel2")
    st.number_input("Effective RGE weighed for stock (mg)", min_value=0.0, key="Meffectivel2")

    finallu2 = st.session_state.finallu2
    measuredl2 = st.session_state.measuredl2
    effectivel2 = st.session_state.effectivel2
    Meffectivel2 = st.session_state.Meffectivel2

    minimal_l2 = (
                             total2 * finallu2) / measuredl2 if measuredl2 > 0 else 0.0  # mg RGE needed per sample 
    M_minimal_l2 = minimal_l2 * total_samples  # mg RGE needed for all samples
    dissolve_l2 = (
                              effectivel2 * rabbit_vol) / minimal_l2 if minimal_l2 > 0 else 0.0  # ml water to dissolve per sample 
    M_dissolve_l2 = (Meffectivel2 * rabbit_vol) / M_minimal_l2 if M_minimal_l2 > 0 else 0.0  # ml to dissolve for stock

    st.write(f"**Minimal RGE needed per sample:** {minimal_l2:.2f} mg")
    st.write(f"**Minimal RGE for {total_samples} samples:** {M_minimal_l2:.2f} mg")
    st.write(f"**Dissolution volume per sample:** {dissolve_l2:.3f} ml")
    st.write(f"**Dissolution volume for stock:** {M_dissolve_l2:.3f} ml")

    # Warnings for RGE solution  
    warnings = []
    if measuredl2 < 1:
        warnings.append("⚠️ Please provide the measured activity of the RGE powder.")
    else:
        if minimal_l2 > effectivel2 and effectivel2 != 0:
            warnings.append("⚠️ Not enough RGE weighed per sample to reach the required lipase units.")
        if effectivel2 > 0 and dissolve_l2 > 0 and (effectivel2 / dissolve_l2 > 250):
            warnings.append("⚠️ High RGE concentration per sample (may be difficult to dissolve).")
        if total_samples > 2:
            if M_minimal_l2 > Meffectivel2 and Meffectivel2 != 0:
                warnings.append("⚠️ Not enough RGE weighed for the stock solution.")
            if Meffectivel2 > 0 and M_dissolve_l2 > 0 and (Meffectivel2 / M_dissolve_l2 > 250):
                warnings.append("⚠️ High RGE concentration in stock solution (dissolution may be difficult).")
    for w in warnings:
        st.markdown(f"<span style='color:red;'>{w}</span>", unsafe_allow_html=True)

## -------------------
# --- Pepsin Solution ---
with st.expander("Pepsin Solution", expanded=False):
    st.number_input("Final pepsin activity in gastric phase (U/ml)", min_value=0.0, key="finalpu2")
    st.number_input("Measured pepsin powder activity (U/mg)", min_value=0.0, key="measuredp2")
    st.number_input("Measured pepsin activity of RGE (U/mg)", min_value=0.0, key="measuredlp2")
    st.number_input("Effective pepsin weighed per sample (mg)", min_value=0.0, key="effectivep2")
    st.number_input("Effective pepsin weighed for stock (mg)", min_value=0.0, key="Meffectivep2")

    finalpu2 = st.session_state.finalpu2
    measuredp2 = st.session_state.measuredp2
    measuredlp2 = st.session_state.measuredlp2
    effectivep2 = st.session_state.effectivep2
    Meffectivep2 = st.session_state.Meffectivep2

    # Calculate minimal pepsin needed
    if measuredp2 > 0:
        if use_rge and measuredlp2 > 0:
            # Subtract RGE's protease contribution from requirement 
            minimal_p2 = ((total2 * finalpu2) - (measuredlp2 * minimal_l2)) / measuredp2
        else:
            minimal_p2 = (total2 * finalpu2) / measuredp2
    else:
        minimal_p2 = 0.0
    M_minimal_p2 = minimal_p2 * total_samples

    dissolve_p2 = (
                              effectivep2 * pepsin_vol) / minimal_p2 if minimal_p2 > 0 else 0.0  # ml water per sample 
    M_dissolve_p2 = (Meffectivep2 * pepsin_vol) / M_minimal_p2 if M_minimal_p2 > 0 else 0.0

    st.write(f"**Minimal pepsin needed per sample:** {minimal_p2:.2f} mg")
    st.write(f"**Minimal pepsin for {total_samples} samples:** {M_minimal_p2:.2f} mg")
    st.write(f"**Dissolution volume per sample:** {dissolve_p2:.3f} ml")
    st.write(f"**Dissolution volume for stock:** {M_dissolve_p2:.3f} ml")

    warnings = []
    if measuredp2 < 1:
        warnings.append("⚠️ Please provide the measured activity of the pepsin powder.")
    else:
        if minimal_p2 > effectivep2:
            warnings.append("⚠️ Not enough pepsin weighed per sample to reach the required activity.")
        if effectivep2 > 0 and dissolve_p2 > 0 and (effectivep2 / dissolve_p2 > 50):
            warnings.append("⚠️ High pepsin concentration per sample (difficult to dissolve).")
        if total_samples > 2:
            if M_minimal_p2 > Meffectivep2:
                warnings.append("⚠️ Not enough pepsin weighed for the stock solution.")
            if Meffectivep2 > 0 and M_dissolve_p2 > 0 and (Meffectivep2 / M_dissolve_p2 > 50):
                warnings.append("⚠️ High pepsin concentration in stock solution (dissolution may be difficult).")
    for w in warnings:
        st.markdown(f"<span style='color:red;'>{w}</span>", unsafe_allow_html=True)

## -------------------
# --- Intestinal phase composition (with pancreatin) ---
if not use_individual:
    with st.expander("Intestinal Phase Composition (Pancreatin)", expanded=True):
        st.number_input("Base (e.g. NaOH) added (ml)", min_value=0.0, key="base3")
        st.number_input("Sampling volume after intestinal phase (ml)", min_value=0.0, key="sampling3")

        gastric3 = final2  # volume entering intestinal phase (ml)
        base3 = st.session_state.base3
        sampling3 = st.session_state.sampling3

        cacl3 = gastric3 * 2.0  # CaCl2 volume (µL) 
        pancreatin3 = gastric3 / 4.0  # Pancreatin solution volume (ml) 
        bile3 = gastric3 / 8.0  # Bile solution volume (ml) 
        sif3 = gastric3 * 4.0 / 5.0 - pancreatin3 - bile3  # SIF volume (ml) 
        imm = gastric3  # intestinal phase initial mix volume (same as gastric3)
        h2o3 = gastric3 - sif3 - pancreatin3 - bile3 - base3 - (
                    cacl3 / 1000.0)  # Water (ml) 
        total3 = gastric3 * 2.0  # total intestinal volume (ml) 
        final3 = total3 - sampling3  # final volume after sampling 

        st.write(f"**Simulated intestinal fluid (SIF):** {sif3:.3f} ml")
        st.write(f"**0.3 M CaCl₂:** {cacl3:.1f} µl")
        st.write(f"**Pancreatin solution:** {pancreatin3:.3f} ml")
        st.write(f"**Bile solution:** {bile3:.3f} ml")
        st.write(f"**Base (NaOH):** {base3:.3f} ml")
        st.write(f"**Water:** {h2o3:.3f} ml")
        st.write(f"**Total intestinal volume:** {total3:.3f} ml")
        st.write(f"**Final volume after intestinal sampling:** {final3:.3f} ml")

## -------------------
# --- Intestinal Mastermix (Pancreatin) ---
if not use_individual:
    with st.expander("Intestinal Mastermix (Pancreatin)", expanded=False):
        M_sif3 = sif3 * total_samples
        M_cacl3 = cacl3 * total_samples
        M_base3 = base3 * total_samples
        M_h2o3 = h2o3 * total_samples
        M_pancreatin3 = pancreatin3 * total_samples
        M_bile3 = bile3 * total_samples
        M_volume3 = imm * total_samples

        st.write(f"**SIF for {total_samples} samples:** {M_sif3:.3f} ml")
        st.write(f"**0.3 M CaCl₂ for {total_samples} samples:** {M_cacl3:.1f} µl")
        st.write(f"**Base for {total_samples} samples:** {M_base3:.3f} ml")
        st.write(f"**Water for {total_samples} samples:** {M_h2o3:.3f} ml")
        st.write(f"**Pancreatin for {total_samples} samples:** {M_pancreatin3:.3f} ml")
        st.write(f"**Bile for {total_samples} samples:** {M_bile3:.3f} ml")
        st.write(f"**Total intestinal volume (mastermix):** {M_volume3:.3f} ml")

## -------------------
# --- Pancreatin Solution (for intestinal phase) ---
if not use_individual:
    with st.expander("Pancreatin Solution", expanded=False):
        st.number_input("Final pancreatin (trypsin) activity (U/ml)", min_value=0.0, key="finalu3a")
        st.number_input("Measured pancreatin activity (U/mg)", min_value=0.0, key="measured3a")
        st.number_input("Effective pancreatin weighed per sample (mg)", min_value=0.0, key="effective3a")
        st.number_input("Effective pancreatin weighed for stock (mg)", min_value=0.0, key="Meffective3a")

        finalu3a = st.session_state.finalu3a
        measured3a = st.session_state.measured3a
        effective3a = st.session_state.effective3a
        Meffective3a = st.session_state.Meffective3a

        minimal3a = (
                                total3 * finalu3a) / measured3a if measured3a > 0 else 0.0  # mg needed per sample 
        M_minimal3a = minimal3a * total_samples
        dissolve3a = (
                                 effective3a * pancreatin3) / minimal3a if minimal3a > 0 else 0.0  # ml per sample 
        M_dissolve3a = (Meffective3a * pancreatin3) / M_minimal3a if M_minimal3a > 0 else 0.0

        st.write(f"**Minimal pancreatin needed per sample:** {minimal3a:.2f} mg")
        st.write(f"**Minimal pancreatin for {total_samples} samples:** {M_minimal3a:.2f} mg")
        st.write(f"**Dissolution volume per sample:** {dissolve3a:.3f} ml")
        st.write(f"**Dissolution volume for stock:** {M_dissolve3a:.3f} ml")

        warnings = []
        if measured3a < 1:
            warnings.append("⚠️ Please provide the measured activity of the pancreatin powder.")
        else:
            if minimal3a > effective3a:
                warnings.append("⚠️ Not enough pancreatin weighed per sample.")
            if effective3a > 0 and dissolve3a > 0 and (effective3a / dissolve3a > 250):
                warnings.append("⚠️ High pancreatin concentration per sample (may be hard to dissolve).")
            if total_samples > 2:
                if M_minimal3a > Meffective3a:
                    warnings.append("⚠️ Not enough pancreatin weighed for the stock solution.")
                if Meffective3a > 0 and M_dissolve3a > 0 and (Meffective3a / M_dissolve3a > 250):
                    warnings.append("⚠️ High pancreatin concentration in stock solution.")
        for w in warnings:
            st.markdown(f"<span style='color:red;'>{w}</span>", unsafe_allow_html=True)

## -------------------
# --- Bile Solution (for pancreatin mode) ---
if not use_individual:
    with st.expander("Bile Solution", expanded=False):
        st.number_input("Final bile concentration in intestinal phase (mM)", min_value=0.0, key="finalu3b")
        st.number_input("Measured bile content (mmol per g)", min_value=0.0, key="measured3b")
        st.number_input("Effective bile weighed per sample (mg)", min_value=0.0, key="effective3b")
        st.number_input("Effective bile weighed for stock (mg)", min_value=0.0, key="Meffective3b")

        finalu3b = st.session_state.finalu3b
        measured3b = st.session_state.measured3b
        effective3b = st.session_state.effective3b
        Meffective3b = st.session_state.Meffective3b

        minimal3b = (
                                total3 * finalu3b) / measured3b if measured3b > 0 else 0.0  # mg needed per sample 
        M_minimal3b = minimal3b * total_samples
        dissolve3b = (
                                 effective3b * bile3) / minimal3b if minimal3b > 0 else 0.0  # ml per sample 
        M_dissolve3b = (Meffective3b * bile3) / M_minimal3b if M_minimal3b > 0 else 0.0

        st.write(f"**Minimal bile needed per sample:** {minimal3b:.2f} mg")
        st.write(f"**Minimal bile for {total_samples} samples:** {M_minimal3b:.2f} mg")
        st.write(f"**Dissolution volume per sample:** {dissolve3b:.3f} ml")
        st.write(f"**Dissolution volume for stock:** {M_dissolve3b:.3f} ml")

        warnings = []
        if measured3b < 1:
            warnings.append("⚠️ Please provide the measured activity of the bile powder.")
        else:
            if minimal3b > effective3b:
                warnings.append("⚠️ Not enough bile weighed per sample.")
            if effective3b > 0 and dissolve3b > 0 and (effective3b / dissolve3b > 500):
                warnings.append("⚠️ High bile concentration per sample (may be hard to dissolve).")
            if total_samples > 2:
                if M_minimal3b > Meffective3b:
                    warnings.append("⚠️ Not enough bile weighed for the stock solution.")
                if Meffective3b > 0 and M_dissolve3b > 0 and (Meffective3b / M_dissolve3b > 500):
                    warnings.append("⚠️ High bile concentration in stock solution.")
        for w in warnings:
            st.markdown(f"<span style='color:red;'>{w}</span>", unsafe_allow_html=True)

## -------------------
# --- Intestinal phase composition (with individual enzymes) ---
if use_individual:
    with st.expander("Intestinal Phase Composition (Individual Enzymes)", expanded=True):
        st.number_input("Base (e.g. NaOH) added (ml)", min_value=0.0, key="base4")
        st.number_input("Sampling volume after intestinal phase (ml)", min_value=0.0, key="sampling4")

        gastric4 = final2  # volume entering intestinal phase (ml)
        base4 = st.session_state.base4
        sampling4 = st.session_state.sampling4

        # Volumes for individual enzyme solutions  
        trypsin4 = gastric4 / 20.0
        chymotrypsin4 = gastric4 / 20.0
        lipase4 = gastric4 / 20.0
        colipase4 = gastric4 / 20.0
        amylase4 = gastric4 / 20.0
        bile4 = gastric4 / 8.0
        cacl4 = gastric4 * 2.0  # µL
        sif4 = gastric4 * 4.0 / 5.0 - (
                    trypsin4 + chymotrypsin4 + lipase4 + colipase4 + amylase4 + bile4)  # 
        inm = gastric4  # initial intestinal mix (same as gastric4)
        h2o4 = gastric4 - sif4 - (cacl4 / 1000.0) - base4 - (
                    trypsin4 + chymotrypsin4 + lipase4 + colipase4 + amylase4 + bile4)  # 
        total4 = gastric4 * 2.0
        final4 = total4 - sampling4

        st.write(f"**Simulated intestinal fluid (SIF):** {sif4:.3f} ml")
        st.write(f"**0.3 M CaCl₂:** {cacl4:.1f} µl")
        st.write(f"**Trypsin solution:** {trypsin4:.3f} ml")
        st.write(f"**Chymotrypsin solution:** {chymotrypsin4:.3f} ml")
        st.write(f"**Lipase solution:** {lipase4:.3f} ml")
        st.write(f"**Colipase solution:** {colipase4:.3f} ml")
        st.write(f"**Amylase solution (pancreatic):** {amylase4:.3f} ml")
        st.write(f"**Bile solution:** {bile4:.3f} ml")
        st.write(f"**Base (NaOH):** {base4:.3f} ml")
        st.write(f"**Water:** {h2o4:.3f} ml")
        st.write(f"**Total intestinal volume:** {total4:.3f} ml")
        st.write(f"**Final volume after intestinal sampling:** {final4:.3f} ml")

## -------------------
# --- Intestinal Mastermix (Individual Enzymes) ---
if use_individual:
    with st.expander("Intestinal Mastermix (Individual Enzymes)", expanded=False):
        M_sif4 = sif4 * total_samples
        M_trypsin4 = trypsin4 * total_samples
        M_chymotrypsin4 = chymotrypsin4 * total_samples
        M_lipase4 = lipase4 * total_samples
        M_colipase4 = colipase4 * total_samples
        M_amylase4 = amylase4 * total_samples
        M_bile4 = bile4 * total_samples
        M_cacl4 = cacl4 * total_samples
        M_base4 = base4 * total_samples
        M_h2o4 = h2o4 * total_samples
        M_volume4 = inm * total_samples

        st.write(f"**SIF for {total_samples} samples:** {M_sif4:.3f} ml")
        st.write(f"**0.3 M CaCl₂ for {total_samples} samples:** {M_cacl4:.1f} µl")
        st.write(f"**Trypsin for {total_samples} samples:** {M_trypsin4:.3f} ml")
        st.write(f"**Chymotrypsin for {total_samples} samples:** {M_chymotrypsin4:.3f} ml")
        st.write(f"**Lipase for {total_samples} samples:** {M_lipase4:.3f} ml")
        st.write(f"**Colipase for {total_samples} samples:** {M_colipase4:.3f} ml")
        st.write(f"**Amylase (pancreatic) for {total_samples} samples:** {M_amylase4:.3f} ml")
        st.write(f"**Bile for {total_samples} samples:** {M_bile4:.3f} ml")
        st.write(f"**Base for {total_samples} samples:** {M_base4:.3f} ml")
        st.write(f"**Water for {total_samples} samples:** {M_h2o4:.3f} ml")
        st.write(f"**Total intestinal volume (mastermix):** {M_volume4:.3f} ml")

## -------------------
# --- Trypsin Solution (intestinal individual) ---
if use_individual:
    with st.expander("Trypsin Solution", expanded=False):
        st.number_input("Final trypsin activity (U/ml)", min_value=0.0, key="finalu4a")
        st.number_input("Measured trypsin activity (U/mg)", min_value=0.0, key="measured4a")
        st.number_input("Effective trypsin weighed per sample (mg)", min_value=0.0, key="effective4a")
        st.number_input("Effective trypsin weighed for stock (mg)", min_value=0.0, key="Meffective4a")

        finalu4a = st.session_state.finalu4a
        measured4a = st.session_state.measured4a
        effective4a = st.session_state.effective4a
        Meffective4a = st.session_state.Meffective4a

        minimal4a = (
                                total4 * finalu4a) / measured4a if measured4a > 0 else 0.0  # mg needed per sample 
        M_minimal4a = minimal4a * total_samples
        dissolve4a = (
                                 effective4a * trypsin4) / minimal4a if minimal4a > 0 else 0.0  # ml per sample 
        M_dissolve4a = (Meffective4a * trypsin4) / M_minimal4a if M_minimal4a > 0 else 0.0

        st.write(f"**Minimal trypsin needed per sample:** {minimal4a:.2f} mg")
        st.write(f"**Minimal trypsin for {total_samples} samples:** {M_minimal4a:.2f} mg")
        st.write(f"**Dissolution volume per sample:** {dissolve4a:.3f} ml")
        st.write(f"**Dissolution volume for stock:** {M_dissolve4a:.3f} ml")

        warnings = []
        if measured4a < 1:
            warnings.append("⚠️ Please provide measured activity of trypsin powder.")
        else:
            if minimal4a > effective4a:
                warnings.append("⚠️ Not enough trypsin weighed per sample.")
            if effective4a > 0 and dissolve4a > 0 and (effective4a / dissolve4a > 250):
                warnings.append("⚠️ High trypsin concentration per sample (may be hard to dissolve).")
            if total_samples > 2:
                if M_minimal4a > Meffective4a:
                    warnings.append("⚠️ Not enough trypsin weighed for stock solution.")
                if Meffective4a > 0 and M_dissolve4a > 0 and (Meffective4a / M_dissolve4a > 250):
                    warnings.append("⚠️ High trypsin concentration in stock solution.")
        for w in warnings:
            st.markdown(f"<span style='color:red;'>{w}</span>", unsafe_allow_html=True)

    # --- Chymotrypsin Solution ---
    with st.expander("Chymotrypsin Solution", expanded=False):
        st.number_input("Final chymotrypsin activity (U/ml)", min_value=0.0, key="finalu4b")
        st.number_input("Measured chymotrypsin activity (U/mg)", min_value=0.0, key="measured4b")
        st.number_input("Effective chymotrypsin weighed per sample (mg)", min_value=0.0, key="effective4b")
        st.number_input("Effective chymotrypsin weighed for stock (mg)", min_value=0.0, key="Meffective4b")

        finalu4b = st.session_state.finalu4b
        measured4b = st.session_state.measured4b
        effective4b = st.session_state.effective4b
        Meffective4b = st.session_state.Meffective4b

        minimal4b = (
                                total4 * finalu4b) / measured4b if measured4b > 0 else 0.0  # mg per sample 
        M_minimal4b = minimal4b * total_samples
        dissolve4b = (
                                 effective4b * chymotrypsin4) / minimal4b if minimal4b > 0 else 0.0  # ml per sample 
        M_dissolve4b = (Meffective4b * chymotrypsin4) / M_minimal4b if M_minimal4b > 0 else 0.0

        st.write(f"**Minimal chymotrypsin needed per sample:** {minimal4b:.2f} mg")
        st.write(f"**Minimal chymotrypsin for {total_samples} samples:** {M_minimal4b:.2f} mg")
        st.write(f"**Dissolution volume per sample:** {dissolve4b:.3f} ml")
        st.write(f"**Dissolution volume for stock:** {M_dissolve4b:.3f} ml")

        warnings = []
        if measured4b < 1:
            warnings.append("⚠️ Please provide measured activity of chymotrypsin powder.")
        else:
            if minimal4b > effective4b:
                warnings.append("⚠️ Not enough chymotrypsin weighed per sample.")
            if effective4b > 0 and dissolve4b > 0 and (effective4b / dissolve4b > 250):
                warnings.append("⚠️ High chymotrypsin concentration per sample.")
            if total_samples > 2:
                if M_minimal4b > Meffective4b:
                    warnings.append("⚠️ Not enough chymotrypsin weighed for stock solution.")
                if Meffective4b > 0 and M_dissolve4b > 0 and (Meffective4b / M_dissolve4b > 250):
                    warnings.append("⚠️ High chymotrypsin concentration in stock solution.")
        for w in warnings:
            st.markdown(f"<span style='color:red;'>{w}</span>", unsafe_allow_html=True)

    # --- Lipase Solution ---
    with st.expander("Lipase Solution", expanded=False):
        st.number_input("Final lipase activity (U/ml)", min_value=0.0, key="finalu4c")
        st.number_input("Measured lipase activity (U/mg)", min_value=0.0, key="measured4c")
        st.number_input("Effective lipase weighed per sample (mg)", min_value=0.0, key="effective4c")
        st.number_input("Effective lipase weighed for stock (mg)", min_value=0.0, key="Meffective4c")

        finalu4c = st.session_state.finalu4c
        measured4c = st.session_state.measured4c
        effective4c = st.session_state.effective4c
        Meffective4c = st.session_state.Meffective4c

        minimal4c = (
                                total4 * finalu4c) / measured4c if measured4c > 0 else 0.0  # mg per sample 
        M_minimal4c = minimal4c * total_samples
        dissolve4c = (
                                 effective4c * lipase4) / minimal4c if minimal4c > 0 else 0.0  # ml per sample 
        M_dissolve4c = (Meffective4c * lipase4) / M_minimal4c if M_minimal4c > 0 else 0.0

        st.write(f"**Minimal lipase needed per sample:** {minimal4c:.2f} mg")
        st.write(f"**Minimal lipase for {total_samples} samples:** {M_minimal4c:.2f} mg")
        st.write(f"**Dissolution volume per sample:** {dissolve4c:.3f} ml")
        st.write(f"**Dissolution volume for stock:** {M_dissolve4c:.3f} ml")

        warnings = []
        if measured4c < 1:
            warnings.append("⚠️ Please provide measured activity of lipase powder.")
        else:
            if minimal4c > effective4c:
                warnings.append("⚠️ Not enough lipase weighed per sample.")
            if effective4c > 0 and dissolve4c > 0 and (effective4c / dissolve4c > 250):
                warnings.append("⚠️ High lipase concentration per sample.")
            if total_samples > 2:
                if M_minimal4c > Meffective4c:
                    warnings.append("⚠️ Not enough lipase weighed for stock solution.")
                if Meffective4c > 0 and M_dissolve4c > 0 and (Meffective4c / M_dissolve4c > 250):
                    warnings.append("⚠️ High lipase concentration in stock solution.")
        for w in warnings:
            st.markdown(f"<span style='color:red;'>{w}</span>", unsafe_allow_html=True)

    # --- Colipase Solution ---
    with st.expander("Colipase Solution", expanded=False):
        st.number_input("Measured colipase activity (U/mg)", min_value=0.0,
                        key="finalu4d")  # finalu4d holds measured colipase activity 
        st.number_input("Effective colipase weighed per sample (mg)", min_value=0.0, key="effective4d")
        st.number_input("Effective colipase weighed for stock (mg)", min_value=0.0, key="Meffective4d")

        finalu4d = st.session_state.finalu4d  # Note: finalu4d is actually measured colipase U/mg
        effective4d = st.session_state.effective4d
        Meffective4d = st.session_state.Meffective4d

        minimal4d = (
                                total4 * finalu4c * 0.4) / finalu4d if finalu4d > 0 else 0.0  # mg per sample 
        M_minimal4d = minimal4d * total_samples
        dissolve4d = (
                                 effective4d * colipase4) / minimal4d if minimal4d > 0 else 0.0  # ml per sample 
        M_dissolve4d = (Meffective4d * colipase4) / M_minimal4d if M_minimal4d > 0 else 0.0

        st.write(f"**Minimal colipase needed per sample:** {minimal4d:.2f} mg")
        st.write(f"**Minimal colipase for {total_samples} samples:** {M_minimal4d:.2f} mg")
        st.write(f"**Dissolution volume per sample:** {dissolve4d:.3f} ml")
        st.write(f"**Dissolution volume for stock:** {M_dissolve4d:.3f} ml")

        warnings = []
        # Colipase measured activity must be provided (no default given)
        if finalu4d < 1:
            warnings.append("⚠️ Please provide the measured activity of the colipase (U/mg).")
        if minimal4d > effective4d:
            warnings.append("⚠️ Not enough colipase weighed per sample.")
        if effective4d > 0 and dissolve4d > 0 and (effective4d / dissolve4d > 250):
            warnings.append("⚠️ High colipase concentration per sample.")
        if total_samples > 2:
            if M_minimal4d > Meffective4d:
                warnings.append("⚠️ Not enough colipase weighed for stock solution.")
            if Meffective4d > 0 and M_dissolve4d > 0 and (Meffective4d / M_dissolve4d > 250):
                warnings.append("⚠️ High colipase concentration in stock solution.")
        for w in warnings:
            st.markdown(f"<span style='color:red;'>{w}</span>", unsafe_allow_html=True)

    # --- Amylase Solution (pancreatic, individual mode) ---
    with st.expander("Pancreatic Amylase Solution", expanded=False):
        st.number_input("Final pancreatic amylase activity (U/ml)", min_value=0.0, key="finalu4e")
        st.number_input("Measured pancreatic amylase activity (U/mg)", min_value=0.0, key="measured4e")
        st.number_input("Effective pancreatic amylase weighed per sample (mg)", min_value=0.0, key="effective4e")
        st.number_input("Effective pancreatic amylase weighed for stock (mg)", min_value=0.0, key="Meffective4e")

        finalu4e = st.session_state.finalu4e
        measured4e = st.session_state.measured4e
        effective4e = st.session_state.effective4e
        Meffective4e = st.session_state.Meffective4e

        minimal4e = (
                                total4 * finalu4e) / measured4e if measured4e > 0 else 0.0  # mg per sample 
        M_minimal4e = minimal4e * total_samples
        dissolve4e = (
                                 effective4e * amylase4) / minimal4e if minimal4e > 0 else 0.0  # ml per sample 
        M_dissolve4e = (Meffective4e * amylase4) / M_minimal4e if M_minimal4e > 0 else 0.0

        st.write(f"**Minimal pancreatic amylase needed per sample:** {minimal4e:.2f} mg")
        st.write(f"**Minimal amylase for {total_samples} samples:** {M_minimal4e:.2f} mg")
        st.write(f"**Dissolution volume per sample:** {dissolve4e:.3f} ml")
        st.write(f"**Dissolution volume for stock:** {M_dissolve4e:.3f} ml")

        warnings = []
        if measured4e < 1:
            warnings.append("⚠️ Please provide measured activity of pancreatic amylase powder.")
        else:
            if minimal4e > effective4e:
                warnings.append("⚠️ Not enough pancreatic amylase weighed per sample.")
            if effective4e > 0 and dissolve4e > 0 and (effective4e / dissolve4e > 250):
                warnings.append("⚠️ High amylase concentration per sample.")
            if total_samples > 2:
                if M_minimal4e > Meffective4e:
                    warnings.append("⚠️ Not enough amylase weighed for stock solution.")
                if Meffective4e > 0 and M_dissolve4e > 0 and (Meffective4e / M_dissolve4e > 250):
                    warnings.append("⚠️ High amylase concentration in stock solution.")
        for w in warnings:
            st.markdown(f"<span style='color:red;'>{w}</span>", unsafe_allow_html=True)

    # --- Bile Solution (individual mode) ---
    with st.expander("Bile Solution (Intestinal Individual)", expanded=False):
        st.number_input("Final bile concentration (mM)", min_value=0.0, key="finalu4f")
        st.number_input("Measured bile content (mmol/g)", min_value=0.0, key="measured4f")
        st.number_input("Effective bile weighed per sample (mg)", min_value=0.0, key="effective4f")
        st.number_input("Effective bile weighed for stock (mg)", min_value=0.0, key="Meffective4f")

        finalu4f = st.session_state.finalu4f
        measured4f = st.session_state.measured4f
        effective4f = st.session_state.effective4f
        Meffective4f = st.session_state.Meffective4f

        minimal4f = (
                                total4 * finalu4f) / measured4f if measured4f > 0 else 0.0  # mg per sample 
        M_minimal4f = minimal4f * total_samples
        dissolve4f = (
                                 effective4f * bile4) / minimal4f if minimal4f > 0 else 0.0  # ml per sample 
        M_dissolve4f = (Meffective4f * bile4) / M_minimal4f if M_minimal4f > 0 else 0.0

        st.write(f"**Minimal bile needed per sample:** {minimal4f:.2f} mg")
        st.write(f"**Minimal bile for {total_samples} samples:** {M_minimal4f:.2f} mg")
        st.write(f"**Dissolution volume per sample:** {dissolve4f:.3f} ml")
        st.write(f"**Dissolution volume for stock:** {M_dissolve4f:.3f} ml")

        warnings = []
        if measured4f < 1:
            warnings.append("⚠️ Please provide measured activity of bile powder.")
        else:
            if minimal4f > effective4f:
                warnings.append("⚠️ Not enough bile weighed per sample.")
            if effective4f > 0 and dissolve4f > 0 and (effective4f / dissolve4f > 500):
                warnings.append("⚠️ High bile concentration per sample.")
            if total_samples > 2:
                if M_minimal4f > Meffective4f:
                    warnings.append("⚠️ Not enough bile weighed for stock solution.")
                if Meffective4f > 0 and M_dissolve4f > 0 and (Meffective4f / M_dissolve4f > 500):
                    warnings.append("⚠️ High bile concentration in stock solution.")
        for w in warnings:
            st.markdown(f"<span style='color:red;'>{w}</span>", unsafe_allow_html=True)

## -------------------

## -------------------