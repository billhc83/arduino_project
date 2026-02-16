import streamlit as st
from utils.utils import hover_zoom_at_cursor
from PIL import Image
from utils.utils import  get_automated_pages
from utils.steps import complete_step_and_continue

circuit_layout = Image.open("graphics/project_three_circuit.png")

st.title("🧪 Project 3 – Mad Scientist Button Machine")

st.markdown("""
Welcome to the Mad Scientist Laboratory! 🧠⚡
            
Strange machines are buzzing… wires are glowing… and something amazing is about to happen!

In this experiment, YOU are the mad scientist 😈
Your job is to control a powerful energy crystal using a button.

👉 Press the button
The crystal wakes up and the light turns ON 💡

✋ Let go of the button
The crystal goes back to sleep and the light turns OFF 😴

This experiment teaches the machine to listen to you.
Press means ON.
Release means OFF.

Mwahahaha!
You are in control of the experiment! 🧪⚡
""")

st.markdown("""
## 🔌 Build the Circuit

###### What parts do I need?

🟦 **Arduino UNO** (The Mad Scientist’s Super Brain!)  
The powerful brain of the lab that controls the experiment and watches for button presses.

⚡ **Resistor** (The Electricity Tamer!)  
Slows the wild electricity down so it doesn’t escape or fry the experiment!

✨ **LED (Any Color)** (The Energy Crystal!)  
This crystal glows with mysterious power when the experiment is activated.

〰️ **Jumper Wires** (The Lab Cables!)  
Carry energy between parts as the experiment comes to life.

🔘 **Push Button** (The Experiment Trigger!)  
Press and hold to activate the energy crystal — release it and the power shuts down!
""")


hover_zoom_at_cursor(circuit_layout, height=300, zoom_factor=2.0, key="circuit1")

st.info("👇 Need help? Click below for detailed instructions")

with st.expander("📋 Step-by-step wiring guide"):

    st.markdown("""
 **💡 LED (Energy Crystal)**

- Long leg → row 12, column **e**  
- Short leg → row 11, column **e**
                  
- Resistor 330 or 220 Ohms → row 11 **d** → row 7 **d**

**Wires**

- Arduino **pin 8** → row 12 **a**  
- Wire from **row 7 e** → negative (–) rail

---

**🔘 Button (Trigger Switch)**

- Button leg → row 18 **e**  
- Button leg → row 18 **f**
- Button leg → row 20 **e**  
- Button leg → row 20 **f**

**Wires**

- Arduino **pin 2** → row 18 **a**  
- Wire from row 20 **j** → negative (–) rail""")


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



from utils.steps import complete_step_and_continue
from utils.utils import get_automated_pages

pages_map = get_automated_pages("pages")
buttoncol1, buttoncol2 = st.columns([1,3])
with buttoncol1:
    if st.button("Next Project", type = "primary"):
        complete_step_and_continue(pages_map, current_page_title=st.session_state.get("current_page"))

with buttoncol2:
    st.markdown("#### ⬅️ Click here to add the next project to the menu")