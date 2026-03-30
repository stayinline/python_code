"""
Superset 4.x -> 6.x 数据迁移适配器
将 megatrix (v4) 的数据逐表迁移到 megatrix_6_dev (v6)

策略:
1. 自动对比两库字段，构建列映射（跳过 v6 中不存在的列）
2. 对类型变更的列做 Python 层类型转换
3. 按 FK 依赖拓扑排序后插入，避免外键冲突
4. 对 sql_metrics / ab_register_user 做特殊行级处理
5. 迁移完成后重置 PostgreSQL 序列
"""

import urllib.parse
import logging
import json
from datetime import datetime, timezone
from typing import Any, Callable
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Inspector, Engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

# ── 连接配置 ──────────────────────────────────────────────────────────────
PASSWORD = urllib.parse.quote_plus("postgresql_admin")
URI_V4 = f"postgresql://postgres:{PASSWORD}@192.168.1.124:5432/megatrix"
URI_V6 = f"postgresql://postgres:{PASSWORD}@192.168.1.124:5432/megatrix_6_dev_init"

BATCH_SIZE = 500

# ── 列名重映射（v4列名 -> v6列名，None 表示跳过该列） ──────────────────────
COLUMN_RENAME_MAP: dict[str, dict[str, str | None]] = {
    # 示例: "sql_metrics": {"old_col": "new_col", "dropped_col": None}
}

# ── 特殊默认值（v6 中新增的 NOT NULL 且无默认值的列） ───────────────────────
EXTRA_DEFAULTS: dict[str, dict[str, Any]] = {
    "ab_register_user": {
        # Flask-AppBuilder 升级后如有新增字段在此填默认值
        # "new_field": "default_value",
    },
    "sql_metrics": {
        # "warning_markdown": None,
    },
}


# ── 工具函数 ──────────────────────────────────────────────────────────────

def get_engine(uri: str) -> Engine:
    return create_engine(uri, echo=False, future=True, pool_pre_ping=True)


def get_columns(insp: Inspector, table: str) -> dict[str, dict]:
    cols = {}
    for col in insp.get_columns(table, schema="public"):
        cols[col["name"]] = {
            "type": str(col["type"]).upper(),
            "nullable": col["nullable"],
            "default": col.get("default"),
        }
    return cols


# ── 类型转换函数 ──────────────────────────────────────────────────────────

def _is_type(t: str, *keywords: str) -> bool:
    return any(k in t.upper() for k in keywords)


def make_converter(v4_type: str, v6_type: str) -> Callable[[Any], Any] | None:
    """
    为类型不同的列生成转换函数，返回 None 表示无需转换（直接透传）
    """
    v4u, v6u = v4_type.upper(), v6_type.upper()
    if v4u == v6u:
        return None

    # INTEGER/SMALLINT -> BIGINT 等整数扩宽，Python int 天然兼容
    if _is_type(v4u, "INT") and _is_type(v6u, "INT", "BIGINT"):
        return None

    # VARCHAR/TEXT 互转，Python str 兼容
    if _is_type(v4u, "VARCHAR", "TEXT", "CHAR") and _is_type(v6u, "VARCHAR", "TEXT", "CHAR"):
        return None

    # JSON/JSONB 互转
    if _is_type(v4u, "JSON") and _is_type(v6u, "JSON"):
        return None

    # FLOAT/REAL/NUMERIC/DECIMAL 互转
    if _is_type(v4u, "FLOAT", "REAL", "NUMERIC", "DECIMAL") and \
       _is_type(v6u, "FLOAT", "REAL", "NUMERIC", "DECIMAL"):
        return None

    # TIMESTAMP -> TIMESTAMP WITH TIME ZONE：添加 UTC 时区
    if _is_type(v4u, "TIMESTAMP") and "TIME ZONE" in v6u:
        def to_utc(val: Any) -> Any:
            if val is None:
                return None
            if isinstance(val, datetime) and val.tzinfo is None:
                return val.replace(tzinfo=timezone.utc)
            return val
        return to_utc

    # TIMESTAMP WITH TIME ZONE -> TIMESTAMP：去除时区
    if "TIME ZONE" in v4u and _is_type(v6u, "TIMESTAMP") and "TIME ZONE" not in v6u:
        def strip_tz(val: Any) -> Any:
            if val is None:
                return None
            if isinstance(val, datetime) and val.tzinfo is not None:
                return val.replace(tzinfo=None)
            return val
        return strip_tz

    # BOOL -> INTEGER
    if _is_type(v4u, "BOOL") and _is_type(v6u, "INT"):
        return lambda val: int(val) if val is not None else None

    # INTEGER -> BOOL
    if _is_type(v4u, "INT") and _is_type(v6u, "BOOL"):
        return lambda val: bool(val) if val is not None else None

    # VARCHAR/TEXT -> JSONB/JSON：尝试解析为 JSON，失败则包装成 {"value": ...}
    if _is_type(v4u, "VARCHAR", "TEXT", "CHAR") and _is_type(v6u, "JSON"):
        def str_to_json(val: Any) -> Any:
            if val is None:
                return None
            if isinstance(val, (dict, list)):
                return val
            s = str(val).strip()
            if not s:
                return None
            try:
                return json.loads(s)
            except (json.JSONDecodeError, ValueError):
                return {"value": s}
        return str_to_json

    # 其他情况：尝试直接 str 转换（兜底，可能在 DB 层报错）
    log.warning(f"    未知类型转换 {v4_type} -> {v6_type}，将直接透传")
    return None


