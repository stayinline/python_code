
CREATE TABLE IF NOT EXISTS rptdw.ods_mes_mm_material
(
    object_rrn              Int64 COMMENT '对象序列号',
    org_rrn                 Nullable(Int64) COMMENT '区域ID',
    is_active               Nullable(String) COMMENT '对象是否生效',
    created                 Nullable(DateTime) COMMENT '创建时间',
    created_by              Nullable(String) COMMENT '创建人ID',
    updated                 Nullable(DateTime) COMMENT '更新时间',
    updated_by              Nullable(String) COMMENT '更新人ID',
    lock_version            Nullable(Int64) COMMENT '锁定版本',

    name                    Nullable(String) COMMENT '物料名称',
    description             Nullable(String) COMMENT '描述',
    version                 Nullable(Int64) COMMENT '物料版本',
    status                  Nullable(String) COMMENT '状态',
    active_time             Nullable(DateTime) COMMENT '激活时间',
    active_user             Nullable(String) COMMENT '激活用户名',

    class                   Nullable(String) COMMENT '类型 (成品/半成品/原料)',
    is_global               Nullable(String) COMMENT '是否全局',

    process_name            Nullable(String) COMMENT '工艺名称',
    process_version         Nullable(Int64) COMMENT '工艺版本',

    partner_code            Nullable(Int64) COMMENT '供应商代码',
    ean                     Nullable(String) COMMENT 'EAN码<商品用条码>',
    sku                     Nullable(String) COMMENT 'SKU号',
    uom_id                  Nullable(String) COMMENT '物料单位',
    category                Nullable(String) COMMENT '类别',
    material_type           Nullable(String) COMMENT '物料类型',
    sub_material_type       Nullable(String) COMMENT '子物料类型',

    group1                  Nullable(String) COMMENT '物料组别1',
    group2                  Nullable(String) COMMENT '物料组别2',
    group3                  Nullable(String) COMMENT '物料组别3',
    group4                  Nullable(String) COMMENT '物料组别4',

    classification          Nullable(String) COMMENT '物料ABC分类法',

    spec1                   Nullable(String) COMMENT '物料规格1',
    spec2                   Nullable(String) COMMENT '物料规格2',
    spec3                   Nullable(String) COMMENT '物料规格3',
    spec4                   Nullable(String) COMMENT '物料规格4',

    bom_verified            Nullable(String) COMMENT '物料清单验证',
    is_production           Nullable(String) COMMENT '是否生产物料',
    is_phantom              Nullable(String) COMMENT '是否虚拟料',

    status_model_rrn        Nullable(Int64) COMMENT '状态模型主键',

    safety_stock_qty        Nullable(Float64) COMMENT '安全库存量',
    max_stock_qty           Nullable(Float64) COMMENT '最大库存量',

    number_of_pack          Nullable(Int64) COMMENT '包装数量',
    number_of_pallet        Nullable(Int64) COMMENT '托盘数量',

    batch_type              Nullable(String) COMMENT 'Batch类型',
    lot_size                Nullable(Float64) COMMENT '批次大小',
    sub_lot_size            Nullable(Float64) COMMENT '子批次大小',

    id_generator            Nullable(String) COMMENT '批号规则',

    is_time_sensitive       Nullable(String) COMMENT '是否时间敏感物料',

    shelf_warning           Nullable(Int64) COMMENT '保质警告期',
    shelf_life              Nullable(Int64) COMMENT '保质期',
    shelf_life_unit         Nullable(String) COMMENT '保质期单位',

    floor_life              Nullable(Int64) COMMENT '使用有效期',
    floor_life_unit         Nullable(String) COMMENT '使用有效期单位',
    floor_life_activator    Nullable(String) COMMENT '使用触发方式',

    limit_warning           Nullable(Int64) COMMENT '次数警告期',
    limit_life              Nullable(Int64) COMMENT '次数有效期',

    volume                  Nullable(Float64) COMMENT '体积',
    weight                  Nullable(Float64) COMMENT '重量',

    shelf_width             Nullable(Float64) COMMENT '宽度',
    shelf_height            Nullable(Float64) COMMENT '高度',
    shelf_depth             Nullable(Float64) COMMENT '深度',

    owner1                  Nullable(String) COMMENT '责任组1',
    owner2                  Nullable(String) COMMENT '责任组2',

    comments                Nullable(String) COMMENT '备注',

    reserved1               Nullable(String) COMMENT '预留栏位',
    reserved2               Nullable(String) COMMENT '预留栏位',
    reserved3               Nullable(String) COMMENT '预留栏位',
    reserved4               Nullable(String) COMMENT '预留栏位',
    reserved5               Nullable(String) COMMENT '预留栏位',
    reserved6               Nullable(String) COMMENT '预留栏位',
    reserved7               Nullable(String) COMMENT '预留栏位',
    reserved8               Nullable(String) COMMENT '预留栏位',

    warehouse_rrn           Nullable(Int64) COMMENT '仓库主键',

    main_mat_type           Nullable(String) COMMENT '主物料类型',
    sub_mat_type            Nullable(String) COMMENT '子物料类型',

    style                   Nullable(Float64) COMMENT 'STYLE',

    display_version         Nullable(String) COMMENT '显示版本',
    package_hierarchy_name  Nullable(String) COMMENT '包装层级',

    tenant_id               Nullable(String) COMMENT '租户ID',

    init_grade              Nullable(String) COMMENT '产品初始化等级',

    rework_limit_count      Nullable(Int64) COMMENT '可返工次数',
    limit_clean_count       Nullable(Int64) COMMENT '清洗限制次数',
    is_need_clean           Nullable(String) COMMENT '是否需要清洗',
    limit_use_count         Nullable(Int64) COMMENT '限制使用次数',
    floor_life_reset        Nullable(String) COMMENT '有效期是否重置',

    update_time             Nullable(DateTime) COMMENT '数据更新时间'
)
ENGINE = MergeTree
ORDER BY (object_rrn)
COMMENT '物料基础信息定义表';


