#!/bin/bash


#往定时任务日志记录文件中加入时间记录
echo "[$(date)] Task started" >> /mnt/inaisfs/data/wangbiao/ChineseTextClassificationBert/logs/scheduled_task.log

# 进入项目目录
cd "/mnt/inaisfs/data/wangbiao/ChineseTextClassificationBert"

# 激活 CTC 虚拟环境
# source "/usr/local/anaconda3/bin/activate" CTC

# eval "$(conda shell.bash hook)"
source "/usr/local/anaconda3/etc/profile.d/conda.sh"
# source "/mnt/inaisfs/data/wangbiao/.conda/envs/CTC/bin/activate"
conda activate "/mnt/inaisfs/data/wangbiao/.conda/envs/CTC"

# 从数据库获取数据并处理
python utils/process_data.py

# 运行主脚本
python main.py