# ── 列映射构建 ────────────────────────────────────────────────────────────

def build_col_mapping(
    table: str,
    v4_cols: dict[str, dict],
    v6_cols: dict[str, dict],
) -> list[tuple[str, str, Callable | None]]:
    """
    返回 [(v4_col, v6_col, converter_fn), ...]
    只包含两端都存在的列
    """
    renames = COLUMN_RENAME_MAP.get(table, {})
    mapping = []
    skipped = []

    for v4_col, v4_meta in v4_cols.items():
        v6_col = renames.get(v4_col, v4_col)
        if v6_col is None:
            skipped.append(v4_col)
            continue
        if v6_col not in v6_cols:
            skipped.append(v4_col)
            continue
        converter = make_converter(v4_meta["type"], v6_cols[v6_col]["type"])
        mapping.append((v4_col, v6_col, converter))

    if skipped:
        log.debug(f"  [{table}] 跳过列（v6 中不存在）: {skipped}")

    # 警告 v6 中新增的 NOT NULL 列
    mapped_v6 = {v6_col for _, v6_col, _ in mapping}
    for col, meta in v6_cols.items():
        if col not in mapped_v6 and not meta["nullable"] and meta["default"] is None:
            extra = EXTRA_DEFAULTS.get(table, {})
            if col not in extra:
                log.warning(
                    f"  [{table}] 列 '{col}' 在 v6 中为 NOT NULL 且无默认值，"
                    f"也不在 EXTRA_DEFAULTS 中 —— 若 v4 有该列则手动配置 COLUMN_RENAME_MAP"
                )

    return mapping


# ── 特殊行级处理 ──────────────────────────────────────────────────────────

def patch_sql_metrics(row: dict) -> dict:
    """
    sql_metrics 迁移时的行级补丁。
    Superset v6 中 sql_metrics 表结构变化较多，在此做必要修正。
    """
    # 如果 v6 中 metric_type 为 NOT NULL 且旧数据为 None，补充默认值
    if row.get("metric_type") is None:
        row["metric_type"] = "METRIC"

    # extra 字段：确保是合法 JSON 字符串（v4 可能存 Python dict repr）
    if "extra" in row and isinstance(row["extra"], str):
        try:
            json.loads(row["extra"])
        except (json.JSONDecodeError, TypeError):
            row["extra"] = "{}"

    return row


def patch_ab_register_user(row: dict) -> dict:
    """
    ab_register_user 迁移时的行级补丁。
    Flask-AppBuilder 4.x 的注册用户表结构调整。
    """
    # registration_hash 如果为空，置为空字符串（部分版本 NOT NULL）
    if row.get("registration_hash") is None:
        row["registration_hash"] = ""

    return row


PATCH_FUNCTIONS: dict[str, Callable[[dict], dict]] = {
    "sql_metrics": patch_sql_metrics,
    "ab_register_user": patch_ab_register_user,
}


# ── FK 拓扑排序 ───────────────────────────────────────────────────────────

