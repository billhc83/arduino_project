"""
Step-by-Step Assembly Guide Component for Streamlit
====================================================
Drop this into your existing electronics education app.

HOW TO USE:
1. Import the function: from assembly_guide import assembly_guide
2. Define your steps list (see example at bottom)
3. Call: assembly_guide(image_path, steps, project_title)

FINDING COORDINATES:
Call coordinate_picker(image_path) temporarily to get a crosshair
tool that shows pixel coordinates as you drag sliders over your image.
"""

import streamlit as st
from PIL import Image, ImageDraw
import io
import math
import os
import base64


# ─────────────────────────────────────────────
#  CORE DRAWING FUNCTION
# ─────────────────────────────────────────────

def draw_step_overlay(image_path: str, step: dict, step_number: int, total_steps: int) -> bytes:
    """
    Opens the base image and draws highlight overlays for the current step.

    New step dict format (all keys optional except instruction):
      highlights   list of dicts:
                     {"pos": (x, y),              "shape": "circle"}   — single hole/pin
                     {"pos": (x1, y1, x2, y2),    "shape": "rect"}    — component area
                     {"pos": (x, y),              "shape": "arrow", "direction": "down"} — arrow only
                   direction options: "up", "down", "left", "right"
      greyout      bool — dim everything outside the highlighted areas (default False)
      color        "#RRGGBB" — active highlight color override
      label        str — text label (placed near first highlight)

    Legacy keys still work unchanged:
      highlight    (x, y)        — single circle (old format)
      arrow_from / arrow_to      — arrow between two explicit points
      previous_highlights        — set automatically by assembly_guide()
    """
    img = Image.open(image_path).convert("RGBA")
    w, h = img.size

    COLORS = {
        "active":    (255, 165,   0, 220),
        "previous":  (100, 200, 100, 130),
        "arrow":     (255,  80,  80, 240),
        "label_bg":  ( 20,  20,  20, 210),
        "label_fg":  (255, 255, 255, 255),
        "greyout":   (  0,   0,   0, 160),
    }

    # Resolve active color
    active_color = COLORS["active"]
    if "color" in step:
        hx = step["color"].lstrip("#")
        r, g, b = tuple(int(hx[i:i+2], 16) for i in (0, 2, 4))
        active_color = (r, g, b, 220)

    # ── Normalise highlights into a unified list ─────────────────────────
    # Supports both new "highlights" list and legacy "highlight" single tuple
    raw_highlights = step.get("highlights", [])
    if "highlight" in step:
        raw_highlights = [{"pos": step["highlight"], "shape": "circle"}] + list(raw_highlights)

    # ── Helper: get bounding box of a highlight for greyout masking ──────
    def highlight_bbox(h, padding=28):
        shape = h.get("shape", "circle")
        pos   = h["pos"]
        if shape == "rect":
            x1, y1, x2, y2 = pos
            return (x1 - padding, y1 - padding, x2 + padding, y2 + padding)
        else:  # circle or arrow — treat as point
            cx, cy = pos[0], pos[1]
            return (cx - padding, cy - padding, cx + padding, cy + padding)

    # ── GREYOUT — draw dark veil then punch clear windows ────────────────
    if step.get("greyout", False) and raw_highlights:
        veil = Image.new("RGBA", img.size, (0, 0, 0, 0))
        vd   = ImageDraw.Draw(veil)
        # Full dark overlay
        vd.rectangle([(0, 0), (w, h)], fill=COLORS["greyout"])
        # Punch out a clear ellipse/rect for each active highlight
        for hl in raw_highlights:
            shape = hl.get("shape", "circle")
            pos   = hl["pos"]
            pad   = 2
            if shape == "rect":
                x1, y1, x2, y2 = pos
                vd.rounded_rectangle(
                    [(x1-pad, y1-pad), (x2+pad, y2+pad)],
                    radius=12,
                    fill=(0, 0, 0, 0),
                )
            else:
                cx, cy = pos[0], pos[1]
                # Use radius from highlight dict, add padding for greyout window
                r = hl.get("radius", 25) + 2
                vd.ellipse([(cx-r, cy-r), (cx+r, cy+r)], fill=(0, 0, 0, 0))
        img = Image.alpha_composite(img, veil)

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw    = ImageDraw.Draw(overlay)


    # ── DRAW EACH ACTIVE HIGHLIGHT ─────────────────────────────────────────
    def draw_circle_highlight(cx, cy, color, label_num, radius=25):
        """Empty function - greyout does all the work."""
        pass


    def draw_rect_highlight(x1, y1, x2, y2, color):
        """Empty function - greyout does all the work."""
        pass


    def draw_arrow_highlight(cx, cy, color, direction="down"):
        """Empty function - greyout does all the work."""
        pass


    for hl in raw_highlights:
        shape = hl.get("shape", "circle")
        pos   = hl["pos"]
        color = active_color

        if shape == "circle":
            radius = hl.get("radius", 25)  # default 25px if not specified
            draw_circle_highlight(pos[0], pos[1], color, step_number, radius)
        elif shape == "rect":
            draw_rect_highlight(pos[0], pos[1], pos[2], pos[3], color)
        elif shape == "arrow":
            direction = hl.get("direction", "down")
            draw_arrow_highlight(pos[0], pos[1], color, direction)

    # ── LEGACY arrow_from / arrow_to ─────────────────────────────────────
    if "arrow_from" in step and "arrow_to" in step:
        ax, ay = step["arrow_from"]
        bx, by = step["arrow_to"]
        draw.line([(ax, ay), (bx, by)], fill=COLORS["arrow"], width=3)
        angle    = math.atan2(by - ay, bx - ax)
        head_len = 14
        head_ang = math.pi / 6
        draw.polygon([
            (bx, by),
            (bx - head_len * math.cos(angle - head_ang),
             by - head_len * math.sin(angle - head_ang)),
            (bx - head_len * math.cos(angle + head_ang),
             by - head_len * math.sin(angle + head_ang)),
        ], fill=COLORS["arrow"])

    # ── TEXT LABEL (near first highlight) ─────────────────────────────────
    label_pos = None
    if raw_highlights:
        first = raw_highlights[0]
        pos   = first["pos"]
        if first.get("shape") == "rect":
            label_pos = (pos[0], pos[1])
        else:
            label_pos = (pos[0], pos[1])
    elif "label" in step and "highlight" in step:
        label_pos = step["highlight"]

    if "label" in step and label_pos:
        lx = label_pos[0] + 30
        ly = label_pos[1] - 14
        label   = step["label"]
        text_w  = len(label) * 7 + 14
        draw.rounded_rectangle(
            [(lx-6, ly-4), (lx+text_w, ly+20)],
            radius=6,
            fill=COLORS["label_bg"],
        )
        draw.text((lx, ly), label, fill=COLORS["label_fg"])

    final = Image.alpha_composite(img, overlay)
    buf   = io.BytesIO()
    final.convert("RGB").save(buf, format="PNG")
    return buf.getvalue()



