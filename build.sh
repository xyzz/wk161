#!/bin/bash

set -e

echo "1) loader.rop"
roptool-legacy -t wk161-roptool-target -x 0xDEADBAB0 -s loader.rop -o loader
python3 extract_rop.py loader loader.bin
python3 jsstring.py loader.bin > loader.txt
python3 make_exploit.py exploit.html.in loader.txt exploit.html

echo "2) second.rop"

