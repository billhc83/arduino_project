import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from components.arduino_blocks import arduino_block_coder
from components.contents import DRAWER_CONTENT
from PIL import Image
from utils.utils import hover_zoom_at_cursor, complete_step_and_continue, get_automated_pages
from utils.assembly_guide import assembly_guide
from utils.step_builder import build_step, intro_step, rect, circle, line

st.set_page_config(layout="wide")

# ════════════════════════════════════════════════════════════
#  PAGE IDENTITY  — edit these 4 lines for every new project
# ════════════════════════════════════════════════════════════

PAGE_TITLE       = "Project Fourteen Part 4: Code Cracker"   # shown in the assembly guide header
BANNER_IMAGE     = "graphics/code_cracker.png"            # top banner         # used in both tabs
ARDUINO_PRESET   = "codebreaker"
# ════════════════════════════════════════════════════════════
#  INTRO MARKDOWN  — replace the triple-quoted block below
# ════════════════════════════════════════════════════════════

INTRO_MD = """
<div style="max-width: 850px; margin: auto;">

## 🕵️ Spy Training – Listening for a Signal

Agent, your Code Breaker is almost ready…

The screen shows the challenge.
The cipher is in place.

But right now, your system is missing something very important:

👉 It can’t *listen* yet.

---

## 🎧 The Next Upgrade: Listening Mode

We are going to teach your system to **wait for a message from the trainee**.

Here is the code you are building:

```cpp
if (Serial.available() > 0) {

}
```

---

## 🔍 Let’s Break It Down

### 🧩 What is `Serial.available()`?

Think of the terminal like a **message inbox 📬**

When a trainee types something, it gets placed into that inbox.

👉 `Serial.available()` checks:

**“Is there anything in the inbox?”**

---

### 🔢 What does `> 0` mean?

The computer counts how many characters are waiting.

For example:

```
spark  → 5 letters → count = 5
```

So when we write:

```cpp
Serial.available() > 0
```

We are asking:

👉 “Is there at least ONE letter waiting?”

If yes → the condition is TRUE ✅
If no → the condition is FALSE ❌

---

### 🚪 The If Statement (The Gate)

```cpp
if (Serial.available() > 0) {
```

This acts like a **security door 🚪**

* If there is a message → the door opens
* If there is no message → the door stays closed

Right now, the door opens…
but nothing happens inside yet.

---

## 💻 What You Will See

When the trainee types a guess:

```
Enter your guess:
spark
```

👉 The system notices something was typed…

…but it doesn’t respond yet.

---

## 🤔 Why Doesn’t It Do Anything?

Because we have only taught it to:

✔ detect input
❌ NOT read it
❌ NOT use it

That comes next.

---

## 🎯 Your Mission

Build the listening check so your system can:

🟢 detect when a trainee types something
🔒 ignore everything else

---

## 🧠 Think Like an Agent

A good code-breaking system does not guess randomly.

It waits…
It listens…
Then it acts.

In the next step, you will teach your system to **capture the message**.

"""


# ════════════════════════════════════════════════════════════
#  PAGE RENDER — nothing below this line needs to change
# ════════════════════════════════════════════════════════════

page   = os.path.basename(__file__).replace(".py", "")
banner = Image.open(BANNER_IMAGE)

st.image(banner)
st.markdown(INTRO_MD, unsafe_allow_html=True)

arduino_block_coder(
    preset=ARDUINO_PRESET,
    drawer_content=DRAWER_CONTENT.get(ARDUINO_PRESET),
    username=st.session_state.get("user_id"),
    page=page,
    height=620,
)

pages_map = get_automated_pages("pages")
buttoncol1, buttoncol2 = st.columns([1, 3])
with buttoncol1:
    if st.button("Next Step", type="primary"):
        complete_step_and_continue(pages_map, current_page_title=st.session_state.get("current_page"))
with buttoncol2:
    st.markdown("#### ⬅️ Click here to continue to the next step!")
