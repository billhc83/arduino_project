import streamlit as st
from PIL import Image
from utils.utils import hover_zoom_at_cursor, complete_step_and_continue, get_automated_pages

# --- PAGE CONFIG ---

# --- ASSETS ---
nightlight_layout = Image.open("graphics/project_seven_circuit.png")

# --- HEADER ---
st.title("💡 Project 7 - The Automagic Night Light!")

st.markdown("""
Put on your **Engineer Hat**! 👷‍♂️👷‍♀️

Have you ever wondered how streetlights know exactly when to turn on at night? They use a "Magic Eye" just like yours! 

Today, you will engineer a **Smart Night Light**. It will stay OFF during the day to save energy, but it will **automagically** glow when the sun goes down! 🌅➡️🌃
""")

# --- CIRCUIT SECTION ---
circuit_col1, circuit_col2 = st.columns(2, vertical_alignment="center")

with circuit_col1:
    st.markdown("""
### 🛠️ The Engineering Blueprint

**What you need:**
- **1x Photoresistor** (The Light Sensor) 👁️
- **1x LED** (The Night Light) 🚨
- **1x 220-ohm Resistor** (For the LED) ⚡
- **1x 10k-ohm Resistor** (For the Sensor) ⚡

## 🧱 Breadboard layout

##### 👁️ :orange[Photoresistor] (The Eye)
*   **Leg 1**: Row 15 column e
    **Leg 2**: Row 20 column e

##### 💡 :red[Red] LED
*   **Long leg:** row 10 column e
*   **Short leg:** row 7 column e

##### ⚡ Resistor (220 Ohm): 
*   **Leg 1:** row 7 column c
*   **Leg 2:** - rail/ ground

##### ⚡ Resistor (10K Ohm): 
*   **Leg 1:** row 20 column c
*   **Leg 2:** row 25 column c
                
##### 🧶 Wires:   
1.  **Pin 13** to **row 10 column a** (Power for the light)
2.  **Pin GND** to  **- rail ** (The ground path)
3.  **- rail/ground** to row 25 column a
4.  **Pin A0** to row 20 column a 
5.  **Pin 5V** to row 15 column a
""")
with circuit_col2:
    st.info("🧠 **Engineer Tip:** We are combining an **INPUT** (the eye) with an **OUTPUT** (the light) to make a smart machine!")
    hover_zoom_at_cursor(nightlight_layout, width=300, height=300, zoom_factor=2.0, key="nightlight_zoom")

# --- CODE SECTION ---
code_col1, code_col2 = st.columns([2.5,1.5])

with code_col1:
    st.markdown("## 💻 The Smart Logic")
    st.code("""
int lightSensor = A0;
int nightLight = 13;

void setup() {
  pinMode(nightLight, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int brightness = analogRead(lightSensor);
  Serial.println(brightness);

  // If it's dark (number is low)...
  if (brightness < 300) {
    digitalWrite(nightLight, HIGH); // Light ON!
    Serial.println("It's dark! Light ON 🌙");
  } 
  // If it's bright...
  else {
    digitalWrite(nightLight, LOW);  // Light OFF!
    Serial.println("Sun is up! Light OFF ☀️");
  }

  delay(100); 
}
""", language="cpp")

with code_col2:
    st.markdown("""
## 🧬 Engineering Secrets

**Input vs. Output**
- The **Sensor** is an input (information coming in). The **LED** is an output (action going out). 📥➡️📤

**The "Else" Statement**
- This is the Arduino's way of saying **"Otherwise."** 
- *IF* it is dark, do this. *ELSE* (otherwise), do that! It’s like a fork in the road. 🍴

**Testing the Threshold**
- We used the number **300**. If your room is very bright, you might need a different number! 🔢
""")

# --- INFO BOXES ---
st.info("""
### 🕵️‍♂️ Lab Testing
1. Open your **Serial Monitor**.
2. Cup your hands over the sensor. Does the LED turn on? 👐
3. Let go. Does it turn off? 💡
4. If it doesn't work, check your **brightness number** in the monitor!
""")

st.info("""
### 🏆 Promotion Challenges
🧪 **Challenge 1:** Can you make the LED turn on only when it is **Pitch Black** (try a very low number like 100)? 🌑

🧪 **Challenge 2:** Engineering Upgrade! Can you make a **Buzzer** beep once whenever the light turns on? 🔊
""")

# --- NAVIGATION ---
pages_map = get_automated_pages("pages")
buttoncol1, buttoncol2 = st.columns([1,3])
with buttoncol1:
    if st.button("Next Project", type="primary"):
        complete_step_and_continue(pages_map, current_page_title=st.session_state.get("current_page"))

with buttoncol2:
    st.markdown("#### ⬅️ Ready for your next Engineering Project?")
