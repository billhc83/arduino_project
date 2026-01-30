import streamlit as st
import pandas
from data_base import save_and_unlock, save_only
from utils import hover_zoom_at_cursor
from PIL import Image
from utils import complete_step_and_continue, get_automated_pages

circuit_layout = Image.open("graphics/circuit_layout.png")

st.title("Project Two - BLINKING BEACON💡 💡")
st.markdown("""
## Goal

🚨 Make your light blink on and off like a lighthouse! 🚨

### New ideas 💭

---

#### ⏱️ The "Wait" Command (Delay)
Imagine you are playing "Red Light, Green Light." When you hear "Red Light," you freeze! 

The Arduino uses a command called `delay()`. This tells the robot brain to stop and do **nothing** for a little bit of time. 
*   `delay(1000)` = Wait for 1 second.
*   `delay(500)` = Wait for half a second (a quick blink!).

#### 🔄 The "Forever" Loop
In your code, the `void loop()` section is like a hamster wheel. The Arduino reads the rules, gets to the bottom, and then jumps back to the top to do it all over again... forever! 

1. **High:** Turn the light ON 💡
2. **Wait:** Hold your breath! ⏱️
3. **Low:** Turn the light OFF 🌑
4. **Wait:** Hold your breath! ⏱️
5. **Jump back to step 1!**

---

### The Code Secret 🖥️

#### `digitalWrite(8, LOW);`
In Project 1, we used `HIGH` to give the light electricity. Now we use **`LOW`**. 
*   **HIGH** = Electricity flows! (Light ON)
*   **LOW** = Electricity stops! (Light OFF)

Think of it like a water tap. `HIGH` is turning the water on, and `LOW` is turning it off.

---
""")

circuit1, circuit2 = st.columns(2, vertical_alignment="bottom")

with circuit1:
   
   st.markdown("""  

    ## 🔌 Build the circuit
    *(If you still have Project 1 built, you are already ready!)*

    ###### What parts do I need?
                
    🟦 Arduino UNO (The blue computer brain!)
                
    ⚡ Resistor (The electricity speed-bump!)

    ✨ Any color LED (The tiny glowing light!)

    〰️ Wires (The robot's veins!)

    ## 🧱 Breadboard layout

    ##### :red[Red] LED
      * Long leg: row 6 column e
      * Short leg: row 6 column f

    ##### Resistor: 
      * row 6 column h, row 10 column h

    ##### 2 Wires:   
    1:  **Pin 8**, row 6 column a
    
    2:  **Pin GND**, row 10 column f

    ---
    """)
   with circuit2:
    hover_zoom_at_cursor(circuit_layout, width=300, height=300, zoom_factor=2.0, key="circuit1")
    st.markdown("---")

st.markdown("""

## Code 
            
            """)

st.code("""
// This part runs just ONCE when you turn it on
void setup() {
  // Tell the brain Pin 8 is a mouth (Output)
  pinMode(8, OUTPUT); 
}

// This part runs OVER and OVER forever!
void loop() {
  digitalWrite(8, HIGH); // Light ON! 💡
  delay(500);            // Wait for half a second ⏱️
  
  digitalWrite(8, LOW);  // Light OFF! 🌑
  delay(500);            // Wait for half a second ⏱️
}
        """)
st.success("### 🌟 Pro-Tips!")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Delay()**")
    st.write("In Arduino land, 1,000 equals 1 second. If you want the light to stay off for a really long time, what number would you use for 5 seconds?")

with col2:
    st.markdown("**The Semicolon** 🧐")
    st.write("Don't forget the **;** at the end of your code lines!")

st.info("🚀Try changing the number inside `delay(500)` to `delay(100)`. Does your robot blink faster or slower?")

if st.button("Complete Project & View Progress", type="primary"):
    pages_map = get_automated_pages("pages")
    complete_step_and_continue(pages_map)