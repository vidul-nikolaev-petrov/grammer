#!/bin/bash

./_1_.remove_empty.sh &&
./_2_.extract_content.py &&
./_3_.wrap_and_style.py &&
./_4_.generate_map.py &&
./_5_.build_index.py
