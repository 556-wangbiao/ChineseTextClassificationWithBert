import pandas as pd
import os 


# 载入Excel文件
def load_excel(file_path):
    return pd.read_excel(file_path)

# 提取并保存类别到class.txt
def save_classes(df, category_col, class_file):
    # 获取唯一的类别
    classes = df[category_col].unique()
    classes.sort()  # 如果需要，可以对类别进行排序

    # 保存类别到文件
    with open(class_file, 'w', encoding='utf-8') as file:
        for c in classes:
            file.write(str(c) + '\n')

    # 创建一个类别到索引的映射字典
    class_to_index = {c: i for i, c in enumerate(classes)}
    return class_to_index

# 处理数据并保存到output.txt
def process_and_save_data(df, category_col, content_col, class_to_index, output_file):
    # 处理内容列
    df[content_col] = df[content_col].apply(lambda x: x.replace('\n', '').replace(' ', '').replace('\t', '')) # 删除换行符、空格和制表符
    df[content_col] = df[content_col].apply(lambda x: x.split("备注")[0] if "备注" in x else x) # 删除“备注”及其后的文本

    # 将类别转换为索引
    df[category_col] = df[category_col].apply(lambda x: class_to_index[x])

    # 合并内容和类别索引为一行，用空格分隔
    df['processed'] = df[content_col] + '\t' + df[category_col].astype(str)

    # 保存处理后的数据
    with open(output_file, 'w', encoding='utf-8') as file:
        for line in df['processed']:
            file.write(line + '\n')

# 主函数
def main():
    root_dir = os.path.dirname(os.path.abspath(__file__)) # 项目根路径
    file_path = os.path.join( root_dir, 'my_data','12345明细表.xlsx') # Excel文件路径
    output_file =  os.path.join( root_dir, 'my_data','train.txt') # 输出TXT文件的名称
    class_file =  os.path.join( root_dir, 'my_data','class.txt') # 类别文件的名称

    df = load_excel(file_path)
    class_to_index = save_classes(df, '分理项目', class_file) # 保存类别并获取类别到索引的映射
    process_and_save_data(df, '分理项目', '事件内容', class_to_index, output_file) # 处理数据并保存到output.txt

# 运行主函数
if __name__ == "__main__":
    main()
