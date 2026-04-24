

--这张表的数据来自“D:\code\python\pandas_demo\efd\日报涉及表结构与数据样例.xlsx” 这个文件
-- 的 “imp_yield_grade” 这个sheet的第 13（表头） 到 23 行，每一列和这个表的每一列一一对应


我需要从Oracle中原封不动的把数据同步到  clickhouse中，把下面这个Oracle的建表语句，转换成clickhouse的：

	CREATE TABLE "RPTDW"."IMP_YIELD_GRADE"
	( "GRADE_ID" NUMBER,
	"PANEL_GRADE" VARCHAR2(32)
	) SEGMENT CREATION IMMEDIATE
	PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255
	NOCOMPRESS LOGGING
	TABLESPACE "LCP_BI_IDX" ;



--下面是手动复制Excel表格中的数据。做check

GRADE_ID	PANEL_GRADE
20	A1
21	A2
3	A
4	B
5	L1
6	L2
7	L3
8	L4
9	L5
10	L6
