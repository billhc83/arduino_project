import re
import streamlit.components.v1 as components


# ── Sketch parser ─────────────────────────────────────────────────────

def parse_sketch(sketch_code):
    result = {'global': [], 'setup': [], 'loop': []}

    def extract_body(code, fn_name):
        m = re.search(fn_name + r'\s*\(\s*\)\s*\{', code)
        if not m:
            return ''
        start = m.end()
        depth, i = 1, start
        while i < len(code) and depth > 0:
            if code[i] == '{': depth += 1
            elif code[i] == '}': depth -= 1
            i += 1
        return code[start:i-1].strip()

    setup_start = re.search(r'void\s+setup\s*\(', sketch_code)
    global_code = sketch_code[:setup_start.start()].strip() if setup_start else ''
    setup_code  = extract_body(sketch_code, 'void setup')
    loop_code   = extract_body(sketch_code, 'void loop')

    def parse_global(code):
        blocks = []
        for line in code.splitlines():
            line = line.strip()
            m = re.match(r'int\s+(\w+)\s*=\s*(-?\d+)\s*;', line)
            if m:
                blocks.append({'type': 'intvar', 'params': [m.group(1), m.group(2)]})
        return blocks

    def parse_section(code):
        blocks = []
        for line in code.splitlines():
            line = line.strip()
            if not line or line.startswith('//'): continue
            m = re.match(r'pinMode\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)\s*;', line)
            if m: blocks.append({'type': 'pinmode', 'params': [m.group(1), m.group(2)]}); continue
            m = re.match(r'digitalWrite\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)\s*;', line)
            if m: blocks.append({'type': 'digitalwrite', 'params': [m.group(1), m.group(2)]}); continue
            m = re.match(r'delay\s*\(\s*(\d+)\s*\)\s*;', line)
            if m: blocks.append({'type': 'delay', 'params': [m.group(1)]}); continue
            m = re.match(r'Serial\.begin\s*\(\s*(\d+)\s*\)\s*;', line)
            if m: blocks.append({'type': 'serialbegin', 'params': [m.group(1)]}); continue
            m = re.match(r'Serial\.print(?:ln)?\s*\(\s*"([^"]*)"\s*\)\s*;', line)
            if m: blocks.append({'type': 'serialprint', 'params': [m.group(1)]}); continue
            m = re.match(r'if\s*\(\s*(\w+)\s*(==|!=|>=|<=|>|<)\s*(\w+)\s*\)', line)
            if m: blocks.append({'type': 'ifblock', 'params': [m.group(1), m.group(2), m.group(3)]}); continue
        return blocks

    result['global'] = parse_global(global_code)
    result['setup']  = parse_section(setup_code)
    result['loop']   = parse_section(loop_code)
    return result


# ── Preset sketches ───────────────────────────────────────────────────

PRESETS = {
    'Blink': """
int ledPin = 13;
void setup() {
  pinMode(ledPin, OUTPUT);
}
void loop() {
  digitalWrite(ledPin, HIGH);
  delay(1000);
  digitalWrite(ledPin, LOW);
  delay(1000);
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
  if (buttonPin == HIGH) {
    digitalWrite(ledPin, HIGH);
  }
  delay(100);
}
""",
}


