#! /bin/bash
DIR="$(dirname "$(readlink "$0")")"
cd $DIR
source $(dirname $0)/venv/bin/activate
python $(dirname $0)/qbit.py $1
