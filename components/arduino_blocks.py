import re
import streamlit.components.v1 as components


# ── Sketch parser ─────────────────────────────────────────────────────

def extract_brace_body(code, start):
    depth = 0
    i = start
    while i < len(code):
        if code[i] == '{': depth += 1
        elif code[i] == '}':
            depth -= 1
            if depth == 0:
                return code[start+1:i].strip(), i+1
        i += 1
    return '', len(code)


def extract_condition(code, start):
    depth = 0
    i = start
    while i < len(code):
        if code[i] == '(': depth += 1
        elif code[i] == ')':
            depth -= 1
            if depth == 0:
                return code[start+1:i].strip(), i+1
        i += 1
    return '', len(code)


def parse_condition(cond_str):
    result = {
        'left': '', 'op': '==', 'right': '',
        'joiner': 'none', 'left2': '', 'op2': '==', 'right2': ''
    }
    and_match = re.search(r'\s*(&&|\|\|)\s*', cond_str)
    if and_match:
        result['joiner'] = 'and' if and_match.group(1) == '&&' else 'or'
        parse_side(cond_str[:and_match.start()].strip(), result, 'left',  'op',  'right')
        parse_side(cond_str[and_match.end():].strip(),   result, 'left2', 'op2', 'right2')
    else:
        parse_side(cond_str, result, 'left', 'op', 'right')
    return result


def parse_side(s, result, lkey, opkey, rkey):
    for op in ['>=', '<=', '!=', '==', '>', '<']:
        if op in s:
            parts = s.split(op, 1)
            result[lkey]  = parts[0].strip()
            result[opkey] = op
            result[rkey]  = parts[1].strip()
            return
    result[lkey] = s.strip()


def parse_blocks(code):
    blocks = []
    i = 0
    code = code.strip()
    while i < len(code):
        while i < len(code) and code[i] in ' \t\n\r': i += 1
        if i >= len(code): break
        if code[i:i+2] == '//':
            end = code.find('\n', i)
            i = end+1 if end != -1 else len(code)
            continue
        if code[i:i+2] == '/*':
            end = code.find('*/', i)
            i = end+2 if end != -1 else len(code)
            continue
        if re.match(r'if\s*\(', code[i:]):
            paren_start = code.index('(', i)
            cond_str, after_paren = extract_condition(code, paren_start)
            brace_start = code.index('{', after_paren)
            body_str, after_body = extract_brace_body(code, brace_start)
            block = {
                'type': 'ifblock',
                'condition': parse_condition(cond_str),
                'ifbody':   parse_blocks(body_str),
                'elseifs':  [],
                'elsebody': None
            }
            i = after_body
            while i < len(code):
                while i < len(code) and code[i] in ' \t\n\r': i += 1
                if re.match(r'else\s+if\s*\(', code[i:]):
                    paren_start = code.index('(', i)
                    ei_cond, after_paren = extract_condition(code, paren_start)
                    brace_start = code.index('{', after_paren)
                    ei_body, after_body = extract_brace_body(code, brace_start)
                    block['elseifs'].append({
                        'condition': parse_condition(ei_cond),
                        'body': parse_blocks(ei_body)
                    })
                    i = after_body
                elif re.match(r'else\s*\{', code[i:]) or (re.match(r'else', code[i:]) and not re.match(r'else\s+if', code[i:])):
                    brace_start = code.index('{', i)
                    else_body, after_body = extract_brace_body(code, brace_start)
                    block['elsebody'] = parse_blocks(else_body)
                    i = after_body
                    break
                else:
                    break
            blocks.append(block)
            continue
        semi = code.find(';', i)
        if semi == -1: break
        line = code[i:semi+1].strip()
        i = semi + 1
        m = re.match(r'int\s+(\w+)\s*=\s*(-?\d+)\s*;', line)
        if m: blocks.append({'type':'intvar','params':[m.group(1),m.group(2)]}); continue
        m = re.match(r'pinMode\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)\s*;', line)
        if m: blocks.append({'type':'pinmode','params':[m.group(1),m.group(2)]}); continue
        m = re.match(r'digitalWrite\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)\s*;', line)
        if m: blocks.append({'type':'digitalwrite','params':[m.group(1),m.group(2)]}); continue
        m = re.match(r'delay\s*\(\s*(\d+)\s*\)\s*;', line)
        if m: blocks.append({'type':'delay','params':[m.group(1)]}); continue
        m = re.match(r'Serial\.begin\s*\(\s*(\d+)\s*\)\s*;', line)
        if m: blocks.append({'type':'serialbegin','params':[m.group(1)]}); continue
        m = re.match(r'Serial\.print(?:ln)?\s*\(\s*"([^"]*)"\s*\)\s*;', line)
        if m: blocks.append({'type':'serialprint','params':[m.group(1)]}); continue
    return blocks


def parse_sketch(sketch_code):
    result = {'global': [], 'setup': [], 'loop': []}
    setup_start = re.search(r'void\s+setup\s*\(', sketch_code)
    global_code = sketch_code[:setup_start.start()].strip() if setup_start else ''
    setup_m = re.search(r'void\s+setup\s*\(\s*\)\s*\{', sketch_code)
    loop_m  = re.search(r'void\s+loop\s*\(\s*\)\s*\{', sketch_code)
    setup_code = extract_brace_body(sketch_code, setup_m.end()-1)[0] if setup_m else ''
    loop_code  = extract_brace_body(sketch_code, loop_m.end()-1)[0]  if loop_m  else ''
    result['global'] = parse_blocks(global_code)
    result['setup']  = parse_blocks(setup_code)
    result['loop']   = parse_blocks(loop_code)
    return result


