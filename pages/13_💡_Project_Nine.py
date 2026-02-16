import streamlit as st
from PIL import Image
from utils.utils import hover_zoom_at_cursor, complete_step_and_continue, get_automated_pages

# --- PAGE CONFIG ---
# (Optionally add st.set_page_config here if not in main.py)

# --- ASSETS ---
workshop_layout = Image.open("graphics/project_one_circuit.png")

# --- HEADER ---
st.title("🛠️ Project 9 - The Universal Power Slot")

st.markdown("""
Welcome to the Design Lab, **Senior Systems Engineer**! 👷‍♂️👷‍♀️

Today, we are mastering **Variable Slots**. In engineering, a "Variable" is just a slot designed to hold a specific part. But you have to be careful—the **Part** must match the **Slot**! 

We have three futuristic battery types and one very delicious lunch to test:
*   **Zappy-Zucchini Juice** 🥒⚡
*   **Sparky-Squirrel Static** 🐿️💥
*   **Mega-Glow Moon-Milk** 🥛🌙
*   **The Crusty Club Sandwich** 🥪

Let's see what happens when we try to power our machine with a sandwich!
""")



hover_zoom_at_cursor(workshop_layout, height=300, zoom_factor=2.0, key="power_slot_zoom")


st.info("👇 Need help? Click below for detailed instructions")

with st.expander("📋 Step-by-step wiring guide"):
    
    st.markdown("""
  ## 🧱 The Power Core Layout

  ##### 💡 :red[System Status LED]
  *   **Long leg:** row 12 column e
  *   **Short leg:** row 11 column e

  ##### ⚡ Resistor (220 Ohm - Red, Red, Brown): 
  *   **Leg 1:** row 11 column d
  *   **Leg 2:** row 7 column d

  ## 🧶 Wiring the Core

  1.  **Pin GND** ➡️ **- rail / Ground Rail** (The Main Drain) 🚰
  2.  **Pin 13** ➡️ **row 10 column a** (Power for the LED)

                
  *Tip: Ensure your Resistor reaches all the way to the blue Ground Rail!* 🔌
                """)

st.info("""
🧠 **Engineer's Data Guide:**
*   **`int` Slots:** These are for **Numbers** (like Battery Power). 🔢
*   **`String` Slots:** These are for **Words** (like the name of a snack). 📝

If you try to put a **String** in an **int** slot, the machine will crash!
""")
# --- CODE SECTION ---
code_col1, code_col2 = st.columns([2.5,1.5])

with code_col1:
    st.markdown("## 📜 The Inspection Script")
    st.code("""
// 📦 This is our Universal Power Slot!
// Remove the // from the one you want to test and upload:

// String powerSlot = "Mega-Glow Moon-Milk"; 
// String powerSlot = "Sparky-Squirrel Static";
// String powerSlot = "Zappy-Zucchini Juice";
String powerSlot = "Crusty Club Sandwich"; 

int currentEnergy = 0; // This starts at 0

void setup() {
  pinMode(13, OUTPUT);
  Serial.begin(9600);
  Serial.println("--- SCANNING POWER SLOT ---");
}

void loop() {
  // 🔍 THE INSPECTION: Matching names to numbers!
  
  if (powerSlot == "Mega-Glow Moon-Milk") {
    currentEnergy = 100; // 🥛 Huge Power!
  } 
  else if (powerSlot == "Sparky-Squirrel Static") {
    currentEnergy = 50;  // 🐿️ Medium Power!
  }
  else if (powerSlot == "Zappy-Zucchini Juice") {
    currentEnergy = 10;  // 🥒 Tiny Power!
  }
  else {
    currentEnergy = 0;   // 🥪 No Power in a Sandwich!
  }

  // 💡 EXECUTION: Use the Energy we found!
  if (currentEnergy > 0) {
    digitalWrite(13, HIGH);
    Serial.print("SUCCESS: Found ");
    Serial.print(powerSlot);
    Serial.print("! Energy Level: ");
    Serial.println(currentEnergy);
  } 
  else {
    digitalWrite(13, LOW);
    Serial.print("⚠️ ERROR: Cannot run on ");
    Serial.println(powerSlot);
    Serial.println("Engineer Note: Wrong part in slot! ❌");
  }
  
  delay(3000);
}
""", language="cpp")

with code_col2:
    st.markdown("""
## 🧬 Engineering Test Procedures

**Test 1: The Empty Port** 📭
Run the code as-is. Since both slots are empty, the system just waits.

**Test 2: The Lunch Disaster** 🥪
Change the top of your code to:
`String snackSlot = "Crusty Club Sandwich";`
The machine sees the word and gives a **Sandwich Alert**! 

**Test 3: High-Voltage Bootup** 🚀
Plug in a battery by changing the number:
`int batterySlot = 100;` // (Mega-Glow Moon-Milk)
The machine prioritizes the battery and turns the **Status LED** ON!
""")

# --- INFO BOXES ---
st.info("""
### 🔎 Inspector's Serial Monitor
Open your [Arduino Serial Monitor](https://docs.arduino.cc) 🔎. 
1. When the battery is 0, read the error message. 
2. When you add a battery number, watch the "System Online" message appear! 📈
""")

st.info("""
### 🏆 Senior Engineer Challenges
🧪 **Challenge 1:** Can you change the `snackSlot` to a **"Taco"**? Why does the machine say "System Waiting" instead of giving an alert? 🌮

🧪 **Challenge 2:** Add `batterySlot = batterySlot - 10;` inside the `loop`. Can you watch your **Zucchini Juice** run out? 📉🥒
""")

# --- NAVIGATION ---
pages_map = get_automated_pages("pages")
buttoncol1, buttoncol2 = st.columns([1,3])
with buttoncol1:
    if st.button("Next Project", type="primary"):
        complete_step_and_continue(pages_map, current_page_title=st.session_state.get("current_page"))

with buttoncol2:
    st.markdown("#### ⬅️ Click here to upgrade the power core!")
