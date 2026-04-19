#!/usr/bin/env python3

import os
from html.parser import HTMLParser

class DivExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.target_class = "aMhyJ"
        self.recording = 0
        self.extracted_chunks = []
        self.current_tag_stack = []
        self.in_p_to_delete = False

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == "div" and attr_dict.get("class") == self.target_class:
            self.recording += 1
        elif self.recording > 0 and tag == "div":
            self.recording += 1
        
        if self.recording > 0:
            self.current_tag_stack.append(tag)
            attr_str = "".join([f' {k}="{v}"' for k, v in attrs])
            self.extracted_chunks.append({"type": "tag", "content": f"<{tag}{attr_str}>", "tag_name": tag})

    def handle_endtag(self, tag):
        if self.recording > 0:
            self.extracted_chunks.append({"type": "tag", "content": f"</{tag}>", "tag_name": tag})
            if tag == "div":
                self.recording -= 1
            if self.current_tag_stack:
                self.current_tag_stack.pop()

    def handle_data(self, data):
        if self.recording > 0:
            self.extracted_chunks.append({"type": "data", "content": data})

def clean_and_save(path, chunks):
    final_output = []
    i = 0
    while i < len(chunks):
        # Check if this is a <p> tag
        if chunks[i].get("tag_name") == "p" and chunks[i]["content"].startswith("<p"):
            # Look ahead to see if data contains the forbidden string
            p_content_indices = []
            temp_i = i
            should_delete = False
            
            # Scan until the closing </p>
            while temp_i < len(chunks):
                p_content_indices.append(temp_i)
                # if chunks[temp_i]["type"] == "data" and "[Вж. и " in chunks[temp_i]["content"]:
                #    should_delete = True
                if chunks[temp_i].get("tag_name") == "p" and chunks[temp_i]["content"] == "</p>":
                    break
                temp_i += 1
            
            if should_delete:
                i = temp_i + 1 # Skip all these chunks
                continue
        
        final_output.append(chunks[i]["content"])
        i += 1

    with open(path, "w", encoding="utf-8") as f:
        f.write("".join(final_output))

def process_files():
    for root, _, files in os.walk("."):
        for name in files:
            if name.endswith(".html") and name != "extract.py":
                path = os.path.join(root, name)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                parser = DivExtractor()
                parser.feed(content)
                
                if parser.extracted_chunks:
                    clean_and_save(path, parser.extracted_chunks)
                    print(f"Processed: {name}")

if __name__ == "__main__":
    process_files()
