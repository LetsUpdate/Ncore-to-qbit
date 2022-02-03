#! /bin/bash
DIR="$(dirname "$(readlink "$0")")"
cd $DIR
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt