#!/bin/bash

set -e

echo "1) loader.rop"
python3 preprocess.py loader.rop loader_processed.rop
roptool-legacy -t wk161-roptool-target -x 0xDEADBAB0 -s loader_processed.rop -o loader
python3 extract_rop.py loader loader.bin
python3 jsstring.py loader.bin > loader.txt
python3 make_exploit.py exploit.html.in loader.txt exploit.html

echo "2) stage2.rop"
python3 preprocess.py stage2.rop stage2_processed.rop
roptool-legacy -t wk161-roptool-target -x 0xDEADBAB0 -s stage2_processed.rop -o stage2
python3 extract_rop.py stage2 stage2.bin

echo "3) dumper.rop"
python3 preprocess.py dumper.rop dumper_processed.rop
roptool-legacy -t wk161-roptool-target -x 0xDEADBAB0 -s dumper_processed.rop -o dumper
python3 extract_rop.py dumper dumper.bin
