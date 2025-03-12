import streamlit as st

st.set_page_config(
    layout="centered"
)

# Title and introductory message
st.title("🚀 Quick Start Protocol")

st.write("""
### PREPARATIONS

1. Fill the Styrofoam box with ice  
2. Get all the simulated digestive solutions, CaCl₂, refill the MilliQ water  
3. Turn on dry bath and set the temperature to 37.9°C -> press start  
4. Warm up the pH buffers  
5. Warm simulated fluids in dry bath (37°C)  
6. Install the temperature sensor from the pH meter in a tube with water and wrap it with parafilm  
7. Weigh RGE and put it on ice  

   - **RGE (42.35 mg)**: (if you don’t weigh precisely, just calculate how much MilliQ you will have to use for dissolving)  

8. While the pH buffers are warming up, prepare the Excel sheet (option to weigh the enzymes here)  
9. Calibrate the pH meter  
10. Set dry bath to 550 SV  

---

## ORAL DIGESTION  

1. Add 400 µL SSF to S1-S7  
2. Add 3 µL CaCl₂ to S1-S7  
3. Add the MilliQ water according to the Excel to S1-S7  
4. Vortex (avoid turning tube upside down)  
5. Incubate for 2 mins  

---

## GASTRIC DIGESTION  

1. Add 800 µL SGF to S1-S7  
2. Adjust the pH to 3 ± 0.2  
3. Add the remaining amount of MilliQ water to S1-S7 according to the Excel  
4. Dissolve RGE in 900 µL MilliQ and add 100 µL of it to the tubes  
5. Start the timer for 2 hours  
6. Re-adjust the pH after 10 and 60-75 minutes  
7. During this time: lunch break, cleanup  
8. After the second pH adjustment, pre-weigh the enzymes **pancreatin** and **bile**  

   - **Pancreatin (425.43 mg)**  
   - **Bile (90.45 mg)**: (if you don’t weigh precisely, just calculate how much SIF you will have to use for dissolving)  

9. Dissolve Bile in 2.250 mL SIF and put it in the water bath but keep pancreatin on ice  

---

## INTESTINAL DIGESTION  

1. Add 850 µL SIF to S1-S7  
2. Add 4 µL CaCl₂ to S1-S7  
3. Adjust the pH to 7 ± 0.2  
4. Dissolve Pancreatin in 4.5 mL SIF, sonicate it for 5 min at frequency = 80, power = 100, T = 20°C, centrifuge 5 min at 2000 g  
5. Add the remaining amount of MilliQ water to S1-S7 according to the Excel  
6. Add 250 µL bile to S1-S7  
7. Add 500 µL pancreatin to S1-S7  
8. Start the timer for 2 hours  
9. Re-adjust the pH after 10 and 60-75 minutes  
10. During this time: pre-label acid-washed tubes for supernatant and full digesta and pre-cool the centrifuge in D31 (4°C)  

---

## CENTRIFUGE  

1. Transfer 1.5 mL of S1-S7 to the pre-labeled 2 mL acid-washed Eppendorf tubes for the full digesta  
2. Centrifuge the remaining tubes at 10,000 g, 4°C, for 30 minutes  
3. During this time: cleanup and preparation to store the tubes  
4. After centrifuge: transfer the supernatant to the 15 mL pre-labeled conical tubes, tape and label everything, and store it in a plastic bag in the -20°C  

---

## Notes  

- **For RGE**: MilliQ water according to Excel → enter measured RGE weight → template, specific volume of water  
- **For pancreatin**: anywhere between 430-450 mg  
- **For Bile in SIF**: MilliQ water according to Excel → enter measured Bile weight → template, specific volume of water  
- **For Pancreatin in SIF**: MilliQ water according to Excel → enter measured Pancreatin weight → template, specific volume of water  

---

## Storage Information  

- **SSIF, SGF, SFF** → 37°C  
- **CaCl₂** → fridge  
- **Other chemicals** → freezer (-5°C)  
- **Pre-cool centrifuge** → 1 hour before use  
""")