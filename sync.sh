#!/bin/bash
rsync -avz /Volumes/CIRCUITPY/code.py   .
rsync -avz /Volumes/CIRCUITPY/lib/      ./lib
rsync -avz /Volumes/CIRCUITPY/examples/ ./examples
