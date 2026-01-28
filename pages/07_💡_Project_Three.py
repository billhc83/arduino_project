import streamlit as st
from utils import hover_zoom_at_cursor
from PIL import Image
from utils import complete_step_and_continue, get_automated_pages

circuit_layout = Image.open("graphics/project_three_circuit.png")

st.title("🧪 Project 3 – Mad Scientist Button Machine")

st.markdown("""
Welcome to the Mad Scientist Laboratory! 🧠⚡

Press the button 👉  
The light turns ON 💡  

Let go…  
The light turns OFF 😴  

Mwahahaha! You control the experiment! 😈
""")

st.markdown("## 🧭 Lab Wiring Map")

# ---------- CIRCUIT COLUMNS ----------
circuit1, circuit2 = st.columns(2, vertical_alignment= "center")

with circuit1:
    st.markdown("""
### 💡 LED (Energy Crystal)

**Parts**

- Long leg → row 6, column **e**  
- Short leg → row 6, column **f**  
- Resistor → row 6 **h** → row 10 **h**

**Wires**

- Arduino **pin 8** → row 6 **a**  
- Wire from **row 10 f** → negative (–) rail

---

### 🔘 Button (Trigger Switch)

**Parts**

- Button leg → row 14 **e**  
- Button leg → row 14 **f**

**Wires**

- Arduino **pin 2** → row 14 **a**  
- Wire from row 14 **j** → negative (–) rail""")

with circuit2:

        hover_zoom_at_cursor(circuit_layout, width=300, height=300, zoom_factor=2.0, key="circuit1")


# ---------- CODE COLUMNS ----------


code1, code2 = st.columns(2)

with code1:
    st.markdown("## 💻 Secret Lab Code")
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
    st.info("""
            
### 🧪 Mad Scientist Pro Tips

💡 **Tip 1: Follow the electricity path!**  
Pretend electricity is a little bug 🐜 traveling from the pin, through the LED, and back to the ground rail. Can you see its path?  

💡 **Tip 2: One lead per hole!**  
Just like a tiny puzzle, each wire or part gets its own hole. Two things in the same hole can cause a “traffic jam”! 🚦  

💡 **Tip 3: Press slowly and watch!**  
Press the button and see the LED wake up. Let go and see it sleep. Your experiment is alive! ⚡😴
""")
    st.info("""

 **Challenge: Mystery Colors**  
If you have LEDs of different colors, swap the green or yellow LED in place of the first one. What happens when the button is pressed? Can you predict the color?  

 🧪 **Challenge: Faster or Slower**  
Add a tiny delay in the code to make the LED blink faster or slower. Watch how the energy crystal behaves! ⚡💡           
            """)

with code2:
    st.markdown("""
## 🧬 Code Translation (Scientist Edition)

**These lines:**

pinMode(8, OUTPUT);
pinMode(2, INPUT_PULLUP);

                
Means:

> “Door 8 sends electricity to the crystal 💡”  
> “Door 2 listens for the button 🔘”

---

 **This spell:**

digitalRead(2)
                

Means:

> “Is the button being pressed?”

LOW = pressed 😄  
HIGH = not pressed 😴  

---

**This spell:**
                
digitalWrite(8, HIGH);
                

Means:

> “Turn the crystal ON!” 💥

And:

digitalWrite(8, LOW);
                

Means:

> “Turn the crystal OFF.” 🌑

---

**The loop**

Runs forever like a bubbling experiment 🧪♻️

Check → Decide → Glow → Repeat!

""")



if st.button("Complete Project & View Progress", type="primary"):
    pages_map = get_automated_pages("pages")
    complete_step_and_continue(pages_map)
