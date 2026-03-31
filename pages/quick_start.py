import streamlit as st
import pandas as pd

st.set_page_config(layout="centered")

# ── Title & intro ────────────────────────────────────────────────────────────
st.title(":material/rocket_launch: Quick Start Protocol")

st.markdown("""
This is a condensed bench-side reference for running the full INFOGEST 2.0
*in vitro* digestion protocol.

↳ **Follow these steps sequentially during your experiment day.
All volumes and enzyme amounts must be confirmed in the INFOGEST 2.0 Calculator.**
""")

st.page_link(
    "pages/dashboard.py",
    label=":red-background[**Open the INFOGEST 2.0 Calculator → Dashboard**]",
    icon=":material/dashboard:",
)

st.write("---")

# ── Section 1: Preparations ──────────────────────────────────────────────────
st.header("1. :material/checklist: Preparations")

with st.container(border=True):
    st.markdown("##### 🧊 Equipment & Environment")
    st.markdown("""
1. Fill a Styrofoam box with crushed ice for enzyme and sample preservation.
2. Turn on the water bath, set the temperature to **37 °C**, and press **Start**.
3. Connect the magnetic stirrer and insert a stir bar into each sample tube.
   > During pH measurements and adjustments, position the stirrer directly beneath
   > the tube being titrated to maintain consistent mixing.
""")

with st.container(border=True):
    st.markdown("##### 🧪 Solutions & Reagents")
    st.markdown("""
4. Retrieve all simulated digestive solutions (**SSF, SGF, SIF**) and **CaCl₂**
   from the refrigerator in the algae corner.
5. Refill the MilliQ water supply from the Chem lab.
6. Warm up the **pH buffers** and the **simulated digestive fluids** in the water bath.
7. Insert the temperature sensor of the pH meter into a water-filled tube and seal
   the opening with Parafilm.
""")

with st.container(border=True):
    st.markdown("##### ⚙️ Calibration & Titrator Setup")
    st.markdown("""
8. To perform automatic titration with the **Ti-Touch Automatic Titrator**, follow
   the printed instructions in the plastic lab. Use **1 M HCl** and **1 M NaOH**
   and complete the initialization procedure as described.
9. Calibrate the pH meter using calibration solutions from the Chem lab.
   Check the brand (**Hamilton** or **Metrohm**) and select the corresponding
   profile on the device before calibrating.
10. Create a new titration method or load an existing one, following the
    instrument's printed instructions.
""")

with st.container(border=True):
    st.markdown("##### 🔬 Calculator & Enzyme Preparation")
    st.markdown("""
11. In the **INFOGEST 2.0 Calculator**, specify the number of samples to process.
    Verify that the enzyme lot number, activity, and purity match those in the
    calculator.
12. Weigh **RGE** or **Pepsin** and extra lipase according to the calculator
13. Dissolve the pre-weighed **RGE** and **Lipase** separately in the volume of
    MilliQ water specified in the enzyme preparation section of the calculator and place them on
    ice immediately.
""")
    st.info(
        "If the weighed amounts differ from target, enter the actual weight in the "
        "INFOGEST 2.0 Calculator to obtain the corrected MilliQ dissolution volume."
    )

st.write("---")

# ── Section 2: Oral Digestion ────────────────────────────────────────────────
st.header("2. :material/water_drop: Oral Digestion")
st.caption("⏱ Duration: 2 minutes")

st.markdown("""
1. Dispense to each sample the volumes of **SSF**, **CaCl₂**, and **MilliQ water**
   as indicated by the INFOGEST 2.0 Calculator.
2. Weigh the required amount of porcine **Amylase** and dissolve it in the volume
   of MilliQ water indicated in the enzyme preparation section of the calculator.
3. Dispense to each sample the volume of porcine **Amylase** as indicated by the
   calculator.
4. Mix thoroughly by vortexing to obtain a homogeneous mass. Turn the tube upside
   down to avoid bolus formation. Keep tubes closed to prevent evaporation.
5. Incubate the samples for **2 minutes**.
""")

st.warning(
    "**Microalgae samples:** Skip step 3 — do not add Amylase.",
    icon=":material/eco:"
)

st.write("---")

# ── Section 3: Gastric Digestion ─────────────────────────────────────────────
st.header("3. :material/science: Gastric Digestion")
st.caption("⏱ Duration: 2 hours")

st.markdown("""
1. Dispense to each sample the volumes of **SGF**, **CaCl₂**, and **MilliQ water**
   as indicated by the INFOGEST 2.0 Calculator.
2. Measure the initial pH of the samples. Adjust to **pH 3.0 ± 0.2** with the
   automatic titrator. Record the initial pH, volume of titrant added, and final
   pH reached.
3. Dispense to each sample the volumes of prepared **RGE** or **Pepsin** and ** extra Lipase** solution as
   indicated by the calculator.
4. **Start the timer for a 2-hour gastric incubation.**
""")

st.warning(
    "**Microalgae samples:** Do not add Lipase. Select **\"RGE only\"** in the "
    "enzyme preparation section of the calculator.",
    icon=":material/eco:"
)

