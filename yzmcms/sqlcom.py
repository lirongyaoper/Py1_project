import re

def extract_table_structures(sql_content):
    table_structures = {}
    # 匹配创建表的语句
    table_pattern = re.compile(r'CREATE TABLE `(\w+)` \((.*?)\) ENGINE=MyISAM DEFAULT CHARSET=\w+;', re.DOTALL)
    for match in table_pattern.findall(sql_content):
        table_name = match[0]
        fields = match[1].strip().split(',\n')
        field_info = {}
        for field in fields:
            field = field.strip()
            parts = field.split()
            field_name = parts[0].strip('`')
            field_type = ' '.join(parts[1:])
            field_info[field_name] = field_type
        table_structures[table_name] = field_info
    return table_structures

def compare_sql_files(file1_name, file1_content, file2_name, file2_content):
    table_structures1 = extract_table_structures(file1_content)
    table_structures2 = extract_table_structures(file2_content)

    differences = []
    for table_name, fields1 in table_structures1.items():
        if table_name in table_structures2:
            fields2 = table_structures2[table_name]
            table_differences = []
            for field_name, field_type1 in fields1.items():
                if field_name in fields2:
                    field_type2 = fields2[field_name]
                    if field_type1 != field_type2:
                        table_differences.append(f"  字段 {field_name} 设置不同："
                                                 f"{file1_name}: {field_type1}, {file2_name}: {field_type2}")
                else:
                    table_differences.append(f"  字段 {field_name} 只存在于 {file1_name} 的 {table_name} 表中")
            for field_name, field_type2 in fields2.items():
                if field_name not in fields1:
                    table_differences.append(f"  字段 {field_name} 只存在于 {file2_name} 的 {table_name} 表中")
            if table_differences:
                differences.append(f"表 {table_name} 存在以下差异：")
                differences.extend(table_differences)
        else:
            differences.append(f"表 {table_name} 只存在于 {file1_name} 中")
    for table_name in table_structures2:
        if table_name not in table_structures1:
            differences.append(f"表 {table_name} 只存在于 {file2_name} 中")
    return differences

# 读取yzm.sql文件内容
file1_name = '/home/lirongyao0916/Documents/sj/yzm.sql'
with open(file1_name, 'r', encoding='utf-8') as file:
    yzm_content = file.read()

# 读取rylcsjk2507042344.sql文件内容
file2_name = '/home/lirongyao0916/Documents/sj/rylcsjk2507042344.sql'
try:
    with open(file2_name, 'r', encoding='utf-8') as file:
        rylcsjk_content = file.read()
    differences = compare_sql_files(file1_name, yzm_content, file2_name, rylcsjk_content)
    if differences:
        for diff in differences:
            print(diff)
    else:
        print("两个文件的表结构和字段设置没有差异（忽略插入语句和多余表及字段）。")
except FileNotFoundError:
    print(f"未找到 {file2_name} 文件，请检查文件路径。")
