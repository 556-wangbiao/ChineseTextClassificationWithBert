#!/bin/bash

# 进入项目目录
cd "/mnt/inaisfs/data/wangbiao/ChineseTextClassificationBert"

# 激活 CTC 虚拟环境
source "/usr/local/anaconda3/bin/activate" CTC

# 从数据库获取数据并处理
python utils/process_data.py

# 运行主脚本
python main.py