def topological_sort(tables: list[str], insp4: Inspector) -> list[str]:
    """按 FK 依赖关系排序，父表先于子表，避免外键约束冲突"""
    table_set = set(tables)
    deps: dict[str, set[str]] = {t: set() for t in tables}

    for table in tables:
        try:
            for fk in insp4.get_foreign_keys(table, schema="public"):
                ref = fk.get("referred_table")
                if ref and ref in table_set and ref != table:
                    deps[table].add(ref)
        except Exception:
            pass

    # Kahn 算法
    sorted_tables: list[str] = []
    remaining = set(tables)

    while remaining:
        # 找出当前无依赖的表
        ready = sorted(t for t in remaining if not (deps[t] & remaining))
        if not ready:
            # 存在循环依赖，强制取第一个
            log.warning(f"检测到循环 FK 依赖，强制处理: {sorted(remaining)[:3]}...")
            ready = [sorted(remaining)[0]]
        for t in ready:
            sorted_tables.append(t)
            remaining.remove(t)

    return sorted_tables


# ── 单表迁移 ──────────────────────────────────────────────────────────────

def migrate_table(
    table: str,
    eng4: Engine,
    eng6: Engine,
) -> tuple[int, int]:
    """迁移单张表，返回 (成功行数, 失败行数)"""
    insp4 = inspect(eng4)
    insp6 = inspect(eng6)
    v4_cols = get_columns(insp4, table)
    v6_cols = get_columns(insp6, table)

    col_mapping = build_col_mapping(table, v4_cols, v6_cols)
    if not col_mapping:
        log.warning(f"  [{table}] 无可迁移的列，跳过")
        return 0, 0

    v4_col_names = [c[0] for c in col_mapping]
    v6_col_names = [c[1] for c in col_mapping]
    converters = [c[2] for c in col_mapping]
    patch_fn = PATCH_FUNCTIONS.get(table)
    extra_defaults = EXTRA_DEFAULTS.get(table, {})

    # SELECT 语句：直接读取原始列
    quoted_cols = ", ".join(f'"{c}"' for c in v4_col_names)
    select_sql = f'SELECT {quoted_cols} FROM public."{table}"'

    # INSERT 语句
    all_v6_cols = v6_col_names + list(extra_defaults.keys())
    col_list = ", ".join(f'"{c}"' for c in all_v6_cols)
    placeholders = ", ".join(f":{c}" for c in all_v6_cols)
    insert_sql = (
        f'INSERT INTO public."{table}" ({col_list}) '
        f'VALUES ({placeholders}) ON CONFLICT DO NOTHING'
    )

    success = 0
    errors = 0

    with eng4.connect() as conn4, eng6.connect() as conn6:
        offset = 0
        while True:
            batch_sql = f"{select_sql} ORDER BY 1 LIMIT {BATCH_SIZE} OFFSET {offset}"
            try:
                rows = conn4.execute(text(batch_sql)).mappings().all()
            except Exception:
                # ORDER BY 1 可能在某些视图上失败，退回无序读取
                batch_sql = f"{select_sql} LIMIT {BATCH_SIZE} OFFSET {offset}"
                rows = conn4.execute(text(batch_sql)).mappings().all()

            if not rows:
                break

            # 构建待插入行列表
            transformed: list[dict] = []
            for raw in rows:
                row: dict = {}
                for v4_col, v6_col, conv in zip(v4_col_names, v6_col_names, converters):
                    val = raw[v4_col]
                    row[v6_col] = conv(val) if conv is not None else val
                # 附加额外默认值
                for col, default in extra_defaults.items():
                    row.setdefault(col, default)
                # 行级补丁
                if patch_fn:
                    row = patch_fn(row)
                transformed.append(row)

            # 批量插入
            try:
                conn6.execute(text(insert_sql), transformed)
                conn6.commit()
                success += len(transformed)
            except Exception as batch_err:
                conn6.rollback()
                log.warning(f"  [{table}] 批量插入失败，转为逐行模式: {batch_err}")
                for row in transformed:
                    try:
                        conn6.execute(text(insert_sql), [row])
                        conn6.commit()
                        success += 1
                    except Exception as row_err:
                        conn6.rollback()
                        errors += 1
                        sample = {k: row[k] for k in list(row)[:3]}
                        log.error(f"  [{table}] 行插入失败: {row_err} | 样本: {sample}")

            offset += BATCH_SIZE
            if offset % (BATCH_SIZE * 10) == 0:
                log.info(f"  [{table}] 进度: 已处理 {offset} 行...")

    return success, errors


