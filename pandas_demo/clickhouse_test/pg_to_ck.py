"""
从 PostgreSQL 读取 public schema 下所有表的建表语句，
转换为 ClickHouse 语法，写入文件。
表名统一前缀：workflow_test.bronze_layer_XXX

保留源表的注释
引擎用PostgreSQL（需要把PostgreSQL中的表全部同步到clickhouse中，使用clickhouse的PostgreSQL引擎），参考：
ENGINE = PostgreSQL('10.10.2.30', 'labillion-workflow', 'workflow_test.silver_layer_experiment', 'postgres', 'e2X4Fg&7b') COMMENT '实验实体表'

依赖：pip install psycopg2-binary
"""

import re
import psycopg2

# ── PostgreSQL 连接配置 ──────────────────────────────────────────────────────
PG_HOST = "123.59.127.6"
PG_PORT = 15432
PG_DB   = "labillion-workflow"
PG_USER = "postgres"
PG_PASS = "e2X4Fg&7b"

# ── 输出文件 ─────────────────────────────────────────────────────────────────
OUTPUT_FILE = "D:\code\python\pandas_demo\clickhouse_test\workflow_test_ck_ddl.sql"

# ── 类型映射表 ───────────────────────────────────────────────────────────────
TYPE_MAP = {
    # 整数
    "smallint":         "Int16",
    "int2":             "Int16",
    "integer":          "Int32",
    "int":              "Int32",
    "int4":             "Int32",
    "bigint":           "Int64",
    "int8":             "Int64",
    "smallserial":      "Int16",
    "serial":           "Int32",
    "bigserial":        "Int64",
    # 浮点
    "real":             "Float32",
    "float4":           "Float32",
    "double precision": "Float64",
    "float8":           "Float64",
    # 布尔
    "boolean":          "UInt8",
    "bool":             "UInt8",
    # 字符串
    "text":             "String",
    "json":             "String",
    "jsonb":            "String",
    "bytea":            "String",
    "xml":              "String",
    "citext":           "String",
    # 时间
    "date":             "Date",
    "time":             "String",
    "time without time zone": "String",
    "time with time zone":    "String",
    "timestamp":              "DateTime",
    "timestamp without time zone": "DateTime",
    "timestamp with time zone":    "DateTime",
    "timestamptz":      "DateTime",
    # UUID
    "uuid":             "UUID",
    # 网络
    "inet":             "String",
    "cidr":             "String",
    "macaddr":          "String",
}


def pg_type_to_ck(pg_type: str, is_nullable: bool) -> str:
    """将 PostgreSQL 列类型转换为 ClickHouse 类型（含 Nullable 包装）。"""
    t = pg_type.strip().lower()

    # 数组：integer[] → Array(Int32)
    if t.endswith("[]"):
        inner = pg_type_to_ck(t[:-2], False)
        ck = f"Array({inner})"
        return f"Nullable({ck})" if is_nullable else ck

    # character varying(n) / varchar(n) / char(n)
    m = re.match(r"character varying\((\d+)\)|varchar\((\d+)\)", t)
    if m:
        ck = "String"
        return f"Nullable({ck})" if is_nullable else ck

    m = re.match(r"character\((\d+)\)|char\((\d+)\)", t)
    if m:
        n = m.group(1) or m.group(2)
        ck = f"FixedString({n})"
        return f"Nullable({ck})" if is_nullable else ck

    # numeric(p,s) / decimal(p,s)
    m = re.match(r"(numeric|decimal)\((\d+),\s*(\d+)\)", t)
    if m:
        ck = f"Decimal({m.group(2)},{m.group(3)})"
        return f"Nullable({ck})" if is_nullable else ck

    m = re.match(r"(numeric|decimal)\((\d+)\)", t)
    if m:
        ck = f"Decimal({m.group(2)}, 0)"
        return f"Nullable({ck})" if is_nullable else ck

    # 不带精度的 numeric/decimal → Decimal(18,6)
    if t in ("numeric", "decimal"):
        ck = "Decimal(18, 6)"
        return f"Nullable({ck})" if is_nullable else ck

    # 直接映射
    ck = TYPE_MAP.get(t)
    if ck:
        return f"Nullable({ck})" if is_nullable else ck

    # 兜底：保留原类型，用 String 代替
    print(f"  [警告] 未知类型 '{pg_type}'，映射为 String")
    return "Nullable(String)" if is_nullable else "String"


def fetch_tables(cur) -> list[str]:
    """获取 public schema 下所有用户表名。"""
    cur.execute("""
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
        ORDER BY tablename
    """)
    return [row[0] for row in cur.fetchall()]