with st.container(border=True):
    st.markdown("##### ⏰ Timed Tasks During Gastric Incubation")
    st.markdown("""
**At 25-30 minutes:**
- Re-adjust the pH to **3.0 ± 0.2**. Record the initial pH, volume of titrant
  added, and final pH reached.
- Accounting for the titrant volume added during *both* pH adjustments to pH 3,
  add MilliQ water according to the INFOGEST 2.0 Calculator.

**At 90 minutes:**
- Pre-weigh **Pancreatin** and **Bile** according to the enzyme preparation
  section of the calculator.
- Dissolve the Bile in the volume of **SIF** specified in the calculator,
  homogenise well, and pre-warm in the water bath.
- Keep Pancreatin on ice until the intestinal phase.
""")

st.success(
    "**After 2 hours of gastric incubation** → proceed immediately to "
    "Intestinal Digestion below.",
    icon=":material/check_circle:"
)

st.write("---")

# ── Section 4: Intestinal Digestion ──────────────────────────────────────────
st.header("4. :material/biotech: Intestinal Digestion")
st.caption("⏱ Duration: 2 hours")

st.markdown("""
1. Dispense to each sample the volumes of **SIF**, **CaCl₂**, and **MilliQ water**
   as indicated by the INFOGEST 2.0 Calculator.
2. Measure the initial pH of the samples. Adjust to **pH 7.0 ± 0.2** with the
   automatic titrator. Record the initial pH, volume of titrant added, and final
   pH reached.
3. Dissolve the pre-weighed **Pancreatin** in the volume of **SIF** specified in
   the enzyme preparation section of the calculator.
""")

with st.container(border=True):
    st.markdown("##### 🔊 Pancreatin Processing (Chem Lab)")
    st.markdown("""
- **Sonicate** for 5 minutes: frequency = **80**, power = **100**, temperature = **20 °C**
- **Centrifuge** at **2,000 × g** for **5 minutes**
- Use the **supernatant** in the next step.
""")

st.markdown("""
4. Dispense to each sample the volumes of pre-warmed **Bile solution** and
   **Pancreatin supernatant** as indicated by the INFOGEST 2.0 Calculator.
5. **Start the timer for a 2-hour intestinal incubation.**
""")

with st.container(border=True):
    st.markdown("##### ⏰ Timed Tasks During Intestinal Incubation")
    st.markdown("""
**At 25 minutes:**
- Re-adjust the pH to **7.0 ± 0.2**. Record the initial pH, volume of titrant
  added, and final pH reached.
- Accounting for the titrant volume added during *both* pH adjustments to pH 7,
  add MilliQ water according to the INFOGEST 2.0 Calculator.

**During incubation:**
- Pre-label containers for full digest, supernatant, and pellet fractions.
- Follow the **Shutdown Procedure** of the Metrohm 916 Ti-Touch Automatic Titrator.
""")

st.write("---")

# ── Section 5: Enzyme Inactivation ───────────────────────────────────────────
st.header("5. :material/whatshot: Enzyme Inactivation")

st.warning(
    "**Microalgae samples:** Skip this entire section. Proceed directly to "
    "Centrifugation.",
    icon=":material/eco:"
)

st.markdown("""
1. Set the water bath in Room **D11.1-3** (Patrick's lab) to **85 °C**.
   Allow approximately 30 minutes to stabilise.
2. Verify the temperature using the pH meter probe from the Chem lab.
3. Place food samples in the water bath for **15 minutes**, then transfer
   immediately onto ice.
""")

st.info(
    "**Unsure about your sample type?** Discuss heating conditions with "
    "Fengzheng or Thomas before proceeding.",
    icon=":material/help:"
)

st.write("---")

# ── Section 6: Centrifugation ─────────────────────────────────────────────────
st.header("6. :material/speed: Centrifugation")

st.markdown("""
1. Prepare labelled containers in advance.
2. Pre-cool the large centrifuge in the microbiology lab to **4 °C**
   (~15 minutes).
3. After intestinal incubation, stop shaking and aliquot approximately **3/8**
   of each sample into labelled **full-digest tubes**.
4. Centrifuge the remaining fraction at **10,000 × g, 4 °C, for 30 minutes**.
   Balance the centrifuge rotor properly before starting.
5. Transfer the supernatant to labelled containers; keep the pellet in the
   original digestion tube.
6. Tape together the corresponding full-digest, supernatant, and pellet tubes.
   Label with name, date, and content. Freeze immediately.
""")

fraction_df = pd.DataFrame({
    "Fraction": ["Full digest", "Supernatant", "Pellet"],
    "Approx. volume": ["≈ 3/8 of total", "≈ 5/8 of total", "Remainder"],
    "Container": ["Full-digest tube", "Labelled conical tube", "Original digestion tube"],
    "Short-term storage": ["−20 °C", "−20 °C", "−20 °C"],
    "Long-term storage": ["−80 °C", "−80 °C", "−80 °C"],
})
st.table(fraction_df)

st.write("---")

# ── Footer ────────────────────────────────────────────────────────────────────
st.page_link(
    "pages/dashboard.py",
    label=":red-background[**Open the INFOGEST 2.0 Calculator → Dashboard**]",
    icon=":material/dashboard:",
)

st.write("")

if st.button(":material/quiz: Continue here → Take the Quiz", type="primary"):
    st.switch_page("pages/quiz.py")
