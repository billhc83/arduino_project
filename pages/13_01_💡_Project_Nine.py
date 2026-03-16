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
*   **Mega-Glow Lightening-Milk** 🥛🌙
*   **The Crusty Club Sandwich** 🥪

Let's see what happens when we try to power our machine with a sandwich!
""")

from utils.assembly_guide import assembly_guide, coordinate_picker
steps = [
    {
        "instruction": "Lets Discover the Universal Power Slot",
        "tip": "Press the next button for a step by step guide",  
    },
    {
        "instruction": "Place the LED long leg in row 12, column E. <br>Place the LED short leg in row 11, column E",
        "tip": "The long leg is positive — it's called the anode!",
        "highlights": [
             {"pos": (708, 175, 899, 331), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
        #"label": "LED +",
    },
    {
        "instruction": "Place one leg of the 220 ohm resistor in row 11, column D. <br>Place the second leg of the resistor in row 7, column D",
        "tip": "The resistor slows down the electricity",
        "highlights": [
             {"pos": (693, 324, 825, 363), "shape": "rect"},
             {"pos": (492, 154), "shape": "circle", "radius": 60}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in the Arduino GND Pin. <br>Place the other end in row 7, column E",
        "tip": "The wires are like roads for electricity",
        "highlights": [
             {"pos": (375, 231, 740, 339), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in the Arduino Pin 8. <br>Place the other end in row 12, column A",
        "tip": "The wires are like roads for electricity",
        "highlights": [
             {"pos": (346, 350, 844, 453), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    }]
tab1, tab2 = st.tabs(["**📋 Quick Overview**", "**🔧 Step-by-Step**"])  

with tab1:
  
  hover_zoom_at_cursor(workshop_layout, zoom_factor=2.0, key="circuit1")

with tab2:

  assembly_guide("graphics/project_one_circuit.png", steps, "Project 9: The Universal Power Slot")

st.info("""
🧠 **Engineer's Data Guide:**
*   **`int` Slots:** These are for **Numbers** (like Battery Power). 🔢
*   **`String` Slots:** These are for **Words** (like the name of a snack). 📝

If you try to put a **String** in an **int** slot, the machine will crash!
""")
# --- CODE SECTION ---
code_col1, code_col2 = st.columns([2.5,1.5])

st.markdown("## 📜 The Inspection Script")
st.code("""
// 📦 This is our Universal Power Slot!
// Remove the // from the one you want to test and upload:

// String powerSlot = "Mega-Glow Lightening-Milk"; 
// String powerSlot = "Sparky-Squirrel Static";
// String powerSlot = "Zappy-Zucchini Juice";
String powerSlot = "Crusty Club Sandwich"; 

int currentEnergy = 0; // This starts at 0

void setup() {
  pinMode(8, OUTPUT);
  Serial.begin(9600);
  Serial.println("--- SCANNING POWER SLOT ---");
}

void loop() {
  // 🔍 THE INSPECTION: Matching names to numbers!
  
  if (powerSlot == "Mega-Glow Lightening-Milk") {
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
    digitalWrite(8, HIGH);
    Serial.print("SUCCESS: Found ");
    Serial.print(powerSlot);
    Serial.print("! Energy Level: ");
    Serial.println(currentEnergy);
  } 
  else {
    digitalWrite(8, LOW);
    Serial.print("⚠️ ERROR: Cannot run on ");
    Serial.println(powerSlot);
    Serial.println("Engineer Note: Wrong part in slot! ❌");
  }
  
  delay(3000);
}
""", language="cpp")

st.markdown("""
## 🛠️ Project Tips

### 1️⃣ How the `//` slashes work (VERY IMPORTANT)

In this code, the double slashes `//` mean **IGNORE THIS LINE**.  
The Arduino will **not read** any line that starts with `//`.

Here is how the code starts **right now**:

<pre><code>
// String powerSlot = "Mega-Glow Lightening-Milk"; 
// String powerSlot = "Sparky-Squirrel Static";
// String powerSlot = "Zappy-Zucchini Juice";
String powerSlot = "Crusty Club Sandwich"; 
</code></pre>

- The **first three lines are OFF** because they have `//`
- The **last line is ON** because it has **no `//`**
- This means the Arduino starts by using **Crusty Club Sandwich**

---

### 2️⃣ How to change which power slot is used

To test a different power slot, you must **move the slashes**.

Example: to turn ON **Mega-Glow Lightening-Milk**:

<pre><code>
String powerSlot = "Mega-Glow Lightening-Milk"; 
// String powerSlot = "Sparky-Squirrel Static";
// String powerSlot = "Zappy-Zucchini Juice";
// String powerSlot = "Crusty Club Sandwich"; 
</code></pre>

What you did:
- Removed `//` from **one line** → turned it ON
- Added `//` to the others → turned them OFF

👉 **Only ONE powerSlot line should be ON at a time.**

---

### 3️⃣ What happens if ALL lines have `//`

If **every** powerSlot line starts with `//`:

<pre><code>
// String powerSlot = "Mega-Glow Lightening-Milk"; 
// String powerSlot = "Sparky-Squirrel Static";
// String powerSlot = "Zappy-Zucchini Juice";
// String powerSlot = "Crusty Club Sandwich"; 
</code></pre>

The program will **NOT work** ❌

Why?
- The code later uses `powerSlot`
- But `powerSlot` was never created
- The computer shows an **error** because something is missing

👉 **At least ONE powerSlot line must NOT have `//`.**

---

### 🧠 Big Idea

- `//` turns code **OFF**
- No `//` turns code **ON**
- Missing code causes errors

That’s how engineers test and fix programs!
""", unsafe_allow_html=True)


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