def arduino_block_coder(height=550, preset=None):

    # Guard: if a string is passed positionally treat it as preset
    if isinstance(height, str):
        preset = height
        height = 550

    # Build initial block state from preset if provided
    if preset and preset in PRESETS:
        blocks = parse_sketch(PRESETS[preset])
        def block_to_js(b):
            params = str(b['params']).replace('"', "'")
            return "{id:Date.now()+Math.random(),type:'" + b['type'] + "',params:" + params + "}"
        gb = '[' + ','.join(block_to_js(b) for b in blocks['global']) + ']'
        sb = '[' + ','.join(block_to_js(b) for b in blocks['setup'])  + ']'
        lb = '[' + ','.join(block_to_js(b) for b in blocks['loop'])   + ']'
        initial_js = "GB=" + gb + ";SB=" + sb + ";LB=" + lb + ";"
    else:
        initial_js = "GB=[];SB=[];LB=[];"

    css = (
        "* { box-sizing:border-box; margin:0; padding:0; }"
        "html, body { width:100%; height:" + str(height) + "px; overflow:hidden;"
        "  background:#0d1117; font-family:'Courier New',monospace; color:#c9d1d9; }"
        "#app { display:flex; flex-direction:row; width:100%; height:" + str(height) + "px; }"
        "#palette { width:110px; flex-shrink:0; background:#161b22;"
        "  border-right:1px solid #30363d; display:flex; flex-direction:column;"
        "  padding:6px; gap:4px; overflow-y:auto; }"
        "#palette::-webkit-scrollbar { width:3px; }"
        "#palette::-webkit-scrollbar-thumb { background:#30363d; }"
        ".pal-title { font-size:9px; color:#8b949e; text-transform:uppercase;"
        "  letter-spacing:.06em; padding:2px 0 4px 0; border-bottom:1px solid #30363d;"
        "  margin-bottom:2px; }"
        ".block-btn { width:100%; padding:5px 6px; border-radius:5px;"
        "  border:1px solid #30363d; background:#21262d; cursor:pointer;"
        "  font-size:10px; color:#c9d1d9; font-family:inherit; text-align:left; }"
        ".block-btn:hover { border-color:#388bfd; color:#79c0ff; }"
        "#workspace { flex:1; display:flex; flex-direction:column; gap:4px;"
        "  padding:6px; overflow:hidden; min-width:0; }"
        ".section { flex:1; border:2px solid #30363d; border-radius:7px;"
        "  background:#161b22; padding:5px 7px; cursor:pointer;"
        "  overflow-y:auto; min-height:0; }"
        ".section::-webkit-scrollbar { width:3px; }"
        ".section::-webkit-scrollbar-thumb { background:#30363d; }"
        ".section h3 { font-size:9px; font-weight:600; letter-spacing:.06em;"
        "  text-transform:uppercase; color:#8b949e; pointer-events:none;"
        "  user-select:none; margin-bottom:3px; }"
        ".s-global.active { border-color:#1f6feb; background:#0d1f3c; }"
        ".s-global.active h3 { color:#388bfd; }"
        ".s-setup.active  { border-color:#2ea043; background:#0d2818; }"
        ".s-setup.active  h3 { color:#3fb950; }"
        ".s-loop.active   { border-color:#d29922; background:#2b1d0e; }"
        ".s-loop.active   h3 { color:#d29922; }"
        ".ws-block { display:flex; align-items:center; flex-wrap:wrap; gap:4px;"
        "  background:#21262d; border:1px solid #30363d; border-radius:5px;"
        "  padding:3px 6px; margin-bottom:3px; }"
        ".blk-name { font-size:9px; font-weight:bold; color:#79c0ff; min-width:60px; }"
        ".blk-field { display:flex; flex-direction:column; font-size:8px; }"
        ".blk-field label { color:#8b949e; margin-bottom:1px; }"
        ".blk-input { font-size:9px; padding:2px 3px; width:64px; background:#0d1117;"
        "  color:#c9d1d9; border:1px solid #30363d; border-radius:3px; font-family:inherit; }"
        ".blk-input:focus { outline:none; border-color:#388bfd; }"
        ".act { background:none; border:1px solid #30363d; color:#8b949e;"
        "  cursor:pointer; font-size:9px; padding:1px 3px; border-radius:3px; }"
        ".act:hover { color:#fff; border-color:#8b949e; }"
        "#codepanel { width:185px; flex-shrink:0; border-left:1px solid #30363d;"
        "  display:flex; flex-direction:column; padding:6px; gap:5px; }"
        "#code-btns { display:flex; gap:5px; flex-shrink:0; }"
        "#msg { font-size:9px; color:#ffcc00; opacity:0; transition:opacity 0.3s;"
        "  flex-shrink:0; min-height:14px; }"
        "#msg.show { opacity:1; }"
        "#codeout { flex:1; background:#0d1117; border:1px solid #21262d;"
        "  border-radius:6px; padding:6px 7px; font-size:9px; white-space:pre;"
        "  overflow-y:auto; color:#79c0ff; line-height:1.5; min-height:0; }"
        "#codeout::-webkit-scrollbar { width:3px; }"
        "#codeout::-webkit-scrollbar-thumb { background:#30363d; }"
        ".cbtn { flex:1; padding:4px; border-radius:5px; border:1px solid #30363d;"
        "  background:#21262d; color:#c9d1d9; cursor:pointer; font-family:inherit; font-size:9px; }"
        ".cbtn:hover { background:#30363d; }"
    )

    body = (
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
        "</div>"
    )

    js = (
        "document.addEventListener('DOMContentLoaded',function(){"
        "var B={"
        "intvar:{allowed:['global'],inputs:[{t:'text',l:'Name'},{t:'number',l:'Value'}],"
        "  gen:function(p){return 'int '+(p[0]||'myVar')+' = '+(p[1]||0)+';';}},"
        "pinmode:{allowed:['setup'],inputs:[{t:'number',l:'Pin'},{t:'sel',l:'Mode',o:['OUTPUT','INPUT','INPUT_PULLUP']}],"
        "  gen:function(p){return 'pinMode('+(p[0]||13)+', '+(p[1]||'OUTPUT')+');';}},"
        "digitalwrite:{allowed:['loop'],inputs:[{t:'number',l:'Pin'},{t:'sel',l:'Value',o:['HIGH','LOW']}],"
        "  gen:function(p){return 'digitalWrite('+(p[0]||13)+', '+(p[1]||'HIGH')+');';}},"
        "delay:{allowed:['loop'],inputs:[{t:'number',l:'ms'}],"
        "  gen:function(p){return 'delay('+(p[0]||1000)+');';}},"
        "serialbegin:{allowed:['setup'],inputs:[{t:'sel',l:'Baud',o:['9600','19200','38400','57600','115200']}],"
        "  gen:function(p){return 'Serial.begin('+(p[0]||'9600')+');';}},"
        "serialprint:{allowed:['setup','loop'],inputs:[{t:'text',l:'Message'}],"
        "  gen:function(p){return 'Serial.print(\"'+(p[0]||'Hello')+'\");';}},"
        "ifblock:{allowed:['loop'],inputs:[{t:'text',l:'Left'},{t:'sel',l:'Cond',o:["
        "  {lb:'equals',v:'=='},{lb:'not equals',v:'!='},{lb:'greater than',v:'>'},"
        "  {lb:'less than',v:'<'},{lb:'>=',v:'>='},{lb:'<=',v:'<='}]},"
        "  {t:'text',l:'Right'}],"
        "  gen:function(p){return 'if ('+(p[0]||'x')+' '+(p[1]||'==')+' '+(p[2]||'0')+') { }';}},"
        "};"
        "var GB=[],SB=[],LB=[],sel=null;"
        + initial_js +
        "var gs=document.getElementById('gs');"
        "var ss=document.getElementById('ss');"
        "var ls=document.getElementById('ls');"
        "var co=document.getElementById('codeout');"
        "var mb=document.getElementById('msg');"
        "function setActive(t){"
        "  sel=t;"
        "  gs.className='section s-global'+(t==='global'?' active':'');"
        "  ss.className='section s-setup' +(t==='setup' ?' active':'');"
        "  ls.className='section s-loop'  +(t==='loop'  ?' active':'');}"
        "function onSec(el,t){el.addEventListener('click',function(e){"
        "  if(e.target===el||e.target.tagName==='H3')setActive(t);});}"
        "onSec(gs,'global');onSec(ss,'setup');onSec(ls,'loop');"
        "document.querySelectorAll('.block-btn').forEach(function(btn){"
        "  btn.addEventListener('click',function(e){"
        "    e.stopPropagation();"
        "    if(!sel){flash('Select a section first');return;}"
        "    var type=btn.getAttribute('data-type'),def=B[type];"
        "    if(!def)return;"
        "    if(def.allowed.indexOf(sel)===-1){flash('Goes in: '+def.allowed.join(' or '));return;}"
        "    var block={id:Date.now(),type:type,params:def.inputs.map(function(inp){"
        "      if(inp.t==='sel'){var f=inp.o[0];return typeof f==='object'?f.v:f;}return '';})}"
        "    ;if(sel==='global')GB.push(block);else if(sel==='setup')SB.push(block);else LB.push(block);"
        "    render();});});"
        "function render(){renderSec(gs,GB);renderSec(ss,SB);renderSec(ls,LB);genCode();}"
        "function renderSec(sec,arr){"
        "  sec.querySelectorAll('.ws-block').forEach(function(e){e.remove();});"
        "  arr.forEach(function(b,i){"
        "    var def=B[b.type],d=document.createElement('div');d.className='ws-block';"
        "    var nm=document.createElement('span');nm.className='blk-name';nm.textContent=b.type;d.appendChild(nm);"
        "    def.inputs.forEach(function(inp,j){"
        "      var f=document.createElement('div');f.className='blk-field';"
        "      var lb=document.createElement('label');lb.textContent=inp.l;f.appendChild(lb);"
        "      var el;"
        "      if(inp.t==='sel'){"
        "        el=document.createElement('select');"
        "        inp.o.forEach(function(opt){"
        "          var o=document.createElement('option');"
        "          if(typeof opt==='object'){o.value=opt.v;o.textContent=opt.lb;}else{o.value=opt;o.textContent=opt;}"
        "          el.appendChild(o);});el.value=b.params[j];"
        "      }else{el=document.createElement('input');el.type=inp.t==='number'?'number':'text';el.value=b.params[j];}"
        "      el.className='blk-input';"
        "      el.addEventListener('click',function(e){e.stopPropagation();});"
        "      el.addEventListener('input',function(e){e.stopPropagation();b.params[j]=e.target.value;genCode();});"
        "      f.appendChild(el);d.appendChild(f);});"
        "    function mkb(ic,fn){"
        "      var bt=document.createElement('button');bt.className='act';bt.textContent=ic;"
        "      bt.addEventListener('click',function(e){e.stopPropagation();fn();});return bt;}"
        "    d.appendChild(mkb('\\u2191',function(){if(i>0){var t=arr[i-1];arr[i-1]=arr[i];arr[i]=t;render();}}));"
        "    d.appendChild(mkb('\\u2193',function(){if(i<arr.length-1){var t=arr[i+1];arr[i+1]=arr[i];arr[i]=t;render();}}));"
        "    d.appendChild(mkb('\\u00D7',function(){arr.splice(i,1);render();}));"
        "    sec.appendChild(d);});}"
        "function flash(txt){mb.textContent=txt;mb.classList.add('show');"
        "  setTimeout(function(){mb.classList.remove('show');},2500);}"
        "function genCode(){"
        "  var gv=GB.map(function(b){return B[b.type].gen(b.params);}).join('\\n');"
        "  var sc=SB.map(function(b){return B[b.type].gen(b.params);}).join('\\n  ');"
        "  var lc=LB.map(function(b){return B[b.type].gen(b.params);}).join('\\n  ');"
        "  co.textContent='// Arduino Sketch\\n// Block Builder\\n// ------------\\n\\n'"
        "    +(gv?gv+'\\n\\n':'')"
        "    +'void setup() {\\n'+(sc?'  '+sc+'\\n':'')+'}'+"
        "    '\\n\\nvoid loop() {\\n'+(lc?'  '+lc+'\\n':'')+'}';}"
        "document.getElementById('copybtn').addEventListener('click',function(){"
        "  var txt=co.textContent;"
        "  if(navigator.clipboard&&navigator.clipboard.writeText)"
        "    navigator.clipboard.writeText(txt).then(function(){flash('Copied!');}).catch(function(){fbCopy(txt);});"
        "  else fbCopy(txt);});"
        "function fbCopy(txt){"
        "  var ta=document.createElement('textarea');ta.value=txt;"
        "  ta.style.cssText='position:fixed;opacity:0;';document.body.appendChild(ta);ta.select();"
        "  try{document.execCommand('copy');flash('Copied!');}catch(e){flash('Select manually');}"
        "  document.body.removeChild(ta);}"
        "document.getElementById('clrbtn').addEventListener('click',function(){"
        "  GB=[];SB=[];LB=[];render();});"
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

    components.html(html, height=height, scrolling=False)