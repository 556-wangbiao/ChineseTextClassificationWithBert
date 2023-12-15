"""
从数据库获取数据并处理，将处理后的数据写进classes.txt和train.txt
classes.txt存储所有类别
train.txt存储训练数据 内容\t类别下标
"""

import mysql.connector
import re
import os


def read_from_database():
    # 连接到MySQL数据库
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="131400",
        database="wushimidong"
    )
    # 创建一个游标对象
    cursor = cnx.cursor()
    # 构建查询SQL语句
    sql_query = f"SELECT split_items, event_content FROM `12345`"
    # 执行SQL语句
    cursor.execute(sql_query)

    classes = set()
    data = []
    for split_items, event_content in cursor:
        # 数据清洗
        event_content = re.sub(r'\s+|备注.*', '', event_content)  # 删除所有空白字符以及从 "备注" 开始到该行结束的所有内容
        classes.add(split_items)
        data.append((event_content, split_items))

    # 关闭游标和连接
    cursor.close()
    cnx.close()

    return classes, data


# 写入 classes.txt 和 train.txt
def write_to_files(classes, data, classes_path, train_path):
    with open(classes_path, 'w', encoding='utf-8') as f_classes, open(train_path, 'w', encoding='utf-8') as f_train:
        class_list = sorted(list(classes))
        class_dict = {cls: idx for idx, cls in enumerate(class_list)}

        for cls in class_list:
            f_classes.write(cls + '\n')

        for event_content, split_items in data:
            f_train.write(f'{event_content}\t{class_dict[split_items]}\n')


if __name__ == '__main__':
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目根路径
    classes_path = os.path.join(root_dir, 'my_data/class.txt')
    train_path = os.path.join(root_dir, 'my_data/train.txt')
    classes, data = read_from_database()
    write_to_files(classes, data, classes_path, train_path)
