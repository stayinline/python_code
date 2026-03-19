#!/usr/bin/env python3
"""
MES模拟数据生成脚本
生成8张表的模拟数据，覆盖16个业务问题
"""

import csv
import random
import os
from datetime import datetime, timedelta

random.seed(42)
OUTPUT_DIR = "mes_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ===== 公共参数 =====
ORG_RRN = 1001
NOW = datetime(2026, 3, 3, 10, 0, 0)

PART_NAMES = ["YE142MDL4AAGZ-14.2", "YE156MDL3BBHZ-15.6", "YE133MDL2CCFZ-13.3"]
PROCESS_NAMES = ["MAIN_PROCESS_V1", "MAIN_PROCESS_V2"]
PROCEDURE_NAMES = ["PROD_FLOW_A", "PROD_FLOW_B"]

# 站点列表（模拟LCD/OLED生产流程）
STEPS = [
    ("A1600", "端子切割"), ("A1500", "CNC"), ("A2000", "研磨粗清洗"),
    ("A2300", "POL"), ("A2600", "贴膜"), ("A2500", "云边处胶"),
    ("A3100", "EC"), ("A3200", "COF"), ("A3300", "FOG固定"),
    ("A3600", "AOI"), ("A3700", "FOB"), ("A3800", "ART"),
    ("A3900", "DI铸模固"), ("A3A00", "TP FOG"), ("A3C00", "TP DIS"),
    ("A3D00", "常温aging"), ("A3E00", "Gamma"), ("A3F00", "MT1&TP1"),
    ("A4200", "CG全贴合"), ("A4600", "融合版腔泡"), ("A4800", "UV固化"),
    ("A4900", "背胶贴纸"), ("A4A00", "Demura"), ("A4B00", "MT2&TP2"),
    ("A5100", "PF&SCF"), ("A5D00", "保压"), ("A5400", "贴附磁板"),
    ("A5600", "常温Aging"), ("A6100", "OQC-C测"), ("A6200", "包装入库"),
]
STEP_NAMES_ONLY = [s[0] for s in STEPS]

EQUIPMENT_IDS = [f"EQP{i:03d}" for i in range(1, 31)]
OPERATORS = [f"OP{i:03d}" for i in range(1, 21)]
LINE_IDS = ["LINE01", "LINE02", "LINE03", "LINE04", "LINE05"]
SHIFT_IDS = ["DAY", "NIGHT", "MIDDLE"]
WO_IDS = ["2SHY2601001", "2SHY2601002", "2SHY2601003", "2SHY2601004", "2SHY2601005",
          "2SHY2601006", "XXX"]

GRADE_LIST = ["A", "B", "L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8", "F", "D", "M", "N", "S1", "S2"]
GOOD_GRADES = ["A", "B", "L1"]
BAD_GRADES = ["L2", "L3", "L4", "L5", "L6", "L7", "L8", "F", "D", "M", "N", "S1", "S2"]

DEFECT_CODES = ["SP白斑", "面内异物", "垂直Mura", "其他类型齐排Mura", "雪斑", "CG贴合不均",
                "水平不均(日)", "2nit3正视亮暗格", "黑边mura", "2nit3合偏", "暗点", "日班mura",
                "红斑", "亮点", "2nit3二班", "2nit3三班", "水平暗线", "CG划伤", "重垂直线"]
DEFECT_CATEGORIES = {"SP白斑": "屏体责", "面内异物": "屏体责", "垂直Mura": "屏体责",
                     "雪斑": "模组责", "CG贴合不均": "模组责", "水平不均(日)": "前工程",
                     "2nit3正视亮暗格": "电性料", "黑边mura": "后工程", "2nit3合偏": "生产科",
                     "暗点": "屏体责", "日班mura": "屏体责", "红斑": "屏体责", "亮点": "SQE",
                     "2nit3二班": "INT", "2nit3三班": "INT", "水平暗线": "模组责",
                     "CG划伤": "模组责", "重垂直线": "屏体责", "其他类型齐排Mura": "屏体责"}

STATES = ["IN_PROCESS", "COMPLETED", "ON_HOLD", "SCRAPPED", "SHIPPED"]
COM_CLASSES = ["WIP", "FIN", "SCRAP", "SHIP"]


def rand_dt(start, end):
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))


