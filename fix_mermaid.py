import os
import re

pages_dir = "c:/Varun/COT/pages"

for filename in os.listdir(pages_dir):
    if filename.endswith(".py"):
        filepath = os.path.join(pages_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Add import at top if not present
        if "from utils import render_mermaid" not in content:
            content = content.replace("import streamlit as st", "import streamlit as st\nimport sys\nimport os\nsys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))\nfrom utils import render_mermaid")
        
        # Match the mermaid block
        mermaid_match = re.search(r'```mermaid\n(.*?)\n```', content, re.DOTALL)
        if mermaid_match:
            mermaid_code = mermaid_match.group(1)
            # Replace the mermaid block in the markdown with string closing and opening
            replacement = f'""")\n\nrender_mermaid("""\n{mermaid_code}\n""")\n\nst.markdown("""'
            content = re.sub(r'```mermaid\n.*?\n```', replacement, content, flags=re.DOTALL)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Fixed mermaid in {filename}")
        else:
            print(f"No mermaid block found in {filename}")
