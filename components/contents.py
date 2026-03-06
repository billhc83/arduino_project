from PIL import Image
import base64
from pathlib import Path

def img_to_base64(path):
    data = Path(path).read_bytes()
    b64 = base64.b64encode(data).decode()
    ext = Path(path).suffix.lstrip(".")  # png, jpg, etc.
    return f"data:image/{ext};base64,{b64}"

from utils.utils import hover_zoom_html
engine_controls = hover_zoom_html("graphics/project_twelve_circuit.png", height=200, key="schematic")
patrol_lights = hover_zoom_html("graphics/project_thirteen_circuit.png", height= 200, key="schematic" )

DRAWER_CONTENT = {
    "engine_start": {
        "title": "📘 Engine Start Guide",
        "tip": "Build the rules that control when the engine is allowed to run.",
        "tabs": {
            "mission": {
                "label": "🧠 Mission",
         "content": f"""

<h3>You are building an engine system with rules:</h3>
<p>
- The switch controls the whole system.
- The button starts the engine.
- The engine keeps running until the switch turns OFF.
- If the switch is OFF, nothing runs.
- The "If" blocks are filled in already no need to change them.

Your job is to build these rules using blocks.
</p>
{engine_controls}

"""


            },
            "wiring": {
                "label": "🔌 Wiring",
                "content": """
<b>Match each part to its pin:</b>

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
<b>🔘 Important Button Rule</b>

Look at the wiring diagram.

If the button connects to GND,
choose:

INPUT_PULLUP

That’s how this wiring style works.

<b>Understanding The "If" statements:</b>

The Arduino sees <b>HIGH</b> when the switch is <b>off</b> or the button is <b>not pressed</b>

The Arduino sees <b>LOW</b> when the switch is <b>on</b> or the button is <b>pressed</b>

So when we write <b>If digitalRead(switch or button pin) equals LOW</b>

The Arduino is checking to see if the switch is on or the button is pressed

<b>Think about the flow:</b>

IF switch is ON  
    Light ON
    IF button pressed  
        engine ON

IF switch is OFF (else)
    everything OFF  


Remember:
The switch is the boss.
"""
            }
        }
    },
    "patrol_alarm": {
    "title": "📘 Light Bar Control Guide",
    "tip": "Build the flashing pattern that controls the patrol light bar.",
    "tabs": {
        "mission": {
            "label": "🧠 Mission",
            "content": f"""
            {patrol_lights}

<h3>You are building the patrol vehicle light bar system.</h3>

<p>
The light bar must flash in a clear pattern so people can see the vehicle at night.
</p>

<p>
The system follows these rules:
</p>

<p>
- The switch controls the whole system.<br>
- If the button is OFF → all lights stay OFF.<br>
- If the button is ON(pressed) → the flashing pattern begins.<br>
- The lights flash one at a time.<br>
- The pattern repeats again and again.
</p>

<p>
Each light flash must use a short pause.
</p>

<p>
At Night Patrol Academy we use:<br>
<b>delay(150)</b>
</p>

<p>
Use this delay after each light turns ON and turns OFF.
</p>

<p>
Your job is to build the flashing pattern using blocks.
</p>
"""
        },
        "wiring": {
            "label": "🔌 Wiring",
            "content": """
<b>Match each part to its pin:</b>

🔘 Master Button → Pin 12  
🔴 Red Light → Pin 8  
🔵 Blue Light → Pin 6  
⚪ Clear Strobe Light → Pin 4  

Find the part in the diagram.  
Follow the wire.  
Match it to the pin.
"""
        },
        "logic": {
            "label": "🧩 Logic",
            "content": """
<b>🔘 Button Input Rule</b>

Look at the wiring diagram.

If the Button connects to GND,
choose:

INPUT_PULLUP

That is how this wiring style works.

<b>Understanding the Button:</b>

The Arduino sees <b>HIGH</b> when the Button is <b>OFF s(not pressed)</b>.

The Arduino sees <b>LOW</b> when the Button is <b>ON (pressed)</b>.

So when we write:

<b>If digitalRead(button pin) equals LOW</b>

The Arduino knows the system should run.

<b>Think about the pattern:</b>

IF button is ON (pressed)

Red light ON  
delay(150)  
Red light OFF  

Blue light ON  
delay(150)  
Blue light OFF  

Clear light ON  
delay(150)  
Clear light OFF  

Then the pattern repeats.

IF button is OFF (not pressed) (else)

All lights OFF.

Remember:

The button controls everything.
"""
        }
    }
}
}