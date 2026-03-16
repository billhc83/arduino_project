import streamlit as st
from PIL import Image
from utils.utils import hover_zoom_at_cursor, complete_step_and_continue, get_automated_pages

# --- PAGE CONFIG ---
# (Optionally add st.set_page_config here if not in main.py)

# --- ASSETS ---
# Replace with your image of the 3 LEDs + Buzzer + Switch setup
# traffic_layout = Image.open("graphics/traffic_light_alarm.png")

# --- HEADER ---
st.title("🚦 Project 7 - The Safety Traffic Light! 🚨")

st.markdown("""
Calling all City Engineers! 🏗️ 

Today, you are building a **Smart Traffic Light**. It counts down like a real light, but it has a secret **Safety Switch**! 

When the switch is ON, a **Buzzer Alarm** sounds if anyone tries to go on Red! 🛑🔊
""")

# --- CIRCUIT SECTION ---
circuit_col1, circuit_col2 = st.columns(2, vertical_alignment="center")

with circuit_col1:
    st.markdown("""
### 🏗️ Build the City Grid

**Inventory Check:**
- **3 LEDs:** Red, Yellow, Green 🔴🟡🟢
- **1 Buzzer:** The Siren 🔊
- **1 Switch:** The Safety Lock 🔓
- **Jumper Wires:** The Power Lines ⚡

**Instructions:**
1. Connect **Red LED** to Pin 12, **Yellow** to 11, and **Green** to 10.
2. Plug the **Buzzer** into Pin 8.
3. Connect your **Switch** to Pin 7.
                """)

with circuit_col2:
    st.info("💡 **Pro Tip:** Make sure the long leg of your LEDs goes to the Arduino Pins!")
    # hover_zoom_at_cursor(traffic_layout, width=300, height=300, zoom_factor=2.0, key="traffic_zoom")

# --- CODE SECTION ---
code_col1, code_col2 = st.columns(2)

with code_col1:
    st.markdown("## 💻 The City Controller")
    st.code("""
int red = 12;
int yellow = 11;
int green = 10;
int buzzer = 8;
int safetySwitch = 7;

void setup() {
  pinMode(red, OUTPUT);
  pinMode(yellow, OUTPUT);
  pinMode(green, OUTPUT);
  pinMode(buzzer, OUTPUT);
  pinMode(safetySwitch, INPUT);
  Serial.begin(9600);
}

void loop() {
  // 🟢 Green Light Go!
  digitalWrite(green, HIGH);
  Serial.println("GO! 🟢");
  delay(3000);
  digitalWrite(green, LOW);

  // 🟡 Yellow Light Slow!
  digitalWrite(yellow, HIGH);
  Serial.println("SLOW DOWN! 🟡");
  delay(1000);
  digitalWrite(yellow, LOW);

  // 🔴 Red Light STOP!
  digitalWrite(red, HIGH);
  Serial.println("STOP! 🔴");
  
  // Is the Safety Switch ON?
  if (digitalRead(safetySwitch) == HIGH) {
    tone(buzzer, 1000, 500); // Beep!
    Serial.println("ALARM ACTIVE! 🚨");
  }
  
  delay(3000);
  digitalWrite(red, LOW);
}
""", language="cpp")

with code_col2:
    st.markdown("""
## 🧬 How it Works

**A Sequence!**
- The code runs from top to bottom. It turns one light ON, waits, turns it OFF, and moves to the next. 🪜

**The "if" Check**
- The Arduino asks: *"Is the switch flipped?"* If yes, it sounds the buzzer! If no, it stays quiet. 🤫

**tone()**
- This makes the buzzer sing! The first number is the **Sound Pin** and the second is the **Pitch** (how high or low the beep is). 🎶
""")

# --- INFO BOXES ---
st.info("""
### 🕵️‍♂️ Terminal Watch
Watch your **Serial Monitor**! It will tell you exactly which light is active. If you flip the switch, you'll see the **ALARM ACTIVE!** message pop up! 🖥️✨
""")

st.info("""
### 🏆 Bonus Missions
🧪 **Challenge 1:** Can you make the **Yellow light** blink 3 times before it turns Red? 
🧪 **Challenge 2:** Change the `tone` number to **200** to make a low robot growl! 🤖
""")

# --- NAVIGATION ---
pages_map = get_automated_pages("pages")
buttoncol1, buttoncol2 = st.columns([1,3])
with buttoncol1:
    if st.button("Next Project", type="primary"):
        complete_step_and_continue(pages_map, current_page_title=st.session_state.get("current_page"))

with buttoncol2:
    st.markdown("#### ⬅️ Ready to upgrade your city?")
