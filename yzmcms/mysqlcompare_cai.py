import pymysql
from tabulate import tabulate
from termcolor import colored
from typing import Dict, List, Tuple, Any


def get_db_schema(conn, db_name: str) -> Dict[str, Dict[str, Dict[str, Any]]]:
    """获取数据库的表结构，包含字段的详细属性"""
    try:
        cursor = conn.cursor()
        cursor.execute(f"SHOW TABLES FROM {db_name}")
        tables = [row[0] for row in cursor.fetchall()]

        schema = {}
        for table in tables:
            cursor.execute(f"SHOW FULL COLUMNS FROM {db_name}.{table}")
            columns = cursor.fetchall()
            column_info = {}
            for column in columns:
                field = column[0]
                column_info[field] = {
                    'Type': column[1],
                    'Collation': column[2],
                    'Null': column[3],
                    'Key': column[4],
                    'Default': column[5],
                    'Extra': column[6],
                    'Privileges': column[7],
                    'Comment': column[8]
                }
            schema[table] = column_info

        return schema
    except pymysql.Error as e:
        print(f"获取数据库 {db_name} 结构时出错: {e}")
        return {}
    finally:
        if cursor:
            cursor.close()


def compare_schemas(
        schema1: Dict[str, Dict[str, Dict[str, Any]]],
        schema2: Dict[str, Dict[str, Dict[str, Any]]],
        db1_name: str,
        db2_name: str,
) -> Dict[str, List[Any]]:
    """比较两个数据库的结构差异，包含字段的详细属性"""
    all_tables = set(schema1.keys()).union(set(schema2.keys()))
    differences = {"missing_tables": [], "extra_tables": [], "field_diffs": []}

    for table in all_tables:
        if table not in schema1:
            differences["missing_tables"].append(
                f"表 {colored(table, 'red')} 在 {colored(db1_name, 'blue')} 中不存在"
            )
        elif table not in schema2:
            differences["extra_tables"].append(
                f"表 {colored(table, 'green')} 在 {colored(db2_name, 'blue')} 中不存在"
            )
        else:
            fields1 = schema1[table]
            fields2 = schema2[table]
            all_fields = set(fields1.keys()).union(set(fields2.keys()))

            for field in all_fields:
                if field not in fields1:
                    differences["field_diffs"].append([
                        table,
                        field,
                        "新增字段",
                        colored("NULL", "red"),
                        colored(str(fields2[field]), "green")
                    ])
                elif field not in fields2:
                    differences["field_diffs"].append([
                        table,
                        field,
                        "已删除字段",
                        colored(str(fields1[field]), "red"),
                        colored("NULL", "green")
                    ])
                else:
                    for attr, value1 in fields1[field].items():
                        value2 = fields2[field][attr]
                        if value1 != value2:
                            differences["field_diffs"].append([
                                table,
                                field,
                                attr,
                                colored(str(value1), "yellow"),
                                colored(str(value2), "yellow")
                            ])

    return differences


def print_differences(differences: Dict[str, List[Any]]):
    """优雅地打印差异，包含字段的详细属性"""
    print("\n" + colored("=" * 50, "cyan"))
    print(colored("数据库结构差异报告", "cyan", attrs=["bold"]))
    print(colored("=" * 50, "cyan") + "\n")

    # 打印缺失的表
    if differences["missing_tables"]:
        print(colored("❌ 缺失的表:", "red", attrs=["bold"]))
        for msg in differences["missing_tables"]:
            print(f"  - {msg}")

    # 打印多余的表
    if differences["extra_tables"]:
        print(colored("\n❌ 多余的表:", "green", attrs=["bold"]))
        for msg in differences["extra_tables"]:
            print(f"  - {msg}")

    # 打印字段差异（表格形式）
    if differences["field_diffs"]:
        print(colored("\n🔄 字段差异:", "yellow", attrs=["bold"]))
        print(
            tabulate(
                differences["field_diffs"],
                headers=["表名", "字段名", "属性", f"数据库1的字段属性值", f"数据库2的字段属性值"],
                tablefmt="grid",
            )
        )


def save_to_file(differences: Dict[str, List[Any]], filename: str = "db_diff.txt"):
    """将差异保存到文件，移除颜色代码"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            if differences["missing_tables"]:
                f.write("❌ 缺失的表:\n")
                f.write("\n".join(differences["missing_tables"]) + "\n\n")

            if differences["extra_tables"]:
                f.write("❌ 多余的表:\n")
                f.write("\n".join(differences["extra_tables"]) + "\n\n")

            if differences["field_diffs"]:
                f.write("🔄 字段差异:\n")
                # 处理不同类型的差异行
                clean_diffs = []
                for row in differences["field_diffs"]:
                    # 移除颜色代码
                    clean_row = [
                        str(row[0]),  # 表名
                        str(row[1]),  # 字段名
                        str(row[2]),  # 操作或属性
                        # 清理值并处理可能的缺失索引
                        str(row[3]).replace("\x1b[31m", "").replace("\x1b[32m", "").replace("\x1b[33m", "").replace("\x1b[0m", ""),
                        str(row[4]).replace("\x1b[31m", "").replace("\x1b[32m", "").replace("\x1b[33m", "").replace("\x1b[0m", "")
                    ]
                    clean_diffs.append(clean_row)

                f.write(
                    tabulate(clean_diffs, headers=["表名", "字段名", "属性", "数据库1的字段属性值", "数据库2的字段属性值"],
                             tablefmt="grid")
                )

        print(colored(f"\n✅ 差异报告已保存到 {filename}", "green"))
    except Exception as e:
        print(f"保存报告时出错: {e}")



if __name__ == "__main__":
    # 数据库连接配置
    DB1_CONFIG = {
        "host": "localhost",
        "user": "root",
        "password": "Xhqsudosql01.",
        "db": "rylcsjk",
    }

    DB2_CONFIG = {
        "host": "localhost",
        "user": "root",
        "password": "Xhqsudosql01.",
        "db": "test",
    }

    # 连接数据库
    conn1 = None
    conn2 = None
    try:
        conn1 = pymysql.connect(**DB1_CONFIG)
        conn2 = pymysql.connect(**DB2_CONFIG)

        # 获取结构并比较
        print("正在获取数据库结构...")
        schema1 = get_db_schema(conn1, DB1_CONFIG["db"])
        schema2 = get_db_schema(conn2, DB2_CONFIG["db"])

        if schema1 and schema2:
            print("正在比较数据库结构...")
            differences = compare_schemas(schema1, schema2, DB1_CONFIG["db"], DB2_CONFIG["db"])

            # 打印并保存结果
            print_differences(differences)
            save_to_file(differences, "db_diff_report.txt")
        else:
            print("无法获取数据库结构，比较终止。")

    except pymysql.Error as e:
        print(f"数据库连接错误: {e}")
    except Exception as e:
        print(f"发生未知错误: {e}")
    finally:
        # 关闭连接
        if conn1:
            conn1.close()
        if conn2:
            conn2.close()
        print("数据库连接已关闭。")