CREATE TABLE IF NOT EXISTS rptdw.ods_mes_wf_process_flow_node
(
    object_rrn           Int64 COMMENT '对象序列号',
    org_rrn              Nullable(Int64) COMMENT '区域ID',
    is_active            Nullable(String) COMMENT '对象是否生效',
    created              Nullable(DateTime) COMMENT '创建时间',
    created_by           Nullable(String) COMMENT '创建人ID',
    updated              Nullable(DateTime) COMMENT '更新时间',
    updated_by           Nullable(String) COMMENT '更新人ID',
    lock_version         Nullable(Int64) COMMENT '锁定版本',

    process_rrn          Nullable(Int64) COMMENT '工艺主键',
    process_name         Nullable(String) COMMENT '工艺名称',
    process_version      Nullable(Int64) COMMENT '工艺版本',

    seq_no               Nullable(Int64) COMMENT '序号',
    step_rrn             Nullable(Int64) COMMENT '工站主键',
    step_name            Nullable(String) COMMENT '工站代码',
    step_version         Nullable(Int64) COMMENT '工站版本',

    previous_node_rrn    Nullable(Int64) COMMENT '前节点主键',
    next_node_rrn        Nullable(Int64) COMMENT '下一个节点主键',

    update_time          Nullable(DateTime) COMMENT '数据更新时间'
)
ENGINE = MergeTree
ORDER BY (object_rrn)
COMMENT '流程站点节点信息表';


CREATE TABLE IF NOT EXISTS rptdw.ods_mes_wf_step
(
    object_rrn Int64 COMMENT '对象序列号',
    org_rrn Int64 COMMENT '区域ID',
    is_active String COMMENT '对象是否生效',

    created DateTime COMMENT '创建时间',
    created_by String COMMENT '创建人ID',
    updated DateTime COMMENT '更新时间',
    updated_by String COMMENT '更新人ID',
    lock_version Int64 COMMENT '锁定版本',

    name String COMMENT '工艺代码',
    description String COMMENT '描述',
    version Int64 COMMENT '版本',
    status String COMMENT '状态',

    active_time DateTime COMMENT '激活时间',
    active_user String COMMENT '激活用户名',

    use_category String COMMENT '工站类型(Main/Sub)',
    stage_id String COMMENT '生产阶段',
    capability Int64 COMMENT '设备能力主键',
    comments String COMMENT '备注',

    reserved1 String COMMENT '预留栏位',
    reserved2 String COMMENT '预留栏位',
    reserved3 String COMMENT '预留栏位',
    reserved4 String COMMENT '预留栏位',
    reserved5 String COMMENT '预留栏位',
    reserved6 String COMMENT '预留栏位',
    reserved7 String COMMENT '预留栏位',
    reserved8 String COMMENT '预留栏位',
    reserved9 String COMMENT '预留栏位',
    reserved10 String COMMENT '预留栏位',

    step_type String COMMENT '工步使用类型',
    update_time DateTime COMMENT '数据同步时间'
)
ENGINE = MergeTree
ORDER BY (object_rrn)
COMMENT '工站基础信息定义表';

CREATE TABLE IF NOT EXISTS rptdw.ods_mes_ct_incoming_check
(
    object_rrn Int64 COMMENT '对象序列号',
    org_rrn Int64 COMMENT '区域号',
    is_active String COMMENT '是否有效',
    created DateTime COMMENT '创建时间',
    created_by String COMMENT '创建者',
    updated DateTime COMMENT '更新时间',
    updated_by String COMMENT '更新者',
    lock_version Int64 COMMENT '锁定版本',

    equipment_id String COMMENT '设备ID',
    panel_id String COMMENT '屏体ID',
    judge String COMMENT '检查结果(OK，NG)',

    reserved1 String COMMENT '预留字段1',
    reserved2 String COMMENT '预留字段2',
    reserved3 String COMMENT '预留字段3',
    reserved4 String COMMENT '预留字段4',
    reserved5 String COMMENT '预留字段5',
    reserved6 String COMMENT '预留字段6',
    reserved7 String COMMENT '预留字段7',
    reserved8 String COMMENT '预留字段8',

    update_time DateTime COMMENT '数据更新时间'
)
ENGINE = MergeTree
ORDER BY object_rrn
COMMENT '通道等级表';

CREATE TABLE IF NOT EXISTS rptdw.ods_mes_wip_future_action
(
    object_rrn Int64 COMMENT '对象序列号',
    org_rrn Int64 COMMENT '区域ID',
    is_active String COMMENT '对象是否生效',
    created DateTime COMMENT '创建时间',
    created_by String COMMENT '创建人ID',
    updated DateTime COMMENT '更新时间',
    updated_by String COMMENT '更新人ID',
    lock_version Int64 COMMENT '锁定版本',

    `action` String COMMENT '未来动作类型',
    name String COMMENT '名称',
    description String COMMENT '描述',
    timer_type String COMMENT '定时器类型',
    timer_duration Int64 COMMENT '时间间隔',
    timer_action String COMMENT '定时器动作',
    early_period Int64 COMMENT '提前期',
    `condition` String COMMENT '条件',
    seq_no Int64 COMMENT '序号',

    parent_lot_rrn Int64 COMMENT '母批主键',
    parent_lot_id String COMMENT '母批ID',
    lot_rrn Int64 COMMENT '批次主键',
    lot_id String COMMENT '批次ID',

    part_name String COMMENT '产品编码',
    part_version Int64 COMMENT '产品版本',
    path String COMMENT '路径',

    process_name String COMMENT '工艺名称',
    process_version Int64 COMMENT '工艺版本',

    procedure_name String COMMENT '流程名称',
    procedure_version Int64 COMMENT '流程版本',

    step_state_name String COMMENT '工步状态名',
    step_name String COMMENT '工站代码',
    step_version Int64 COMMENT '工站版本',
    step_placement String COMMENT '触发位置',

    end_path String COMMENT '结束路径',
    end_procedure_name String COMMENT '结束流程名称',
    end_procedure_version Int64 COMMENT '结束流程版本',
    end_step_state_name String COMMENT '结束工步状态',
    end_step_name String COMMENT '结束工步名称',

    rework_code String COMMENT '返工码',
    rework_procedure String COMMENT '返工流程',
    rework_procedure_version String COMMENT '返工流程版本',

    owner String COMMENT '责任组',
    user_name String COMMENT '用户名',

    hold_code String COMMENT 'Hold代码',
    hold_reason String COMMENT 'Hold原因',
    hold_pwd String COMMENT 'Hold密码',
    hold_level String COMMENT 'Hold级别(预留)',
    hold_owner String COMMENT 'Hold责任组',

    note String COMMENT '笔记',
    sampling_plan_name String COMMENT 'Lot抽样计划名称',
    subgroup_plan_name String COMMENT 'Component抽样计划名称',
    is_component_level String COMMENT 'Component是否分级',

    new_part_version String COMMENT '新产品版本',
    new_part_name String COMMENT '新产品名称',
    is_repeat String COMMENT '是否允许重复(默认N)',

    rework_start_step_state_name String COMMENT '返工流程开始节点',
    rework_start_step_name String COMMENT '返工流程开始工步',
    rework_end_step_state_name String COMMENT '新增流程结束节点',
    rework_end_step_name String COMMENT '新增流程结束工步',

    end_step_placement String COMMENT '结束工步定位',
    parent_rrn Int64 COMMENT '父Rrn,当parentRrn与objectRrn一致时为主数据',

    run_card_id String COMMENT 'RunCard编号',
    equipment_id String COMMENT '设备ID',

    is_start_pilot_use_currentstep String COMMENT '是否当前工步作为开始工步',
    is_hold_process_eqp String COMMENT '是否暂停加工设备',
    is_same_pilot_eqp String COMMENT '是否相同有Pilot设备作业',

    action_path String COMMENT '站点在流程中的路径',
    action_step_name String COMMENT '工站代码',
    action_step_state_name String COMMENT '工步状态名',
    action_step_placement String COMMENT '动作触发位置',

    priority Int64 COMMENT '优先级',
    hold_comment String COMMENT 'Hold备注',
    is_force String COMMENT '是否强制',

    update_time DateTime COMMENT '数据修改时间'
)
ENGINE = MergeTree
ORDER BY object_rrn
COMMENT '未来动作定义表';

