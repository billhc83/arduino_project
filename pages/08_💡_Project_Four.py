import streamlit as st
from utils.utils import hover_zoom_at_cursor
from PIL import Image
from utils.utils import complete_step_and_continue, get_automated_pages

# Show toast **once** after rerun
# User-closable toast notification


circuit_layout = Image.open("graphics/project_three_circuit.png")

st.title("🚀Project 4 – Space Explorer Button Buzzer")

st.markdown("""
Welcome aboard your spaceship, Cadet! 🧑‍🚀🌌

Today you’ll build a **button-activated rocket alarm**!  

Press the launch button 👉  
The buzzer sounds like a rocket engine 🔊🚀  

Release the button…  
The engine quiets down 😴  

Prepare for liftoff, but watch your lab carefully! ⚡
""")

circuit1,circuit2 = st.columns(2, vertical_alignment = "center")

with circuit1:

    st.markdown("""
### 🔌 Power Setup

- Arduino **GND** → breadboard **negative (–) rail**  
  (All return wires go here — the spaceship’s ground system)

---

### 🔊 Rocket Buzzer

**Parts**

- Buzzer positive (+) → row 6, column **e**  
- Buzzer negative (–) → row 6, column **f**

**Wires**

- Arduino **pin 8** → row 6 **a**  
- Wire from row 6 **f** → negative (–) rail

---

### 🔘 Launch Button

**Parts**

- Button leg → row 14 **e**  
- Button leg → row 14 **f**

**Wires**

- Arduino **pin 2** → row 14 **a**  
- Wire from row 14 **j** → negative (–) rail

---
                """)
with circuit2:

    hover_zoom_at_cursor(circuit_layout, width=300, height=300, zoom_factor=2.0, key="circuit1")


code1,code2 = st.columns(2)

with code1:
    st.markdown("## 💻 Rocket Control Code")
    st.code("""
void setup() {
  pinMode(8, OUTPUT);
  pinMode(2, INPUT_PULLUP);
}

void loop() {
  if (digitalRead(2) == LOW) {
    digitalWrite(8, HIGH);
  } else {
    digitalWrite(8, LOW);
  }
}
""", language="cpp")

with code2:
    st.markdown("""
## 🧬 Code Translation (Space Edition)

**setup()**

- Pin 8 powers the rocket buzzer 🔊🚀  
- Pin 2 listens for your launch button 👆

**loop()**

- Check the button 👀  
- Pressed → Buzzer ON (engine roaring!) 🛸  
- Not pressed → Buzzer OFF (rocket rests) 😴
""")

# ---------- Optional Info Boxes ----------
st.info("""
### 🌟 Space Explorer Pro Tips

💡 Tip 1: Make sure the buzzer’s + and – are in the correct holes!  
💡 Tip 2: Follow the energy path like a rocket fuel line 🚀  
💡 Tip 3: Press the button slowly and watch your spaceship come alive ⚡
""")

st.info("""
### 🔬 Space Explorer Challenges

🧪 Challenge 1: Make the buzzer beep faster or slower by adding delays.  
🧪 Challenge 2: Add a second button that activates a warning light in addition to the buzzer.  
""")
from utils.steps import complete_step_and_continue
from utils.utils import get_automated_pages

pages_map = get_automated_pages("pages")
buttoncol1, buttoncol2 = st.columns([1,3])
with buttoncol1:
    if st.button("Next Project", type = "primary"):
        complete_step_and_continue(pages_map, current_page_title=st.session_state.get("current_page"))

with buttoncol2:
    st.markdown("#### ⬅️ Click here to add the next project to the menu")