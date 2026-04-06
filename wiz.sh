#!/usr/bin/env bash

echo "Cleaning..."
rm -rf pdf_output html_temp

echo "Running generator..."
python generate.py

echo "DONE ✅"