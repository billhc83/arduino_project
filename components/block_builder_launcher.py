import streamlit as st
import streamlit.components.v1 as components
import requests
import base64

def block_builder_launcher(preset, username=None, page=None, drawer_content=None, pin_refs=None):
    builder_url = ""
    try:
        url = "https://arduino-builder-service.onrender.com/builder"
        payload = {
            "preset": preset,
            "username": username,
            "page": page,
            "drawer_content": drawer_content,
            "pin_refs": pin_refs
        }
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        b64_html = base64.b64encode(resp.text.encode('utf-8')).decode('utf-8')
        builder_url = f"data:text/html;base64,{b64_html}"
    except Exception as e:
        st.error(f"Error loading block builder: {e}")
        return

    # Inject FAB and overlay directly into Streamlit DOM
    st.markdown(f"""
    <style>
    #bb-fab {{
        position: fixed; bottom: 28px; right: 28px; z-index: 999999;
        width: 56px; height: 56px; border-radius: 50%;
        background: #0969da; border: none; cursor: pointer;
        box-shadow: 0 4px 16px rgba(9,105,218,0.4);
        display: flex; align-items: center; justify-content: center;
        transition: transform 0.2s ease, background 0.2s ease;
    }}
    #bb-fab:hover {{ transform: scale(1.1); background: #0550ae; }}
    #bb-fab svg {{ width: 28px; height: 28px; fill: white; }}
    #bb-fab.open {{ background: #cf222e; }}

    @keyframes fab-pulse {{
        0% {{ box-shadow: 0 0 0 0 rgba(9,105,218,0.7); }}
        70% {{ box-shadow: 0 0 0 15px rgba(9,105,218,0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(9,105,218,0); }}
    }}
    #bb-fab {{ animation: fab-pulse 1.5s 3; }}

    #bb-overlay {{
        position: fixed; top: 0; left: 0;
        width: 100vw; height: 100vh;
        background: #f4f8ff; z-index: 999998;
        display: none; opacity: 0;
        transform: scale(0.97);
        transition: opacity 0.25s ease, transform 0.25s ease;
    }}
    #bb-overlay.visible {{
        display: block; opacity: 1; transform: scale(1);
    }}
    #bb-iframe {{
        width: 100%; height: 100%; border: none;
    }}
    </style>

    <div id="bb-fab" title="Open Block Builder">
        <svg viewBox="0 0 24 24">
            <path d="M19,3H5C3.9,3 3,3.9 3,5V19C3,20.1 3.9,21 5,21H19C20.1,21 21,20.1 21,19V5C21,3.9 20.1,3 19,3M9,17H7V15H9V17M9,13H7V11H9V13M9,9H7V7H9V9M19,17H17V15H19V17M19,13H17V11H19V13M19,9H17V7H19V9Z" />
        </svg>
    </div>

    <div id="bb-overlay">
        <iframe id="bb-iframe" src="{builder_url}"></iframe>
    </div>

    <script>
    (function() {{
        var fab = document.getElementById('bb-fab');
        var overlay = document.getElementById('bb-overlay');
        var isOpen = false;

        function openBuilder() {{
            isOpen = true;
            overlay.style.display = 'block';
            setTimeout(function() {{
                overlay.classList.add('visible');
            }}, 10);
            fab.classList.add('open');
            fab.innerHTML = '<span style="color:white;font-size:24px;font-weight:300;">✕</span>';
        }}

        function closeBuilder() {{
            isOpen = false;
            overlay.classList.remove('visible');
            fab.classList.remove('open');
            setTimeout(function() {{
                overlay.style.display = 'none';
            }}, 250);
            fab.innerHTML = '<svg viewBox="0 0 24 24"><path fill="white" d="M19,3H5C3.9,3 3,3.9 3,5V19C3,20.1 3.9,21 5,21H19C20.1,21 21,20.1 21,19V5C21,3.9 20.1,3 19,3M9,17H7V15H9V17M9,13H7V11H9V13M9,9H7V7H9V9M19,17H17V15H19V17M19,13H17V11H19V13M19,9H17V7H19V9Z" /></svg>';
        }}

        fab.addEventListener('click', function() {{
            isOpen ? closeBuilder() : openBuilder();
        }});

        window.addEventListener('message', function(e) {{
            if (e.data && e.data.type === 'bb_close') {{
                closeBuilder();
            }}
        }});
    }})();
    </script>
    """, unsafe_allow_html=True)

    components.html("""
<script>
(function() {
    var parent = window.parent.document;
    var fab = parent.getElementById('bb-fab');
    var overlay = parent.getElementById('bb-overlay');
    if(!fab || !overlay) return;
    
    var isOpen = false;

    function openBuilder() {
        isOpen = true;
        overlay.style.display = 'block';
        setTimeout(function() {
            overlay.classList.add('visible');
        }, 10);
        fab.classList.add('open');
        fab.innerHTML = '<span style="color:white;font-size:24px;font-weight:300;">✕</span>';
    }

    function closeBuilder() {
        isOpen = false;
        overlay.classList.remove('visible');
        fab.classList.remove('open');
        setTimeout(function() {
            overlay.style.display = 'none';
        }, 250);
        fab.innerHTML = '<svg viewBox="0 0 24 24"><path fill="white" d="M19,3H5C3.9,3 3,3.9 3,5V19C3,20.1 3.9,21 5,21H19C20.1,21 21,20.1 21,19V5C21,3.9 20.1,3 19,3M9,17H7V15H9V17M9,13H7V11H9V13M9,9H7V7H9V9M19,17H17V15H19V17M19,13H17V11H19V13M19,9H17V7H19V9Z" /></svg>';
    }

    fab.addEventListener('click', function() {
        isOpen ? closeBuilder() : openBuilder();
    });

    window.addEventListener('message', function(e) {
        if (e.data && e.data.type === 'bb_close') {
            closeBuilder();
        }
    });
})();
</script>
""", height=0)