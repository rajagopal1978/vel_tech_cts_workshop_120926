import streamlit.components.v1 as components

def render_mermaid(code: str, height=400):
    components.html(
        f"""
        <div class="mermaid" style="display: flex; justify-content: center; align-items: center; width: 100%; height: 100%;">
            {code}
        </div>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
        </script>
        """,
        height=height
    )
