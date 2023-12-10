import pandas as pd
import os

# 载入Excel文件
def load_excel(file_path):
    return pd.read_excel(file_path)

# 处理数据
def process_data(df, category_col, content_col):
    # 提取指定的类别和内容列
    df = df[[category_col, content_col]]

    # 处理内容列
    df[content_col] = df[content_col].apply(lambda x: x.replace('\n', '').replace(' ', '')) # 删除换行符和空格
    df[content_col] = df[content_col].apply(lambda x: x.split("备注")[0] if "备注" in x else x) # 删除“备注”及其后的文本

    # 合并内容和类别为一行，用空格分隔
    df['processed'] = df[content_col] + ' ' + df[category_col].astype(str)

    return df['processed']

# 保存为TXT文件
def save_to_txt(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for line in data:

            file.write(line + '\n')

# 主函数
def main():
    file_path = os.path.join( os.path.dirname(os.path.abspath(__file__)), 'data','12345明细表.xlsx') # 替换为您的Excel文件路径
    output_file = 'output.txt' # 输出TXT文件的名称

    df = load_excel(file_path)
    processed_data = process_data(df, '分理项目', '事件内容') 
    save_to_txt(processed_data, output_file)
    

# 运行主函数
if __name__ == "__main__":
    main()
