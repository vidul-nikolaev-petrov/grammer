#!/usr/bin/env python3

import os
import re

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="bg">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/svg+xml" href="favicon.svg">
    <link rel="stylesheet" href="style.css">
    <script type="module" src="common.js" defer></script>
</head>
<body>
<a href="index.html" id="searchBtn" title="Към показалеца">◉</a>
{content}
<button id="backToTop" title="Go to top">↑</button>
</body>
</html>"""

HREF_CLEANER = re.compile(r'href="#/([^"]+)"')
ID_FIX_PATTERN = re.compile(r'(<h2[^>]*data-ref="([^"]+)"[^>]*)\sid="[^"]+"')

def wrap_files():
    for root, _, files in os.walk("."):
        for name in files:
            if name.endswith(".html") and not name.startswith("_"):
                path = os.path.join(root, name)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                def replace_id(match):
                    return f'{match.group(1)} id="{match.group(2).strip(".")}"'
                
                content = ID_FIX_PATTERN.sub(replace_id, content)
                content = HREF_CLEANER.sub(r'href="#\1"', content)
                content = re.sub(r'href="/rechnik/(\d+)"', r'href="\1.html"', content)

                try:
                    new_html = HTML_TEMPLATE.format(content=content)
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_html)
                    print(f"Success: {name}")
                except Exception as e:
                    print(f"Error in {name}: {e}")

if __name__ == "__main__":
    wrap_files()