# ── Preset sketches ───────────────────────────────────────────────────

PRESETS = {
    'engine_start': """
void setup() {
  pinMode(2, INPUT);   // Arm switch
  pinMode(3, INPUT);   // Engage button
  pinMode(9, OUTPUT);  // Engine light
  pinMode(10, OUTPUT); // Engine buzzer
}

void loop() {

  if (digitalRead(2) == HIGH) {   // Switch ON

    digitalWrite(9, HIGH);        // Light ON (armed)

    if (digitalRead(3) == HIGH) {
      digitalWrite(10, HIGH);     // Start engine
    }

  } else {                        // Switch OFF

    digitalWrite(9, LOW);         // Light OFF
    digitalWrite(10, LOW);        // Engine OFF (reset)

  }
}
""",
    'Serial Hello': """
void setup() {
  Serial.begin(9600);
  Serial.print("Hello World");
}
void loop() {
  delay(1000);
}
""",
    'Button Read': """
int buttonPin = 2;
int ledPin = 13;
void setup() {
  pinMode(buttonPin, INPUT);
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}
void loop() {
  delay(100);
}
""",
}


# ── Component ─────────────────────────────────────────────────────────

def arduino_block_coder(height=550, preset=None, drawer_content=None):

    # Guard: if a string is passed positionally treat it as preset
    if isinstance(height, str):
        preset = height
        height = 550

    # Build initial block state from preset if provided
    if preset and preset in PRESETS:
        blocks = parse_sketch(PRESETS[preset])
        def cond_to_js(c):
            return ("{"
                    "left:'" + c['left']   + "',"
                    "op:'"   + c['op']     + "',"
                    "right:'"  + c['right']  + "',"
                    "joiner:'" + c['joiner'] + "',"
                    "left2:'"  + c['left2']  + "',"
                    "op2:'"    + c['op2']    + "',"
                    "right2:'" + c['right2'] + "'"
                    "}")
        def block_to_js(b):
            if b['type'] == 'ifblock':
                ifbody_js  = '[' + ','.join(block_to_js(x) for x in b['ifbody']) + ']'
                elseifs_js = '[' + ','.join(
                    '{condition:' + cond_to_js(ei['condition']) + ',body:' +
                    '[' + ','.join(block_to_js(x) for x in ei['body']) + ']' + '}'
                    for ei in b['elseifs']
                ) + ']'
                else_js = ('null' if b['elsebody'] is None
                           else '[' + ','.join(block_to_js(x) for x in b['elsebody']) + ']')
                return ('{id:Date.now()+Math.random(),type:\'ifblock\','
                        'condition:' + cond_to_js(b['condition']) + ','
                        'ifbody:' + ifbody_js + ','
                        'elseifs:' + elseifs_js + ','
                        'elsebody:' + else_js + '}')
            blank = str(['' for _ in b['params']])
            return "{id:Date.now()+Math.random(),type:'" + b['type'] + "',params:" + blank + "}"
        gb = '[' + ','.join(block_to_js(b) for b in blocks['global']) + ']'
        sb = '[' + ','.join(block_to_js(b) for b in blocks['setup'])  + ']'
        lb = '[' + ','.join(block_to_js(b) for b in blocks['loop'])   + ']'
        initial_js = "SECTIONS.global=" + gb + ";SECTIONS.setup=" + sb + ";SECTIONS.loop=" + lb + ";"
    else:
        initial_js = ""

    css = (
        "* { box-sizing:border-box; margin:0; padding:0; }"
        "html, body { width:100%; height:" + str(height) + "px; overflow:hidden;"
        "  background:#f6f8fa; font-family:'Courier New',monospace; color:#24292f; }"
        "#palette { width:110px; flex-shrink:0; background:#ffffff;"
        "  border-right:1px solid #d0d7de; display:flex; flex-direction:column;"
        "  padding:6px; gap:4px; overflow-y:auto; }"
        "#palette::-webkit-scrollbar { width:3px; }"
        "#palette::-webkit-scrollbar-thumb { background:#d0d7de; }"
        ".pal-title { font-size:9px; color:#57606a; text-transform:uppercase;"
        "  letter-spacing:.06em; padding:2px 0 4px 0; border-bottom:1px solid #d0d7de; margin-bottom:2px; }"
        ".block-btn { width:100%; padding:5px 6px; border-radius:5px; border:1px solid #d0d7de;"
        "  background:#f6f8fa; cursor:pointer; font-size:10px; color:#24292f;"
        "  font-family:inherit; text-align:left; }"
        ".block-btn:hover { border-color:#0969da; color:#0969da; background:#ddf4ff; }"
        "#workspace { flex:1; display:flex; flex-direction:column; gap:4px;"
        "  padding:6px 6px 10px 6px; overflow:hidden; min-width:0; }"
        ".section { flex:1; border:2px solid #d0d7de; border-radius:7px;"
        "  background:#ffffff; padding:5px 7px; cursor:pointer; overflow-y:auto; min-height:0; }"
        ".section::-webkit-scrollbar { width:3px; }"
        ".section::-webkit-scrollbar-thumb { background:#d0d7de; }"
        ".section h3 { font-size:9px; font-weight:600; letter-spacing:.06em; text-transform:uppercase;"
        "  color:#57606a; pointer-events:none; user-select:none; margin-bottom:3px; }"
        ".s-global.active { border-color:#0969da; background:#ddf4ff; }"
        ".s-global.active h3 { color:#0969da; }"
        ".s-setup.active  { border-color:#1a7f37; background:#dafbe1; }"
        ".s-setup.active  h3 { color:#1a7f37; }"
        ".s-loop.active   { border-color:#9a6700; background:#fff8c5; }"
        ".s-loop.active   h3 { color:#9a6700; }"
        ".ws-block { display:flex; align-items:center; flex-wrap:wrap; gap:4px;"
        "  background:#f6f8fa; border:1px solid #d0d7de; border-radius:5px;"
        "  padding:3px 6px; margin-bottom:3px; }"
        ".blk-name { font-size:9px; font-weight:bold; color:#0969da; min-width:60px; }"
        ".blk-field { display:flex; flex-direction:column; font-size:8px; }"
        ".blk-field label { color:#57606a; margin-bottom:1px; }"
        ".blk-input { font-size:9px; padding:2px 3px; width:64px; background:#ffffff;"
        "  color:#24292f; border:1px solid #d0d7de; border-radius:3px; font-family:inherit; }"
        ".blk-input:focus { outline:none; border-color:#0969da; }"
        ".act { background:none; border:1px solid #d0d7de; color:#57606a; cursor:pointer;"
        "  font-size:9px; padding:1px 3px; border-radius:3px; }"
        ".act:hover { color:#24292f; border-color:#57606a; background:#f6f8fa; }"
        ".if-block { margin-bottom:3px; }"
        ".if-header, .elseif-header, .else-header { display:flex; align-items:center;"
        "  gap:4px; flex-wrap:wrap; background:#fff8c5; border:1px solid #d4a72c; padding:3px 6px; }"
        ".if-header    { border-radius:5px 5px 0 0; }"
        ".elseif-header { border-top:none; }"
        ".else-header   { border-top:none; }"
        ".if-keyword { font-size:9px; font-weight:bold; color:#cf222e; }"
        ".cond-field { display:flex; flex-direction:column; font-size:8px; }"
        ".cond-field label { color:#57606a; margin-bottom:1px; }"
        ".cond-input  { font-size:9px; padding:2px 3px; width:100px; background:#ffffff;"
        "  color:#24292f; border:1px solid #d0d7de; border-radius:3px; font-family:inherit; }"
        ".cond-select { font-size:9px; padding:2px 3px; width:80px; background:#ffffff;"
        "  color:#24292f; border:1px solid #d0d7de; border-radius:3px; font-family:inherit; }"
        ".cond-joiner { font-size:9px; padding:2px 3px; width:46px; background:#ffffff;"
        "  color:#9a6700; border:1px solid #d4a72c; border-radius:3px; font-family:inherit; }"
        ".cond-input:focus, .cond-select:focus, .cond-joiner:focus { outline:none; border-color:#cf222e; }"
        ".if-body { border-left:1px dashed #d0d7de; border-right:1px dashed #d0d7de;"
        "  border-bottom:none; padding:4px 4px 4px 60px; min-height:28px; cursor:pointer; }"
        ".if-body.last { border-bottom:1px dashed #d0d7de; border-radius:0 0 5px 5px; }"
        ".if-body:hover { border-color:#57606a; }"
        ".if-body.selected { border-color:#0969da; border-style:solid; background:#ddf4ff; }"
        ".if-body.ancestor { border-color:#84c7fb; border-style:solid; }"
        ".if-block.ancestor > .if-header { border-color:#84c7fb !important; background:#eaf6ff !important; }"
        ".if-block.ancestor > .elseif-header { border-color:#84c7fb !important; background:#eaf6ff !important; }"
        ".if-block.ancestor > .else-header { border-color:#84c7fb !important; background:#eaf6ff !important; }"
        ".body-hint { font-size:8px; color:#bbb; pointer-events:none; padding:2px 0; }"
        "#statusbar { font-size:9px; color:#57606a; padding:3px 7px; flex-shrink:0;"
        "  background:#ffffff; border-bottom:1px solid #d0d7de; }"
        "#statusbar span { color:#0969da; }"
        "#codepanel { width:250px; flex-shrink:0; border-left:1px solid #d0d7de;"
        "  display:flex; flex-direction:column; padding:6px; gap:5px; }"
        "#code-btns { display:flex; gap:5px; flex-shrink:0; }"
        "#msg { font-size:9px; color:#cf222e; opacity:0; transition:opacity 0.3s; flex-shrink:0; min-height:14px; }"
        "#msg.show { opacity:1; }"
        "#codeout { flex:1; background:#f6f8fa; border:1px solid #d0d7de; border-radius:6px;"
        "  padding:6px 7px; font-size:9px; white-space:pre; overflow-y:auto;"
        "  color:#0550ae; line-height:1.5; min-height:0; }"
        "#codeout::-webkit-scrollbar { width:3px; }"
        "#codeout::-webkit-scrollbar-thumb { background:#d0d7de; }"
        ".cbtn { flex:1; padding:4px; border-radius:5px; border:1px solid #d0d7de;"
        "  background:#f6f8fa; color:#24292f; cursor:pointer; font-family:inherit; font-size:9px; }"
        ".cbtn:hover { background:#e6ebf1; }"
        "#app { display:flex; flex-direction:row; width:calc(100% - 22px); height:" + str(height) + "px; position:relative; }"
        "#drawer-tab { position:absolute; right:0; top:0; height:" + str(height) + "px; width:24px;"
        "  background:#e53935; border-left:1px solid #d0d7de;"
        "  display:flex; align-items:center; justify-content:center;"
        "  cursor:pointer; z-index:10; user-select:none; transition:background 0.15s; }"
        "#drawer-tab:hover { background:#e6ebf1; }"
        "#drawer-tab span { writing-mode:vertical-rl; text-orientation:mixed;"
        "  font-size:14px; letter-spacing:.1em; color:#ffffff;"
        "  text-transform:uppercase; transform:rotate(180deg); }"
        "#drawer-tab:hover span { color:#0969da; }"
        "#drawer-panel { position:absolute; right:18px; top:0; height:" + str(height) + "px; width:0;"
        "  background:#ffffff; border-left:1px solid #d0d7de;"
        "  overflow:hidden; z-index:9; transition:width 0.25s ease; display:flex; flex-direction:column; }"
        "#drawer-panel.open { width:600px; }"
        "#drawer-inner { width:600px; height:100%; display:flex; flex-direction:column; flex-shrink:0; }"
        ".drawer-title { font-size:13px; font-weight:700; color:#0969da;"
        "  text-transform:uppercase; letter-spacing:.08em; flex-shrink:0;"
        "  border-bottom:1px solid #d0d7de; padding:12px 14px 8px 14px; }"
        ".drawer-tip { background:#ddf4ff; border-bottom:1px solid #84c7fb;"
        "  padding:8px 14px; font-size:11px; color:#0969da; line-height:1.7; flex-shrink:0; }"
        ".drawer-tabs { display:flex; flex-shrink:0; border-bottom:1px solid #d0d7de; }"
        ".drawer-tab-btn { flex:1; padding:8px 4px; font-size:11px; font-family:inherit;"
        "  background:none; border:none; border-bottom:2px solid transparent;"
        "  color:#57606a; cursor:pointer; text-align:center; transition:color 0.15s; }"
        ".drawer-tab-btn:hover { color:#24292f; }"
        ".drawer-tab-btn.active { color:#0969da; border-bottom-color:#0969da; }"
        ".drawer-tab-panels { flex:1; overflow-y:auto; }"
        ".drawer-tab-panels::-webkit-scrollbar { width:3px; }"
        ".drawer-tab-panels::-webkit-scrollbar-thumb { background:#d0d7de; }"
        ".drawer-tab-panel { display:none; padding:14px; }"
        ".drawer-tab-panel.active { display:block; }"
        ".drawer-tab-panel p { font-size:12px; color:#24292f; line-height:1.8; white-space:pre-wrap; margin-bottom:8px; }"
        ".drawer-tab-panel img { width:100%; border-radius:5px; border:1px solid #d0d7de; margin-top:8px; }"
        ".drawer-tab-panel code { display:inline-block; background:#f6f8fa; border:1px solid #d0d7de;"
        "  border-radius:3px; padding:2px 6px; font-size:11px; color:#953800; font-family:'Courier New',monospace; }"
    )

    # ── Build drawer inner HTML ───────────────────────────────────────────
    if drawer_content is None:
        drawer_content = {
            "title": "&#128214; Reference",
            "tip": "Select a section, then click a block in the palette to add it.",
            "tabs": {
                "start": {
                    "label": "&#128161; Quick Start",
                    "content": "Select Global, setup(), or loop() first.\nThen click any block in the palette to add it to that section."
                }
            }
        }

    # Build tab buttons and panels
    tabs = drawer_content.get("tabs", {})
    tab_keys = list(tabs.keys())

    tab_buttons_html = ""
    tab_panels_html = ""
    for i, key in enumerate(tab_keys):
        tab = tabs[key]
        active_class = " active" if i == 0 else ""
        tab_buttons_html += (
            "<button class='drawer-tab-btn" + active_class + "' "
            "onclick='switchTab(this,\"dtab-" + key + "\")'>"
            + tab.get("label", key) +
            "</button>"
        )
        image_html = "<img src='" + tab["image"] + "' alt=''/>" if "image" in tab else ""
        tab_panels_html += (
            "<div class='drawer-tab-panel" + active_class + "' id='dtab-" + key + "'>"
            "<p>" + tab.get("content", "") + "</p>"
            + image_html +
            "</div>"
        )

    tip_html = "<div class='drawer-tip'>" + drawer_content["tip"] + "</div>" if "tip" in drawer_content else ""

    drawer_html = (
        "<div id='drawer-panel'>"
        "<div id='drawer-inner'>"
        "<div class='drawer-title'>" + drawer_content.get("title", "Info") + "</div>"
        + tip_html +
        "<div class='drawer-tabs'>" + tab_buttons_html + "</div>"
        "<div class='drawer-tab-panels'>" + tab_panels_html + "</div>"
        "</div></div>"
        "<div id='drawer-tab'><span>&#128214; Info</span></div>"
    )

    body = (
        "<div id='statusbar'>click a section or if body to select it</div>"
        "<div id='app'>"
        "<div id='palette'>"
        "<div class='pal-title'>Blocks</div>"
        "<button class='block-btn' data-type='intvar'>int var</button>"
        "<button class='block-btn' data-type='pinmode'>pinMode</button>"
        "<button class='block-btn' data-type='digitalwrite'>digitalWrite</button>"
        "<button class='block-btn' data-type='delay'>delay</button>"
        "<button class='block-btn' data-type='serialbegin'>Serial.begin</button>"
        "<button class='block-btn' data-type='serialprint'>Serial.print</button>"
        "<button class='block-btn' data-type='ifblock'>if statement</button>"
        "</div>"
        "<div id='workspace'>"
        "<div class='section s-global' id='gs'><h3>&#127757; Global</h3></div>"
        "<div class='section s-setup'  id='ss'><h3>&#128295; setup()</h3></div>"
        "<div class='section s-loop'   id='ls'><h3>&#128257; loop()</h3></div>"
        "</div>"
        "<div id='codepanel'>"
        "<div id='code-btns'>"
        "<button class='cbtn' id='copybtn'>&#128203; Copy</button>"
        "<button class='cbtn' id='clrbtn'>&#128465; Clear</button>"
        "</div>"
        "<div id='msg'></div>"
        "<div id='codeout'>// sketch&#10;// appears&#10;// here</div>"
        "</div>"
        + drawer_html +
        "</div>"
    )

    js = (
        "function switchTab(btn,panelId){"
        "  var inner=document.getElementById('drawer-inner');"
        "  inner.querySelectorAll('.drawer-tab-btn').forEach(function(b){b.classList.remove('active');});"
        "  inner.querySelectorAll('.drawer-tab-panel').forEach(function(p){p.classList.remove('active');});"
        "  btn.classList.add('active');"
        "  document.getElementById(panelId).classList.add('active');}"
        "document.addEventListener('DOMContentLoaded',function(){"
        "var B={"
        "intvar:{allowed:['global'],inputs:[{t:'text',l:'Name'},{t:'number',l:'Value'}],"
        "  gen:function(p){return 'int '+(p[0]||'myVar')+' = '+(p[1]||0)+';';}},"
        "pinmode:{allowed:['setup'],inputs:[{t:'text',l:'Pin'},{t:'sel',l:'Mode',o:['OUTPUT','INPUT','INPUT_PULLUP']}],"
        "  gen:function(p){return 'pinMode('+(p[0]||13)+', '+(p[1]||'OUTPUT')+');';}},"
        "digitalwrite:{allowed:['loop','if'],inputs:[{t:'text',l:'Pin'},{t:'sel',l:'Value',o:['HIGH','LOW']}],"
        "  gen:function(p){return 'digitalWrite('+(p[0]||13)+', '+(p[1]||'HIGH')+');';}},"
        "delay:{allowed:['loop','if'],inputs:[{t:'number',l:'ms'}],"
        "  gen:function(p){return 'delay('+(p[0]||1000)+');';}},"
        "serialbegin:{allowed:['setup'],inputs:[{t:'sel',l:'Baud',o:['9600','19200','38400','57600','115200']}],"
        "  gen:function(p){return 'Serial.begin('+(p[0]||'9600')+');';}},"
        "serialprint:{allowed:['setup','loop','if'],inputs:[{t:'text',l:'Message'}],"
        "  gen:function(p){return 'Serial.print(\"'+(p[0]||'Hello')+'\");';}},"
        "ifblock:{allowed:['loop','if'],inputs:[],gen:function(){return '';}},"
        "};"
        "var SECTIONS={global:[],setup:[],loop:[]};"
        "var sel=null;"
        + initial_js +
        "function setSelection(section,targetArr,pathStr){"
        "  sel={section:section,targetArr:targetArr,pathStr:pathStr};"
        "  document.getElementById('statusbar').innerHTML='adding to: <span>'+pathStr+'</span>';"
        "  render();}"
        "function clearSelection(){"
        "  sel=null;"
        "  document.getElementById('statusbar').textContent='click a section or if body to select it';"
        "  render();}"
        "document.addEventListener('click',function(e){"
        "  if(!e.target.closest('.section')&&!e.target.closest('.if-body')&&"
        "     !e.target.closest('.block-btn')&&!e.target.closest('#codepanel'))clearSelection();});"
        "function setupSection(elId,sName,label){"
        "  var el=document.getElementById(elId);"
        "  el.addEventListener('click',function(e){"
        "    if(e.target===el||e.target.tagName==='H3'){e.stopPropagation();setSelection(sName,SECTIONS[sName],label);}});}"
        "setupSection('gs','global','Global');"
        "setupSection('ss','setup','setup()');"
        "setupSection('ls','loop','loop()');"
        "document.querySelectorAll('.block-btn').forEach(function(btn){"
        "  btn.addEventListener('click',function(e){"
        "    e.stopPropagation();"
        "    if(!sel){flash('Select a section or if body first');return;}"
        "    var type=btn.getAttribute('data-type'),def=B[type];if(!def)return;"
        "    var inIf=sel.pathStr.indexOf('\\u2192')!==-1;"
        "    if(inIf){if(def.allowed.indexOf('if')===-1){flash('\"'+type+'\" not allowed in if body');return;}}"
        "    else{if(def.allowed.indexOf(sel.section)===-1){flash('Goes in: '+def.allowed.filter(function(a){return a!=='if';}).join(' or '));return;}}"
        "    var block;"
        "    if(type==='ifblock'){"
        "      block={id:Date.now(),type:'ifblock',"
        "        condition:{left:'',op:'==',right:'',joiner:'none',left2:'',op2:'==',right2:''},"
        "        ifbody:[],elseifs:[],elsebody:null};"
        "    }else{"
        "      block={id:Date.now(),type:type,params:def.inputs.map(function(inp){"
        "        if(inp.t==='sel'){var f=inp.o[0];return typeof f==='object'?f.v:f;}return '';})};"
        "    }"
        "    sel.targetArr.push(block);render();});});"
        "function render(){"
        "  var anc=collectAncestorArrays();"
        "  renderSection('gs','global',anc);renderSection('ss','setup',anc);renderSection('ls','loop',anc);"
        "  ['gs','ss','ls'].forEach(function(id){"
        "    var el=document.getElementById(id);"
        "    var sn=id==='gs'?'global':id==='ss'?'setup':'loop';"
        "    var base='section s-'+(id==='gs'?'global':id==='ss'?'setup':'loop');"
        "    el.className=(sel&&sel.targetArr===SECTIONS[sn])?base+' active':base;});"
        "  genCode();}"
        "function collectAncestorArrays(){"
        "  var anc=[];if(!sel)return anc;"
        "  function walk(arr){for(var i=0;i<arr.length;i++){var b=arr[i];if(b.type!=='ifblock')continue;"
        "    if(containsTarget(b))anc.push(b.id);"
        "    walk(b.ifbody);b.elseifs.forEach(function(ei){walk(ei.body);});if(b.elsebody)walk(b.elsebody);}}"
        "  walk(SECTIONS[sel.section]);return anc;}"
        "function containsTarget(ifBlock){"
        "  if(ifBlock.ifbody===sel.targetArr)return true;"
        "  for(var i=0;i<ifBlock.elseifs.length;i++)if(ifBlock.elseifs[i].body===sel.targetArr)return true;"
        "  if(ifBlock.elsebody===sel.targetArr)return true;"
        "  function walkDeep(arr){for(var j=0;j<arr.length;j++){var b=arr[j];if(b.type==='ifblock'&&containsTarget(b))return true;}return false;}"
        "  return walkDeep(ifBlock.ifbody)||ifBlock.elseifs.some(function(ei){return walkDeep(ei.body);})||"
        "         (ifBlock.elsebody?walkDeep(ifBlock.elsebody):false);}"
        "function renderSection(elId,sName,anc){"
        "  var sec=document.getElementById(elId);"
        "  sec.querySelectorAll('.ws-block,.if-block').forEach(function(e){e.remove();});"
        "  SECTIONS[sName].forEach(function(block,idx){sec.appendChild(renderBlock(block,idx,SECTIONS[sName],sName,sName,anc));});}"
        "function renderBlock(block,idx,parentArr,section,pathStr,anc){"
        "  if(block.type==='ifblock')return renderIfBlock(block,idx,parentArr,section,pathStr,anc);"
        "  return renderActionBlock(block,idx,parentArr);}"
        "function renderActionBlock(block,idx,parentArr){"
        "  var def=B[block.type],d=document.createElement('div');d.className='ws-block';"
        "  var nm=document.createElement('span');nm.className='blk-name';nm.textContent=block.type;d.appendChild(nm);"
        "  def.inputs.forEach(function(inp,j){"
        "    var f=document.createElement('div');f.className='blk-field';"
        "    var lb=document.createElement('label');lb.textContent=inp.l;f.appendChild(lb);"
        "    var el;"
        "    if(inp.t==='sel'){el=document.createElement('select');"
        "      inp.o.forEach(function(opt){var o=document.createElement('option');"
        "        if(typeof opt==='object'){o.value=opt.v;o.textContent=opt.lb;}else{o.value=opt;o.textContent=opt;}"
        "        el.appendChild(o);});el.value=block.params[j];"
        "    }else{el=document.createElement('input');el.type=inp.t==='number'?'number':'text';el.value=block.params[j];}"
        "    el.className='blk-input';"
        "    el.addEventListener('click',function(e){e.stopPropagation();});"
        "    el.addEventListener('input',function(e){e.stopPropagation();block.params[j]=e.target.value;genCode();});"
        "    f.appendChild(el);d.appendChild(f);});"
        "  function mkb(ic,fn){var bt=document.createElement('button');bt.className='act';bt.textContent=ic;"
        "    bt.addEventListener('click',function(e){e.stopPropagation();fn();});return bt;}"
        "  d.appendChild(mkb('\\u2191',function(){if(idx>0){var t=parentArr[idx-1];parentArr[idx-1]=parentArr[idx];parentArr[idx]=t;render();}}));"
        "  d.appendChild(mkb('\\u2193',function(){if(idx<parentArr.length-1){var t=parentArr[idx+1];parentArr[idx+1]=parentArr[idx];parentArr[idx]=t;render();}}));"
        "  d.appendChild(mkb('\\u00D7',function(){parentArr.splice(idx,1);render();}));"
        "  return d;}"
        "function renderIfBlock(block,idx,parentArr,section,parentPathStr,anc){"
        "  var wrap=document.createElement('div');"
        "  wrap.className='if-block'+(anc.indexOf(block.id)!==-1?' ancestor':'');"
        "  var hdr=document.createElement('div');hdr.className='if-header';"
        "  hdr.appendChild(kw('if ('));appendCondFields(hdr,block.condition);hdr.appendChild(kw(')'));"
        "  hdr.appendChild(mkact('+ else if',function(){"
        "    block.elseifs.push({condition:{left:'',op:'==',right:'',joiner:'none',left2:'',op2:'==',right2:''},body:[]});render();}));"
        "  if(block.elsebody===null)hdr.appendChild(mkact('+ else',function(){block.elsebody=[];render();}));"
        "  hdr.appendChild(mkact('\\u00D7',function(){"
        "    parentArr.splice(idx,1);"
        "    if(sel&&(sel.targetArr===block.ifbody||isDescendant(block,sel.targetArr)))clearSelection();else render();}));"
        "  wrap.appendChild(hdr);"
        "  var ifPathStr=parentPathStr+' \\u2192 if';"
        "  var isOnlyBody=block.elseifs.length===0&&block.elsebody===null;"
        "  wrap.appendChild(makeBodyZone(block.ifbody,section,ifPathStr,isOnlyBody,anc));"
        "  block.elseifs.forEach(function(ei,eiIdx){"
        "    var eiHdr=document.createElement('div');eiHdr.className='elseif-header';"
        "    eiHdr.appendChild(kw('else if ('));appendCondFields(eiHdr,ei.condition);eiHdr.appendChild(kw(')'));"
        "    eiHdr.appendChild(mkact('\\u00D7',function(){block.elseifs.splice(eiIdx,1);render();}));"
        "    wrap.appendChild(eiHdr);"
        "    var eiPathStr=parentPathStr+' \\u2192 else if';"
        "    var eiIsLast=eiIdx===block.elseifs.length-1&&block.elsebody===null;"
        "    wrap.appendChild(makeBodyZone(ei.body,section,eiPathStr,eiIsLast,anc));});"
        "  if(block.elsebody!==null){"
        "    var elHdr=document.createElement('div');elHdr.className='else-header';"
        "    elHdr.appendChild(kw('else'));"
        "    elHdr.appendChild(mkact('\\u00D7',function(){block.elsebody=null;render();}));"
        "    wrap.appendChild(elHdr);"
        "    wrap.appendChild(makeBodyZone(block.elsebody,section,parentPathStr+' \\u2192 else',true,anc));}"
        "  return wrap;}"
        "function makeBodyZone(arr,section,pathStr,isLast,anc){"
        "  var div=document.createElement('div');"
        "  div.className='if-body'+(isLast?' last':'');"
        "  if(sel&&sel.targetArr===arr)div.classList.add('selected');"
        "  arr.forEach(function(block,idx){div.appendChild(renderBlock(block,idx,arr,section,pathStr,anc));});"
        "  if(arr.length===0){var hint=document.createElement('div');hint.className='body-hint';"
        "    hint.textContent='click to select, then add blocks';div.appendChild(hint);}"
        "  div.addEventListener('click',function(e){"
        "    if(e.target===div||e.target.classList.contains('body-hint')){"
        "      e.stopPropagation();setSelection(section,arr,pathStr);}});"
        "  return div;}"
        "function isDescendant(ifBlock,targetArr){"
        "  if(ifBlock.ifbody===targetArr)return true;"
        "  for(var i=0;i<ifBlock.elseifs.length;i++)if(ifBlock.elseifs[i].body===targetArr)return true;"
        "  if(ifBlock.elsebody===targetArr)return true;"
        "  function walkDeep(arr){for(var j=0;j<arr.length;j++){var b=arr[j];if(b.type==='ifblock'&&isDescendant(b,targetArr))return true;}return false;}"
        "  return walkDeep(ifBlock.ifbody)||ifBlock.elseifs.some(function(ei){return walkDeep(ei.body);})||"
        "         (ifBlock.elsebody?walkDeep(ifBlock.elsebody):false);}"
        "function kw(text){var s=document.createElement('span');s.className='if-keyword';s.textContent=text;return s;}"
        "function mkact(text,fn){var b=document.createElement('button');b.className='act';b.textContent=text;"
        "  b.addEventListener('click',function(e){e.stopPropagation();fn();});return b;}"
        "function appendCondFields(parent,cond){"
        "  parent.appendChild(condField('left',cond,'text'));"
        "  parent.appendChild(condField('op',cond,'opsel'));"
        "  parent.appendChild(condField('right',cond,'text'));"
        "  parent.appendChild(condField('joiner',cond,'joinsel'));"
        "  var g2=document.createElement('span');"
        "  g2.style.display=cond.joiner!=='none'?'contents':'none';"
        "  g2.appendChild(condField('left2',cond,'text'));"
        "  g2.appendChild(condField('op2',cond,'opsel'));"
        "  g2.appendChild(condField('right2',cond,'text'));"
        "  parent.appendChild(g2);"
        "  var joinEl=parent.querySelector('.cond-joiner');"
        "  joinEl.addEventListener('change',function(){g2.style.display=joinEl.value!=='none'?'contents':'none';});}"
        "function condField(labelText,obj,type){"
        "  var f=document.createElement('div');f.className='cond-field';"
        "  var lb=document.createElement('label');lb.textContent=labelText;f.appendChild(lb);"
        "  var el;"
        "  if(type==='opsel'){el=document.createElement('select');el.className='cond-select';"
        "    [['==','equals'],['!=','not equals'],['>','greater than'],['<','less than'],['>=','>='],['<=','<=']].forEach(function(o){"
        "      var opt=document.createElement('option');opt.value=o[0];opt.textContent=o[1];el.appendChild(opt);});"
        "    el.value=obj[labelText];"
        "  }else if(type==='joinsel'){el=document.createElement('select');el.className='cond-joiner';"
        "    [['none','\\u2014'],['and','and'],['or','or']].forEach(function(o){"
        "      var opt=document.createElement('option');opt.value=o[0];opt.textContent=o[1];el.appendChild(opt);});"
        "    el.value=obj[labelText];"
        "  }else{el=document.createElement('input');el.type='text';el.className='cond-input';el.value=obj[labelText]||'';}"
        "  el.addEventListener('click',function(e){e.stopPropagation();});"
        "  el.addEventListener('input',function(e){e.stopPropagation();obj[labelText]=e.target.value;genCode();});"
        "  el.addEventListener('change',function(e){e.stopPropagation();obj[labelText]=e.target.value;genCode();});"
        "  f.appendChild(el);return f;}"
        "function genCond(c){"
        "  var base=(c.left||'x')+' '+(c.op||'==')+' '+(c.right||'0');"
        "  if(c.joiner&&c.joiner!=='none'&&c.left2)"
        "    base+=' '+(c.joiner==='and'?'&&':'||')+' '+(c.left2||'x')+' '+(c.op2||'==')+' '+(c.right2||'0');"
        "  return base;}"
        "function genBlock(block,indent){"
        "  var pad='';for(var i=0;i<indent;i++)pad+='   ';"
        "  if(block.type==='ifblock'){"
        "    var lines=[pad+'if ('+genCond(block.condition)+') {'];"
        "    block.ifbody.forEach(function(b){lines.push(genBlock(b,indent+1));});"
        "    lines.push(pad+'}');"
        "    block.elseifs.forEach(function(ei){"
        "      lines.push(pad+'else if ('+genCond(ei.condition)+') {');"
        "      ei.body.forEach(function(b){lines.push(genBlock(b,indent+1));});"
        "      lines.push(pad+'}');});"
        "    if(block.elsebody!==null){"
        "      lines.push(pad+'else {');"
        "      block.elsebody.forEach(function(b){lines.push(genBlock(b,indent+1));});"
        "      lines.push(pad+'}');}"
        "    return lines.join('\\n');}"
        "  return pad+B[block.type].gen(block.params);}"
        "function genCode(){"
        "  var co=document.getElementById('codeout');"
        "  var gv=SECTIONS.global.map(function(b){return genBlock(b,0);}).join('\\n');"
        "  var sc=SECTIONS.setup.map(function(b){return genBlock(b,1);}).join('\\n');"
        "  var lc=SECTIONS.loop.map(function(b){return genBlock(b,1);}).join('\\n');"
        "  co.textContent='// Arduino Sketch\\n// Block Builder\\n// ------------\\n\\n'"
        "    +(gv?gv+'\\n\\n':'')"
        "    +'void setup() {\\n'+(sc?sc+'\\n':'')+'}'+"
        "    '\\n\\nvoid loop() {\\n'+(lc?lc+'\\n':'')+'}';}"
        "function flash(txt){"
        "  var mb=document.getElementById('msg');mb.textContent=txt;mb.classList.add('show');"
        "  setTimeout(function(){mb.classList.remove('show');},2500);}"
        "document.getElementById('copybtn').addEventListener('click',function(){"
        "  var txt=document.getElementById('codeout').textContent;"
        "  if(navigator.clipboard&&navigator.clipboard.writeText)"
        "    navigator.clipboard.writeText(txt).then(function(){flash('Copied!');}).catch(function(){fbCopy(txt);});"
        "  else fbCopy(txt);});"
        "function fbCopy(txt){"
        "  var ta=document.createElement('textarea');ta.value=txt;"
        "  ta.style.cssText='position:fixed;opacity:0;';document.body.appendChild(ta);ta.select();"
        "  try{document.execCommand('copy');flash('Copied!');}catch(e){flash('Select manually');}"
        "  document.body.removeChild(ta);}"
        "document.getElementById('clrbtn').addEventListener('click',function(){"
        "  SECTIONS.global=[];SECTIONS.setup=[];SECTIONS.loop=[];clearSelection();});"
        "var drawerOpen=false;"
        "document.getElementById('drawer-tab').addEventListener('click',function(e){"
        "  e.stopPropagation();"
        "  drawerOpen=!drawerOpen;"
        "  document.getElementById('drawer-panel').classList.toggle('open',drawerOpen);});"
        "render();"
        "});"
    )

    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'>"
        "<style>" + css + "</style>"
        "</head><body>"
        + body +
        "<script>" + js + "</script>"
        "</body></html>"
    )

    components.html(html, height=height+20, scrolling=True)