# ─────────────────────────────────────────────
#  HOVER ZOOM COMPONENT
# ─────────────────────────────────────────────

def hover_zoom_at_cursor(image, height=500, zoom_factor=2.5, key="unique"):
    """
    Displays a PIL image with smooth cursor-tracking zoom on hover.
    Hover over any part of the image to zoom into that exact spot.

    Args:
        image:       PIL Image object (already rendered with overlays)
        height:      Display height in pixels
        zoom_factor: How much to zoom in on hover (default 2.5x)
        key:         Unique key — must be different for each call on the page
    """
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # Sanitise key so it is safe as an HTML id and CSS selector
    # (colons, spaces, slashes all break CSS id selectors)
    safe_key = "".join(c if c.isalnum() else "_" for c in str(key))
    container_id = f"zc{safe_key}"   # prefix with letter so id never starts with digit

    html_code = f"""<!DOCTYPE html>
<html>
<head>
<style>
  body {{ margin: 0; padding: 0; background: transparent; overflow: hidden; }}
  .outer-{safe_key} {{
      width: 100%;
      height: {height}px;
      overflow: hidden;
      border-radius: 10px;
      background: #ffffff;
      cursor: crosshair;
  }}
  #{container_id} {{
      width: 100%;
      height: 100%;
      display: block;
      object-fit: contain;
      transition: transform 0.1s ease-out;
      transform-origin: center center;
      will-change: transform;
  }}
</style>
</head>
<body>
  <div class="outer-{safe_key}">
    <img id="{container_id}" src="data:image/png;base64,{img_str}">
  </div>
  <script>
  (function() {{
      const img = document.getElementById("{container_id}");
      const outer = img.parentElement;
      let isHovered = false;

      outer.addEventListener("mouseenter", function() {{
          isHovered = true;
          img.style.transform = "scale({zoom_factor})";
      }});

      outer.addEventListener("mousemove", function(e) {{
          if (!isHovered) return;
          const rect = outer.getBoundingClientRect();
          const x = ((e.clientX - rect.left) / rect.width) * 100;
          const y = ((e.clientY - rect.top) / rect.height) * 100;
          img.style.transformOrigin = x + "% " + y + "%";
      }});

      outer.addEventListener("mouseleave", function() {{
          isHovered = false;
          img.style.transform = "scale(1)";
          img.style.transformOrigin = "center center";
      }});
  }})();
  </script>
</body>
</html>"""
    st.components.v1.html(html_code, height=height + 10)

