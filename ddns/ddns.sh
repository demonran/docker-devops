#!/usr/bin/env bash

current_path=$(cd "$(dirname $0)";pwd)

cd $current_path

pip install -r requirements.txt && python ddns.py