# ── 序列重置 ──────────────────────────────────────────────────────────────

RESET_SEQUENCES_SQL = """
DO $$
DECLARE
    rec RECORD;
    max_val BIGINT;
BEGIN
    FOR rec IN
        SELECT
            c.table_name,
            c.column_name,
            pg_get_serial_sequence(
                quote_ident(c.table_name), c.column_name
            ) AS seq_name
        FROM information_schema.tables t
        JOIN information_schema.columns c
            ON c.table_name = t.table_name
           AND c.table_schema = t.table_schema
        WHERE t.table_schema = 'public'
          AND t.table_type = 'BASE TABLE'
          AND pg_get_serial_sequence(
                quote_ident(c.table_name), c.column_name
              ) IS NOT NULL
    LOOP
        EXECUTE format(
            'SELECT COALESCE(MAX(%I), 1) FROM public.%I',
            rec.column_name, rec.table_name
        ) INTO max_val;
        PERFORM setval(rec.seq_name, GREATEST(max_val, 1));
    END LOOP;
END $$;
"""


def reset_sequences(eng6: Engine) -> None:
    """重置 v6 中所有序列到当前表的最大值，防止后续插入时主键冲突"""
    with eng6.connect() as conn:
        conn.execute(text(RESET_SEQUENCES_SQL))
        conn.commit()
    log.info("所有序列已重置")


# ── 主流程 ────────────────────────────────────────────────────────────────

def run():
    log.info("=" * 70)
    log.info("Superset 数据迁移  v4(megatrix) -> v6(megatrix_6_dev)")
    log.info("=" * 70)

    eng4 = get_engine(URI_V4)
    eng6 = get_engine(URI_V6)

    # 获取表清单
    with eng4.connect() as c4, eng6.connect() as c6:
        insp4 = inspect(c4)
        insp6 = inspect(c6)
        tables4 = set(insp4.get_table_names(schema="public"))
        tables6 = set(insp6.get_table_names(schema="public"))

    common = sorted(tables4 & tables6)
    only_v4 = sorted(tables4 - tables6)
    only_v6 = sorted(tables6 - tables4)

    log.info(f"v4 表数量: {len(tables4)},  v6 表数量: {len(tables6)}")
    log.info(f"共同表: {len(common)},  仅 v4 存在(跳过): {len(only_v4)},  仅 v6 新增: {len(only_v6)}")

    if only_v4:
        log.warning(f"以下表仅存在于 v4，将跳过迁移: {only_v4}")

    # 拓扑排序（依赖少的表先迁移）
    ordered = topological_sort(common, inspect(eng4))

    log.info(f"\n迁移顺序确定，共 {len(ordered)} 张表")
    log.info("-" * 70)

    total_success = 0
    total_errors = 0
    failed_tables: list[str] = []

    for table in ordered:
        log.info(f"\n>> 迁移表: {table}")
        try:
            ok, err = migrate_table(table, eng4, eng6)
            total_success += ok
            total_errors += err
            status = "完成" if err == 0 else f"部分失败({err} 行)"
            log.info(f"   [{table}] {status}，成功 {ok} 行")
            if err:
                failed_tables.append(table)
        except Exception as e:
            log.error(f"   [{table}] 迁移异常: {e}", exc_info=True)
            failed_tables.append(table)

    # 重置序列
    log.info("\n" + "-" * 70)
    log.info("重置 PostgreSQL 序列...")
    try:
        reset_sequences(eng6)
    except Exception as e:
        log.error(f"序列重置失败: {e}")

    # 汇总
    log.info("\n" + "=" * 70)
    log.info("迁移汇总")
    log.info("=" * 70)
    log.info(f"  总成功行数 : {total_success}")
    log.info(f"  总失败行数 : {total_errors}")
    log.info(f"  失败表数量 : {len(failed_tables)}")
    if failed_tables:
        log.warning(f"  失败的表   : {failed_tables}")
        log.warning("  建议检查上方日志，按需调整 COLUMN_RENAME_MAP / EXTRA_DEFAULTS 后重跑")
    else:
        log.info("  结论: 所有表迁移成功！")

    eng4.dispose()
    eng6.dispose()


if __name__ == "__main__":
    run()