def fmt(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def fmt6(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S.000000")


# ===================================================
# 1. WIP_LOT - 在制品批次信息表
# ===================================================
print("生成 WIP_LOT...")
wip_lot_rows = []
lot_rrn_map = {}  # lot_id -> object_rrn

total_lots = 3000
start_date = NOW - timedelta(days=90)

for i in range(1, total_lots + 1):
    object_rrn = 10000000 + i
    lot_id = f"LOT{20260101 + i:010d}"
    lot_rrn_map[lot_id] = object_rrn

    created = rand_dt(start_date, NOW)
    part_name = random.choices(PART_NAMES, weights=[0.6, 0.25, 0.15])[0]
    wo_id = random.choice(WO_IDS)
    step_idx = random.randint(0, len(STEPS) - 1)
    step_name, step_desc = STEPS[step_idx]
    equipment_id = random.choice(EQUIPMENT_IDS)
    line_id = random.choice(LINE_IDS)
    operator1 = random.choice(OPERATORS)

    # 等级分布
    grade1 = random.choices(GRADE_LIST,
                            weights=[20, 15, 5, 4, 4, 3, 3, 2, 2, 5, 3, 5, 8, 6, 2, 3])[0]
    grade2 = grade1
    judge1 = "OK" if grade1 in GOOD_GRADES else "NG"

    # 状态
    state = random.choices(STATES, weights=[50, 25, 5, 5, 15])[0]
    com_class = "WIP" if state == "IN_PROCESS" else "FIN" if state == "COMPLETED" else \
        "SCRAP" if state == "SCRAPPED" else "SHIP" if state == "SHIPPED" else "WIP"

    main_qty = random.randint(1, 1)
    track_in_time = rand_dt(created, NOW)
    track_out_time = track_in_time + timedelta(minutes=random.randint(5, 120)) if state != "IN_PROCESS" else None

    # 入库时间（包装站点后）
    in_stock_time = None
    if step_name in ["A6100", "A6200"] and state in ["COMPLETED", "SHIPPED"]:
        in_stock_time = track_out_time

    # OQC状态
    oqc_state = None
    oqc_grade = None
    sampling_flag = None
    if step_name == "A6100":
        oqc_state = "Y"
        oqc_grade = grade1
        sampling_flag = random.choice(["Y", "N", "N", "N"])

    scrap_num = f"SCRAP{i:06d}" if state == "SCRAPPED" else None
    rework_count = random.randint(0, 3) if state in ["IN_PROCESS", "COMPLETED"] else 0

    row = {
        "OBJECT_RRN": object_rrn,
        "ORG_RRN": ORG_RRN,
        "IS_ACTIVE": "Y",
        "CREATED": fmt(created),
        "CREATED_BY": operator1,
        "UPDATED": fmt(track_in_time),
        "UPDATED_BY": operator1,
        "LOCK_VERSION": 1,
        "LOT_ID": lot_id,
        "LOT_TYPE": "PRODUCTION",
        "LOT_ALIAS": "",
        "WO_ID": wo_id,
        "SUBSTRATE_ID1": f"SUB{i:08d}",
        "SUBSTRATE_ID2": "",
        "PART_RRN": 2000000 + PART_NAMES.index(part_name),
        "PART_NAME": part_name,
        "PART_VERSION": 1,
        "PART_DESC": part_name + " 笔电",
        "PART_TYPE": "FG",
        "LAST_PART_NAME": "",
        "MAIN_MAT_TYPE": "PANEL",
        "SUB_MAT_TYPE": "MODULE",
        "CUSTOMER_CODE": "CUSTOMER_A",
        "CUSTOMER_ORDER": wo_id,
        "CUSTOMER_PART_ID": part_name,
        "CUSTOMER_LOT_ID": lot_id,
        "PRIORITY": random.randint(1, 5),
        "PLAN_START_DATE": fmt(created),
        "PLAN_END_DATE": fmt(created + timedelta(days=7)),
        "REQUIRE_DATE": fmt(created + timedelta(days=14)),
        "GRADE1": grade1,
        "GRADE2": grade2,
        "JUDGE1": judge1,
        "JUDGE2": judge1,
        "REWORK_CODE": "",
        "WAREHOUSE_ID": "WH01" if state in ["COMPLETED", "SHIPPED"] else "",
        "LOCATOR_ID": f"LOC{random.randint(1, 100):03d}" if state in ["COMPLETED", "SHIPPED"] else "",
        "LOCATION": "PROD_AREA_A",
        "LINE_ID": line_id,
        "STAGE_ID": "CELL" if step_idx < 15 else "MODULE" if step_idx < 25 else "FG",
        "DURABLE": f"CARRIER{random.randint(1, 50):03d}",
        "POSITION": "",
        "OWNER": random.choice(["GROUP_A", "GROUP_B", "GROUP_C"]),
        "LOT_COMMENT": "",
        "SCHEDULE_TIME": fmt(created),
        "START_MAIN_QTY": main_qty,
        "START_SUB_QTY": 0,
        "START_TIME": fmt(created),
        "END_MAIN_QTY": main_qty if state != "IN_PROCESS" else "",
        "END_SUB_QTY": 0,
        "END_TIME": fmt(track_out_time) if track_out_time else "",
        "MAIN_QTY": main_qty,
        "SUB_QTY": 0,
        "EQUIPMENT_ID": equipment_id,
        "LAST_EQUIPMENT_ID": random.choice(EQUIPMENT_IDS),
        "OPERATOR1": operator1,
        "OPERATOR2": random.choice(OPERATORS),
        "QUEUE_TIME": fmt(track_in_time - timedelta(minutes=random.randint(1, 30))),
        "TRACK_IN_MAIN_QTY": main_qty,
        "TRACK_IN_SUB_QTY": 0,
        "TRACK_IN_TIME": fmt(track_in_time),
        "TRACK_OUT_MAIN_QTY": main_qty if track_out_time else "",
        "TRACK_OUT_SUB_QTY": 0,
        "TRACK_OUT_TIME": fmt(track_out_time) if track_out_time else "",
        "ROOT_LOT_RRN": object_rrn,
        "PARENT_LOT_RRN": "",
        "PARENT_UNIT_RRN": "",
        "SUB_UNIT_TYPE": "",
        "IS_SUB_LOT": "N",
        "COM_CLASS": com_class,
        "STATE": state,
        "SUB_STATE": "",
        "HOLD_STATE": "N" if state != "ON_HOLD" else "Y",
        "TRANSFER_STATE": "IDLE",
        "STATE_ENTRY_TIME": fmt(track_in_time),
        "PRE_TRANS_TYPE": "TRACK_IN",
        "PRE_COM_CLASS": "WIP",
        "PRE_STATE": "IN_PROCESS",
        "PRE_SUB_STATE": "",
        "CURRENT_SEQ": f"SEQ{i:010d}",
        "PROCESS_INSTANCE_RRN": 3000000 + i,
        "PROCESS_RRN": 4000001 if part_name == PART_NAMES[0] else 4000002,
        "PROCESS_NAME": PROCESS_NAMES[0] if part_name == PART_NAMES[0] else PROCESS_NAMES[1],
        "PROCESS_VERSION": 1,
        "PROCEDURE_RRN": 5000001,
        "PROCEDURE_NAME": PROCEDURE_NAMES[0],
        "PROCEDURE_VERSION": 1,
        "STEP_RRN": 6000000 + step_idx,
        "STEP_NAME": step_name,
        "STEP_VERSION": 1,
        "STEP_DESC": step_desc,
        "STEP_STACK": f"PROD_FLOW_A/{step_name}",
        "LAST_STEP_NAME": STEPS[step_idx - 1][0] if step_idx > 0 else "",
        "BATCH_ID": "",
        "REWORK_STACK_COUNT": 0,
        "REWORK_COUNT": rework_count,
        "RECIPE_NAME": f"RECIPE_{step_name}",
        "RECIPE_VERSION": 1,
        "MASK": "",
        "IS_PILOT": "N",
        "USE_COUNT": 1,
        "EXPIRE_TIME": fmt(created + timedelta(days=365)),
        "MINIMAL_EXPIRE_TIME": fmt(created + timedelta(days=180)),
        "TENANT_ID": "DEFAULT",
        "OCAP_ID": "",
        "CONTAMINATION_LEVEL": "",
        "CONTROL_ID": "",
        "RECYCLE_COUNT": 0,
        "SUB_LOCATION": "",
        "EQUIPMENT_MASK": "",
        "EQUIPMENT_RECIPE": f"RECIPE_{step_name}_V1",
        "FAB_BOX_ID": "",
        "FAB_PALLET_ID": "",
        "LOT_PACK_TYPE": "SINGLE" if step_idx >= 28 else "",
        "SAMPLING_FLAG": sampling_flag or "",
        "OQC_GRADE": oqc_grade or "",
        "OQC_STATE": oqc_state or "",
        "OQC_COUNT": 1 if oqc_state else 0,
        "FORBID_PACK": "N",
        "NODE_RRN": 7000000 + step_idx,
        "SUB_PROCESS_TOKEN_RRN": "",
        "INNER_BOX_WEIGHT": "",
        "OUTER_BOX_WEIGHT": "",
        "IS_NEED_REPRINT": "N",
        "LIGHT_TIME": "",
        "IN_STOCK_TIME": fmt(in_stock_time) if in_stock_time else "",
        "RISK_HOLD_FLAG": "N",
        "LAST_JUDGE_STEP_NAME": step_name,
        "LAST_JUDGE_EQP": equipment_id,
        "LAST_DEFECT_EVENT_TIME": fmt(track_in_time) if judge1 == "NG" else "",
        "LAST_DEFECT_CODE": random.choice(DEFECT_CODES) if judge1 == "NG" else "",
        "FORBID_SHIP": "N",
        "IS_ABNORMAL": "N",
        "IS_LINE_OUT": "N",
        "RECOVERY_STATE": "",
        "IS_START": "Y",
        "LAST_MAIN_STEP_GRADE": grade1,
        "RECOVER_WO": "",
        "RECOVER_TIME": "",
        "DATE_CODE": created.strftime("%Y%W"),
        "TRAY_ID": "",
        "CURRENT_PACK_LEVEL": "",
        "LAST_JUDGE_EVENT_TIME": fmt(track_in_time),
        "RECOVER_PLAN_WO": "",
        "SFG_MATERIAL_NAME": "",
        "ACTION_NAME": "TRACK_IN",
        "FIRST_PACK_TIME": "",
        "LOT_FORM": "PANEL",
        "OBA_RESULT": "",
        "OUT_MAIN_PROCESS_NAME": "",
        "OUT_MAIN_STEP_NAME": "",
        "DEBUG_EQP_FLAG": "N",
        "RECOVER_BATCH_ID": "",
        "LAST_MAIN_NODE_STEP": step_name,
        "ACTION_GROUP": "PRODUCTION",
        "OBA_GRADE": "",
        "OBA_STATE": "",
        "TOBEJUDGE_WAREHOUSE": "",
        "BURN_COUNT": 0,
        "OQC_CHECK_OPERATOR": operator1 if oqc_state else "",
        "CHECK_CSN": "",
        "CSN_APPROVAL": "",
        "OQC_INFO_MARK": "",
        "RMA_FLAG": "N",
        "PALLET_NO": "",
        "ARRAY_GRADE": grade1,
        "OLED_GRADE": "",
        "LOT_NO": created.strftime("%Y%m%d"),
        "SCRAP_NUM": scrap_num or "",
        "HOLD_TYPE": "",
        "RWIN_MARK": "",
    }
    wip_lot_rows.append(row)

# 写CSV
with open(f"{OUTPUT_DIR}/WIP_LOT.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(wip_lot_rows[0].keys()))
    writer.writeheader()
    writer.writerows(wip_lot_rows)
print(f"  WIP_LOT: {len(wip_lot_rows)} 行")

# ===================================================
# 2. WIP_LOT_HIS - 在制品历史表（核心！覆盖大多数问题）
# ===================================================
print("生成 WIP_LOT_HIS...")
his_rows = []
his_id = 1

# 为每个LOT生成历史记录（经过各站点）
# 确保有充足的历史数据覆盖各时间维度

# 特殊LOT：工单XXX经过设备EQP001判NG的记录（问题4）
special_wo = "XXX"
special_eqp = "EQP001"

for lot_row in wip_lot_rows:
    lot_id = lot_row["LOT_ID"]
    lot_rrn = lot_row["OBJECT_RRN"]
    part_name = lot_row["PART_NAME"]
    wo_id = lot_row["WO_ID"]
    created = datetime.strptime(lot_row["CREATED"], "%Y-%m-%d %H:%M:%S")
    line_id = lot_row["LINE_ID"]

    # 每个LOT走过几个站点
    num_steps = random.randint(1, len(STEPS))
    current_time = created

    for si in range(num_steps):
        step_name, step_desc = STEPS[si]
        equipment_id = lot_row["EQUIPMENT_ID"] if si == num_steps - 1 else random.choice(EQUIPMENT_IDS)
        operator1 = lot_row["OPERATOR1"]

        # 特殊处理：工单XXX在设备EQP001判NG（问题4）
        if wo_id == special_wo and step_name in ["A3600", "A4200", "A6100"]:
            equipment_id = special_eqp
            judge1 = random.choice(["NG", "NG", "OK"])
        else:
            judge1 = "OK" if random.random() > 0.05 else "NG"

        grade1 = random.choice(GOOD_GRADES) if judge1 == "OK" else random.choice(BAD_GRADES)
        defect_code = random.choice(DEFECT_CODES) if judge1 == "NG" else ""

        track_in_time = current_time + timedelta(minutes=random.randint(1, 60))
        duration = random.randint(10, 180)
        track_out_time = track_in_time + timedelta(minutes=duration)
        current_time = track_out_time

        if current_time > NOW:
            break

        trans_type = "TRACK_OUT"

        row = {
            "OBJECT_RRN": lot_rrn,
            "ORG_RRN": ORG_RRN,
            "IS_ACTIVE": "Y",
            "UPDATED_BY": operator1,
            "TRANS_TYPE": trans_type,
            "TRANS_TIME": fmt6(track_out_time),
            "HISTORY_SEQ": f"HIS{his_id:012d}",
            "HISTORY_SEQ_NO": si + 1,
            "LOT_RRN": lot_rrn,
            "LOT_ID": lot_id,
            "LOT_TYPE": "PRODUCTION",
            "LOT_ALIAS": "",
            "WO_ID": wo_id,
            "SUBSTRATE_ID1": lot_row["SUBSTRATE_ID1"],
            "SUBSTRATE_ID2": "",
            "PART_RRN": lot_row["PART_RRN"],
            "PART_NAME": part_name,
            "PART_VERSION": 1,
            "PART_DESC": part_name + " 笔电",
            "PART_TYPE": "FG",
            "MAIN_MAT_TYPE": "PANEL",
            "SUB_MAT_TYPE": "MODULE",
            "CUSTOMER_CODE": "CUSTOMER_A",
            "CUSTOMER_ORDER": wo_id,
            "CUSTOMER_PART_ID": part_name,
            "CUSTOMER_LOT_ID": lot_id,
            "PRIORITY": lot_row["PRIORITY"],
            "PLAN_START_DATE": lot_row["PLAN_START_DATE"],
            "PLAN_END_DATE": lot_row["PLAN_END_DATE"],
            "REQUIRE_DATE": lot_row["REQUIRE_DATE"],
            "GRADE1": grade1,
            "GRADE2": grade1,
            "JUDGE1": judge1,
            "JUDGE2": judge1,
            "REWORK_CODE1": "",
            "WAREHOUSE_ID": "",
            "LOCATOR_ID": "",
            "LOCATION": "PROD_AREA_A",
            "LINE_ID": line_id,
            "TEAM_ID": random.choice(SHIFT_IDS),
            "STAGE_ID": "CELL" if si < 15 else "MODULE" if si < 25 else "FG",
            "DURABLE": lot_row["DURABLE"],
            "OWNER": lot_row["OWNER"],
            "LOT_COMMENT": "",
            "SCHEDULE_TIME": lot_row["SCHEDULE_TIME"],
            "START_MAIN_QTY": 1,
            "START_SUB_QTY": 0,
            "START_TIME": fmt(track_in_time),
            "END_MAIN_QTY": 1,
            "END_SUB_QTY": 0,
            "END_TIME": fmt(track_out_time),
            "MAIN_QTY": 1,
            "SUB_QTY": 0,
            "TRANS_MAIN_QTY": 1,
            "TRANS_SUB_QTY": 0,
            "EQUIPMENT_ID": equipment_id,
            "LAST_EQUIPMENT_ID": random.choice(EQUIPMENT_IDS),
            "OPERATOR1": operator1,
            "OPERATOR2": random.choice(OPERATORS),
            "QUEUE_TIME": fmt(track_in_time - timedelta(minutes=random.randint(1, 10))),
            "TRACK_IN_MAIN_QTY": 1,
            "TRACK_IN_SUB_QTY": 0,
            "TRACK_IN_TIME": fmt(track_in_time),
            "TRACK_OUT_MAIN_QTY": 1,
            "TRACK_OUT_SUB_QTY": 0,
            "TRACK_OUT_TIME": fmt(track_out_time),
            "ROOT_LOT_RRN": lot_rrn,
            "PARENT_LOT_RRN": "",
            "PARENT_UNIT_RRN": "",
            "SUB_UNIT_TYPE": "",
            "IS_SUB_LOT": "N",
            "COM_CLASS": "WIP",
            "STATE": "IN_PROCESS",
            "SUB_STATE": "",
            "HOLD_STATE": "N",
            "TRANSFER_STATE": "IDLE",
            "STATE_ENTRY_TIME": fmt(track_in_time),
            "PRE_TRANS_TYPE": "TRACK_IN",
            "PRE_COM_CLASS": "WIP",
            "PRE_STATE": "IN_PROCESS",
            "PRE_SUB_STATE": "",
            "CURRENT_SEQ": f"SEQ{his_id:010d}",
            "PROCESS_INSTANCE_RRN": lot_row["PROCESS_INSTANCE_RRN"],
            "PROCESS_RRN": lot_row["PROCESS_RRN"],
            "PROCESS_NAME": lot_row["PROCESS_NAME"],
            "PROCESS_VERSION": 1,
            "PROCEDURE_RRN": 5000001,
            "PROCEDURE_NAME": PROCEDURE_NAMES[0],
            "PROCEDURE_VERSION": 1,
            "STEP_RRN": 6000000 + si,
            "STEP_NAME": step_name,
            "STEP_VERSION": 1,
            "STEP_DESC": step_desc,
            "STEP_STACK": f"PROD_FLOW_A/{step_name}",
            "LAST_STEP_NAME": STEPS[si - 1][0] if si > 0 else "",
            "BATCH_ID": "",
            "REWORK_STACK_COUNT": 0,
            "REWORK_COUNT": lot_row["REWORK_COUNT"],
            "RECIPE_NAME": f"RECIPE_{step_name}",
            "RECIPE_VERSION": 1,
            "MASK": "",
            "ITEM_SET_NAME": "",
            "ITEM_SET_VERSION": "",
            "ACTION_CODE": defect_code,
            "ACTION_REASON": defect_code,
            "ACTION_COMMENT": "",
            "OCAP_ID": "",
            "HIS_COMMENT": "",
            "USE_COUNT": 1,
            "TENANT_ID": "DEFAULT",
            "LOT_CREATE_TIME": lot_row["CREATED"],
            "CONTAMINATION_LEVEL": "",
            "REWORK_CODE": "",
            "IS_PILOT": "N",
            "CONTROL_ID": "",
            "RECYCLE_COUNT": 0,
            "SUB_LOCATION": "",
            "POSITION": "",
            "EQUIPMENT_MASK": "",
            "EQUIPMENT_RECIPE": f"RECIPE_{step_name}_V1",
            "FAB_BOX_ID": "",
            "FAB_PALLET_ID": "",
            "LOT_PACK_TYPE": "",
            "SAMPLING_FLAG": "",
            "OQC_GRADE": grade1 if step_name == "A6100" else "",
            "OQC_STATE": "Y" if step_name == "A6100" else "",
            "OQC_COUNT": 1 if step_name == "A6100" else 0,
            "FORBID_PACK": "N",
            "NODE_RRN": 7000000 + si,
            "SUB_PROCESS_TOKEN_RRN": "",
            "INNER_BOX_WEIGHT": "",
            "OUTER_BOX_WEIGHT": "",
            "IS_NEED_REPRINT": "N",
            "LIGHT_TIME": "",
            "IN_STOCK_TIME": fmt(track_out_time) if step_name == "A6200" else "",
            "RISK_HOLD_FLAG": "N",
            "LAST_JUDGE_STEP_NAME": step_name,
            "LAST_JUDGE_EQP": equipment_id,
            "LAST_DEFECT_EVENT_TIME": fmt(track_out_time) if judge1 == "NG" else "",
            "FORBID_SHIP": "N",
            "IS_ABNORMAL": "N",
            "IS_LINE_OUT": "N",
            "RECOVERY_STATE": "",
            "IS_START": "Y",
            "LAST_MAIN_STEP_GRADE": grade1,
            "RECOVER_WO": "",
            "RECOVER_TIME": "",
            "TRAY_ID": "",
            "CURRENT_PACK_LEVEL": "",
            "LAST_JUDGE_EVENT_TIME": fmt(track_out_time),
            "LAST_DEFECT_CODE": defect_code,
            "RECOVER_PLAN_WO": "",
            "SFG_MATERIAL_NAME": "",
            "DATE_CODE": track_out_time.strftime("%Y%W"),
            "ACTION_NAME": trans_type,
            "FIRST_PACK_TIME": fmt(track_out_time) if step_name == "A6200" else "",
            "LOT_FORM": "PANEL",
            "OBA_RESULT": "",
            "OUT_MAIN_PROCESS_NAME": "",
            "OUT_MAIN_STEP_NAME": "",
            "DEBUG_EQP_FLAG": "N",
            "RECOVER_BATCH_ID": "",
            "LAST_MAIN_NODE_STEP": step_name,
            "ACTION_GROUP": "PRODUCTION",
            "OBA_GRADE": "",
            "OBA_STATE": "",
            "TOBEJUDGE_WAREHOUSE": "",
            "BURN_COUNT": 0,
            "OQC_CHECK_OPERATOR": operator1 if step_name == "A6100" else "",
            "CHECK_CSN": "",
            "CSN_APPROVAL": "",
            "OQC_INFO_MARK": "",
            "RMA_FLAG": "N",
            "PALLET_NO": "",
            "ARRAY_GRADE": grade1,
            "OLED_GRADE": "",
            "LOT_NO": track_out_time.strftime("%Y%m%d"),
            "LAST_STEP_GRADE": grade1,
            "SCRAP_NUM": lot_row["SCRAP_NUM"],
            "HOLD_TYPE": "",
            "RWIN_MARK": "",
        }
        his_rows.append(row)
        his_id += 1

        # 控制总数量
        if len(his_rows) >= 80000:
            break
    if len(his_rows) >= 80000:
        break

# 确保有今天和昨天的包装入库记录（问题2）
today = datetime(2026, 3, 3, 8, 0, 0)
yesterday = datetime(2026, 3, 2, 8, 0, 0)
for day_start, n in [(today, 150), (yesterday, 120)]:
    for j in range(n):
        t = day_start + timedelta(hours=random.uniform(0, 12))
        lot_id = f"PKG{j:08d}_{day_start.strftime('%m%d')}"
        his_id += 1
        grade1 = random.choices(GRADE_LIST, weights=[20, 15, 5, 4, 4, 3, 3, 2, 2, 5, 3, 5, 8, 6, 2, 3])[0]
        row = his_rows[0].copy()
        row.update({
            "OBJECT_RRN": 90000000 + his_id,
            "TRANS_TIME": fmt6(t),
            "HISTORY_SEQ": f"HIS{his_id:012d}",
            "HISTORY_SEQ_NO": 29,
            "LOT_ID": lot_id,
            "LOT_RRN": 90000000 + his_id,
            "STEP_NAME": "A6200",
            "STEP_DESC": "包装入库",
            "TRANS_TYPE": "TRACK_OUT",
            "ACTION_NAME": "TRACK_OUT",
            "IN_STOCK_TIME": fmt(t),
            "COM_CLASS": "FIN",
            "STATE": "COMPLETED",
            "GRADE1": grade1,
            "GRADE2": grade1,
            "JUDGE1": "OK" if grade1 in GOOD_GRADES else "NG",
            "JUDGE2": "OK" if grade1 in GOOD_GRADES else "NG",
            "PART_NAME": random.choice(PART_NAMES),
            "WO_ID": random.choice(WO_IDS[:-1]),
            "TRACK_IN_TIME": fmt(t - timedelta(minutes=30)),
            "TRACK_OUT_TIME": fmt(t),
            "END_TIME": fmt(t),
            "LOT_NO": t.strftime("%Y%m%d"),
        })
        his_rows.append(row)

# 确保有来料责不良记录（问题6）- 上个月
last_month_start = datetime(2026, 2, 1)
last_month_end = datetime(2026, 2, 28)
for j in range(500):
    t = rand_dt(last_month_start, last_month_end)
    his_id += 1
    defect_code = random.choices(DEFECT_CODES, weights=[10, 8, 7, 6, 5, 4, 4, 3, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1])[0]
    defect_cat = DEFECT_CATEGORIES.get(defect_code, "屏体责")
    is_sqe = defect_cat == "SQE"
    grade1 = random.choice(BAD_GRADES)
    row = his_rows[0].copy()
    row.update({
        "OBJECT_RRN": 91000000 + j,
        "TRANS_TIME": fmt6(t),
        "HISTORY_SEQ": f"HIS{his_id:012d}",
        "HISTORY_SEQ_NO": random.randint(1, 20),
        "LOT_ID": f"SQE{j:08d}",
        "LOT_RRN": 91000000 + j,
        "STEP_NAME": random.choice(STEP_NAMES_ONLY),
        "TRANS_TYPE": "TRACK_OUT",
        "ACTION_NAME": "TRACK_OUT",
        "JUDGE1": "NG",
        "JUDGE2": "NG",
        "GRADE1": grade1,
        "GRADE2": grade1,
        "ACTION_CODE": defect_code,
        "ACTION_REASON": defect_code,
        "LAST_DEFECT_CODE": defect_code,
        "OWNER": "SQE_GROUP" if is_sqe else "PROD_GROUP",
        "LOT_NO": t.strftime("%Y%m%d"),
        "WO_ID": random.choice(WO_IDS[:-1]),
        "PART_NAME": PART_NAMES[0],
    })
    his_rows.append(row)

with open(f"{OUTPUT_DIR}/WIP_LOT_HIS.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(his_rows[0].keys()))
    writer.writeheader()
    writer.writerows(his_rows)
print(f"  WIP_LOT_HIS: {len(his_rows)} 行")

# ===================================================
# 3. WIP_LOT_MAP - ID关联表
# ===================================================
print("生成 WIP_LOT_MAP...")
map_rows = []
for i, lot_row in enumerate(wip_lot_rows[:1000]):
    created = datetime.strptime(lot_row["CREATED"], "%Y-%m-%d %H:%M:%S")
    map_rows.append({
        "OBJECT_RRN": 20000000 + i,
        "ORG_RRN": ORG_RRN,
        "IS_ACTIVE": "Y",
        "CREATED": fmt(created),
        "CREATED_BY": lot_row["CREATED_BY"],
        "UPDATED": fmt(created),
        "UPDATED_BY": lot_row["CREATED_BY"],
        "LOCK_VERSION": 1,
        "LOT_ID": lot_row["LOT_ID"],
        "LOT_RRN": lot_row["OBJECT_RRN"],
        "TARGET_TYPE": "SUBSTRATE",
        "TARGET_ID": lot_row["SUBSTRATE_ID1"],
        "STEP_NAME": lot_row["STEP_NAME"],
        "EQUIPMENT_ID": lot_row["EQUIPMENT_ID"],
    })

with open(f"{OUTPUT_DIR}/WIP_LOT_MAP.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(map_rows[0].keys()))
    writer.writeheader()
    writer.writerows(map_rows)
print(f"  WIP_LOT_MAP: {len(map_rows)} 行")

# ===================================================
# 4. MM_MATERIAL - 物料定义表
# ===================================================
print("生成 MM_MATERIAL...")
mat_rows = []
created_base = datetime(2024, 1, 1)
for i, pn in enumerate(PART_NAMES):
    mat_rows.append({
        "OBJECT_RRN": 2000000 + i,
        "ORG_RRN": ORG_RRN,
        "IS_ACTIVE": "Y",
        "CREATED": fmt(created_base),
        "CREATED_BY": "ADMIN",
        "UPDATED": fmt(created_base),
        "UPDATED_BY": "ADMIN",
        "LOCK_VERSION": 1,
        "NAME": pn,
        "DESCRIPTION": pn + " 模组",
        "VERSION": 1,
        "STATUS": "ACTIVE",
        "ACTIVE_TIME": fmt(created_base),
        "ACTIVE_USER": "ADMIN",
        "CLASS": "FG",
        "IS_GLOBAL": "N",
        "PROCESS_NAME": PROCESS_NAMES[0] if i == 0 else PROCESS_NAMES[1],
        "PROCESS_VERSION": 1,
        "PARTNER_CODE": "",
        "EAN": "",
        "SKU": pn,
        "UOM_ID": "PCS",
        "CATEGORY": "DISPLAY",
        "MATERIAL_TYPE": "MODULE",
        "SUB_MATERIAL_TYPE": "LCD",
        "GROUP1": "NOTEBOOK",
        "GROUP2": "14INCH" if "14" in pn else "15INCH" if "15" in pn else "13INCH",
        "GROUP3": "", "GROUP4": "",
        "CLASSIFICATION": "A",
        "SPEC1": pn, "SPEC2": "", "SPEC3": "", "SPEC4": "",
        "BOM_VERIFIED": "Y",
        "IS_PRODUCTION": "Y",
        "IS_PHANTOM": "N",
        "STATUS_MODEL_RRN": "",
        "SAFETY_STOCK_QTY": 100,
        "MAX_STOCK_QTY": 10000,
        "NUMBER_OF_PACK": 1,
        "NUMBER_OF_PALLET": 100,
        "BATCH_TYPE": "LOT",
        "LOT_SIZE": 1,
        "SUB_LOT_SIZE": "",
        "ID_GENERATOR": "AUTO",
        "IS_TIME_SENSITIVE": "N",
        "SHELF_WARNING": 30,
        "SHELF_LIFE": 365,
        "SHELF_LIFE_UNIT": "DAY",
        "FLOOR_LIFE": 168,
        "FLOOR_LIFE_UNIT": "HOUR",
        "FLOOR_LIFE_ACTIVATOR": "OPEN",
        "LIMIT_WARNING": "", "LIMIT_LIFE": "",
        "VOLUME": "", "WEIGHT": "",
        "SHELF_WIDTH": "", "SHELF_HEIGHT": "", "SHELF_DEPTH": "",
        "OWNER1": "GROUP_A", "OWNER2": "",
        "COMMENTS": "",
        "RESERVED1": "", "RESERVED2": "", "RESERVED3": "", "RESERVED4": "",
        "RESERVED5": "", "RESERVED6": "", "RESERVED7": "", "RESERVED8": "",
        "WAREHOUSE_RRN": "",
        "MAIN_MAT_TYPE": "PANEL",
        "SUB_MAT_TYPE": "MODULE",
        "STYLE": "",
        "DISPLAY_VERSION": "V1",
        "PACKAGE_HIERARCHY_NAME": "BOX>PALLET",
        "TENANT_ID": "DEFAULT",
        "INIT_GRADE": "A",
        "REWORK_LIMIT_COUNT": 3,
        "LIMIT_CLEAN_COUNT": "",
        "IS_NEED_CLEAN": "N",
        "LIMIT_USE_COUNT": "",
        "FLOOR_LIFE_RESET": "N",
        "CUSTOMER_CODE": "CUSTOMER_A",
        "RECOVERY_INIT_GRADE": "N",
    })

with open(f"{OUTPUT_DIR}/MM_MATERIAL.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(mat_rows[0].keys()))
    writer.writeheader()
    writer.writerows(mat_rows)
print(f"  MM_MATERIAL: {len(mat_rows)} 行")

# ===================================================
# 5. WF_PROCESS - 工艺流程定义表
# ===================================================
print("生成 WF_PROCESS...")
proc_rows = []
created_base = datetime(2024, 1, 1)
for i, pn in enumerate(PROCESS_NAMES):
    proc_rows.append({
        "OBJECT_RRN": 4000001 + i,
        "ORG_RRN": ORG_RRN,
        "IS_ACTIVE": "Y",
        "CREATED": fmt(created_base),
        "CREATED_BY": "ADMIN",
        "UPDATED": fmt(created_base),
        "UPDATED_BY": "ADMIN",
        "LOCK_VERSION": 1,
        "NAME": pn,
        "DESCRIPTION": f"主工艺流程{i + 1}",
        "VERSION": 1,
        "STATUS": "ACTIVE",
        "ACTIVE_TIME": fmt(created_base),
        "ACTIVE_USER": "ADMIN",
        "USE_CATEGORY": "Main",
        "COMMENTS": "",
        "RESERVED1": "", "RESERVED2": "", "RESERVED3": "", "RESERVED4": "", "RESERVED5": "",
        "RESERVED6": "", "RESERVED7": "", "RESERVED8": "", "RESERVED9": "", "RESERVED10": "",
    })

with open(f"{OUTPUT_DIR}/WF_PROCESS.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(proc_rows[0].keys()))
    writer.writeheader()
    writer.writerows(proc_rows)
print(f"  WF_PROCESS: {len(proc_rows)} 行")

# ===================================================
# 6. WF_PROCESS_FLOW_NODE - 流程节点表
# ===================================================
print("生成 WF_PROCESS_FLOW_NODE...")
node_rows = []
created_base = datetime(2024, 1, 1)
for proc_idx, proc_rrn in enumerate([4000001, 4000002]):
    for si, (step_name, step_desc) in enumerate(STEPS):
        node_rrn = 7000000 + proc_idx * 100 + si
        node_rows.append({
            "OBJECT_RRN": node_rrn,
            "ORG_RRN": ORG_RRN,
            "IS_ACTIVE": "Y",
            "CREATED": fmt(created_base),
            "CREATED_BY": "ADMIN",
            "UPDATED": fmt(created_base),
            "UPDATED_BY": "ADMIN",
            "LOCK_VERSION": 1,
            "PROCESS_RRN": proc_rrn,
            "PROCESS_NAME": PROCESS_NAMES[proc_idx],
            "PROCESS_VERSION": 1,
            "SEQ_NO": si + 1,
            "STEP_RRN": 6000000 + si,
            "STEP_NAME": step_name,
            "STEP_VERSION": 1,
            "PRIVIOUS_NODE_RRN": 7000000 + proc_idx * 100 + si - 1 if si > 0 else "",
            "NEXT_NODE_RRN": 7000000 + proc_idx * 100 + si + 1 if si < len(STEPS) - 1 else "",
            "NODE_TYPE": "NORMAL",
        })

with open(f"{OUTPUT_DIR}/WF_PROCESS_FLOW_NODE.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(node_rows[0].keys()))
    writer.writeheader()
    writer.writerows(node_rows)
print(f"  WF_PROCESS_FLOW_NODE: {len(node_rows)} 行")

# ===================================================
# 7. WIP_GRADE_DEFINATION - 等级定义表
# ===================================================
print("生成 WIP_GRADE_DEFINATION...")
grade_def_rows = []
created_base = datetime(2024, 1, 1)
grade_configs = [
    ("A", "GOOD", 1), ("B", "GOOD", 2), ("L1", "GOOD", 3),
    ("L2", "BAD", 4), ("L3", "BAD", 5), ("L4", "BAD", 6),
    ("L5", "BAD", 7), ("L6", "BAD", 8), ("L7", "BAD", 9),
    ("L8", "BAD", 10), ("F", "SCRAP", 11), ("D", "BAD", 12),
    ("M", "BAD", 13), ("N", "BAD", 14), ("S1", "BAD", 15), ("S2", "BAD", 16),
]
for i, (grade, category, seq) in enumerate(grade_configs):
    grade_def_rows.append({
        "OBJECT_RRN": 8000000 + i,
        "ORG_RRN": ORG_RRN,
        "IS_ACTIVE": "Y",
        "CREATED": fmt(created_base),
        "CREATED_BY": "ADMIN",
        "UPDATED": fmt(created_base),
        "UPDATED_BY": "ADMIN",
        "LOCK_VERSION": 1,
        "SEQ": seq,
        "GRADE": grade,
        "GRADE_CATEGORY": category,
    })

with open(f"{OUTPUT_DIR}/WIP_GRADE_DEFINATION.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(grade_def_rows[0].keys()))
    writer.writeheader()
    writer.writerows(grade_def_rows)
print(f"  WIP_GRADE_DEFINATION: {len(grade_def_rows)} 行")

# ===================================================
# 8. PRD_PART_DEFECT_CODE - 不良规则表
# ===================================================
print("生成 PRD_PART_DEFECT_CODE...")
defect_rows = []
created_base = datetime(2024, 1, 1)
di = 0
for part_name in PART_NAMES:
    for step_name, _ in STEPS[5:]:  # 从A2500开始才有不良
        for defect_code in DEFECT_CODES:
            for grade in BAD_GRADES[:6]:  # L2-L7
                di += 1
                defect_rows.append({
                    "OBJECT_RRN": 9000000 + di,
                    "ORG_RRN": ORG_RRN,
                    "IS_ACTIVE": "Y",
                    "CREATED": fmt(created_base),
                    "CREATED_BY": "ADMIN",
                    "UPDATED": fmt(created_base),
                    "UPDATED_BY": "ADMIN",
                    "LOCK_VERSION": 1,
                    "PART_NAME": part_name,
                    "STEP_NAME": step_name,
                    "DEFECT_CODE": defect_code,
                    "DEFECT_CATEGORY": DEFECT_CATEGORIES.get(defect_code, "屏体责"),
                    "DEFECT_DESC": defect_code + "不良",
                    "GRADE": grade,
                    "GRADE_DESC": grade + "级",
                    "RESPONSIBILITY_GROUP": DEFECT_CATEGORIES.get(defect_code, "屏体责"),
                })

with open(f"{OUTPUT_DIR}/PRD_PART_DEFECT_CODE.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(defect_rows[0].keys()))
    writer.writeheader()
    writer.writerows(defect_rows)
print(f"  PRD_PART_DEFECT_CODE: {len(defect_rows)} 行")

print(f"\n✅ 所有CSV文件已生成到: {OUTPUT_DIR}")
print("文件列表:")
for f in os.listdir(OUTPUT_DIR):
    size = os.path.getsize(f"{OUTPUT_DIR}/{f}") / 1024 / 1024
    print(f"  {f}: {size:.1f} MB")
