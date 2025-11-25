#!/bin/bash
# Script helper para ejecutar el analizador léxico

if [ -f "/opt/homebrew/bin/python3.12" ]; then
    /opt/homebrew/bin/python3.12 main.py
elif [ -f "/usr/local/bin/python3.12" ]; then
    /usr/local/bin/python3.12 main.py
else
    python3 main.py
fi