CREATE TABLE IF NOT EXISTS rptdw.ods_mes_wip_lot_hld
(
    object_rrn      Int64 NOT NULL COMMENT '对象序列号',
    org_rrn         Nullable(Int64) COMMENT '区域ID',
    is_active       Nullable(String) COMMENT '对象是否生效',
    created         Nullable(DateTime) COMMENT '创建时间',
    created_by      Nullable(String) COMMENT '创建人ID',
    updated         Nullable(DateTime) COMMENT '更新时间',
    updated_by      Nullable(String) COMMENT '更新人ID',
    lock_version    Nullable(Int64) COMMENT '锁定版本',

    lot_rrn         Nullable(Int64) COMMENT '批次主键',
    seq_no          Nullable(Int64) COMMENT '序号',
    hold_user_rrn   Nullable(Int64) COMMENT '预留',
    hold_user_name  Nullable(String) COMMENT 'Hold用户名',
    hold_code       Nullable(String) COMMENT 'Hold代码',
    hold_reason     Nullable(String) COMMENT 'Hold原因',
    hold_pwd        Nullable(String) COMMENT 'Hold密码',
    hold_ocap_id    Nullable(String) COMMENT '预留',
    hold_comment    Nullable(String) COMMENT 'Hold备注',
    hold_level      Nullable(String) COMMENT 'Hold级别(预留)',
    hold_owner      Nullable(String) COMMENT 'Hold责任组',
    hold_time       Nullable(DateTime) COMMENT 'Hold时间',

    pre_com_class   Nullable(String) COMMENT '前状态大类',
    pre_state       Nullable(String) COMMENT '前状态',
    pre_sub_state   Nullable(String) COMMENT '前子状态',

    component_rrn   Nullable(Int64) COMMENT 'WIP_COMPONENTUNIT主键',
    rpt_time        Nullable(DateTime) COMMENT '报表时间'
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(created)
ORDER BY (lot_rrn, hold_time, object_rrn)
COMMENT 'WIP批次Hold历史表';


CREATE TABLE IF NOT EXISTS rptdw.dwd_panel_inout_his
(
    date_key Nullable(String) COMMENT '日期维度',
    shift_id Nullable(String) COMMENT '班次ID',
    hour_key Nullable(String) COMMENT '小时KEY',
    product_key Nullable(Int64) COMMENT '产品KEY',
    line_id Nullable(String) COMMENT '线别ID',
    stage_id Nullable(String) COMMENT '阶段ID',
    step_key Nullable(Int64) COMMENT '工步KEY',
    wo_id Nullable(String) COMMENT '工单ID',
    eqp_id Nullable(String) COMMENT '设备ID',
    panel_key Nullable(Int64) COMMENT '面板KEY',
    panel_id Nullable(String) COMMENT '面板ID',
    glass_id Nullable(String) COMMENT '玻璃ID',
    panel_type Nullable(String) COMMENT '面板类型',
    trans_type Nullable(String) COMMENT '流转类型',
    trans_time Nullable(DateTime) COMMENT '流转时间',
    updated_user Nullable(String) COMMENT '更新人',
    operator_id Nullable(String) COMMENT '操作员ID',
    history_seq Nullable(String) COMMENT '历史序列',
    panel_grade Nullable(String) COMMENT '面板等级',
    panel_judge Nullable(String) COMMENT '判定结果',
    main_qty Nullable(Int64) COMMENT '主数量',
    track_in_main_qty Nullable(Int64) COMMENT '进站主数量',
    track_in_time Nullable(DateTime) COMMENT '进站时间',
    track_out_main_qty Nullable(Int64) COMMENT '出站主数量',
    track_out_time Nullable(DateTime) COMMENT '出站时间',
    root_lot_key Nullable(Int64) COMMENT '根批次KEY',
    parent_lot_key Nullable(Int64) COMMENT '父批次KEY',
    panel_state Nullable(String) COMMENT '面板状态',
    box_id Nullable(String) COMMENT '箱号',
    process_key Nullable(Int64) COMMENT '工艺KEY',
    procedure_key Nullable(Int64) COMMENT '流程KEY',
    recipe_id Nullable(String) COMMENT '配方ID',
    fab_box_id Nullable(String) COMMENT '工厂箱ID',
    fab_pallet_id Nullable(String) COMMENT '托盘ID',
    oqc_grade Nullable(String) COMMENT 'OQC等级',
    oqc_state Nullable(String) COMMENT 'OQC状态',
    product_sn Nullable(String) COMMENT '产品SN',
    operator_position Nullable(String) COMMENT '操作位置',
    pre_track_out_time Nullable(DateTime) COMMENT '前出站时间',
    next_track_in_time Nullable(DateTime) COMMENT '下一进站时间',
    eqp_tt Nullable(Float64) COMMENT '设备TT',
    ct Nullable(Float64) COMMENT 'CT时间',
    last_judge_step_name Nullable(String) COMMENT '最后判定站点',
    last_judge_eqp Nullable(String) COMMENT '最后判定设备',
    last_defect_event_time Nullable(String) COMMENT '最后不良时间',
    last_defect_code Nullable(String) COMMENT '最后不良代码',
    last_flag Nullable(String) COMMENT '最后标识',
    rpt_time Nullable(DateTime) COMMENT '报表时间',
    wo_type Nullable(String) COMMENT '工单类型',
    wo_type_desc Nullable(String) COMMENT '工单类型描述',
    eqp_next_pnl_outtime Nullable(DateTime) COMMENT '设备下一出站时间',
    op_next_pnl_outtime Nullable(DateTime) COMMENT '操作下一出站时间',
    op_tt Nullable(Float64) COMMENT '操作TT',
    last_step_name Nullable(String) COMMENT '最后工步',
    step_name Nullable(String) COMMENT '工步名称',
    trackin_pnl_grade Nullable(String) COMMENT '进站等级',
    out_main_step_name Nullable(String) COMMENT '出站主工步',
    eqp_flag Nullable(String) COMMENT '设备标识',
    main_step_name Nullable(String) COMMENT '主工步',
    re_grade Nullable(String) COMMENT '返工等级',
    re_judge Nullable(String) COMMENT '返工判定',
    re_flage Nullable(String) COMMENT '返工标识',
    re_step_name Nullable(String) COMMENT '返工工步',
    hold_state Nullable(String) COMMENT 'Hold状态',
    product_id Nullable(String) COMMENT '产品ID',
    recovery_cnt Nullable(Int64) COMMENT '恢复次数',
    sampling_flag Nullable(String) COMMENT '抽检标识',
    re_defect_code Nullable(String) COMMENT '返工不良代码',
    re_user Nullable(String) COMMENT '返工人员',
    rework_count Nullable(Int64) COMMENT '返工次数',
    batch_id Nullable(String) COMMENT '批次ID',
    action_comment Nullable(String) COMMENT '动作备注',
    up_hourkey Nullable(String) COMMENT '上级小时KEY',
    up_flag_time Nullable(DateTime) COMMENT '上级标记时间',
    yld_grade Nullable(String) COMMENT '良率等级'
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(trans_time)
ORDER BY (trans_time, panel_id, trans_type, last_flag, product_id, step_name)
COMMENT 'DWD 面板进出站历史表';


CREATE TABLE IF NOT EXISTS rptdw.ods_mes_prd_part_defect_code
(
    `object_rrn` Int64 COMMENT '主键',

    `org_rrn` Nullable(Int64) COMMENT '区域ID',
    `is_active` Nullable(String) COMMENT '对象是否可用',

    `created` Nullable(DateTime) COMMENT '创建时间',
    `created_by` Nullable(String) COMMENT '创建者',

    `updated` Nullable(DateTime) COMMENT '修改时间',
    `updated_by` Nullable(String) COMMENT '更新者ID',

    `lock_version` Nullable(Int64) COMMENT '锁定版本',

    `part_name` Nullable(String) COMMENT '产品名称',
    `step_name` Nullable(String) COMMENT '站点名称',

    `defect_code` Nullable(String) COMMENT '不良Code',
    `defect_category` Nullable(String) COMMENT '不良类型',
    `defect_desc` Nullable(String) COMMENT '不良描述',

    `grade` Nullable(String) COMMENT '等级',
    `grade_desc` Nullable(String) COMMENT '等级描述',

    `responsibility_group` Nullable(String) COMMENT '责任组',

    `update_time` Nullable(DateTime) COMMENT '数据更新时间'
)
ENGINE = ReplacingMergeTree(update_time)
PRIMARY KEY object_rrn
ORDER BY (object_rrn, part_name, step_name)
SETTINGS index_granularity = 8192;

CREATE TABLE IF NOT EXISTS rptdw.ods_mes_ad_user
(
    `object_rrn` Int64 COMMENT '对象序列号',

    `org_rrn` Nullable(Int64) COMMENT '区域ID',
    `is_active` Nullable(String) COMMENT '对象是否生效',

    `created` Nullable(DateTime) COMMENT '创建时间',
    `created_by` Nullable(String) COMMENT '创建人ID',
    `updated` Nullable(DateTime) COMMENT '更新时间',
    `updated_by` Nullable(String) COMMENT '更新人ID',
    `lock_version` Nullable(Int64) COMMENT '锁定版本',

    `user_name` String COMMENT '用户名',
    `description` Nullable(String) COMMENT '描述',
    `password` Nullable(String) COMMENT '密码',

    `is_invalid` Nullable(String) COMMENT '密码是否失效',

    `email` Nullable(String) COMMENT '邮箱',
    `phone` Nullable(String) COMMENT '电话',
    `phone2` Nullable(String) COMMENT '电话2',

    `department` Nullable(String) COMMENT '部门',

    `birth_day` Nullable(DateTime) COMMENT '生日',
    `sex` Nullable(String) COMMENT '性别',
    `join_time` Nullable(DateTime) COMMENT '入职时间',

    `default_language` Nullable(String) COMMENT '默认语言',
    `comments` Nullable(String) COMMENT '备注',

    `pwd_changed` Nullable(DateTime) COMMENT '修改密码时间',
    `pwd_life` Nullable(Int64) COMMENT '密码有效天数',
    `pwd_expiry` Nullable(DateTime) COMMENT '密码失效时间',
    `last_logon` Nullable(DateTime) COMMENT '最后登录时间',

    `menu_start` Nullable(String) COMMENT '菜单入口',

    `default_org_rrn` Nullable(Int64) COMMENT '默认工作区域',

    `is_show_launcher` Nullable(String) COMMENT '是否显示启动页',
    `default_view` Nullable(String) COMMENT '默认视图',

    `process_flag` Nullable(String) COMMENT '流程标识',
    `jobs` Nullable(String) COMMENT '职位',

    `pwd_wrong_count` Nullable(Int64) COMMENT '密码错误次数',

    `default_location` Nullable(String) COMMENT '默认区域',

    `update_time` Nullable(DateTime) COMMENT '数据更新时间'
)
ENGINE = ReplacingMergeTree(update_time)
PRIMARY KEY object_rrn
ORDER BY (object_rrn, user_name)
SETTINGS index_granularity = 8192;

CREATE TABLE IF NOT EXISTS rptdw.ods_mes_wip_lot
(
    `object_rrn` Int64 COMMENT '对象序列号',
    `org_rrn` Nullable(Int64) COMMENT '区域ID',
    `is_active` Nullable(String) COMMENT '对象是否生效',
    `created` Nullable(DateTime) COMMENT '创建时间',
    `created_by` Nullable(String) COMMENT '创建人ID',
    `updated` Nullable(DateTime) COMMENT '更新时间',
    `updated_by` Nullable(String) COMMENT '更新人ID',
    `lock_version` Nullable(Int64) COMMENT '锁定版本',

    `lot_id` String COMMENT '批次ID',
    `lot_type` Nullable(String) COMMENT '批次类型',
    `lot_alias` Nullable(String) COMMENT '批次别名',
    `wo_id` Nullable(String) COMMENT '工单ID',

    `substrate_id1` Nullable(String) COMMENT '基板编号1',
    `substrate_id2` Nullable(String) COMMENT '基板编号2',

    `part_rrn` Nullable(Int64) COMMENT '产品主键',
    `part_name` Nullable(String) COMMENT '产品编码',
    `part_version` Nullable(Int64) COMMENT '产品版本',
    `part_desc` Nullable(String) COMMENT '产品描述',
    `part_type` Nullable(String) COMMENT '产品类型',
    `last_part_name` Nullable(String) COMMENT '上一个产品',

    `main_mat_type` Nullable(String) COMMENT '投入产品形态',
    `sub_mat_type` Nullable(String) COMMENT '产出产品形态',

    `customer_code` Nullable(String) COMMENT '客户代码',
    `customer_order` Nullable(String) COMMENT '客户工单',
    `customer_part_id` Nullable(String) COMMENT '客户产品',
    `customer_lot_id` Nullable(String) COMMENT '客户批次',

    `priority` Nullable(Int64) COMMENT '优先级',

    `plan_start_date` Nullable(DateTime) COMMENT '计划开始时间',
    `plan_end_date` Nullable(DateTime) COMMENT '计划结束时间',
    `require_date` Nullable(DateTime) COMMENT '产品交期',

    `grade1` Nullable(String) COMMENT '等级1',
    `grade2` Nullable(String) COMMENT '等级2',
    `judge1` Nullable(String) COMMENT '判定结果1',
    `judge2` Nullable(String) COMMENT '判定结果2',

    `rework_code` Nullable(String) COMMENT '返工码',

    `warehouse_id` Nullable(String) COMMENT '仓库ID',
    `locator_id` Nullable(String) COMMENT '仓库位置ID',
    `location` Nullable(String) COMMENT '生产区域',
    `line_id` Nullable(String) COMMENT '线别',
    `stage_id` Nullable(String) COMMENT '工步阶段',

    `durable` Nullable(String) COMMENT '载具ID',
    `position` Nullable(String) COMMENT '位置',
    `owner` Nullable(String) COMMENT '责任组',

    `lot_comment` Nullable(String) COMMENT '批次备注',

    `schedule_time` Nullable(DateTime) COMMENT '计划时间',

    `start_main_qty` Nullable(Decimal(38, 10)) COMMENT '开始主数量',
    `start_sub_qty` Nullable(Decimal(38, 10)) COMMENT '开始子数量',
    `start_time` Nullable(DateTime) COMMENT '开始时间',

    `end_main_qty` Nullable(Decimal(38, 10)) COMMENT '结束主数量',
    `end_sub_qty` Nullable(Decimal(38, 10)) COMMENT '结束子数量',
    `end_time` Nullable(DateTime) COMMENT '结束时间',

    `main_qty` Nullable(Decimal(38, 10)) COMMENT '主数量',
    `sub_qty` Nullable(Decimal(38, 10)) COMMENT '子数量',

    `equipment_id` Nullable(String) COMMENT '设备ID',
    `last_equipment_id` Nullable(String) COMMENT '上一个设备ID',

    `operator1` Nullable(String) COMMENT '操作人1',
    `operator2` Nullable(String) COMMENT '操作人2',

    `queue_time` Nullable(DateTime) COMMENT '排队时间',

    `track_in_main_qty` Nullable(Decimal(38, 10)) COMMENT '进站主数量',
    `track_in_sub_qty` Nullable(Decimal(38, 10)) COMMENT '进站子数量',
    `track_in_time` Nullable(DateTime) COMMENT '进站时间',

    `track_out_main_qty` Nullable(Decimal(38, 10)) COMMENT '出站主数量',
    `track_out_sub_qty` Nullable(Decimal(38, 10)) COMMENT '出站子数量',
    `track_out_time` Nullable(DateTime) COMMENT '出站时间',

    `root_lot_rrn` Nullable(Int64) COMMENT 'Root批次主键',
    `parent_lot_rrn` Nullable(Int64) COMMENT '父批次主键',
    `parent_unit_rrn` Nullable(Int64) COMMENT '父Unit主键',

    `sub_unit_type` Nullable(String) COMMENT 'SUB UNIT类型',
    `is_sub_lot` Nullable(String) COMMENT '是否子批',

    `com_class` Nullable(String) COMMENT '状态大类',
    `state` Nullable(String) COMMENT '状态',
    `sub_state` Nullable(String) COMMENT '子状态',
    `hold_state` Nullable(String) COMMENT 'Hold状态',
    `transfer_state` Nullable(String) COMMENT '搬运状态',

    `state_entry_time` Nullable(DateTime) COMMENT '进入状态时间',

    `pre_trans_type` Nullable(String) COMMENT '前事务类型',
    `pre_com_class` Nullable(String) COMMENT '前状态大类',
    `pre_state` Nullable(String) COMMENT '前状态',
    `pre_sub_state` Nullable(String) COMMENT '前子状态',

    `current_seq` Nullable(String) COMMENT '事务序号',

    `process_instance_rrn` Nullable(Int64) COMMENT '工艺实例主键',
    `process_rrn` Nullable(Int64) COMMENT '工艺主键',
    `process_name` Nullable(String) COMMENT '工艺名称',
    `process_version` Nullable(Int32) COMMENT '工艺版本',

    `procedure_rrn` Nullable(Int64) COMMENT '流程主键',
    `procedure_name` Nullable(String) COMMENT '流程名称',
    `procedure_version` Nullable(Int32) COMMENT '流程版本',

    `step_rrn` Nullable(Int64) COMMENT '工站主键',
    `step_name` Nullable(String) COMMENT '工站代码',
    `step_version` Nullable(Int32) COMMENT '工站版本',
    `step_desc` Nullable(String) COMMENT '工站描述',
    `step_stack` Nullable(String) COMMENT '工步路径',

    `last_step_name` Nullable(String) COMMENT '上一步工站',

    `batch_id` Nullable(String) COMMENT 'OQC BatchID',

    `rework_stack_count` Nullable(Int16) COMMENT '返工堆叠次数',
    `rework_count` Nullable(Int16) COMMENT '返工次数',

    `recipe_name` Nullable(String) COMMENT 'Recipe名称',
    `recipe_version` Nullable(Int32) COMMENT 'Recipe版本',

    `mask` Nullable(String) COMMENT '加工Mask',
    `is_pilot` Nullable(String) COMMENT '是否试产',

    `use_count` Nullable(Int16) COMMENT '使用次数',

    `expire_time` Nullable(DateTime) COMMENT '过期时间',
    `minimal_expire_time` Nullable(DateTime) COMMENT '最小过期时间',

    `tenant_id` Nullable(String) COMMENT '租户ID',

    `ocap_id` Nullable(String) COMMENT 'OCAP ID',
    `contamination_level` Nullable(String) COMMENT '污染等级',
    `control_id` Nullable(String) COMMENT '控制ID',

    `recycle_count` Nullable(Int64) COMMENT '回收次数',

    `sub_location` Nullable(String) COMMENT '子区域',

    `equipment_mask` Nullable(String) COMMENT '设备Mask',
    `equipment_recipe` Nullable(String) COMMENT '设备Recipe',

    `fab_box_id` Nullable(String) COMMENT 'Fab Box ID',
    `fab_pallet_id` Nullable(String) COMMENT 'Fab Pallet ID',

    `lot_pack_type` Nullable(String) COMMENT '包装类型',
    `sampling_flag` Nullable(String) COMMENT '抽检标志',

    `oqc_grade` Nullable(String) COMMENT 'OQC等级',
    `oqc_state` Nullable(String) COMMENT 'OQC状态',
    `oqc_count` Nullable(Int64) COMMENT 'OQC次数',

    `forbid_pack` Nullable(String) COMMENT '禁止包装',

    `node_rrn` Nullable(Int64) COMMENT '节点主键',
    `sub_process_token_rrn` Nullable(Int64) COMMENT '返工单据主键',

    `inner_box_weight` Nullable(Decimal(19,2)) COMMENT '内箱重量',
    `outer_box_weight` Nullable(Decimal(19,2)) COMMENT '外箱重量',

    `is_need_reprint` Nullable(String) COMMENT '是否需要重打',

    `light_time` Nullable(DateTime) COMMENT '点亮时间',
    `in_stock_time` Nullable(DateTime) COMMENT '入库时间',

    `risk_hold_flag` Nullable(String) COMMENT '风险Hold标识',

    `last_judge_step_name` Nullable(String) COMMENT '上次判定站点',
    `last_judge_eqp` Nullable(String) COMMENT '上次判定设备',

    `last_defect_event_time` Nullable(DateTime) COMMENT '缺陷时间',
    `last_defect_code` Nullable(String) COMMENT '缺陷代码',

    `forbid_ship` Nullable(String) COMMENT '禁止出货',
    `is_abnormal` Nullable(String) COMMENT '异常标识',
    `is_line_out` Nullable(String) COMMENT '是否出线',

    `recovery_state` Nullable(String) COMMENT '恢复状态',
    `is_start` Nullable(String) COMMENT '是否开始',

    `last_main_step_grade` Nullable(String) COMMENT '主工序等级',

    `recover_wo` Nullable(String) COMMENT '返工工单',
    `recover_time` Nullable(DateTime) COMMENT '返工时间',

    `date_code` Nullable(String) COMMENT 'DC周期',
    `tray_id` Nullable(String) COMMENT 'Tray ID',

    `current_pack_level` Nullable(String) COMMENT '当前包装层级',

    `last_judge_event_time` Nullable(DateTime) COMMENT '上次判定时间',

    `recover_plan_wo` Nullable(String) COMMENT '返工计划工单',

    `sfg_material_name` Nullable(String) COMMENT '半成品料号',

    `action_name` Nullable(String) COMMENT '操作动作',
    `first_pack_time` Nullable(DateTime) COMMENT '首次包装时间',

    `lot_form` Nullable(String) COMMENT '产品形态',

    `oba_result` Nullable(String) COMMENT 'OBA结果',

    `out_main_process_name` Nullable(String) COMMENT '返回主流程',
    `out_main_step_name` Nullable(String) COMMENT '返回主站点',

    `debug_eqp_flag` Nullable(String) COMMENT '调机片标识',

    `recover_batch_id` Nullable(String) COMMENT '返工批次',

    `last_main_node_step` Nullable(String) COMMENT '主节点站点',

    `action_group` Nullable(String) COMMENT '操作组',

    `oba_grade` Nullable(String) COMMENT 'OBA等级',
    `oba_state` Nullable(String) COMMENT 'OBA状态',

    `tobejudge_warehouse` Nullable(String) COMMENT '待检仓位',

    `burn_count` Nullable(Int64) COMMENT '烧录次数',

    `oqc_check_operator` Nullable(String) COMMENT 'OQC抽检人',

    `check_csn` Nullable(String) COMMENT 'CSN回读标识',
    `csn_approval` Nullable(String) COMMENT 'CSN审批',

    `oqc_info_mark` Nullable(String) COMMENT 'OQC标记',

    `rma_flag` Nullable(String) COMMENT '客诉标识',

    `pallet_no` Nullable(String) COMMENT '栈板批次',

    `array_grade` Nullable(String) COMMENT 'Array等级',
    `oled_grade` Nullable(String) COMMENT 'OLED等级',

    `lot_no` Nullable(String) COMMENT '批次号',
    `scrap_num` Nullable(String) COMMENT '报废单号',

    `hold_type` Nullable(String) COMMENT 'Hold类型'
)
ENGINE = ReplacingMergeTree(updated)
PRIMARY KEY object_rrn
ORDER BY (object_rrn, lot_id, org_rrn)
COMMENT '在制品批次信息表';


CREATE TABLE IF NOT EXISTS rptdw.dim_calendar
(
    `factory`               Nullable(String) COMMENT '厂别',
    `time_type`             Nullable(String) COMMENT '时间类型',
    `time_key`              String COMMENT '时间Key',
    `shift_start_timekey`   Nullable(String) COMMENT '班次开始时间Key',
    `shift_end_timekey`     Nullable(String) COMMENT '班次结束时间Key',
    `date_start_timekey`    Nullable(String) COMMENT '日期开始时间Key',
    `date_end_timekey`      Nullable(String) COMMENT '日期结束时间Key',
    `shift_timekey`         Nullable(String) COMMENT '班别时间：0160806 073000',
    `shift_name`            Nullable(String) COMMENT '班别名称',
    `date_timekey`          Nullable(String) COMMENT '日期',
    `week_timekey`          Nullable(String) COMMENT '周',
    `month_timekey`         Nullable(String) COMMENT '月',
    `quarter_timekey`       Nullable(String) COMMENT '季度',
    `year_timekey`          Nullable(String) COMMENT '年份',
    `interface_time`        Nullable(DateTime64(6)) COMMENT '接口时间'
)
ENGINE = MergeTree
ORDER BY (time_key, time_type)
SETTINGS index_granularity = 8192;

CREATE TABLE IF NOT EXISTS rptdw.dwd_panel_scrap_his
(
    `date_key`                 String COMMENT '日期Key',
    `shift_id`                 Nullable(String) COMMENT '班次',
    `hour_key`                 Nullable(String) COMMENT '小时Key',
    `product_key`              Nullable(Int64) COMMENT '产品Key',
    `line_id`                  Nullable(String) COMMENT '线别',
    `stage_id`                 Nullable(String) COMMENT 'Stage',
    `step_key`                 Nullable(Int64) COMMENT '工序Key',
    `wo_id`                    Nullable(String) COMMENT '工单号',
    `wo_type`                  Nullable(String) COMMENT '工单类型',
    `wo_type_desc`             Nullable(String) COMMENT '工单类型描述',
    `eqp_id`                   Nullable(String) COMMENT '设备号',
    `panel_key`                Nullable(Int64) COMMENT 'Panel Key',
    `panel_id`                 String COMMENT 'Panel ID',
    `glass_id`                 Nullable(String) COMMENT 'Glass ID',
    `panel_type`               Nullable(String) COMMENT 'Panel类型',
    `trans_type`               Nullable(String) COMMENT '交易类型',
    `trans_time`               Nullable(DateTime) COMMENT '过站时间',
    `updated_user`             Nullable(String) COMMENT '更新人',
    `operator_id`              Nullable(String) COMMENT '操作员',
    `panel_grade`              Nullable(String) COMMENT 'Panel等级',
    `panel_judge`              Nullable(String) COMMENT 'Panel判定',
    `main_qty`                 Nullable(Int64) COMMENT '数量',
    `root_lot_key`             Nullable(Int64) COMMENT 'Root Lot Key',
    `parent_lot_key`           Nullable(Int64) COMMENT 'Parent Lot Key',
    `panel_state`              Nullable(String) COMMENT 'Panel状态',
    `box_id`                   Nullable(String) COMMENT 'Box ID',
    `recipe_id`                Nullable(String) COMMENT 'Recipe ID',
    `fab_box_id`               Nullable(String) COMMENT 'FAB Box ID',
    `fab_pallet_id`            Nullable(String) COMMENT 'FAB Pallet ID',
    `oqc_grade`                Nullable(String) COMMENT 'OQC等级',
    `oqc_state`                Nullable(String) COMMENT 'OQC状态',
    `product_sn`               Nullable(String) COMMENT '产品序列号',
    `last_judge_step_name`     Nullable(String) COMMENT '最后判定工序',
    `last_judge_eqp`           Nullable(String) COMMENT '最后判定设备',
    `last_defect_event_time`   Nullable(String) COMMENT '最后缺陷时间',
    `last_defect_code`         Nullable(String) COMMENT '最后缺陷代码',
    `rpt_time`                 Nullable(DateTime) COMMENT '报表时间',
    `history_seq`              Nullable(String) COMMENT '历史序列',
    `rework_count`             Nullable(Int64) COMMENT '返工次数',
    `step_name`                Nullable(String) COMMENT '当前工序',
    `last_step_name`           Nullable(String) COMMENT '上一工序',
    `action_code`              Nullable(String) COMMENT '动作代码',
    `action_reason`            Nullable(String) COMMENT '动作原因',
    `action_comment`           Nullable(String) COMMENT '动作备注',
    `action_group`             Nullable(String) COMMENT '动作组',
    `action_name`              Nullable(String) COMMENT '动作名称',
    `last_main_step_grade`     Nullable(String) COMMENT '上一主工序等级',
    `last_flag`                Nullable(String) COMMENT '最后标识',
    `up_hourkey`               Nullable(String) COMMENT '更新时间小时',
    `up_flag_time`             Nullable(DateTime) COMMENT '更新时间'
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(trans_time)
ORDER BY (date_key, hour_key, panel_id)
SETTINGS index_granularity = 8192;

CREATE TABLE IF NOT EXISTS rptdw.ods_mes_wip_wo
(
    `object_rrn`                Int64 COMMENT '对象序列号',
    `org_rrn`                   Nullable(Int64) COMMENT '区域ID',
    `is_active`                 Nullable(String) COMMENT '对象是否生效',
    `created`                   Nullable(DateTime) COMMENT '创建时间',
    `created_by`                Nullable(String) COMMENT '创建人ID',
    `updated`                   Nullable(DateTime) COMMENT '更新时间',
    `updated_by`                Nullable(String) COMMENT '更新人ID',
    `lock_version`              Nullable(Int64) COMMENT '锁定版本',
    `doc_id`                    Nullable(String) COMMENT '工单ID',
    `doc_type`                  Nullable(String) COMMENT '类型',
    `doc_status`                Nullable(String) COMMENT '工单状态',
    `created_user`              Nullable(String) COMMENT '创建人',
    `created_date`              Nullable(DateTime) COMMENT '创建时间',
    `approved_user`             Nullable(String) COMMENT '审核人',
    `approved_date`             Nullable(DateTime) COMMENT '审核时间',
    `owner`                     Nullable(String) COMMENT '责任组',
    `parent_id`                 Nullable(String) COMMENT '父工单ID',
    `part_name`                 Nullable(String) COMMENT '产品编码',
    `part_version`              Nullable(Int64) COMMENT '产品版本',
    `customer_code`             Nullable(String) COMMENT '客户代码',
    `customer_order`            Nullable(String) COMMENT '客户订单',
    `customer_part_id`          Nullable(String) COMMENT '客户产品ID',
    `main_qty`                  Nullable(Int64) COMMENT '主数量',
    `sub_qty`                   Nullable(Int64) COMMENT '子数量',
    `schedule_main_qty`         Nullable(Int64) COMMENT '计划主数量',
    `schedule_sub_qty`          Nullable(Int64) COMMENT '计划子数量',
    `started_main_qty`          Nullable(Int64) COMMENT '开始主数量',
    `started_sub_qty`           Nullable(Int64) COMMENT '开始子数量',
    `complete_main_qty`         Nullable(Int64) COMMENT '完成主数量',
    `complete_sub_qty`          Nullable(Int64) COMMENT '完成子数量',
    `lot_type`                  Nullable(String) COMMENT '批次类型',
    `grade1`                    Nullable(String) COMMENT '等级1',
    `grade2`                    Nullable(String) COMMENT '等级2',
    `line_id`                   Nullable(String) COMMENT '线别',
    `equipment_id`              Nullable(String) COMMENT '设备ID',
    `priority`                  Nullable(Int64) COMMENT '优先级',
    `rework_process_name`       Nullable(String) COMMENT '返工工艺代码',
    `rework_process_version`    Nullable(Int64) COMMENT '返工流程版本',
    `rework_start_step_name`    Nullable(String) COMMENT '返工开始工步名',
    `rework_end_step_name`      Nullable(String) COMMENT '返工结束工步名',
    `plan_start_date`           Nullable(DateTime) COMMENT '计划开始时间',
    `plan_end_date`             Nullable(DateTime) COMMENT '计划结束时间',
    `require_date`              Nullable(DateTime) COMMENT '产品交期',
    `schedule_date`             Nullable(DateTime) COMMENT '计划日期',
    `comments`                  Nullable(String) COMMENT '备注',
    `hold_state`                Nullable(String) COMMENT 'Hold状态(On/Off)',
    `floor`                     Nullable(String) COMMENT '楼层',
    `shift`                     Nullable(String) COMMENT '班别',
    `reserved1`                 Nullable(String) COMMENT '预留栏位',
    `reserved2`                 Nullable(String) COMMENT '预留栏位',
    `reserved3`                 Nullable(String) COMMENT '预留栏位',
    `reserved4`                 Nullable(String) COMMENT '预留栏位',
    `reserved5`                 Nullable(String) COMMENT '预留栏位',
    `reserved6`                 Nullable(String) COMMENT '预留栏位',
    `reserved7`                 Nullable(String) COMMENT '预留栏位',
    `reserved8`                 Nullable(String) COMMENT '预留栏位',
    `workorder_type`            Nullable(String) COMMENT '工单类型',
    `scrap_main_qty`            Nullable(Int64) COMMENT '报废数量',
    `receive_main_qty`          Nullable(Int64) COMMENT '转入数量',
    `split_main_qty`            Nullable(Int64) COMMENT '转出数量',
    `reserved_main_qty`         Nullable(Int64) COMMENT '工单绑定数量',
    `is_lock_version`           Nullable(String) COMMENT '是否锁版本',
    `erp_wo_id`                 Nullable(String) COMMENT 'SAP工单编号',
    `return_main_qty`           Nullable(Int64) COMMENT '退回数量',
    `erp_bom_no`                Nullable(String) COMMENT 'ERP BOM编号',
    `ct_customer_pn`            Nullable(String) COMMENT '客户端物料号',
    `ct_vender_code`            Nullable(String) COMMENT '厂商代码',
    `ct_domestic_flag`          Nullable(String) COMMENT '内外销标识',
    `ct_fab_part_no`            Nullable(String) COMMENT '前厂料号',
    `ct_fab_part_name`          Nullable(String) COMMENT '前厂料号名称',
    `ct_fab_part_version`       Nullable(String) COMMENT '前厂料号版本号',
    `update_time`               Nullable(DateTime) COMMENT '数据更新时间'
)
ENGINE = ReplacingMergeTree(update_time)
PARTITION BY toYYYYMM(update_time)
ORDER BY (object_rrn, org_rrn, doc_id)
SETTINGS index_granularity = 8192;

CREATE TABLE IF NOT EXISTS rptdw.dwd_panel_a3g70_defect
(
    `date_key`          String COMMENT '业务日期',
    `product_id`        Nullable(String) COMMENT '产品编码',
    `wo_id`             Nullable(String) COMMENT '工单编码',
    `step_name`         Nullable(String) COMMENT '工序名称',
    `trans_type`        Nullable(String) COMMENT '事务类型',
    `trans_time`        Nullable(DateTime) COMMENT '过站时间',
    `panel_grade`       Nullable(String) COMMENT 'Panel等级',
    `panel_judge`       Nullable(String) COMMENT 'Panel判定',
    `last_defect_code`  Nullable(String) COMMENT '最终缺陷代码',
    `last_flag`         Nullable(FixedString(1)) COMMENT '最终标识',
    `panel_id`          String COMMENT 'Panel编号'
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(trans_time)
ORDER BY (date_key, product_id, panel_id, trans_time)
SETTINGS index_granularity = 8192;





CREATE TABLE IF NOT EXISTS rptdw.dwd_panel_a4710_defect
(
    `date_key`          String COMMENT '业务日期',
    `product_id`        Nullable(String) COMMENT '产品ID',
    `wo_id`             Nullable(String) COMMENT '工单ID',
    `step_name`         Nullable(String) COMMENT '工序名称',
    `trans_type`        Nullable(String) COMMENT '事务类型',
    `trans_time`        Nullable(DateTime) COMMENT '交易时间',
    `panel_grade`       Nullable(String) COMMENT 'Panel等级',
    `panel_judge`       Nullable(String) COMMENT 'Panel判定',
    `last_defect_code`  Nullable(String) COMMENT '最终缺陷代码',
    `last_flag`         Nullable(FixedString(1)) COMMENT '最终标记',
    `panel_id`          String COMMENT 'Panel唯一标识'
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(trans_time)
ORDER BY (date_key, product_id, panel_id, trans_time)
SETTINGS index_granularity = 8192;




CREATE TABLE IF NOT EXISTS rptdw.imp_yield_grade
(
    `grade_id`     Nullable(Decimal(38, 0)) COMMENT 'Oracle NUMBER',
    `panel_grade`  Nullable(String) COMMENT 'Oracle VARCHAR2(32)'
)
ENGINE = MergeTree
ORDER BY grade_id
SETTINGS index_granularity = 8192;