def fetch_columns(cur, table: str) -> list[dict]:
    """获取表的列信息（名称、类型、是否可空、默认值、注释）。"""
    cur.execute("""
        SELECT
            c.column_name,
            c.udt_name,
            c.data_type,
            c.character_maximum_length,
            c.numeric_precision,
            c.numeric_scale,
            c.is_nullable,
            c.column_default,
            pgd.description AS comment
        FROM information_schema.columns c
        LEFT JOIN pg_catalog.pg_statio_all_tables st
            ON st.schemaname = c.table_schema AND st.relname = c.table_name
        LEFT JOIN pg_catalog.pg_description pgd
            ON pgd.objoid = st.relid AND pgd.objsubid = c.ordinal_position
        WHERE c.table_schema = 'public' AND c.table_name = %s
        ORDER BY c.ordinal_position
    """, (table,))
    rows = []
    for r in cur.fetchall():
        col_name, udt_name, data_type, char_len, num_prec, num_scale, \
            is_nullable, col_default, comment = r

        # 还原完整类型字符串
        if data_type == "ARRAY":
            # udt_name 形如 _int4，去掉下划线前缀再加 []
            base = udt_name.lstrip("_")
            full_type = base + "[]"
        elif data_type in ("character varying", "character") and char_len:
            full_type = f"{data_type}({char_len})"
        elif data_type in ("numeric", "decimal") and num_prec:
            full_type = f"{data_type}({num_prec},{num_scale or 0})"
        elif data_type == "USER-DEFINED":
            full_type = udt_name   # enum 等，映射为 String
        else:
            full_type = data_type

        rows.append({
            "name":       col_name,
            "pg_type":    full_type,
            "nullable":   is_nullable == "YES",
            "default":    col_default,
            "comment":    comment or "",
        })
    return rows


def fetch_primary_keys(cur, table: str) -> list[str]:
    """获取表的主键列列表。"""
    cur.execute("""
        SELECT kcu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
           AND tc.table_schema     = kcu.table_schema
        WHERE tc.constraint_type = 'PRIMARY KEY'
          AND tc.table_schema    = 'public'
          AND tc.table_name      = %s
        ORDER BY kcu.ordinal_position
    """, (table,))
    return [row[0] for row in cur.fetchall()]


def fetch_table_comment(cur, table: str) -> str:
    """获取表的注释（pg_description 中 objsubid=0 为表级注释）。"""
    cur.execute("""
        SELECT pgd.description
        FROM pg_catalog.pg_statio_all_tables st
        JOIN pg_catalog.pg_description pgd
            ON pgd.objoid = st.relid AND pgd.objsubid = 0
        WHERE st.schemaname = 'public' AND st.relname = %s
    """, (table,))
    row = cur.fetchone()
    return row[0] if row and row[0] else ""


def build_ck_ddl(table: str, columns: list[dict], table_comment: str) -> str:
    """生成 ClickHouse 建表语句（PostgreSQL 引擎）。"""
    ck_table = f"workflow_test.bronze_layer_{table}"

    col_lines = []
    for col in columns:
        ck_type = pg_type_to_ck(col["pg_type"], col["nullable"])
        comment = f" COMMENT '{col['comment']}'" if col["comment"] else ""
        col_lines.append(f"    `{col['name']}` {ck_type}{comment}")

    cols_sql = ",\n".join(col_lines)

    engine = (
        f"ENGINE = PostgreSQL('{PG_HOST}:{PG_PORT}', '{PG_DB}', "
        f"'{table}', '{PG_USER}', '{PG_PASS}')"
    )
    tbl_comment = f" COMMENT '{table_comment}'" if table_comment else ""

    ddl = (
        f"CREATE TABLE IF NOT EXISTS {ck_table}\n"
        f"(\n"
        f"{cols_sql}\n"
        f")\n"
        f"{engine}{tbl_comment};\n"
    )
    return ddl


def main():
    print("连接 PostgreSQL …")
    conn = psycopg2.connect(
        host=PG_HOST, port=PG_PORT, dbname=PG_DB,
        user=PG_USER, password=PG_PASS,
        connect_timeout=10,
    )
    cur = conn.cursor()

    tables = fetch_tables(cur)
    print(f"共发现 {len(tables)} 张表：{tables}\n")

    ddl_blocks = []
    for tbl in tables:
        print(f"处理表：{tbl}")
        columns       = fetch_columns(cur, tbl)
        table_comment = fetch_table_comment(cur, tbl)
        ddl           = build_ck_ddl(tbl, columns, table_comment)
        ddl_blocks.append(f"-- 源表：public.{tbl}\n{ddl}")

    cur.close()
    conn.close()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n\n".join(ddl_blocks))
        f.write("\n")

    print(f"\n已写入 {len(ddl_blocks)} 条建表语句 → {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
