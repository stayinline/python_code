"""
Superset 4.x -> 6.0.0 数据库表结构兼容性对比工具
对比两个 PostgreSQL 数据库的表结构，判断升级兼容性

"""

import urllib.parse
import logging
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Inspector

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
log = logging.getLogger(__name__)

# ── 数据库连接配置 ──────────────────────────────────────────────
PASSWORD = urllib.parse.quote_plus("postgresql_admin")

URI_V4 = f"postgresql://postgres:{PASSWORD}@192.168.1.124:5432/megatrix"
URI_V6 = f"postgresql://postgres:{PASSWORD}@192.168.1.124:5432/superset_6_dev"


# ── 工具函数 ────────────────────────────────────────────────────

def get_engine(uri: str):
    return create_engine(uri, echo=False, future=True)


def get_table_names(insp: Inspector) -> set[str]:
    return set(insp.get_table_names(schema="public"))


def get_columns(insp: Inspector, table: str) -> dict[str, dict]:
    """返回 {列名: {type, nullable, default, ...}}"""
    cols = {}
    for col in insp.get_columns(table, schema="public"):
        cols[col["name"]] = {
            "type": str(col["type"]),
            "nullable": col["nullable"],
            "default": col.get("default"),
        }
    return cols


def get_pk(insp: Inspector, table: str) -> list[str]:
    pk = insp.get_pk_constraint(table, schema="public")
    return sorted(pk.get("constrained_columns") or [])


def get_indexes(insp: Inspector, table: str) -> dict[str, dict]:
    """返回 {索引名: {unique, columns}}"""
    idxs = {}
    for idx in insp.get_indexes(table, schema="public"):
        idxs[idx["name"]] = {
            "unique": idx.get("unique", False),
            "columns": sorted(idx.get("column_names") or []),
        }
    return idxs


def get_fks(insp: Inspector, table: str) -> list[dict]:
    """返回外键列表，每项含 constrained_columns / referred_table / referred_columns"""
    result = []
    for fk in insp.get_foreign_keys(table, schema="public"):
        result.append({
            "constrained_columns": sorted(fk.get("constrained_columns") or []),
            "referred_table": fk.get("referred_table"),
            "referred_columns": sorted(fk.get("referred_columns") or []),
        })
    return result


# ── 核心对比逻辑 ────────────────────────────────────────────────

def compare_columns(table: str, v4_cols: dict, v6_cols: dict) -> list[str]:
    issues = []
    v4_names = set(v4_cols)
    v6_names = set(v6_cols)

    for col in v4_names - v6_names:
        issues.append(f"  [列缺失]  v4 列 '{col}' 在 v6 中不存在（升级可能丢失数据）")

    for col in v6_names - v4_names:
        meta = v6_cols[col]
        nullable_hint = "（NOT NULL，需要默认值或迁移脚本）" if not meta["nullable"] else "（nullable，兼容）"
        issues.append(f"  [新增列]  v6 新增列 '{col}' {nullable_hint}")

    for col in v4_names & v6_names:
        c4, c6 = v4_cols[col], v6_cols[col]
        if c4["type"] != c6["type"]:
            issues.append(
                f"  [类型变更] 列 '{col}': v4={c4['type']}  ->  v6={c6['type']}"
            )
        if c4["nullable"] != c6["nullable"]:
            direction = "nullable->NOT NULL" if not c6["nullable"] else "NOT NULL->nullable"
            issues.append(f"  [约束变更] 列 '{col}' nullable 变化: {direction}")

    return issues


