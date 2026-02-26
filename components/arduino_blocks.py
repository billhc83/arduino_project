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
  delay(100);
}
""",
}


# ── Component ─────────────────────────────────────────────────────────

def arduino_block_coder(height=550, preset=None):

    # Guard: if a string is passed positionally treat it as preset
    if isinstance(height, str):
        preset = height
        height = 550

    # Build initial block state from preset if provided
    if preset and preset in PRESETS:
        blocks = parse_sketch(PRESETS[preset])
        def block_to_js(b):
            # blank all params - user fills in values themselves
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
        "  background:#0d1117; font-family:'Courier New',monospace; color:#c9d1d9; }"
        "#app { display:flex; flex-direction:row; width:100%; height:" + str(height) + "px; }"
        "#palette { width:110px; flex-shrink:0; background:#161b22;"
        "  border-right:1px solid #30363d; display:flex; flex-direction:column;"
        "  padding:6px; gap:4px; overflow-y:auto; }"
        "#palette::-webkit-scrollbar { width:3px; }"
        "#palette::-webkit-scrollbar-thumb { background:#30363d; }"
        ".pal-title { font-size:9px; color:#8b949e; text-transform:uppercase;"
        "  letter-spacing:.06em; padding:2px 0 4px 0; border-bottom:1px solid #30363d; margin-bottom:2px; }"
        ".block-btn { width:100%; padding:5px 6px; border-radius:5px; border:1px solid #30363d;"
        "  background:#21262d; cursor:pointer; font-size:10px; color:#c9d1d9;"
        "  font-family:inherit; text-align:left; }"
        ".block-btn:hover { border-color:#388bfd; color:#79c0ff; }"
        "#workspace { flex:1; display:flex; flex-direction:column; gap:4px;"
        "  padding:6px; overflow:hidden; min-width:0; }"
        ".section { flex:1; border:2px solid #30363d; border-radius:7px;"
        "  background:#161b22; padding:5px 7px; cursor:pointer; overflow-y:auto; min-height:0; }"
        ".section::-webkit-scrollbar { width:3px; }"
        ".section::-webkit-scrollbar-thumb { background:#30363d; }"
        ".section h3 { font-size:9px; font-weight:600; letter-spacing:.06em; text-transform:uppercase;"
        "  color:#8b949e; pointer-events:none; user-select:none; margin-bottom:3px; }"
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
        ".act { background:none; border:1px solid #30363d; color:#8b949e; cursor:pointer;"
        "  font-size:9px; padding:1px 3px; border-radius:3px; }"
        ".act:hover { color:#fff; border-color:#8b949e; }"
        ".if-block { margin-bottom:3px; }"
        ".if-header, .elseif-header, .else-header { display:flex; align-items:center;"
        "  gap:4px; flex-wrap:wrap; background:#1a1f2e; border:1px solid #30363d; padding:3px 6px; }"
        ".if-header    { border-radius:5px 5px 0 0; }"
        ".elseif-header { border-top:none; }"
        ".else-header   { border-top:none; }"
        ".if-keyword { font-size:9px; font-weight:bold; color:#ff7b72; }"
        ".cond-field { display:flex; flex-direction:column; font-size:8px; }"
        ".cond-field label { color:#8b949e; margin-bottom:1px; }"
        ".cond-input  { font-size:9px; padding:2px 3px; width:52px; background:#0d1117;"
        "  color:#c9d1d9; border:1px solid #30363d; border-radius:3px; font-family:inherit; }"
        ".cond-select { font-size:9px; padding:2px 3px; width:80px; background:#0d1117;"
        "  color:#c9d1d9; border:1px solid #30363d; border-radius:3px; font-family:inherit; }"
        ".cond-joiner { font-size:9px; padding:2px 3px; width:46px; background:#0d1117;"
        "  color:#ffa657; border:1px solid #30363d; border-radius:3px; font-family:inherit; }"
        ".cond-input:focus, .cond-select:focus, .cond-joiner:focus { outline:none; border-color:#ff7b72; }"
        ".if-body { border-left:1px dashed #30363d; border-right:1px dashed #30363d;"
        "  border-bottom:none; padding:4px 4px 4px 14px; min-height:28px; cursor:pointer; }"
        ".if-body.last { border-bottom:1px dashed #30363d; border-radius:0 0 5px 5px; }"
        ".if-body:hover { border-color:#555; }"
        ".if-body.selected { border-color:#388bfd; border-style:solid; background:#0a1628; }"
        ".if-body.ancestor { border-color:#1f3a5e; border-style:solid; }"
        ".if-block.ancestor > .if-header { border-color:#2a4a7f !important; background:#0e1c36 !important; }"
        ".if-block.ancestor > .elseif-header { border-color:#2a4a7f !important; background:#0e1c36 !important; }"
        ".if-block.ancestor > .else-header { border-color:#2a4a7f !important; background:#0e1c36 !important; }"
        ".body-hint { font-size:8px; color:#444; pointer-events:none; padding:2px 0; }"
        "#statusbar { font-size:9px; color:#8b949e; padding:3px 7px; flex-shrink:0;"
        "  background:#161b22; border-bottom:1px solid #21262d; }"
        "#statusbar span { color:#79c0ff; }"
        "#codepanel { width:185px; flex-shrink:0; border-left:1px solid #30363d;"
        "  display:flex; flex-direction:column; padding:6px; gap:5px; }"
        "#code-btns { display:flex; gap:5px; flex-shrink:0; }"
        "#msg { font-size:9px; color:#ffcc00; opacity:0; transition:opacity 0.3s; flex-shrink:0; min-height:14px; }"
        "#msg.show { opacity:1; }"
        "#codeout { flex:1; background:#0d1117; border:1px solid #21262d; border-radius:6px;"
        "  padding:6px 7px; font-size:9px; white-space:pre; overflow-y:auto;"
        "  color:#79c0ff; line-height:1.5; min-height:0; }"
        "#codeout::-webkit-scrollbar { width:3px; }"
        "#codeout::-webkit-scrollbar-thumb { background:#30363d; }"
        ".cbtn { flex:1; padding:4px; border-radius:5px; border:1px solid #30363d;"
        "  background:#21262d; color:#c9d1d9; cursor:pointer; font-family:inherit; font-size:9px; }"
        ".cbtn:hover { background:#30363d; }"
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
        "</div>"
    )

    js = (
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
        "  var pad='';for(var i=0;i<indent;i++)pad+='  ';"
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