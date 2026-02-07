import streamlit as st
from data_base import notify_discord_feedback
from utils.challenge_save_data import save_challenge_submission, get_challenge_submission
from PIL import Image
from utils.utils import hover_zoom_at_cursor

challenge_circuit_layout = Image.open("graphics/challenge_one_circuit.png")
# At the top of the page, load their work
existing_data = get_challenge_submission(st.session_state.current_page)

st.write(f"Current Status: **{existing_data['status'].upper()}**")
import streamlit as st
from PIL import Image

status = existing_data.get('status')
feedback = existing_data.get('admin_feedback')

if status == 'rejected':
    st.error(f"### ❌ Revision Needed\n**Admin Feedback:** {feedback}")
elif status == 'pending':
    st.info("🕒 This challenge is currently pending admin review.")
elif status == 'approved':
    st.success("✅ This challenge has been approved!")

# --- CHALLENGE HEADER ---
st.title("🕵️‍♂️ Challenge 1 - The Case of the Sleeping LED!")

st.markdown("""
Calling all **Junior Detectives**! 🕵️‍♀️🔍

Someone has built a circuit, but the code has gone missing! Your job is to write a script that wakes up the system.

**The Mission:**
1. Look at the **Circuit Blueprint** below.
2. Write a code that makes the **Red Warning Light** (LED) blink on and off like a heartbeat! ❤️⚡
3. Submit your secret code in the box at the bottom for the **Head Detective** to check!
""")

# --- MYSTERY CIRCUIT SECTION ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
### 🧱 Mystery Blueprint
*Follow these coordinates to see the crime scene!*

##### 💡 :red[Warning Light] (LED)
*   **Long leg:** row 10 column e
*   **Short leg:** row 7 column e

##### ⚡ The Helper (220 Ohm Resistor)
*   **Leg 1:** row 7 column c
*   **Leg 2:** **- rail** (Ground Rail)

##### 🧶 The Wires
1. **Pin 13** ➡️ row 10 column a
2. **Pin GND** ➡️ **- rail / Ground Rail**
    """)

with col2:
    st.info("""
### 📝 The Goal
Make the LED turn **ON** for 1 second, then **OFF** for 1 second. It should keep doing this forever so everyone knows the castle is safe! 🏰✨
    """)

    hover_zoom_at_cursor(challenge_circuit_layout, width=300, height=300, zoom_factor=2.0, key="circuit1")


# --- NAVIGATION ---
st.markdown("---")
st.markdown("#### ⬅️ Back to the Workshop")

# The auto-saving text area
template = """void setup() {
  // put your setup code here, to run once:
}

void loop() {
  // put your main code here, to run repeatedly:
}"""

user_data = existing_data['content']
default_text = user_data if user_data else template

st.markdown("### 📤 Submit Your Evidence")
st.text_area(
    """## Put your sketch here""",
    value=default_text,
    key="challenge_draft_input",
    height=300,
    on_change=lambda: save_challenge_submission(
        st.session_state.current_page, 
        st.session_state.challenge_draft_input, 
        status='draft'
    )
)
if st.button("Submit to the Head Detective", type="primary"):
    save_challenge_submission(
        st.session_state.current_page, 
        st.session_state.challenge_draft_input, 
        status='pending'
    )
    notify_discord_feedback(
        username=st.session_state.user_id, 
        category="Challenge Submission", 
        message= st.session_state.challenge_draft_input)
    st.success("Work submitted! Admin will unlock the next challenge after review.")

with st.expander("🔍 Need a Detective's Hint? (Click to open)"):
    st.markdown("""
    *   **Hint 1:** Remember to use 'pinMode' and 'OUTPUT' in your `setup` so the light knows it needs to glow! 💡
    *   **Hint 2:** Use 'digitalWrite' and 'HIGH' to turn the light on and `LOW` to turn it off. 🕯️
    *   **Hint 3:** Don't forget a `delay(1000);` between your commands so the light has time to wake up and sleep! 😴
    """)