def compare_table(table: str, insp4: Inspector, insp6: Inspector) -> tuple[bool, list[str]]:
    """对比单张表，返回 (is_compatible, messages)"""
    messages = []

    v4_cols = get_columns(insp4, table)
    v6_cols = get_columns(insp6, table)

    col_issues = compare_columns(table, v4_cols, v6_cols)
    messages.extend(col_issues)

    # 主键
    pk4 = get_pk(insp4, table)
    pk6 = get_pk(insp6, table)
    if pk4 != pk6:
        messages.append(f"  [主键变更] v4={pk4}  ->  v6={pk6}")

    # 索引（按列组合对比，忽略索引名变化）
    idx4 = {str(v["columns"]): v["unique"] for v in get_indexes(insp4, table).values()}
    idx6 = {str(v["columns"]): v["unique"] for v in get_indexes(insp6, table).values()}
    for cols_str in set(idx4) - set(idx6):
        messages.append(f"  [索引移除] v4 中存在的索引 {cols_str} 在 v6 中不存在")
    for cols_str in set(idx6) - set(idx4):
        messages.append(f"  [索引新增] v6 新增索引 {cols_str}")

    is_compatible = not any(
        tag in m for m in messages
        for tag in ("[列缺失]", "[类型变更]", "[主键变更]", "[约束变更]")
        if "NOT NULL" in m or "[列缺失]" in m or "[类型变更]" in m or "[主键变更]" in m
    )
    # 更精确地判断是否存在不兼容项
    incompatible_tags = ["[列缺失]", "[类型变更]", "[主键变更]"]
    not_null_new = [m for m in messages if "[新增列]" in m and "NOT NULL" in m]
    nullable_to_notnull = [m for m in messages if "[约束变更]" in m and "NOT NULL" in m]

    has_breaking = (
        any(tag in m for m in messages for tag in incompatible_tags)
        or bool(not_null_new)
        or bool(nullable_to_notnull)
    )

    return not has_breaking, messages


# ── 主流程 ──────────────────────────────────────────────────────

def run():
    log.info("=" * 70)
    log.info("Superset 表结构兼容性对比  v4(megatrix)  vs  v6(superset_6_dev)")
    log.info("=" * 70)

    eng4 = get_engine(URI_V4)
    eng6 = get_engine(URI_V6)

    with eng4.connect() as c4, eng6.connect() as c6:
        insp4 = inspect(c4)
        insp6 = inspect(c6)

        tables4 = get_table_names(insp4)
        tables6 = get_table_names(insp6)

    log.info(f"v4 表数量: {len(tables4)}")
    log.info(f"v6 表数量: {len(tables6)}")

    only_in_v4 = tables4 - tables6
    only_in_v6 = tables6 - tables4
    common = tables4 & tables6

    if only_in_v4:
        log.warning(f"\n[仅 v4 存在的表] ({len(only_in_v4)} 张) — 升级后将不再存在，需确认数据是否需要迁移:")
        for t in sorted(only_in_v4):
            log.warning(f"  - {t}")

    if only_in_v6:
        log.info(f"\n[仅 v6 新增的表] ({len(only_in_v6)} 张) — 升级后新建，无需迁移:")
        for t in sorted(only_in_v6):
            log.info(f"  + {t}")

    log.info(f"\n[共同表对比] ({len(common)} 张)")
    log.info("-" * 70)

    compatible_tables = []
    incompatible_tables = []

    for table in sorted(common):
        try:
            with eng4.connect() as c4, eng6.connect() as c6:
                insp4 = inspect(c4)
                insp6 = inspect(c6)
                ok, msgs = compare_table(table, insp4, insp6)

            if ok and not msgs:
                compatible_tables.append(table)
                log.info(f"  [OK] {table}  — 结构完全兼容")
            elif ok:
                compatible_tables.append(table)
                log.info(f"  [OK*] {table}  — 基本兼容（有非破坏性变更）:")
                for m in msgs:
                    log.info(m)
            else:
                incompatible_tables.append(table)
                log.warning(f"  [!!] {table}  — 存在不兼容变更:")
                for m in msgs:
                    log.warning(m)
        except Exception as e:
            log.error(f"  [ERR] {table}  — 对比出错: {e}")
            incompatible_tables.append(table)

    # ── 汇总报告 ──
    log.info("\n" + "=" * 70)
    log.info("对比汇总")
    log.info("=" * 70)
    log.info(f"  共同表总数      : {len(common)}")
    log.info(f"  完全/基本兼容   : {len(compatible_tables)}")
    log.info(f"  存在不兼容变更  : {len(incompatible_tables)}")
    log.info(f"  仅 v4 存在(废弃): {len(only_in_v4)}")
    log.info(f"  仅 v6 存在(新增): {len(only_in_v6)}")

    if incompatible_tables:
        log.warning("\n不兼容表清单（需要手动处理）:")
        for t in incompatible_tables:
            log.warning(f"  - {t}")
        log.warning("\n结论: 直接升级存在风险，建议先执行 Alembic 迁移脚本并备份数据。")
    else:
        log.info("\n结论: 所有共同表结构兼容，可安全升级（仍建议备份）。")

    eng4.dispose()
    eng6.dispose()


if __name__ == "__main__":
    run()
