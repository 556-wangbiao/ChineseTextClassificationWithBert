@REM 关闭命令行中的回显
@echo off

@REM 进入项目目录
cd /d "E:\my_works\WuShiMiDong\ChineseTextClassificationBert/"

@REM 激活CTC虚拟环境
call "E:\Program Files\Anaconda\Scripts\activate.bat" CTC

@REM 从数据库获取数据并处理
python utils\process_data.py

python main.py
