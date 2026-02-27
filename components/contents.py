DRAWER_CONTENT = {
    "engine_start": {
        "title": "📘 Engine Start Guide",
        "tip": "Build the rules that control when the engine is allowed to run.",
        "tabs": {
            "mission": {
                "label": "🧠 Mission",
                "content": """
You are building an engine system with rules:

- The switch controls the whole system.
- The button starts the engine.
- The engine keeps running until the switch turns OFF.
- If the switch is OFF, nothing runs.

Your job is to build these rules using blocks.
"""
            },
            "wiring": {
                "label": "🔌 Wiring",
                "content": """
Match each part to its pin:

🔘 Arm Switch → Pin 2  
🔴 Engage Button → Pin 3  
💡 Engine Light → Pin 9  
🔊 Engine Buzzer → Pin 10  

Find the part in the diagram.  
Follow the wire.  
Match it to the pin.
"""
            },
            "logic": {
                "label": "🧩 Logic",
                "content": """
Think about the flow:

IF switch is OFF  
    everything OFF  

IF switch is ON  
    IF button pressed  
        engine ON  

Remember:
The switch is the boss.
"""
            }
        }
    }
}