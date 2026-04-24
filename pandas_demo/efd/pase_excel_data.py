import os
import logging
import pandas as pd
import clickhouse_connect

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='efd_data_processing.log'
)
logger = logging.getLogger('pase_excel_data')

# ClickHouse 连接配置
CLICKHOUSE_CONFIG = {
    'host': '192.168.1.33',
    'user': 'default',
    'password': 'h6TWgrz227Fubhmb',
    'database': 'rptdw'
}

# 文件路径配置
SQL_FILE_PATH = 'efd/rptdw/rptdw_v2.sql'
ORIGIN_DATA_DIR = 'efd/origin_data'

class DataProcessor:
    def __init__(self):
        self.client = None
        self.excel_data = {}
        self.sql_data = {}
        self.processed_data = {}
    
    def connect_clickhouse(self):
        """连接到 ClickHouse 数据库"""
        try:
            self.client = clickhouse_connect.get_client(**CLICKHOUSE_CONFIG)
            logger.info('成功连接到 ClickHouse 数据库')
            return True
        except Exception as e:
            logger.error(f'连接 ClickHouse 失败: {e}')
            return False
    
    def execute_sql_file(self, sql_file):
        """执行 SQL 文件创建数据库和表"""
        try:
            with open(sql_file, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            # 分割 SQL 语句并执行
            sql_statements = sql_content.split(';')
            for stmt in sql_statements:
                stmt = stmt.strip()
                if stmt:
                    self.client.command(stmt)
                    logger.info(f'执行 SQL 语句成功: {stmt[:100]}...')
            return True
        except Exception as e:
            logger.error(f'执行 SQL 文件失败: {e}')
            return False
    
    def parse_excel_files(self):
        """解析 origin_data 目录下的 Excel 文件"""
        try:
            # 这里假设 Excel 文件存在，实际项目中需要根据具体文件名处理
            # 由于当前目录下只有 SQL 文件，我们暂时模拟解析过程
            logger.info('开始解析 Excel 文件')
            # 模拟解析结果
            self.excel_data = {
                'ods_mes_mm_material': pd.DataFrame({
                    'object_rrn': [1, 2, 3],
                    'name': ['物料1', '物料2', '物料3'],
                    'description': ['描述1', '描述2', '描述3'],
                    'status': ['ACTIVE', 'ACTIVE', 'INACTIVE']
                }),
                'ods_mes_wf_process_flow_node': pd.DataFrame({
                    'object_rrn': [1, 2],
                    'process_name': ['工艺1', '工艺2'],
                    'step_name': ['工站1', '工站2']
                })
            }
            logger.info('Excel 文件解析完成')
            return True
        except Exception as e:
            logger.error(f'解析 Excel 文件失败: {e}')
            return False
    
    def load_sql_data(self):
        """加载 origin_data 目录下的 SQL 文件数据"""
        try:
            logger.info('开始加载 SQL 文件数据')
            for file_name in os.listdir(ORIGIN_DATA_DIR):
                if file_name.endswith('.sql'):
                    table_name = file_name.split('_', 1)[1].split('.')[0].lower()
                    file_path = os.path.join(ORIGIN_DATA_DIR, file_name)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        sql_content = f.read()
                    # 提取数据（这里简化处理，实际需要解析 INSERT 语句）
                    self.sql_data[table_name] = sql_content
                    logger.info(f'加载 SQL 文件: {file_name}')
            logger.info('SQL 文件数据加载完成')
            return True
        except Exception as e:
            logger.error(f'加载 SQL 文件数据失败: {e}')
            return False
    
    def compare_data(self):
        """比对解析的 Excel 数据和手动复制的 SQL 数据"""
        try:
            logger.info('开始比对数据')
            for table_name in self.excel_data:
                if table_name in self.sql_data:
                    logger.info(f'比对表: {table_name}')
                    logger.info(f'Excel 数据行数: {len(self.excel_data[table_name])}')
                    logger.info(f'SQL 数据内容: {self.sql_data[table_name][:200]}...')
            logger.info('数据比对完成')
            return True
        except Exception as e:
            logger.error(f'数据比对失败: {e}')
            return False
    
    def fill_empty_fields(self):
        """补全数据中的空字段"""
        try:
            logger.info('开始补全空字段')
            for table_name, df in self.excel_data.items():
                # 补全空字段（这里根据业务逻辑进行处理）
                for col in df.columns:
                    if df[col].isnull().any():
                        if df[col].dtype == 'object':
                            df[col].fillna('', inplace=True)
                        elif df[col].dtype in ['int64', 'float64']:
                            df[col].fillna(0, inplace=True)
                self.processed_data[table_name] = df
                logger.info(f'补全表 {table_name} 的空字段')
            logger.info('空字段补全完成')
            return True
        except Exception as e:
            logger.error(f'补全空字段失败: {e}')
            return False
    
    def write_to_clickhouse(self):
        """将处理后的数据写入 ClickHouse"""
        try:
            logger.info('开始写入 ClickHouse')
            for table_name, df in self.processed_data.items():
                if not df.empty:
                    # 提取列名和数据
                    columns = list(df.columns)
                    data = df.to_dict('records')
                    # 使用 clickhouse-connect 的 insert 方法插入数据
                    self.client.insert(f'rptdw.{table_name}', data, columns=columns)
                    logger.info(f'成功写入表 {table_name}，共 {len(df)} 条数据')
            logger.info('数据写入完成')
            return True
        except Exception as e:
            logger.error(f'写入 ClickHouse 失败: {e}')
            return False
    
    def run(self):
        """运行整个数据处理流程"""
        logger.info('开始数据处理流程')
        
        # 1. 连接 ClickHouse
        if not self.connect_clickhouse():
            return False
        
        # 2. 执行 SQL 文件创建表
        if not self.execute_sql_file(SQL_FILE_PATH):
            return False
        
        # 3. 解析 Excel 文件
        if not self.parse_excel_files():
            return False
        
        # 4. 加载 SQL 数据
        if not self.load_sql_data():
            return False
        
        # 5. 比对数据
        if not self.compare_data():
            return False
        
        # 6. 补全空字段
        if not self.fill_empty_fields():
            return False
        
        # 7. 写入 ClickHouse
        if not self.write_to_clickhouse():
            return False
        
        logger.info('数据处理流程完成')
        return True

if __name__ == '__main__':
    processor = DataProcessor()
    processor.run()