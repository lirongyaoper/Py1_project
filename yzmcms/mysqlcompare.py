import pymysql


def compare_databases(conn1, conn2, db1, db2):
    # 获取 db1 的表结构
    cursor1 = conn1.cursor()
    cursor1.execute(f"SHOW TABLES FROM {db1}")
    tables1 = [row[0] for row in cursor1.fetchall()]

    # 获取 db2 的表结构
    cursor2 = conn2.cursor()
    cursor2.execute(f"SHOW TABLES FROM {db2}")
    tables2 = [row[0] for row in cursor2.fetchall()]

    # 比较表
    all_tables = set(tables1 + tables2)
    for table in all_tables:
        if table not in tables1:
            print(f"表 {table} 在 {db1} 中不存在")
        elif table not in tables2:
            print(f"表 {table} 在 {db2} 中不存在")
        else:
            # 比较字段
            cursor1.execute(f"DESCRIBE {db1}.{table}")
            fields1 = {row[0]: row[1:] for row in cursor1.fetchall()}

            cursor2.execute(f"DESCRIBE {db2}.{table}")
            fields2 = {row[0]: row[1:] for row in cursor2.fetchall()}

            all_fields = set(fields1.keys()).union(set(fields2.keys()))
            for field in all_fields:
                if field not in fields1:
                    print(f"表 {table} 的字段 {field} 在 {db1} 中不存在")
                elif field not in fields2:
                    print(f"表 {table} 的字段 {field} 在 {db2} 中不存在")
                elif fields1[field] != fields2[field]:
                    print(f"表 {table} 的字段 {field} 不一致:")
                    print(f"{db1}: {fields1[field]}")
                    print(f"{db2}: {fields2[field]}")

if __name__ =="__main__":
    # 连接数据库
    conn1 = pymysql.connect(host="localhost", user="root", password="Xhqsudosql01.", db="rylcsjk")
    conn2 = pymysql.connect(host="localhost", user="root", password="Xhqsudosql01.", db="test")

    compare_databases(conn1, conn2, "rylcsjk", "test")
    conn1.close()
    conn2.close()