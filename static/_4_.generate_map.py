#!/usr/bin/env python3

import os
import re
import json

def create_map():
    ref_map = {}
    # Regex to find the id we just created in the previous step
    id_pattern = re.compile(r'<h2[^>]*id="([^"]+)"')

    for root, _, files in os.walk("."):
        for name in files:
            if name.endswith(".html") and name != "generate_map.py":
                path = os.path.join(root, name)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                ids = id_pattern.findall(content)
                for header_id in ids:
                    # Store which file contains this ID
                    ref_map[header_id] = name

    with open("refs.js", "w", encoding="utf-8") as f:
        f.write("export const refMap = ")
        json.dump(ref_map, f, indent=4)
        f.write(";")

    print("Created refs.js with " + str(len(ref_map)) + " references.")

if __name__ == "__main__":
    create_map()

