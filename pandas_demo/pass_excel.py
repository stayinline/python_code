import pandas as pd
from datetime import datetime


def excel_to_sql_insert(excel_file_path, output_sql_file=None):
    """
    解析Excel文件并生成PostgreSQL INSERT语句

    Args:
        excel_file_path: Excel文件路径
        output_sql_file: 输出的SQL文件路径（可选）
    """

    # 读取Excel文件
    df = pd.read_excel(excel_file_path)

    # 检查必要的列是否存在
    required_columns = ['原代培养板ID', '第几次换液', '完成时间']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Excel文件中缺少必要的列: {col}")

    # 生成INSERT语句列表
    insert_statements = []

    for index, row in df.iterrows():
        # 构建INSERT语句
        insert_sql = f"""
INSERT INTO sl_change_liquid (
    id, project_id, project_no, initial_sample_id, protocol_step_id, 
    plate_barcode, operation_time, volume, generation, drug_info, 
    change_liquid_count, extra, digestion, report_time, _source_type
) VALUES (
    {index + 1},  -- id (使用行号+1作为示例ID)
    NULL,  -- project_id
    NULL,  -- project_no
    NULL,  -- initial_sample_id
    'change_liquid_step_{row['第几次换液']}',  -- protocol_step_id
    '{row['原代培养板ID']}',  -- plate_barcode
    '{row['完成时间']}',  -- operation_time
    NULL,  -- volume
    NULL,  -- generation
    NULL,  -- drug_info
    '{row['第几次换液']}',  -- change_liquid_count
    NULL,  -- extra
    NULL,  -- digestion
    '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}',  -- report_time (使用当前时间)
    2  -- _source_type
);"""

        insert_statements.append(insert_sql)

    # 输出或保存SQL语句
    sql_content = '\n'.join(insert_statements)

    if output_sql_file:
        with open(output_sql_file, 'w', encoding='utf-8') as f:
            f.write(sql_content)
        print(f"SQL文件已生成: {output_sql_file}")

    # 打印到控制台
    print("生成的INSERT语句:")
    print(sql_content)

    return insert_statements


# 使用示例
if __name__ == "__main__":
    # 替换为你的Excel文件路径
    # excel_file = "D:\download\麒麟项目demo数据9-8\麒麟项目demo数据9-8\原代样本换液记录.xlsx"
    excel_file = "D:\download\麒麟项目demo数据9-8\麒麟项目demo数据9-8\样本换液记录1-传代.xlsx"

    try:
        # 生成SQL语句
        sql_statements = excel_to_sql_insert(excel_file, "insert_data.sql")
        print(f"成功生成 {len(sql_statements)} 条INSERT语句")
    except Exception as e:
        print(f"错误: {e}")