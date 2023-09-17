import os
import re
import pandas as pd
import sqlite3

# 指定目录和配置文件路径
my_file = './XD_00001_导出.csv'
config_file = './column_mapping.propties'


# 1.校验store_code格式是否为"JD_数字"
def isCode(file_name):
    gs = r'^JD_\d+$'
    store_code = re.findall(gs, file_name)
    print(bool(store_code))
    return bool(store_code)


# 2.获取配置文件中指定的所有列
def get_config_column(config_file):
    li = []
    with open(config_file, 'r', encoding='utf-8') as f:
        for line in f:
            if '=' in line:
                column = line.split('=')[0].strip()
                li.append(column)
    return li


# 校验csv文件是否包含配置文件中指定的所有列(csv文件列)，如果没有报错，并打印缺少的列名
def isAll(csv_file, config_columns):
    df = pd.read_csv(csv_file, encoding='gbk')
    csv_columns = df.columns.tolist()
    missing_columns = [col for col in config_columns if col not in csv_columns]
    if missing_columns:
        raise ValueError("CSV文件缺少的列".format(missing_columns))


# 3.将csv中的每一行转换为insert语句并插入数据库
# def insert_csv(csv_file, config_file):
#     # 读取配置文件，获取字段映射关系
#     config = {}
#     with open(config_file, 'r', encoding='utf-8') as cf:
#         for line in cf.readlines():
#             key, value = line.strip().split('=')
#             config[key] = value
#
#     # 读取CSV文件
#     df = pd.read_csv(csv_file, encoding='gbk')
#
#     # 添加 store_code 列到 DataFrame 中
#     df['store_code'] = ''
#
#     # # 遍历配置文件中的字段映射关系，填充对应列的值
#     # for column, mapped_column in config.items():
#     #     if mapped_column == 'store_code':
#     #         df['store_code'] = df[column]
#     #     else:
#     #         df[mapped_column] = df[column]
#     #
#     # # 连接到 SQLite 数据库
#     conn = sqlite3.connect('database1.db')
#     cursor = conn.cursor()
#     #
#     # # 将 DataFrame 写入数据库表
#     # df.to_sql('items', conn, if_exists='append', index=False)
#     for index, row in df.iterrows():
#         # 构建插入语句
#         columns = []
#         values = []
#         for column, mapped_column in config.items():
#             columns.append(mapped_column)
#             if mapped_column == 'store_code':
#                 values.append(row[column])
#             else:
#                 values.append(row[column])
#
#         insert_query = "INSERT INTO items ({}) VALUES ({})".format(
#             ', '.join(columns),
#             ', '.join(['?' for _ in range(len(columns))])
#         )
#         cursor.execute(insert_query, values)
#     # 关闭数据库连接
#     conn.close()


# 4. 处理成功的csv文件重命名为：原文件名称.COMPLETED；处理失败的csv文件重命名为：原文件名称.FAILED
def insert_csv(csv_file, config_file, table_name='items'):
    # 读取配置文件，获取字段映射关系
    config = {}
    with open(config_file, 'r', encoding='utf-8') as cf:
        for line in cf.readlines():
            key, value = line.strip().split('=')
            config[key] = value

    # 读取CSV文件
    df = pd.read_csv(csv_file, encoding='gbk')

    # 添加 store_code 列到 DataFrame 中
    df['store_code'] = ''

    # 遍历每一行，将对应列值填充到新的列中
    for column, mapped_column in config.items():
        if mapped_column == 'store_code':
            df['store_code'] = df[column]
        else:
            df[mapped_column] = df[column]

    # 连接到 SQLite 数据库
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # 创建数据表
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({','.join(config.values())})"
    cursor.execute(create_table_query)

    # 遍历每一行，生成并执行INSERT语句

    for index, row in df.iterrows():
        # 构建插入语句
        columns = []
        values = []
        for column, mapped_column in config.items():
            columns.append(mapped_column)
            values.append(row[column])

        insert_query = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({','.join(['?' for _ in range(len(columns))])})"

        # 执行插入操作
        cursor.execute(insert_query, values)

    # 提交更改并关闭数据库连接
    conn.commit()
    conn.close()


def rename_csv(csv_file, success=True):
    if success:
        new_filename = os.path.splitext(csv_file)[0] + ".COMPLETED"
    else:
        new_filename = os.path.splitext(csv_file)[0] + ".FAILED"
    os.rename(csv_file, new_filename)


# isCode(my_file)
# print(isAll(my_file, get_config_column(config_file)))
# insert_csv(my_file, config_file)
rename_csv(my_file, success=True)
