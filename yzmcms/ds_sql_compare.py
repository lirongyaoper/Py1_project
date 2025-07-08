import re
import sys
from collections import defaultdict


def remove_comments(sql):
    """移除SQL注释"""
    # 移除 /* */ 注释
    sql = re.sub(r'/\*.*?\*/', '', sql, flags=re.DOTALL)
    # 移除 -- 单行注释
    sql = re.sub(r'--.*$', '', sql, flags=re.MULTILINE)
    # 移除 # 单行注释
    sql = re.sub(r'#.*$', '', sql, flags=re.MULTILINE)
    return sql


def parse_sql_file(file_path):
    """解析SQL文件，返回表结构的字典"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    content = remove_comments(content)
    table_blocks = re.findall(
        r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?`?(\w+)`?\s*\((.*?)\)\s*;',
        content,
        re.DOTALL | re.IGNORECASE
    )

    tables = {}
    for table_name, block in table_blocks:
        columns = {}
        lines = [line.strip() for line in block.split('\n') if line.strip()]
        for line in lines:
            # 匹配列定义（忽略约束）
            match = re.match(
                r'`?(\w+)`?\s+([\w\(\)\s,]+)\s*((?:NOT\s+NULL|NULL|DEFAULT\s+\S+|AUTO_INCREMENT|PRIMARY\s+KEY|UNIQUE|COMMENT\s+\'.*?\')*)',
                line,
                re.IGNORECASE
            )
            if match:
                col_name = match.group(1)
                col_type = match.group(2).strip()
                attributes = match.group(3).strip()
                columns[col_name] = {
                    'type': col_type,
                    'attributes': attributes
                }
        tables[table_name] = columns
    return tables


def compare_tables(file1_tables, file2_tables, file1_name, file2_name):
    """比较两个文件的表结构差异"""
    report = []
    all_tables = set(file1_tables.keys()) | set(file2_tables.keys())

    # 比较表的存在性
    only_in_file1 = sorted(set(file1_tables.keys()) - set(file2_tables.keys()))
    only_in_file2 = sorted(set(file2_tables.keys()) - set(file1_tables.keys()))

    if only_in_file1:
        report.append(f"表只存在于 {file1_name}:")
        report.extend([f"  - {table}" for table in only_in_file1])
    if only_in_file2:
        report.append(f"\n表只存在于 {file2_name}:")
        report.extend([f"  - {table}" for table in only_in_file2])

    # 比较共有表的结构
    common_tables = sorted(set(file1_tables.keys()) & set(file2_tables.keys()))
    for table in common_tables:
        table_report = []
        cols1 = file1_tables[table]
        cols2 = file2_tables[table]
        all_cols = set(cols1.keys()) | set(cols2.keys())

        # 检查列存在性
        missing_in_file2 = [col for col in cols1 if col not in cols2]
        extra_in_file2 = [col for col in cols2 if col not in cols1]

        if missing_in_file2:
            table_report.append(f"  列只存在于 {file1_name}: {', '.join(missing_in_file2)}")
        if extra_in_file2:
            table_report.append(f"  列只存在于 {file2_name}: {', '.join(extra_in_file2)}")

        # 比较共有列的属性
        common_cols = set(cols1.keys()) & set(cols2.keys())
        for col in sorted(common_cols):
            col1 = cols1[col]
            col2 = cols2[col]
            differences = []

            # 比较数据类型
            if col1['type'] != col2['type']:
                differences.append(f"    类型: {file1_name}为 {col1['type']}, {file2_name}为 {col2['type']}")

            # 比较其他属性
            attrs1 = parse_attributes(col1['attributes'])
            attrs2 = parse_attributes(col2['attributes'])

            all_attrs = set(attrs1.keys()) | set(attrs2.keys())
            for attr in all_attrs:
                val1 = attrs1.get(attr, '未指定')
                val2 = attrs2.get(attr, '未指定')
                if val1 != val2:
                    differences.append(f"    {attr}: {file1_name}为 '{val1}', {file2_name}为 '{val2}'")

            if differences:
                table_report.append(f"  列 '{col}' 差异:")
                table_report.extend(differences)

        if table_report:
            report.append(f"\n表 '{table}' 差异:")
            report.extend(table_report)

    return report


def parse_attributes(attr_str):
    """解析列属性字符串为字典"""
    attributes = {}
    # 提取属性键值对
    parts = re.findall(
        r'(NOT\s+NULL|NULL|DEFAULT\s+\S+|AUTO_INCREMENT|PRIMARY\s+KEY|UNIQUE|COMMENT\s+\'.*?\')',
        attr_str,
        re.IGNORECASE
    )

    for part in parts:
        part = part.upper()
        if 'NOT NULL' in part:
            attributes['允许NULL'] = 'NO'
        elif 'NULL' in part:
            attributes['允许NULL'] = 'YES'
        elif 'DEFAULT' in part:
            attributes['默认值'] = re.search(r'DEFAULT\s+(\S+)', part, re.IGNORECASE).group(1)
        elif 'AUTO_INCREMENT' in part:
            attributes['自增'] = 'YES'
        elif 'PRIMARY KEY' in part:
            attributes['主键'] = 'YES'
        elif 'UNIQUE' in part:
            attributes['唯一'] = 'YES'
        elif 'COMMENT' in part:
            attributes['注释'] = re.search(r'COMMENT\s+\'(.*?)\'', part, re.IGNORECASE).group(1)

    return attributes


def main(file1, file2, output_file):
    """主比较函数"""
    tables1 = parse_sql_file(file1)
    tables2 = parse_sql_file(file2)

    report = [
        f"SQL文件比较报告",
        "=" * 50,
        f"比较文件1: {file1}",
        f"比较文件2: {file2}\n"
    ]

    diff_report = compare_tables(tables1, tables2, file1, file2)

    if not diff_report:
        report.append("两个SQL文件中的表结构完全相同")
    else:
        report.extend(diff_report)

    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))

    print(f"比较完成! 结果已保存到: {output_file}")

#python ds_sql_compare.py /home/lirongyao0916/Projects/lryper.com/sql/rylcsjk2507042344.sql  /home/lirongyao0916/Projects/lryper.com/sql/rylcsjk2507082249.sql comparison_result.txt
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("用法: python sql_compare.py <文件1.sql> <文件2.sql> <输出.txt>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2], sys.argv[3])