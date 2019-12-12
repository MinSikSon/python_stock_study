#!/bin/sh
#python3 main.py --username=$1 --password=$2 --count=1
python3 main.py --website="tesla"
python3 main.py --website="bbc"

./2_git__add_commit_push.sh
