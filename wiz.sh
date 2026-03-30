#!/usr/bin/env bash

filename="csc_assignment_$1.zip"
echo "getting destination ready..."
rm -r pdf_output/ html_temp/
echo "READY!!... GO!"
python generate.py 
echo "source code pdf generated"
echo ""
python generate2.py -d output_txt/
echo "output pdf generated"
rm -r pdf_output/generate.pdf pdf_output/generate2.pdf
echo "generating zip archive..."
7z a -tzip $filename pdf_output/
echo "DONE"