# ─────────────────────────────────────────────
#  MAIN COMPONENT FUNCTION
# ─────────────────────────────────────────────

def assembly_guide(image_path: str, steps: list, project_title: str = "Assembly Guide"):
    """
    Renders a step-by-step assembly guide widget in Streamlit.

    Args:
        image_path:    Path to your Fritzing breadboard image.
        steps:         List of step dicts.
        project_title: Title shown at the top of the guide.

    Step dict format:
        {
            "instruction": "Place the LED long leg in row 10, column E",
            "tip":         "The long leg is positive — it's called the anode!",  # optional
            "highlight":   (280, 200),     # pixel coords on image
            "label":       "LED +",        # optional text label on image
            "arrow_from":  (200, 150),     # optional
            "arrow_to":    (280, 200),     # optional
            "color":       "#f5a623",      # optional hex color override
        }
    """

    state_key = f"guide_{project_title.replace(' ', '_')}"
    if state_key not in st.session_state:
        st.session_state[state_key] = 0

    current_step = st.session_state[state_key]
    total_steps  = len(steps)
    step         = steps[current_step]

    enriched_step = dict(step)
    # Collect previous step positions for the dimmed green rings.
    # Works with both legacy "highlight": (x,y) and new "highlights": [...]
    prev_positions = []
    for s in steps[:current_step]:
        if "highlight" in s:
            prev_positions.append(s["highlight"])
        for hl in s.get("highlights", []):
            if hl.get("shape", "circle") in ("circle", "arrow"):
                pos = hl["pos"]
                prev_positions.append((pos[0], pos[1]))
            elif hl.get("shape") == "rect":
                x1, y1, x2, y2 = hl["pos"]
                prev_positions.append(((x1+x2)//2, (y1+y2)//2))
    enriched_step["previous_highlights"] = prev_positions

    # Header
    st.markdown(
        f"""
        <div style="
            background:linear-gradient(135deg,#e8f4f8 0%,#d4e7f0 100%);
            border-radius:16px; padding:20px 28px; margin-bottom:16px;
            border-left:5px solid #2196F3;
        ">
            <h2 style="color:#1976D2;margin:0 0 4px 0;font-family:'Georgia',serif;">
                🔧 {project_title}
            </h2>
            <p style="color:#455a64;margin:0;font-size:14px;">
                Follow the steps below — build one connection at a time!
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Progress bar
    progress  = (current_step + 1) / total_steps
    bar_color = "#42a5f5" if current_step < total_steps - 1 else "#66bb6a"

    st.markdown(
        f"""
        <div style="margin-bottom:8px;">
            <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                <span style="color:#546e7a;font-size:13px;font-weight:600;">
                    STEP {current_step + 1} OF {total_steps}
                </span>
                <span style="color:{bar_color};font-size:13px;font-weight:600;">
                    {int(progress * 100)}% complete
                </span>
            </div>
            <div style="background:#e0e0e0;border-radius:10px;height:10px;overflow:hidden;">
                <div style="
                    background:linear-gradient(90deg,{bar_color},#2196F3);
                    width:{progress * 100}%;height:100%;border-radius:10px;
                "></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Annotated image — rendered via hover zoom so kids can inspect connections closely
    if os.path.exists(image_path):
        img_bytes = draw_step_overlay(image_path, enriched_step, current_step + 1, total_steps)
        annotated_pil = Image.open(io.BytesIO(img_bytes))
        hover_zoom_at_cursor(annotated_pil, key=f"{state_key}_step{current_step}")
    else:
        st.warning(f"Image not found at `{image_path}` — add your Fritzing image to see the overlay.")
        placeholder = Image.new("RGB", (700, 400), color="#1a1a2e")
        pd = ImageDraw.Draw(placeholder)
        pd.text((350, 200), "Your Fritzing\nBreadboard Image Here", fill="#f5a623", anchor="mm")
        hover_zoom_at_cursor(placeholder, key=f"{state_key}_placeholder")

    # Instruction card
    tip_html = ""
    if "tip" in step:
        tip_html = f"""
        <div style="
            background:#e8f5e9;border:1px solid #81c784;border-radius:10px;
            padding:10px 14px;margin-top:12px;display:flex;gap:10px;align-items:flex-start;
        ">
            <span style="font-size:18px;">💡</span>
            <span style="color:#2e7d32;font-size:14px;line-height:1.5;">{step['tip']}</span>
        </div>
        """

    st.markdown(
        f"""
        <div style="
            background:#f5f5f5;border:1px solid #e0e0e0;border-radius:14px;
            padding:20px 24px;margin:16px 0;
        ">
            <div style="display:flex;align-items:flex-start;gap:16px;">
                <div style="
                    background:#2196F3;color:#ffffff;font-weight:bold;font-size:18px;
                    min-width:40px;height:40px;border-radius:50%;
                    display:flex;align-items:center;justify-content:center;flex-shrink:0;
                ">{current_step + 1}</div>
                <p style="color:#212121;font-size:17px;margin:6px 0 0 0;line-height:1.6;">
                    {step['instruction']}
                </p>
            </div>
            {tip_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if current_step > 0:
            if st.button("◀ Back", key=f"{state_key}_back", use_container_width=True):
                st.session_state[state_key] -= 1
                st.rerun()

    with col2:
        dots_html = ""
        for i in range(total_steps):
            if i == current_step:
                dot = "background:#f5a623;width:14px;height:14px;"
            elif i < current_step:
                dot = "background:#4ecdc4;width:10px;height:10px;opacity:0.8;"
            else:
                dot = "background:#2a2a5a;width:10px;height:10px;"
            dots_html += f'<div style="border-radius:50%;{dot}display:inline-block;margin:0 3px;"></div>'
        st.markdown(
            f'<div style="text-align:center;padding-top:8px;">{dots_html}</div>',
            unsafe_allow_html=True,
        )

    with col3:
        if current_step < total_steps - 1:
            if st.button("Next ▶", key=f"{state_key}_next",
                         use_container_width=True, type="primary"):
                st.session_state[state_key] += 1
                st.rerun()
        else:
            if st.button("✅ Done!", key=f"{state_key}_done",
                         use_container_width=True, type="primary"):
                st.balloons()
                st.session_state[state_key] = 0

    if current_step == total_steps - 1:
        st.success("🎉 **You've reached the final step!** Double-check all your connections, then hit Done!")


# ─────────────────────────────────────────────
#  COORDINATE PICKER (developer helper)
# ─────────────────────────────────────────────

def coordinate_picker(image_path: str):
    """
    Interactive coordinate picker with click and drag modes.
    
    CIRCLE MODE: Click anywhere → copies circle highlight coords
    RECT MODE: Click and drag → copies rect highlight coords
    
    Much faster than sliders for building your steps list.
    """
    with st.expander("🎯 Coordinate Picker (click to close when done)", expanded=True):
        if not os.path.exists(image_path):
            st.warning(f"Image not found: `{image_path}`")
            return

        img = Image.open(image_path)
        w, h = img.size
        
        # Convert to base64 for embedding
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_b64 = base64.b64encode(buffered.getvalue()).decode()

        mode = st.radio("Pick mode:", ["Circle (click)", "Rectangle (drag)"], horizontal=True, key="picker_mode")
        
        if mode == "Circle (click)":
            circle_radius = st.number_input("Circle radius (px):", min_value=10, max_value=100, value=25, step=5, key="circle_r")
        else:
            circle_radius = 25  # not used in rect mode
        
        st.caption(f"Image size: {w} × {h} px")
        if mode == "Circle (click)":
            st.info("👆 **Click** anywhere on the image below to capture circle coordinates. The snippet will appear below and copy to your clipboard.")
        else:
            st.info("👆 **Click and drag** on the image to draw a rectangle. Release to capture. The snippet will appear below.")

        # HTML canvas for interactive picking
        html_code = f"""<!DOCTYPE html>
<html>
<head>
<style>
body {{ margin: 0; padding: 20px; background: #fafafa; font-family: monospace; }}
.container {{ max-width: 100%; margin: 0 auto; }}
#canvas {{ 
    border: 2px solid #2196F3; 
    cursor: crosshair; 
    display: block;
    max-width: 100%;
    background: white;
}}
#output {{ 
    margin-top: 15px; 
    padding: 12px; 
    background: #f5f5f5; 
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    font-size: 13px;
    color: #212121;
    display: none;
}}
.coords {{ 
    background: #e3f2fd; 
    padding: 8px 12px; 
    border-radius: 6px; 
    margin-top: 8px;
    border-left: 3px solid #2196F3;
}}
</style>
</head>
<body>
<div class="container">
    <canvas id="canvas" width="{w}" height="{h}"></canvas>
    <div id="output">
        <div style="color: #2e7d32; font-weight: 600;">✓ Copied to clipboard!</div>
        <div class="coords" id="coordText"></div>
    </div>
</div>
<script>
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const output = document.getElementById('output');
const coordText = document.getElementById('coordText');
const mode = "{mode}";

const img = new Image();
img.onload = function() {{
    ctx.drawImage(img, 0, 0);
}};
img.src = "data:image/png;base64,{img_b64}";

let isDrawing = false;
let startX, startY;
let baseImage = null;

// Save base image once loaded
img.onload = function() {{
    ctx.drawImage(img, 0, 0);
    baseImage = ctx.getImageData(0, 0, canvas.width, canvas.height);
}};

function copyToClipboard(text) {{
    navigator.clipboard.writeText(text).then(() => {{
        output.style.display = 'block';
        coordText.textContent = text;
        setTimeout(() => {{
            output.style.display = 'none';
        }}, 3000);
    }});
}}

if (mode === "Circle (click)") {{
    canvas.addEventListener('click', function(e) {{
        const rect = canvas.getBoundingClientRect();
        const x = Math.round((e.clientX - rect.left) * (canvas.width / rect.width));
        const y = Math.round((e.clientY - rect.top) * (canvas.height / rect.height));
        
        // Redraw base image
        if (baseImage) ctx.putImageData(baseImage, 0, 0);
        
        // Draw preview circle
        const radius = {circle_radius};
        ctx.strokeStyle = '#2196F3';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, 2 * Math.PI);
        ctx.stroke();
        
        ctx.fillStyle = '#2196F3';
        ctx.beginPath();
        ctx.arc(x, y, radius * 0.7, 0, 2 * Math.PI);
        ctx.fill();
        
        const snippet = `{{"pos": (${{x}}, ${{y}}), "shape": "circle", "radius": ${{radius}}}}`;
        copyToClipboard(snippet);
    }});
}} else {{
    // Rectangle drag mode
    canvas.addEventListener('mousedown', function(e) {{
        const rect = canvas.getBoundingClientRect();
        startX = Math.round((e.clientX - rect.left) * (canvas.width / rect.width));
        startY = Math.round((e.clientY - rect.top) * (canvas.height / rect.height));
        isDrawing = true;
    }});
    
    canvas.addEventListener('mousemove', function(e) {{
        if (!isDrawing) return;
        const rect = canvas.getBoundingClientRect();
        const x = Math.round((e.clientX - rect.left) * (canvas.width / rect.width));
        const y = Math.round((e.clientY - rect.top) * (canvas.height / rect.height));
        
        if (baseImage) ctx.putImageData(baseImage, 0, 0);
        
        ctx.strokeStyle = '#2196F3';
        ctx.lineWidth = 3;
        ctx.strokeRect(startX, startY, x - startX, y - startY);
        
        ctx.fillStyle = 'rgba(33, 150, 243, 0.15)';
        ctx.fillRect(startX, startY, x - startX, y - startY);
    }});
    
    canvas.addEventListener('mouseup', function(e) {{
        if (!isDrawing) return;
        isDrawing = false;
        
        const rect = canvas.getBoundingClientRect();
        const endX = Math.round((e.clientX - rect.left) * (canvas.width / rect.width));
        const endY = Math.round((e.clientY - rect.top) * (canvas.height / rect.height));
        
        const x1 = Math.min(startX, endX);
        const y1 = Math.min(startY, endY);
        const x2 = Math.max(startX, endX);
        const y2 = Math.max(startY, endY);
        
        const snippet = `{{"pos": (${{x1}}, ${{y1}}, ${{x2}}, ${{y2}}), "shape": "rect"}}`;
        copyToClipboard(snippet);
    }});
    
    canvas.addEventListener('mouseleave', function() {{
        if (isDrawing) {{
            isDrawing = false;
            if (baseImage) ctx.putImageData(baseImage, 0, 0);
        }}
    }});
}}
</script>
</body>
</html>"""
        
        st.components.v1.html(html_code, height=h + 100, scrolling=False)
        
        st.markdown("---")
        st.caption("**Tip:** Switch between Circle and Rectangle mode using the radio buttons above. Each click/drag automatically copies the coordinate snippet — just paste it into your steps list!")

# ─────────────────────────────────────────────
#  DEMO — run with: streamlit run assembly_guide.py
# ─────────────────────────────────────────────

if __name__ == "__main__":

    st.set_page_config(
        page_title="Circuit Assembly Guide",
        page_icon="⚡",
        layout="wide",
    )

    # Use st.html() for <style> injection — st.markdown() strips style tags in modern Streamlit
    st.html("""
    <style>
        .stApp { background: #0d0d1f; }
        .stButton > button { border-radius: 10px !important; font-weight: 600 !important; }
    </style>
    """)

    st.title("⚡ Circuit Assembly Guide — Demo")
    st.caption("Replace DEMO_IMAGE with your Fritzing export path to use your own breadboard image.")

    DEMO_IMAGE = "demo_breadboard.png"

    # Generate a placeholder breadboard image for the demo
    if not os.path.exists(DEMO_IMAGE):
        demo_img = Image.new("RGB", (700, 420), color="#2c3e50")
        d = ImageDraw.Draw(demo_img)
        for row in range(10, 410, 15):
            for col in range(50, 660, 20):
                d.ellipse([(col-4, row-4), (col+4, row+4)], fill="#3d5166", outline="#546e7a")
        d.rectangle([(15,  5), (32, 415)], fill="#c0392b")
        d.rectangle([(668, 5), (685, 415)], fill="#2980b9")
        d.text((350, 210), "Demo Breadboard", fill="#546e7a", anchor="mm")
        demo_img.save(DEMO_IMAGE)

    demo_steps = [
        {
            # Legacy single highlight — still works exactly as before
            "instruction": "Find the two long rails running down the sides of your breadboard. The red strip is Power (+) and the blue strip is Ground (−).",
            "tip": "Always connect power and ground first — it makes everything else easier to think about!",
            "highlight": (24, 80),
            "label": "Power rail",
            "color": "#e74c3c",
            "greyout": True,
        },
        {
            # Single circle highlight with greyout
            "instruction": "Place your LED so the LONG leg (anode +) goes into row 10, column E, and the SHORT leg into row 10, column D.",
            "tip": "Not sure which leg is longer? Look closely — one is slightly longer. That's the positive (+) leg.",
            "highlights": [
                {"pos": (310, 145), "shape": "circle"},
            ],
            "label": "LED here",
            "color": "#f5a623",
            "greyout": True,
        },
        {
            # Rect highlight around a component area
            "instruction": "Insert a 330Ω resistor between row 10, column B and row 16, column B. It acts like a speed bump to protect your LED!",
            "tip": "Resistors don't have a direction — either way round is fine.",
            "highlights": [
                {"pos": (285, 155, 340, 245), "shape": "rect"},
            ],
            "label": "Resistor",
            "color": "#9b59b6",
            "greyout": True,
        },
        {
            # Multiple circles — both ends of a wire
            "instruction": "Connect a RED jumper wire from the (+) power rail to row 16, column A. This brings power to your resistor.",
            "highlights": [
                {"pos": (24, 235),  "shape": "circle"},
                {"pos": (165, 235), "shape": "circle"},
            ],
            "label": "Red wire",
            "color": "#e74c3c",
            "greyout": True,
        },
        {
            # Arrow pointing at a connection point
            "instruction": "Connect a BLACK jumper wire from row 10, column C to the (−) ground rail. This completes the loop!",
            "highlights": [
                {"pos": (310, 145), "shape": "arrow", "direction": "up"},
                {"pos": (460, 145), "shape": "arrow", "direction": "up"},
            ],
            "color": "#3498db",
            "greyout": True,
        },
        {
            # No greyout on final step — show the full completed board
            "instruction": "Plug in your 9V battery — red clip to (+) rail, black clip to (−) rail. Your LED should glow! 🎉",
            "tip": "If it doesn't light up: check the LED is the right way round, and make sure all legs are fully pushed into the holes.",
            "highlights": [
                {"pos": (24, 350), "shape": "circle"},
            ],
            "label": "Battery",
            "color": "#2ecc71",
            "greyout": False,
        },
    ]

    # Uncomment while finding coordinates for your own image:
    # coordinate_picker(DEMO_IMAGE)

    assembly_guide(DEMO_IMAGE, demo_steps, "Project 1: LED Night Light")