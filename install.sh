#! /bin/bash
python -m venv $(dirname $0)/venv
source $(dirname $0)/venv/bin/activate
pip install -r $(dirname $0)/requirements.txt