#!/usr/bin/env bash

current_path=$(cd "$(dirname $0)";pwd)

cd $current_path

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple >/dev/nul 2>&1  && python ddns.py