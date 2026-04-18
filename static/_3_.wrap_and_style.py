#!/usr/bin/env python3

import os
import re

# 1. DEFINE THE TEMPLATE FIRST
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="bg">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            font-size: 18px;
            line-height: 1.8;
            color: #222;
            max-width: 850px;
            margin: 50px auto;
            padding: 0 30px;
            background-color: #fcfcfc;
        }}
        /* Prettier Links */
        a {{
            color: #3498db;
            text-decoration: none;
            border-bottom: 1px solid rgba(52, 152, 219, 0.3);
            transition: all 0.2s ease;
        }}
        a:hover {{
            color: #2980b9;
            border-bottom: 2px solid #2980b9;
            background-color: rgba(52, 152, 219, 0.05);
        }}
        h1 {{ color: #1a2a3a; border-bottom: 3px solid #3498db; padding-bottom: 12px; font-size: 2.5em; }}
        h2 {{ color: #2980b9; margin-top: 1.8em; font-size: 2em; }}
        .samp {{
            background-color: #f4f4f4;
            border-left: 5px solid #2980b9;
            padding: 20px;
            font-family: 'Consolas', 'Monaco', monospace;
            display: block;
            margin: 25px 0;
            white-space: pre-wrap;
            border-radius: 6px;
        }}
    </style>
    <script>
    document.addEventListener("click", async (e) => {{
        const link = e.target.closest("a");
        if (link && link.getAttribute("href") && link.getAttribute("href").startsWith("#")) {{
            const targetId = link.getAttribute("href").replace(/^#\\/?/, "");
            
            const localElement = document.getElementById(targetId);
            if (localElement) {{
                e.preventDefault();
                localElement.scrollIntoView({{ behavior: 'smooth' }});
            }} else {{
                e.preventDefault();
                try {{
                    const response = await fetch("refs.json");
                    const refMap = await response.json();
                    if (refMap[targetId]) {{
                        window.location.href = refMap[targetId] + "#" + targetId;
                    }}
                }} catch (err) {{
                    console.error("Navigation error");
                }}
            }}
        }}
    }});
    </script>
</head>
<body>
{content}
</body>
</html>"""

# 2. DEFINE PATTERNS
HREF_CLEANER = re.compile(r'href="#/([^"]+)"')
ID_FIX_PATTERN = re.compile(r'(<h2[^>]*data-ref="([^"]+)"[^>]*)\sid="[^"]+"')

# 3. DEFINE THE FUNCTION
def wrap_files():
    for root, _, files in os.walk("."):
        for name in files:
            if name.endswith(".html") and not name.startswith("_"):
                path = os.path.join(root, name)
                
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Fix IDs ("38.6." -> "38.6")
                def replace_id(match):
                    return f'{match.group(1)} id="{match.group(2).strip(".")}"'
                content = ID_FIX_PATTERN.sub(replace_id, content)

                # Fix HREFs ("#/38.6" -> "#38.6")
                content = HREF_CLEANER.sub(r'href="#\1"', content)

                # Step 1.5: Fix rechnik links ("/rechnik/1648" -> "1648.html")
                content = re.sub(r'href="/rechnik/(\d+)"', r'href="\1.html"', content)


                try:
                    new_html = HTML_TEMPLATE.format(content=content)
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_html)
                    print(f"Success: {name}")
                except Exception as e:
                    print(f"Error in {name}: {e}")

# 4. RUN
if __name__ == "__main__":
    wrap_files()
