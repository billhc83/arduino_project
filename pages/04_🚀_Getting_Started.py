import streamlit as st
import pandas as pd
from PIL import Image
import sys
import os
from utils.utils import complete_step_and_continue, get_automated_pages

# This adds the parent directory (arduino_project) to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_base import save_and_unlock, save_only

uno = Image.open("graphics/uno.jpg")
breadboard = Image.open("graphics/breadboard.jpg")
led = Image.open("graphics/LED.jpg")
resistor = Image.open("graphics/resistor.png")
button = Image.open("graphics/button.png")
jump = Image.open("graphics/jumper.jpg")
labeled_breadboard = Image.open("graphics/labled_breadboard.jpg")

st.title("🚀GETTING STARTED")
st.markdown("""
              #   🧰 Parts we will use!
            """,unsafe_allow_html = True)
uno1 , uno2 = st.columns(2)
bread1, bread2 = st.columns(2)
led1, led2 = st.columns(2)
res1, res2 = st.columns(2)
but1, but2 = st.columns(2)
jump1, jump2 = st.columns(2)

with uno1:
    st.markdown("""
    ---
                
    # 🔌 Arduino Uno


    The brain 🧠

    It thinks and follows your code.
        
            """)
with uno2:
    st.markdown("---")
    st.image(uno, caption="Arduino UNO")

with bread1:
    st.markdown("""
    ---
                
    # 🧱 Breadboard


    A playground for wires 🛝

    No glue. No solder. Just plug things in.
                
            """)

with bread2:
    st.markdown("---")
    st.image(breadboard, width= 200, caption="Breadboard")

with led1:
    st.markdown("""
    ---
                
    # 💡 LED (Light)


    A tiny light bulb.

    It has two legs:

    Long leg = PLUS (+)

    Short leg = MINUS (–)

    If it’s backwards, it won’t light up.
            
            """)

with led2:
    st.markdown("---")
    st.image(led, caption="LED")

with res1:
    st.markdown("""
    ---            
    
    # 🛑 Resistor

    A tiny traffic police officer 🚓 for electricity.

    It slows electricity down so the LED does not break.

    Always use one with LEDs.
                
            """)
    
with res2:
    st.markdown("---")
    st.image(resistor, width= 200, caption="Resistor")

with but1:
    st.markdown("""
    ---
    
    # 🔘 Button
            
    A tiny door 🚪

    Press = door open Release = door closed
                
            """)
    
with but2:
    st.markdown("---")
    st.image(button, width= 200, caption="Button")

with jump1:
    st.markdown("""
    ---
                
    # 🧵 Jumper wires

                
    Tiny roads for electricity 🛣️

    They connect everything together.
                
        """)

with jump2:
    st.markdown("---")
    st.image(jump, width=250, caption="Jumper Wire")
    
st.markdown("# 🧱 How a breadboard works (kid version)")

col1, col2 = st.columns(2)
with col1:

    st.markdown("""
    Think of the breadboard like a LEGO city for wires 🏙️

    Inside are hidden metal clips that grab the legs of parts.

    🧠 Three important rules
    <br><br>
    ## Rule 1 – Rows are friends 🤝 

    If you plug two legs in the same row, they are holding hands.
    <br><br>
    ## Rule 2 – The middle gap is a river 🌊

    Electricity cannot jump across the middle.

    So parts like LEDs and buttons usually sit across the river.        

    ## Rule 3 -  The rows on the long egdes are connected

    The long lines on the sides are electricity highways:

    :red[Red] line = PLUS (+)

    :blue[Blue] line = MINUS (– / GND)
    <br><br>
    ## 🧪 How we build a circuit
    <br><br>
    Put parts in different rows

    Use wires to connect rows

    Make a loop so electricity can go out and back home

    A circle path = a circuit 🔁""", unsafe_allow_html = True)

with col2:
    st.image(labeled_breadboard, width=400, caption="How all the holes are connected on a breadboard")

# --- NAVIGATION SECTION ---
# (Note: Imports are already at the top of the file, so we don't need them here)

st.divider()

st.markdown("""
    <style>
    /* Hides the three-dot menu and download button in Chrome/Edge/Safari */
    video::-internal-media-controls-download-button {
        display:none;
    }
    video::-webkit-media-controls-enclosure {
        overflow:hidden;
    }
    video::-webkit-media-controls-panel {
        width: calc(100% + 30px);
    }
    </style>
    

""", unsafe_allow_html=True)

st.title("Arduino IDE Download Walkthrough")

install_arduino = "https://github.com/billhc83/arduino_project/releases/download/v1.0.0/download_arduino.mp4"
st.video(install_arduino)

st.title("How To Load Your Code")

load_code = "https://github.com/billhc83/arduino_project/releases/download/v1.0.1/First.arduino.code.mp4"
st.video(load_code)

pages_map = get_automated_pages("pages")
buttoncol1, buttoncol2 = st.columns([1,3])
with buttoncol1:
    if st.button("Next Project", type = "primary"):
        complete_step_and_continue(pages_map, current_page_title=st.session_state.get("current_page"))

with buttoncol2:
    st.markdown("#### ⬅️ Click here to add the next project to the menu")

    