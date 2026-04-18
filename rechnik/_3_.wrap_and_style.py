#!/usr/bin/env python3

import os

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="bg">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            font-size: 16px; /* Increased from default 16px */
            line-height: 1.8; /* More breathing room between lines */
            color: #222;
            max-width: 850px;
            margin: 50px auto;
            padding: 0 30px;
            background-color: #fcfcfc;
        }}
        h1 {{
            color: #1a2a3a;
            border-bottom: 3px solid #3498db;
            padding-bottom: 12px;
            font-size: 2.5em; /* Larger, bolder heading */
            margin-bottom: 1em;
        }}
        h2 {{
            color: #2980b9;
            margin-top: 1.8em;
            font-size: 2em;
        }}
        .samp {{
            background-color: #f4f4f4;
            border-left: 5px solid #2980b9;
            padding: 20px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 17px; /* Scaled sample text */
            display: block;
            margin: 25px 0;
            white-space: pre-wrap;
            border-radius: 6px;
            color: #444;
        }}
        p {{ margin-bottom: 1.5em; }}
    </style>
</head>
<body>
{content}
</body>
</html>"""

def wrap_files():
    for root, _, files in os.walk("."):
        for name in files:
            if name.endswith(".html") and name != "wrap_and_style.py":
                path = os.path.join(root, name)
                
                with open(path, "r", encoding="utf-8") as f:
                    current_content = f.read()
                
                # Wrap content in template
                new_html = HTML_TEMPLATE.format(content=current_content)
                
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_html)
                print(f"Styled: {name}")

if __name__ == "__main__":
    wrap_files()
