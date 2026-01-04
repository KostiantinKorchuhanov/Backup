#!/bin/bash

set -e
echo "Installation started"

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
  echo "Virtual environment created in venv"
fi

source .venv/bin/activate
pip install --upgrade pip
pip install .
echo "Installation complete. Use bt --help or bt-gui to start"



