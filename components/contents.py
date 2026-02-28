from PIL import Image
import base64
from pathlib import Path

def img_to_base64(path):
    data = Path(path).read_bytes()
    b64 = base64.b64encode(data).decode()
    ext = Path(path).suffix.lstrip(".")  # png, jpg, etc.
    return f"data:image/{ext};base64,{b64}"

from utils.utils import hover_zoom_html
zoom_html = hover_zoom_html("graphics/project_twelve_circuit.png", height=200      , key="schematic")

DRAWER_CONTENT = {
    "engine_start": {
        "title": "📘 Engine Start Guide",
        "tip": "Build the rules that control when the engine is allowed to run.",
        "tabs": {
            "mission": {
                "label": "🧠 Mission",
         "content": f"""
<p>
You are building an engine system with rules:

- The switch controls the whole system.
- The button starts the engine.
- The engine keeps running until the switch turns OFF.
- If the switch is OFF, nothing runs.

Your job is to build these rules using blocks.
</p>
{zoom_html}

"""


            },
            "wiring": {
                "label": "🔌 Wiring",
                "content": """
Match each part to its pin:

🔘 Arm Switch → Pin 9  
🔴 Engage Button → Pin 7  
💡 Engine Light → Pin 2  
🔊 Engine Buzzer → Pin 5  

Find the part in the diagram.  
Follow the wire.  
Match it to the pin.
"""
            },
            "logic": {
                "label": "🧩 Logic",
                "content": """
🔘 Important Button Rule

Look at the wiring diagram.

If the button connects to GND,
choose:

INPUT_PULLUP

That’s how this wiring style works.

Think about the flow:

IF switch is ON  
    IF button pressed  
        engine ON

IF switch is OFF  
    everything OFF  


Remember:
The switch is the boss.
"""
            }
        }
    }
}