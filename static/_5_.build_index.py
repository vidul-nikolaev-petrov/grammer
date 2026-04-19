#!/usr/bin/env python3
import os
import re

HTML_OUT_FILE = "index.html"

INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="bg">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link
        rel="icon"
        type="image/svg+xml"
        href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect x='20' y='10' width='60' height='80' rx='5' fill='%232980b9'/%3E%3Cpath d='M30 10v80M20 25h60M20 40h60' stroke='white' stroke-width='2'/%3E%3Ctext x='42' y='65' fill='white' font-family='Arial' font-weight='bold' font-size='40'%3EБ%3C/text%3E%3C/svg%3E"
    />
    <style>
        body {{
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            font-size: 18px;
            line-height: 1.6;
            color: #222;
            max-width: 1000px;
            margin: 50px auto;
            padding: 0 30px;
            background-color: #fcfcfc;
        }}
        h1 {{ color: #1a2a3a; border-bottom: 3px solid #3498db; padding-bottom: 12px; margin-bottom: 30px; }}
        
        details {{
            background: white;
            border: 1px solid #eef2f7;
            border-radius: 8px;
            margin-bottom: 8px;
            overflow: hidden;
        }}
        summary {{
            padding: 12px 20px;
            font-weight: 600;
            font-size: 0.95em;
            color: #3498db;
            cursor: pointer;
            list-style: none;
            display: flex;
            justify-content: space-between;
            align-items: center;
            user-select: none;
            -webkit-tap-highlight-color: transparent;
        }}
        summary::-webkit-details-marker {{ display: none; }}
        summary:hover {{ background-color: #f0f7fd; }}

        .count {{
            font-weight: normal;
            font-size: 0.82em;
            color: #aaa;
            margin-right: 12px;
        }}

        .toggle-icon::after {{ content: '+'; font-size: 1.2em; font-weight: bold; }}
        details[open] > summary .toggle-icon::after {{ content: '−'; }}

        .sub-group {{
            border: 1px dashed #d1e7f7;
            margin: 5px 15px 10px 15px;
            border-radius: 6px;
            background: #fff;
        }}
        .sub-summary {{
            padding: 8px 15px;
            font-size: 0.9em;
            color: #2980b9;
        }}

        .sub-sub-group {{
            border: 1px dotted #a9d4f0;
            margin: 5px 10px 5px 25px;
            border-radius: 4px;
        }}
        .sub-sub-summary {{
            padding: 6px 12px;
            font-size: 0.85em;
            color: #4682b4;
        }}

        .link-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 8px;
            padding: 12px;
        }}
        .single-link-container {{
            padding: 2px 20px 8px 20px;
        }}
        .index-link {{
            background: white;
            padding: 8px 12px;
            border-radius: 5px;
            border: 1px solid #eee;
            text-decoration: none;
            color: #3498db;
            font-size: 0.9em;
            display: inline-block;
            width: 100%;
            box-sizing: border-box;
            transition: all 0.2s;
        }}
        .index-link:hover {{
            border-color: #3498db;
            background-color: #f0f7fd;
        }}
    </style>
</head>
<body>
    <h1>Азбучен показалец</h1>
    <div class="alphabet-container">
        {content}
    </div>
</body>
</html>"""

def build():
    title_re = re.compile(r'<div[^>]*class="[^"]*deNwD o1-H2"[^>]*>.*?<span>(.*?)</span>', re.DOTALL | re.IGNORECASE)
    header_re = re.compile(r'<(h1|h2|h3)[^>]*>(.*?)</\1>', re.IGNORECASE | re.DOTALL)
    has_digit = re.compile(r'\d')
    lookalikes = {'A': 'А', 'B': 'В', 'E': 'Е', 'K': 'К', 'M': 'М', 'H': 'Н', 'O': 'О', 'P': 'Р', 'C': 'С', 'T': 'Т', 'X': 'Х'}
    bg_alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЬЮЯ"

    alpha_groups = {}
    files = [f for f in os.listdir(".") if f.endswith(".html") and f != HTML_OUT_FILE]

    for name in files:
        try:
            with open(name, "r", encoding="utf-8") as f:
                html = f.read()
            match = title_re.search(html) or header_re.search(html)
            if match:
                raw_text = match.group(1 if "deNwD" in match.group(0) else 2)
                clean_text = re.sub('<[^>]*>', '', raw_text).strip()
                if not has_digit.search(clean_text) and len(clean_text) > 1:
                    first_char = clean_text.upper()[0]
                    if first_char in lookalikes: first_char = lookalikes[first_char]
                    if first_char not in alpha_groups: alpha_groups[first_char] = []
                    alpha_groups[first_char].append({"file": name, "text": clean_text})
        except: continue

    sorted_letters = sorted(alpha_groups.keys(), key=lambda char: bg_alphabet.find(char) if char in bg_alphabet else 99)

    html_out = ""
    for letter in sorted_letters:
        # Group Level 1: First Word
        prefix1_map = {}
        for item in alpha_groups[letter]:
            words = item['text'].split(' ')
            p1 = words[0].strip(',.:;')
            if p1 not in prefix1_map: prefix1_map[p1] = []
            prefix1_map[p1].append(item)

        html_out += f'<details><summary><span>{letter}</span><div><span class="count">{len(alpha_groups[letter])}</span><span class="toggle-icon"></span></div></summary>'
        
        for p1 in sorted(prefix1_map.keys()):
            items_p1 = prefix1_map[p1]
            if len(items_p1) > 1:
                # Group Level 2: Second Word
                prefix2_map = {}
                for item in items_p1:
                    words = item['text'].split(' ')
                    p2 = ' '.join(words[:2]).strip(',.:;') if len(words) > 1 else words[0]
                    if p2 not in prefix2_map: prefix2_map[p2] = []
                    prefix2_map[p2].append(item)

                html_out += f'<details class="sub-group"><summary class="sub-summary"><span>{p1}</span><div><span class="count">{len(items_p1)}</span><span class="toggle-icon"></span></div></summary>'
                
                for p2 in sorted(prefix2_map.keys()):
                    items_p2 = prefix2_map[p2]
                    # Only create sub-subgroup if p2 is actually two words and has multiple items
                    if len(items_p2) > 1 and len(p2.split(' ')) > 1:
                        html_out += f'<details class="sub-sub-group"><summary class="sub-sub-summary"><span>{p2}</span><div><span class="count">{len(items_p2)}</span><span class="toggle-icon"></span></div></summary>'
                        html_out += '<div class="link-grid">'
                        for item in sorted(items_p2, key=lambda x: x['text']):
                            html_out += f'<a class="index-link" href="./{item["file"]}">{item["text"]}</a>'
                        html_out += '</div></details>'
                    else:
                        html_out += '<div class="link-grid" style="padding-top:0; padding-bottom:0;">'
                        for item in sorted(items_p2, key=lambda x: x['text']):
                            html_out += f'<a class="index-link" href="./{item["file"]}">{item["text"]}</a>'
                        html_out += '</div>'
                
                html_out += '</details>'
            else:
                item = items_p1[0]
                html_out += f'<div class="single-link-container"><a class="index-link" href="./{item["file"]}">{item["text"]}</a></div>'
        
        html_out += '</details>'

    with open(HTML_OUT_FILE, "w", encoding="utf-8") as f:
        f.write(INDEX_TEMPLATE.format(content=html_out))
    print(f"Success! Created {HTML_OUT_FILE} with 3 levels of grouping.")

if __name__ == "__main__":
    build()
