# -*- coding:utf-8 -*-
# @author: 木子川
# @Email:  m21z50c71@163.com
# @VX：fylaicai

import argparse
import os.path

from dotenv import load_dotenv

# def parsers():
#     parser = argparse.ArgumentParser(description="Bert model of argparse")
#     parser.add_argument("--train_file", type=str, default=os.path.join("my_data", "train.txt"))
#     parser.add_argument("--dev_file", type=str, default=os.path.join("my_data", "dev.txt"))
#     # parser.add_argument("--test_file", type=str, default=os.path.join("./data", "test.txt"))
#     parser.add_argument("--classification", type=str, default=os.path.join("my_data", "class.txt"))
#     parser.add_argument("--bert_pred", type=str, default="bert-base-chinese")
#     parser.add_argument("--class_num", type=int, default=174)
#     parser.add_argument("--max_len", type=int, default=512)
#     parser.add_argument("--batch_size", type=int, default=1)
#     parser.add_argument("--epochs", type=int, default=1)
#     parser.add_argument("--patience", type=int, default=5)
#     parser.add_argument("--nums", type=int, default=3)
#     parser.add_argument("--learn_rate", type=float, default=1e-5)
#     parser.add_argument("--num_filters", type=int, default=768)
#     parser.add_argument("--save_model_path", type=str, default=os.path.join("my_models"))
#     # parser.add_argument("--save_model_best", type=str, default=os.path.join("my_models", "best_model.pth"))
#     # parser.add_argument("--save_model_last", type=str, default=os.path.join("my_models", "last_model.pth"))
#     # parser.add_argument("--app_model", type=str, default=os.path.join("my_models", "app_model.pth"))
#     args = parser.parse_args()
#     return args
# 获取项目根目录的绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 获取环境变量
dotenv_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


def parsers():
    class Args:
        train_file = os.path.join(BASE_DIR, os.getenv('TRAIN_FILE', 'my_data/train.txt'))
        dev_file = os.path.join(BASE_DIR, os.getenv('DEV_FILE', 'my_data/dev.txt'))
        classification = os.path.join(BASE_DIR, os.getenv('CLASSIFICATION', 'my_data/class.txt'))
        bert_pred = os.path.join(BASE_DIR, os.getenv('BERT_PRED', 'bert-base-chinese'))
        class_num = int(os.getenv('CLASS_NUM'))
        max_len = int(os.getenv('MAX_LEN'))
        batch_size = int(os.getenv('BATCH_SIZE'))
        epochs = int(os.getenv('EPOCHS'))
        patience = int(os.getenv('PATIENCE'))
        nums = int(os.getenv('NUMS'))
        learn_rate = float(os.getenv('LEARN_RATE'))
        num_filters = int(os.getenv('NUM_FILTERS'))
        save_model_path = os.path.join(BASE_DIR, os.getenv('SAVE_MODEL_PATH', 'my_models'))

    return Args()
