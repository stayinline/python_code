CREATE DATABASE IF NOT EXISTS workflow_prod;

-- 源表：public.act_app_appdef
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_app_appdef
(
    `id_` String,
    `rev_` Int32,
    `name_` Nullable(String),
    `key_` String,
    `version_` Int32,
    `category_` Nullable(String),
    `deployment_id_` Nullable(String),
    `resource_name_` Nullable(String),
    `description_` Nullable(String),
    `tenant_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_app_appdef', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_app_deployment
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_app_deployment
(
    `id_` String,
    `name_` Nullable(String),
    `category_` Nullable(String),
    `key_` Nullable(String),
    `deploy_time_` Nullable(DateTime),
    `tenant_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_app_deployment', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_app_deployment_resource
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_app_deployment_resource
(
    `id_` String,
    `name_` Nullable(String),
    `deployment_id_` Nullable(String),
    `resource_bytes_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_app_deployment_resource', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_cmmn_casedef
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_cmmn_casedef
(
    `id_` String,
    `rev_` Int32,
    `name_` Nullable(String),
    `key_` String,
    `version_` Int32,
    `category_` Nullable(String),
    `deployment_id_` Nullable(String),
    `resource_name_` Nullable(String),
    `description_` Nullable(String),
    `has_graphical_notation_` Nullable(UInt8),
    `dgrm_resource_name_` Nullable(String),
    `has_start_form_key_` Nullable(UInt8),
    `tenant_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_cmmn_casedef', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_cmmn_deployment
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_cmmn_deployment
(
    `id_` String,
    `name_` Nullable(String),
    `category_` Nullable(String),
    `key_` Nullable(String),
    `deploy_time_` Nullable(DateTime),
    `parent_deployment_id_` Nullable(String),
    `tenant_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_cmmn_deployment', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_cmmn_deployment_resource
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_cmmn_deployment_resource
(
    `id_` String,
    `name_` Nullable(String),
    `deployment_id_` Nullable(String),
    `resource_bytes_` Nullable(String),
    `generated_` Nullable(UInt8)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_cmmn_deployment_resource', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_cmmn_hi_case_inst
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_cmmn_hi_case_inst
(
    `id_` String,
    `rev_` Int32,
    `business_key_` Nullable(String),
    `name_` Nullable(String),
    `parent_id_` Nullable(String),
    `case_def_id_` Nullable(String),
    `state_` Nullable(String),
    `start_time_` Nullable(DateTime),
    `end_time_` Nullable(DateTime),
    `start_user_id_` Nullable(String),
    `callback_id_` Nullable(String),
    `callback_type_` Nullable(String),
    `reference_id_` Nullable(String),
    `reference_type_` Nullable(String),
    `last_reactivation_time_` Nullable(DateTime),
    `last_reactivation_user_id_` Nullable(String),
    `business_status_` Nullable(String),
    `tenant_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_cmmn_hi_case_inst', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_cmmn_hi_mil_inst
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_cmmn_hi_mil_inst
(
    `id_` String,
    `rev_` Int32,
    `name_` String,
    `time_stamp_` DateTime,
    `case_inst_id_` String,
    `case_def_id_` String,
    `element_id_` String,
    `tenant_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_cmmn_hi_mil_inst', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_cmmn_hi_plan_item_inst
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_cmmn_hi_plan_item_inst
(
    `id_` String,
    `rev_` Int32,
    `name_` Nullable(String),
    `state_` Nullable(String),
    `case_def_id_` Nullable(String),
    `case_inst_id_` Nullable(String),
    `stage_inst_id_` Nullable(String),
    `is_stage_` Nullable(UInt8),
    `element_id_` Nullable(String),
    `item_definition_id_` Nullable(String),
    `item_definition_type_` Nullable(String),
    `create_time_` Nullable(DateTime),
    `last_available_time_` Nullable(DateTime),
    `last_enabled_time_` Nullable(DateTime),
    `last_disabled_time_` Nullable(DateTime),
    `last_started_time_` Nullable(DateTime),
    `last_suspended_time_` Nullable(DateTime),
    `completed_time_` Nullable(DateTime),
    `occurred_time_` Nullable(DateTime),
    `terminated_time_` Nullable(DateTime),
    `exit_time_` Nullable(DateTime),
    `ended_time_` Nullable(DateTime),
    `last_updated_time_` Nullable(DateTime),
    `start_user_id_` Nullable(String),
    `reference_id_` Nullable(String),
    `reference_type_` Nullable(String),
    `entry_criterion_id_` Nullable(String),
    `exit_criterion_id_` Nullable(String),
    `show_in_overview_` Nullable(UInt8),
    `extra_value_` Nullable(String),
    `derived_case_def_id_` Nullable(String),
    `last_unavailable_time_` Nullable(DateTime),
    `tenant_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_cmmn_hi_plan_item_inst', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_cmmn_ru_case_inst
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_cmmn_ru_case_inst
(
    `id_` String,
    `rev_` Int32,
    `business_key_` Nullable(String),
    `name_` Nullable(String),
    `parent_id_` Nullable(String),
    `case_def_id_` Nullable(String),
    `state_` Nullable(String),
    `start_time_` Nullable(DateTime),
    `start_user_id_` Nullable(String),
    `callback_id_` Nullable(String),
    `callback_type_` Nullable(String),
    `lock_time_` Nullable(DateTime),
    `lock_owner_` Nullable(String),
    `is_completeable_` Nullable(UInt8),
    `reference_id_` Nullable(String),
    `reference_type_` Nullable(String),
    `last_reactivation_time_` Nullable(DateTime),
    `last_reactivation_user_id_` Nullable(String),
    `business_status_` Nullable(String),
    `tenant_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_cmmn_ru_case_inst', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_cmmn_ru_mil_inst
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_cmmn_ru_mil_inst
(
    `id_` String,
    `name_` String,
    `time_stamp_` DateTime,
    `case_inst_id_` String,
    `case_def_id_` String,
    `element_id_` String,
    `tenant_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_cmmn_ru_mil_inst', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_cmmn_ru_plan_item_inst
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_cmmn_ru_plan_item_inst
(
    `id_` String,
    `rev_` Int32,
    `case_def_id_` Nullable(String),
    `case_inst_id_` Nullable(String),
    `stage_inst_id_` Nullable(String),
    `is_stage_` Nullable(UInt8),
    `element_id_` Nullable(String),
    `name_` Nullable(String),
    `state_` Nullable(String),
    `create_time_` Nullable(DateTime),
    `start_user_id_` Nullable(String),
    `reference_id_` Nullable(String),
    `reference_type_` Nullable(String),
    `item_definition_id_` Nullable(String),
    `item_definition_type_` Nullable(String),
    `is_completeable_` Nullable(UInt8),
    `is_count_enabled_` Nullable(UInt8),
    `var_count_` Nullable(Int32),
    `sentry_part_inst_count_` Nullable(Int32),
    `last_available_time_` Nullable(DateTime),
    `last_enabled_time_` Nullable(DateTime),
    `last_disabled_time_` Nullable(DateTime),
    `last_started_time_` Nullable(DateTime),
    `last_suspended_time_` Nullable(DateTime),
    `completed_time_` Nullable(DateTime),
    `occurred_time_` Nullable(DateTime),
    `terminated_time_` Nullable(DateTime),
    `exit_time_` Nullable(DateTime),
    `ended_time_` Nullable(DateTime),
    `entry_criterion_id_` Nullable(String),
    `exit_criterion_id_` Nullable(String),
    `extra_value_` Nullable(String),
    `derived_case_def_id_` Nullable(String),
    `last_unavailable_time_` Nullable(DateTime),
    `tenant_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_cmmn_ru_plan_item_inst', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_cmmn_ru_sentry_part_inst
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_cmmn_ru_sentry_part_inst
(
    `id_` String,
    `rev_` Int32,
    `case_def_id_` Nullable(String),
    `case_inst_id_` Nullable(String),
    `plan_item_inst_id_` Nullable(String),
    `on_part_id_` Nullable(String),
    `if_part_id_` Nullable(String),
    `time_stamp_` Nullable(DateTime)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_cmmn_ru_sentry_part_inst', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_dmn_decision
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_dmn_decision
(
    `id_` String,
    `name_` Nullable(String),
    `version_` Nullable(Int32),
    `key_` Nullable(String),
    `category_` Nullable(String),
    `deployment_id_` Nullable(String),
    `tenant_id_` Nullable(String),
    `resource_name_` Nullable(String),
    `description_` Nullable(String),
    `decision_type_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_dmn_decision', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_dmn_deployment
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_dmn_deployment
(
    `id_` String,
    `name_` Nullable(String),
    `category_` Nullable(String),
    `deploy_time_` Nullable(DateTime),
    `tenant_id_` Nullable(String),
    `parent_deployment_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_dmn_deployment', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_dmn_deployment_resource
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_dmn_deployment_resource
(
    `id_` String,
    `name_` Nullable(String),
    `deployment_id_` Nullable(String),
    `resource_bytes_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_dmn_deployment_resource', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_dmn_hi_decision_execution
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_dmn_hi_decision_execution
(
    `id_` String,
    `decision_definition_id_` Nullable(String),
    `deployment_id_` Nullable(String),
    `start_time_` Nullable(DateTime),
    `end_time_` Nullable(DateTime),
    `instance_id_` Nullable(String),
    `execution_id_` Nullable(String),
    `activity_id_` Nullable(String),
    `failed_` Nullable(UInt8),
    `tenant_id_` Nullable(String),
    `execution_json_` Nullable(String),
    `scope_type_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_dmn_hi_decision_execution', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_evt_log
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_evt_log
(
    `log_nr_` Int32,
    `type_` Nullable(String),
    `proc_def_id_` Nullable(String),
    `proc_inst_id_` Nullable(String),
    `execution_id_` Nullable(String),
    `task_id_` Nullable(String),
    `time_stamp_` DateTime,
    `user_id_` Nullable(String),
    `data_` Nullable(String),
    `lock_owner_` Nullable(String),
    `lock_time_` Nullable(DateTime),
    `is_processed_` Nullable(Int16)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_evt_log', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_ge_bytearray
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_ge_bytearray
(
    `id_` String,
    `rev_` Nullable(Int32),
    `name_` Nullable(String),
    `deployment_id_` Nullable(String),
    `bytes_` Nullable(String),
    `generated_` Nullable(UInt8)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_ge_bytearray', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_ge_property
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_ge_property
(
    `name_` String,
    `value_` Nullable(String),
    `rev_` Nullable(Int32)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_ge_property', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_hi_actinst
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_hi_actinst
(
    `id_` String,
    `rev_` Nullable(Int32),
    `proc_def_id_` String,
    `proc_inst_id_` String,
    `execution_id_` String,
    `act_id_` String,
    `task_id_` Nullable(String),
    `call_proc_inst_id_` Nullable(String),
    `act_name_` Nullable(String),
    `act_type_` String,
    `assignee_` Nullable(String),
    `start_time_` DateTime,
    `end_time_` Nullable(DateTime),
    `transaction_order_` Nullable(Int32),
    `duration_` Nullable(Int64),
    `delete_reason_` Nullable(String),
    `tenant_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_hi_actinst', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_hi_attachment
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_hi_attachment
(
    `id_` String,
    `rev_` Nullable(Int32),
    `user_id_` Nullable(String),
    `name_` Nullable(String),
    `description_` Nullable(String),
    `type_` Nullable(String),
    `task_id_` Nullable(String),
    `proc_inst_id_` Nullable(String),
    `url_` Nullable(String),
    `content_id_` Nullable(String),
    `time_` Nullable(DateTime)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_hi_attachment', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_hi_comment
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_hi_comment
(
    `id_` String,
    `type_` Nullable(String),
    `time_` DateTime,
    `user_id_` Nullable(String),
    `task_id_` Nullable(String),
    `proc_inst_id_` Nullable(String),
    `action_` Nullable(String),
    `message_` Nullable(String),
    `full_msg_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_hi_comment', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_hi_detail
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_hi_detail
(
    `id_` String,
    `type_` String,
    `proc_inst_id_` Nullable(String),
    `execution_id_` Nullable(String),
    `task_id_` Nullable(String),
    `act_inst_id_` Nullable(String),
    `name_` String,
    `var_type_` Nullable(String),
    `rev_` Nullable(Int32),
    `time_` DateTime,
    `bytearray_id_` Nullable(String),
    `double_` Nullable(Float64),
    `long_` Nullable(Int64),
    `text_` Nullable(String),
    `text2_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_hi_detail', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_hi_entitylink
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_hi_entitylink
(
    `id_` String,
    `link_type_` Nullable(String),
    `create_time_` Nullable(DateTime),
    `scope_id_` Nullable(String),
    `sub_scope_id_` Nullable(String),
    `scope_type_` Nullable(String),
    `scope_definition_id_` Nullable(String),
    `parent_element_id_` Nullable(String),
    `ref_scope_id_` Nullable(String),
    `ref_scope_type_` Nullable(String),
    `ref_scope_definition_id_` Nullable(String),
    `root_scope_id_` Nullable(String),
    `root_scope_type_` Nullable(String),
    `hierarchy_type_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_hi_entitylink', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_hi_identitylink
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_hi_identitylink
(
    `id_` String,
    `group_id_` Nullable(String),
    `type_` Nullable(String),
    `user_id_` Nullable(String),
    `task_id_` Nullable(String),
    `create_time_` Nullable(DateTime),
    `proc_inst_id_` Nullable(String),
    `scope_id_` Nullable(String),
    `sub_scope_id_` Nullable(String),
    `scope_type_` Nullable(String),
    `scope_definition_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_hi_identitylink', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_hi_procinst
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_hi_procinst
(
    `id_` String,
    `rev_` Nullable(Int32),
    `proc_inst_id_` String,
    `business_key_` Nullable(String),
    `proc_def_id_` String,
    `start_time_` DateTime,
    `end_time_` Nullable(DateTime),
    `duration_` Nullable(Int64),
    `start_user_id_` Nullable(String),
    `start_act_id_` Nullable(String),
    `end_act_id_` Nullable(String),
    `super_process_instance_id_` Nullable(String),
    `delete_reason_` Nullable(String),
    `tenant_id_` Nullable(String),
    `name_` Nullable(String),
    `callback_id_` Nullable(String),
    `callback_type_` Nullable(String),
    `reference_id_` Nullable(String),
    `reference_type_` Nullable(String),
    `propagated_stage_inst_id_` Nullable(String),
    `business_status_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_hi_procinst', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_hi_taskinst
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_hi_taskinst
(
    `id_` String,
    `rev_` Nullable(Int32),
    `proc_def_id_` Nullable(String),
    `task_def_id_` Nullable(String),
    `task_def_key_` Nullable(String),
    `proc_inst_id_` Nullable(String),
    `execution_id_` Nullable(String),
    `scope_id_` Nullable(String),
    `sub_scope_id_` Nullable(String),
    `scope_type_` Nullable(String),
    `scope_definition_id_` Nullable(String),
    `propagated_stage_inst_id_` Nullable(String),
    `state_` Nullable(String),
    `name_` Nullable(String),
    `parent_task_id_` Nullable(String),
    `description_` Nullable(String),
    `owner_` Nullable(String),
    `assignee_` Nullable(String),
    `start_time_` DateTime,
    `in_progress_time_` Nullable(DateTime),
    `in_progress_started_by_` Nullable(String),
    `claim_time_` Nullable(DateTime),
    `claimed_by_` Nullable(String),
    `suspended_time_` Nullable(DateTime),
    `suspended_by_` Nullable(String),
    `end_time_` Nullable(DateTime),
    `completed_by_` Nullable(String),
    `duration_` Nullable(Int64),
    `delete_reason_` Nullable(String),
    `priority_` Nullable(Int32),
    `in_progress_due_date_` Nullable(DateTime),
    `due_date_` Nullable(DateTime),
    `form_key_` Nullable(String),
    `category_` Nullable(String),
    `tenant_id_` Nullable(String),
    `last_updated_time_` Nullable(DateTime)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_hi_taskinst', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_hi_tsk_log
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_hi_tsk_log
(
    `id_` Int32,
    `type_` Nullable(String),
    `task_id_` String,
    `time_stamp_` DateTime,
    `user_id_` Nullable(String),
    `data_` Nullable(String),
    `execution_id_` Nullable(String),
    `proc_inst_id_` Nullable(String),
    `proc_def_id_` Nullable(String),
    `scope_id_` Nullable(String),
    `scope_definition_id_` Nullable(String),
    `sub_scope_id_` Nullable(String),
    `scope_type_` Nullable(String),
    `tenant_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_hi_tsk_log', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_hi_varinst
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_hi_varinst
(
    `id_` String,
    `rev_` Nullable(Int32),
    `proc_inst_id_` Nullable(String),
    `execution_id_` Nullable(String),
    `task_id_` Nullable(String),
    `name_` String,
    `var_type_` Nullable(String),
    `scope_id_` Nullable(String),
    `sub_scope_id_` Nullable(String),
    `scope_type_` Nullable(String),
    `bytearray_id_` Nullable(String),
    `double_` Nullable(Float64),
    `long_` Nullable(Int64),
    `text_` Nullable(String),
    `text2_` Nullable(String),
    `meta_info_` Nullable(String),
    `create_time_` Nullable(DateTime),
    `last_updated_time_` Nullable(DateTime)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_hi_varinst', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_id_bytearray
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_id_bytearray
(
    `id_` String,
    `rev_` Nullable(Int32),
    `name_` Nullable(String),
    `bytes_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_id_bytearray', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_id_group
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_id_group
(
    `id_` String,
    `rev_` Nullable(Int32),
    `name_` Nullable(String),
    `type_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_id_group', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_id_info
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_id_info
(
    `id_` String,
    `rev_` Nullable(Int32),
    `user_id_` Nullable(String),
    `type_` Nullable(String),
    `key_` Nullable(String),
    `value_` Nullable(String),
    `password_` Nullable(String),
    `parent_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_id_info', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_id_membership
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_id_membership
(
    `user_id_` String,
    `group_id_` String
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_id_membership', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_id_priv
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_id_priv
(
    `id_` String,
    `name_` String
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_id_priv', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_id_priv_mapping
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_id_priv_mapping
(
    `id_` String,
    `priv_id_` String,
    `user_id_` Nullable(String),
    `group_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_id_priv_mapping', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_id_property
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_id_property
(
    `name_` String,
    `value_` Nullable(String),
    `rev_` Nullable(Int32)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_id_property', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_id_token
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_id_token
(
    `id_` String,
    `rev_` Nullable(Int32),
    `token_value_` Nullable(String),
    `token_date_` Nullable(DateTime),
    `ip_address_` Nullable(String),
    `user_agent_` Nullable(String),
    `user_id_` Nullable(String),
    `token_data_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_id_token', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_id_user
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_id_user
(
    `id_` String,
    `rev_` Nullable(Int32),
    `first_` Nullable(String),
    `last_` Nullable(String),
    `display_name_` Nullable(String),
    `email_` Nullable(String),
    `pwd_` Nullable(String),
    `picture_id_` Nullable(String),
    `tenant_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_id_user', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_procdef_info
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_procdef_info
(
    `id_` String,
    `proc_def_id_` String,
    `rev_` Nullable(Int32),
    `info_json_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_procdef_info', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_re_deployment
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_re_deployment
(
    `id_` String,
    `name_` Nullable(String),
    `category_` Nullable(String),
    `key_` Nullable(String),
    `tenant_id_` Nullable(String),
    `deploy_time_` Nullable(DateTime),
    `derived_from_` Nullable(String),
    `derived_from_root_` Nullable(String),
    `parent_deployment_id_` Nullable(String),
    `engine_version_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_re_deployment', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_re_model
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_re_model
(
    `id_` String,
    `rev_` Nullable(Int32),
    `name_` Nullable(String),
    `key_` Nullable(String),
    `category_` Nullable(String),
    `create_time_` Nullable(DateTime),
    `last_update_time_` Nullable(DateTime),
    `version_` Nullable(Int32),
    `meta_info_` Nullable(String),
    `deployment_id_` Nullable(String),
    `editor_source_value_id_` Nullable(String),
    `editor_source_extra_value_id_` Nullable(String),
    `tenant_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_re_model', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_re_procdef
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_re_procdef
(
    `id_` String,
    `rev_` Nullable(Int32),
    `category_` Nullable(String),
    `name_` Nullable(String),
    `key_` String,
    `version_` Int32,
    `deployment_id_` Nullable(String),
    `resource_name_` Nullable(String),
    `dgrm_resource_name_` Nullable(String),
    `description_` Nullable(String),
    `has_start_form_key_` Nullable(UInt8),
    `has_graphical_notation_` Nullable(UInt8),
    `suspension_state_` Nullable(Int32),
    `tenant_id_` Nullable(String),
    `derived_from_` Nullable(String),
    `derived_from_root_` Nullable(String),
    `derived_version_` Int32,
    `engine_version_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_re_procdef', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_ru_actinst
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_ru_actinst
(
    `id_` String,
    `rev_` Nullable(Int32),
    `proc_def_id_` String,
    `proc_inst_id_` String,
    `execution_id_` String,
    `act_id_` String,
    `task_id_` Nullable(String),
    `call_proc_inst_id_` Nullable(String),
    `act_name_` Nullable(String),
    `act_type_` String,
    `assignee_` Nullable(String),
    `start_time_` DateTime,
    `end_time_` Nullable(DateTime),
    `duration_` Nullable(Int64),
    `transaction_order_` Nullable(Int32),
    `delete_reason_` Nullable(String),
    `tenant_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_ru_actinst', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_ru_deadletter_job
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_ru_deadletter_job
(
    `id_` String,
    `rev_` Nullable(Int32),
    `category_` Nullable(String),
    `type_` String,
    `exclusive_` Nullable(UInt8),
    `execution_id_` Nullable(String),
    `process_instance_id_` Nullable(String),
    `proc_def_id_` Nullable(String),
    `element_id_` Nullable(String),
    `element_name_` Nullable(String),
    `scope_id_` Nullable(String),
    `sub_scope_id_` Nullable(String),
    `scope_type_` Nullable(String),
    `scope_definition_id_` Nullable(String),
    `correlation_id_` Nullable(String),
    `exception_stack_id_` Nullable(String),
    `exception_msg_` Nullable(String),
    `duedate_` Nullable(DateTime),
    `repeat_` Nullable(String),
    `handler_type_` Nullable(String),
    `handler_cfg_` Nullable(String),
    `custom_values_id_` Nullable(String),
    `create_time_` Nullable(DateTime),
    `tenant_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_ru_deadletter_job', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_ru_entitylink
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_ru_entitylink
(
    `id_` String,
    `rev_` Nullable(Int32),
    `create_time_` Nullable(DateTime),
    `link_type_` Nullable(String),
    `scope_id_` Nullable(String),
    `sub_scope_id_` Nullable(String),
    `scope_type_` Nullable(String),
    `scope_definition_id_` Nullable(String),
    `parent_element_id_` Nullable(String),
    `ref_scope_id_` Nullable(String),
    `ref_scope_type_` Nullable(String),
    `ref_scope_definition_id_` Nullable(String),
    `root_scope_id_` Nullable(String),
    `root_scope_type_` Nullable(String),
    `hierarchy_type_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_ru_entitylink', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_ru_event_subscr
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_ru_event_subscr
(
    `id_` String,
    `rev_` Nullable(Int32),
    `event_type_` String,
    `event_name_` Nullable(String),
    `execution_id_` Nullable(String),
    `proc_inst_id_` Nullable(String),
    `activity_id_` Nullable(String),
    `configuration_` Nullable(String),
    `created_` DateTime,
    `proc_def_id_` Nullable(String),
    `sub_scope_id_` Nullable(String),
    `scope_id_` Nullable(String),
    `scope_definition_id_` Nullable(String),
    `scope_definition_key_` Nullable(String),
    `scope_type_` Nullable(String),
    `lock_time_` Nullable(DateTime),
    `lock_owner_` Nullable(String),
    `tenant_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_ru_event_subscr', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_ru_execution
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_ru_execution
(
    `id_` String,
    `rev_` Nullable(Int32),
    `proc_inst_id_` Nullable(String),
    `business_key_` Nullable(String),
    `parent_id_` Nullable(String),
    `proc_def_id_` Nullable(String),
    `super_exec_` Nullable(String),
    `root_proc_inst_id_` Nullable(String),
    `act_id_` Nullable(String),
    `is_active_` Nullable(UInt8),
    `is_concurrent_` Nullable(UInt8),
    `is_scope_` Nullable(UInt8),
    `is_event_scope_` Nullable(UInt8),
    `is_mi_root_` Nullable(UInt8),
    `suspension_state_` Nullable(Int32),
    `cached_ent_state_` Nullable(Int32),
    `tenant_id_` Nullable(String),
    `name_` Nullable(String),
    `start_act_id_` Nullable(String),
    `start_time_` Nullable(DateTime),
    `start_user_id_` Nullable(String),
    `lock_time_` Nullable(DateTime),
    `lock_owner_` Nullable(String),
    `is_count_enabled_` Nullable(UInt8),
    `evt_subscr_count_` Nullable(Int32),
    `task_count_` Nullable(Int32),
    `job_count_` Nullable(Int32),
    `timer_job_count_` Nullable(Int32),
    `susp_job_count_` Nullable(Int32),
    `deadletter_job_count_` Nullable(Int32),
    `external_worker_job_count_` Nullable(Int32),
    `var_count_` Nullable(Int32),
    `id_link_count_` Nullable(Int32),
    `callback_id_` Nullable(String),
    `callback_type_` Nullable(String),
    `reference_id_` Nullable(String),
    `reference_type_` Nullable(String),
    `propagated_stage_inst_id_` Nullable(String),
    `business_status_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_ru_execution', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_ru_external_job
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_ru_external_job
(
    `id_` String,
    `rev_` Nullable(Int32),
    `category_` Nullable(String),
    `type_` String,
    `lock_exp_time_` Nullable(DateTime),
    `lock_owner_` Nullable(String),
    `exclusive_` Nullable(UInt8),
    `execution_id_` Nullable(String),
    `process_instance_id_` Nullable(String),
    `proc_def_id_` Nullable(String),
    `element_id_` Nullable(String),
    `element_name_` Nullable(String),
    `scope_id_` Nullable(String),
    `sub_scope_id_` Nullable(String),
    `scope_type_` Nullable(String),
    `scope_definition_id_` Nullable(String),
    `correlation_id_` Nullable(String),
    `retries_` Nullable(Int32),
    `exception_stack_id_` Nullable(String),
    `exception_msg_` Nullable(String),
    `duedate_` Nullable(DateTime),
    `repeat_` Nullable(String),
    `handler_type_` Nullable(String),
    `handler_cfg_` Nullable(String),
    `custom_values_id_` Nullable(String),
    `create_time_` Nullable(DateTime),
    `tenant_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_ru_external_job', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_ru_history_job
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_ru_history_job
(
    `id_` String,
    `rev_` Nullable(Int32),
    `lock_exp_time_` Nullable(DateTime),
    `lock_owner_` Nullable(String),
    `retries_` Nullable(Int32),
    `exception_stack_id_` Nullable(String),
    `exception_msg_` Nullable(String),
    `handler_type_` Nullable(String),
    `handler_cfg_` Nullable(String),
    `custom_values_id_` Nullable(String),
    `adv_handler_cfg_id_` Nullable(String),
    `create_time_` Nullable(DateTime),
    `scope_type_` Nullable(String),
    `tenant_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_ru_history_job', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_ru_identitylink
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_ru_identitylink
(
    `id_` String,
    `rev_` Nullable(Int32),
    `group_id_` Nullable(String),
    `type_` Nullable(String),
    `user_id_` Nullable(String),
    `task_id_` Nullable(String),
    `proc_inst_id_` Nullable(String),
    `proc_def_id_` Nullable(String),
    `scope_id_` Nullable(String),
    `sub_scope_id_` Nullable(String),
    `scope_type_` Nullable(String),
    `scope_definition_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_ru_identitylink', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_ru_job
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_ru_job
(
    `id_` String,
    `rev_` Nullable(Int32),
    `category_` Nullable(String),
    `type_` String,
    `lock_exp_time_` Nullable(DateTime),
    `lock_owner_` Nullable(String),
    `exclusive_` Nullable(UInt8),
    `execution_id_` Nullable(String),
    `process_instance_id_` Nullable(String),
    `proc_def_id_` Nullable(String),
    `element_id_` Nullable(String),
    `element_name_` Nullable(String),
    `scope_id_` Nullable(String),
    `sub_scope_id_` Nullable(String),
    `scope_type_` Nullable(String),
    `scope_definition_id_` Nullable(String),
    `correlation_id_` Nullable(String),
    `retries_` Nullable(Int32),
    `exception_stack_id_` Nullable(String),
    `exception_msg_` Nullable(String),
    `duedate_` Nullable(DateTime),
    `repeat_` Nullable(String),
    `handler_type_` Nullable(String),
    `handler_cfg_` Nullable(String),
    `custom_values_id_` Nullable(String),
    `create_time_` Nullable(DateTime),
    `tenant_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_ru_job', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_ru_suspended_job
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_ru_suspended_job
(
    `id_` String,
    `rev_` Nullable(Int32),
    `category_` Nullable(String),
    `type_` String,
    `exclusive_` Nullable(UInt8),
    `execution_id_` Nullable(String),
    `process_instance_id_` Nullable(String),
    `proc_def_id_` Nullable(String),
    `element_id_` Nullable(String),
    `element_name_` Nullable(String),
    `scope_id_` Nullable(String),
    `sub_scope_id_` Nullable(String),
    `scope_type_` Nullable(String),
    `scope_definition_id_` Nullable(String),
    `correlation_id_` Nullable(String),
    `retries_` Nullable(Int32),
    `exception_stack_id_` Nullable(String),
    `exception_msg_` Nullable(String),
    `duedate_` Nullable(DateTime),
    `repeat_` Nullable(String),
    `handler_type_` Nullable(String),
    `handler_cfg_` Nullable(String),
    `custom_values_id_` Nullable(String),
    `create_time_` Nullable(DateTime),
    `tenant_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_ru_suspended_job', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_ru_task
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_ru_task
(
    `id_` String,
    `rev_` Nullable(Int32),
    `execution_id_` Nullable(String),
    `proc_inst_id_` Nullable(String),
    `proc_def_id_` Nullable(String),
    `task_def_id_` Nullable(String),
    `scope_id_` Nullable(String),
    `sub_scope_id_` Nullable(String),
    `scope_type_` Nullable(String),
    `scope_definition_id_` Nullable(String),
    `propagated_stage_inst_id_` Nullable(String),
    `state_` Nullable(String),
    `name_` Nullable(String),
    `parent_task_id_` Nullable(String),
    `description_` Nullable(String),
    `task_def_key_` Nullable(String),
    `owner_` Nullable(String),
    `assignee_` Nullable(String),
    `delegation_` Nullable(String),
    `priority_` Nullable(Int32),
    `create_time_` Nullable(DateTime),
    `in_progress_time_` Nullable(DateTime),
    `in_progress_started_by_` Nullable(String),
    `claim_time_` Nullable(DateTime),
    `claimed_by_` Nullable(String),
    `suspended_time_` Nullable(DateTime),
    `suspended_by_` Nullable(String),
    `in_progress_due_date_` Nullable(DateTime),
    `due_date_` Nullable(DateTime),
    `category_` Nullable(String),
    `suspension_state_` Nullable(Int32),
    `tenant_id_` Nullable(String),
    `form_key_` Nullable(String),
    `is_count_enabled_` Nullable(UInt8),
    `var_count_` Nullable(Int32),
    `id_link_count_` Nullable(Int32),
    `sub_task_count_` Nullable(Int32)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_ru_task', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_ru_timer_job
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_ru_timer_job
(
    `id_` String,
    `rev_` Nullable(Int32),
    `category_` Nullable(String),
    `type_` String,
    `lock_exp_time_` Nullable(DateTime),
    `lock_owner_` Nullable(String),
    `exclusive_` Nullable(UInt8),
    `execution_id_` Nullable(String),
    `process_instance_id_` Nullable(String),
    `proc_def_id_` Nullable(String),
    `element_id_` Nullable(String),
    `element_name_` Nullable(String),
    `scope_id_` Nullable(String),
    `sub_scope_id_` Nullable(String),
    `scope_type_` Nullable(String),
    `scope_definition_id_` Nullable(String),
    `correlation_id_` Nullable(String),
    `retries_` Nullable(Int32),
    `exception_stack_id_` Nullable(String),
    `exception_msg_` Nullable(String),
    `duedate_` Nullable(DateTime),
    `repeat_` Nullable(String),
    `handler_type_` Nullable(String),
    `handler_cfg_` Nullable(String),
    `custom_values_id_` Nullable(String),
    `create_time_` Nullable(DateTime),
    `tenant_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_ru_timer_job', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.act_ru_variable
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_act_ru_variable
(
    `id_` String,
    `rev_` Nullable(Int32),
    `type_` String,
    `name_` String,
    `execution_id_` Nullable(String),
    `proc_inst_id_` Nullable(String),
    `task_id_` Nullable(String),
    `scope_id_` Nullable(String),
    `sub_scope_id_` Nullable(String),
    `scope_type_` Nullable(String),
    `bytearray_id_` Nullable(String),
    `double_` Nullable(Float64),
    `long_` Nullable(Int64),
    `text_` Nullable(String),
    `text2_` Nullable(String),
    `meta_info_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'act_ru_variable', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.flw_channel_definition
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_flw_channel_definition
(
    `id_` String,
    `name_` Nullable(String),
    `version_` Nullable(Int32),
    `key_` Nullable(String),
    `category_` Nullable(String),
    `deployment_id_` Nullable(String),
    `create_time_` Nullable(DateTime),
    `tenant_id_` Nullable(String),
    `resource_name_` Nullable(String),
    `description_` Nullable(String),
    `type_` Nullable(String),
    `implementation_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'flw_channel_definition', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.flw_event_definition
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_flw_event_definition
(
    `id_` String,
    `name_` Nullable(String),
    `version_` Nullable(Int32),
    `key_` Nullable(String),
    `category_` Nullable(String),
    `deployment_id_` Nullable(String),
    `tenant_id_` Nullable(String),
    `resource_name_` Nullable(String),
    `description_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'flw_event_definition', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.flw_event_deployment
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_flw_event_deployment
(
    `id_` String,
    `name_` Nullable(String),
    `category_` Nullable(String),
    `deploy_time_` Nullable(DateTime),
    `tenant_id_` Nullable(String),
    `parent_deployment_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'flw_event_deployment', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.flw_event_resource
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_flw_event_resource
(
    `id_` String,
    `name_` Nullable(String),
    `deployment_id_` Nullable(String),
    `resource_bytes_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'flw_event_resource', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.flw_ru_batch
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_flw_ru_batch
(
    `id_` String,
    `rev_` Nullable(Int32),
    `type_` String,
    `search_key_` Nullable(String),
    `search_key2_` Nullable(String),
    `create_time_` DateTime,
    `complete_time_` Nullable(DateTime),
    `status_` Nullable(String),
    `batch_doc_id_` Nullable(String),
    `tenant_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'flw_ru_batch', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.flw_ru_batch_part
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_flw_ru_batch_part
(
    `id_` String,
    `rev_` Nullable(Int32),
    `batch_id_` Nullable(String),
    `type_` String,
    `scope_id_` Nullable(String),
    `sub_scope_id_` Nullable(String),
    `scope_type_` Nullable(String),
    `search_key_` Nullable(String),
    `search_key2_` Nullable(String),
    `create_time_` DateTime,
    `complete_time_` Nullable(DateTime),
    `status_` Nullable(String),
    `result_doc_id_` Nullable(String),
    `tenant_id_` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'flw_ru_batch_part', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.hplc_method
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_hplc_method
(
    `id` String,
    `instrument` Nullable(String),
    `column_name` Nullable(String),
    `mobile_phase` Nullable(String),
    `flow_rate` Nullable(Decimal(5,3)),
    `stop_time` Nullable(Decimal(5,1)),
    `detector` Nullable(String),
    `column_temperature` Nullable(Decimal(5,1)),
    `run_id` Nullable(String),
    `block_id` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'hplc_method', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.hplc_result
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_hplc_result
(
    `id` String,
    `barcode` Nullable(String),
    `product_name` Nullable(String),
    `hmw` Nullable(Decimal(6,2)),
    `main_peak` Nullable(Decimal(6,2)),
    `lmw` Nullable(Decimal(6,2)),
    `run_id` Nullable(String),
    `block_id` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'hplc_result', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.molecule_info
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_molecule_info
(
    `id` String,
    `molecule_name` Nullable(String),
    `molecule_subtype` Nullable(String),
    `mw` Nullable(Decimal(12,4)),
    `pi` Nullable(Decimal(4,2)),
    `ec` Nullable(Decimal(10,6)),
    `run_id` Nullable(String),
    `block_id` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'molecule_info', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.pipetting_record
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_pipetting_record
(
    `id` String,
    `sample_name` Nullable(String),
    `source_plate` Nullable(String),
    `source_well` Nullable(String),
    `target_plate` Nullable(String),
    `target_well` Nullable(String),
    `pipetting_volume` Nullable(Decimal(8,2)),
    `product_name` Nullable(String),
    `run_id` Nullable(String),
    `block_id` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'pipetting_record', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.plasmid_construction
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_plasmid_construction
(
    `id` String,
    `construction_no` Nullable(String),
    `plasmid_name` Nullable(String),
    `project_type` Nullable(String),
    `clone_no` Nullable(String),
    `fragment_size` Nullable(Decimal(10,2)),
    `cloning_enzyme` Nullable(String),
    `vector_type` Nullable(String),
    `resistance` Nullable(String),
    `plate_no` Nullable(String),
    `vector` Nullable(String),
    `screening_primer` Nullable(String),
    `screening_size_kb` Nullable(Decimal(10,2)),
    `sequencing_primer` Nullable(String),
    `required_amount` Nullable(String),
    `extraction_method` Nullable(String),
    `comment` Nullable(String),
    `run_id` Nullable(String),
    `block_id` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'plasmid_construction', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.plasmid_sequencing
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_plasmid_sequencing
(
    `id` String,
    `plasmid_name` Nullable(String),
    `clone_no` Nullable(String),
    `sequencing_time` Nullable(DateTime),
    `plasmid_yield` Nullable(Decimal(8,2)),
    `sequencing_primer` Nullable(String),
    `sequencing_result` Nullable(String),
    `processing_opinion` Nullable(String),
    `destination` Nullable(String),
    `run_id` Nullable(String),
    `block_id` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'plasmid_sequencing', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.primer_info
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_primer_info
(
    `id` String,
    `primer_type` Nullable(String),
    `primer_name` Nullable(String),
    `primer_seq` Nullable(String),
    `primer_length` Nullable(Int32),
    `annealing_temperature` Nullable(Decimal(6,2)),
    `plasmid_name` Nullable(String),
    `plate_name` Nullable(String),
    `plate_well` Nullable(String),
    `run_id` Nullable(String),
    `block_id` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'primer_info', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.project
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_project
(
    `project_id` String COMMENT '项目id',
    `project_no` String COMMENT '项目编号',
    `project_name` String COMMENT '项目名称',
    `description` Nullable(String) COMMENT '项目描述',
    `creator` String COMMENT '项目创建人',
    `lead_researcher` String COMMENT '项目负责人',
    `start_date` Date COMMENT '启动日期',
    `end_date` Nullable(Date) COMMENT '计划结束日期',
    `status` Int16 COMMENT '项目状态',
    `budget` Nullable(String) COMMENT '项目预算',
    `report` Nullable(String) COMMENT '项目报告',
    `customer_name` Nullable(String) COMMENT '客户名称',
    `created_time` Nullable(DateTime) COMMENT '创建时间',
    `is_deleted` Nullable(UInt8) COMMENT '是否删除',
    `deleted_time` Nullable(DateTime) COMMENT '删除时间',
    `updater` Nullable(String) COMMENT '更新人',
    `updated_time` Nullable(DateTime) COMMENT '更新时间',
    `deleter` Nullable(String),
    `stop_reason` Nullable(String),
    `start_time` Nullable(DateTime),
    `end_time` Nullable(DateTime)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'project', 'postgres', 'I6Yvg/GD61UjyJsES5Q') COMMENT '项目实体表';


-- 源表：public.purified_protein
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_purified_protein
(
    `id` String,
    `protein_name` Nullable(String),
    `molecular_weight` Nullable(Decimal(10,4)),
    `pi` Nullable(Decimal(5,2)),
    `cell_line` Nullable(String),
    `cell_supernatant_volume` Nullable(Decimal(10,2)),
    `filter_column_matrix` Nullable(String),
    `purification_method` Nullable(String),
    `elution_buffer` Nullable(String),
    `solvent` Nullable(String),
    `final_volume` Nullable(Decimal(10,2)),
    `final_concentration` Nullable(Decimal(8,3)),
    `purity_sds_page_non_reducing` Nullable(Decimal(5,2)),
    `purity_sds_page_reducing` Nullable(Decimal(5,2)),
    `purity_asec` Nullable(Decimal(5,2)),
    `ms_intact` Nullable(String),
    `endotoxin_content` Nullable(Decimal(8,3)),
    `run_id` Nullable(String),
    `block_id` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'purified_protein', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.sample_antigen
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_sample_antigen
(
    `sample_id` String COMMENT '主键ID',
    `source` Nullable(String) COMMENT '来源',
    `current_status` Nullable(String) COMMENT '状态',
    `barcode` Nullable(String) COMMENT '条形码',
    `sample_name` Nullable(String) COMMENT '样本名称',
    `sample_type` Nullable(String) COMMENT '样本类型',
    `concentration` Nullable(Decimal(15,6)) COMMENT '浓度值',
    `concentration_unit` Nullable(String) COMMENT '基础浓度单位',
    `concentration_unit_display` Nullable(String) COMMENT '展示浓度单位',
    `sample_volume` Nullable(Decimal(15,6)) COMMENT '体积值',
    `volume_unit` Nullable(String) COMMENT '基础体积单位',
    `volume_unit_display` Nullable(String) COMMENT '展示体积单位',
    `mass` Nullable(Decimal(15,6)) COMMENT '质量值',
    `mass_unit` Nullable(String) COMMENT '基础质量单位',
    `mass_unit_display` Nullable(String) COMMENT '展示质量单位',
    `harvesting_time` Nullable(DateTime) COMMENT '收获时间',
    `harvesting_person` Nullable(String) COMMENT '收获人员',
    `plate_id` Nullable(String) COMMENT '所在板ID',
    `well` Nullable(String) COMMENT '所在孔号',
    `storage_location` Nullable(String) COMMENT '存储位置',
    `project_id` Nullable(String) COMMENT '项目ID',
    `project_no` Nullable(String) COMMENT '项目编号',
    `species` Nullable(String) COMMENT '物种',
    `passage_no` Nullable(Int32) COMMENT '传代次数',
    `doubling_time` Nullable(Decimal(10,2)) COMMENT '倍增时间（小时）',
    `viability` Nullable(Decimal(15,2)) COMMENT '活率（百分比）',
    `total_cell_concentration` Nullable(Decimal(15,2)) COMMENT '总细胞浓度',
    `live_cell_concentration` Nullable(Decimal(15,2)) COMMENT '活细胞浓度',
    `diameter` Nullable(Decimal(8,3)) COMMENT '直径（微米）',
    `creator` Nullable(String) COMMENT '创建人',
    `created_time` Nullable(DateTime) COMMENT '创建时间',
    `is_deleted` Nullable(UInt8) COMMENT '是否删除：0-否，1-是',
    `deleted_time` Nullable(DateTime) COMMENT '删除时间',
    `updater` Nullable(String) COMMENT '更新人',
    `updated_time` Nullable(DateTime) COMMENT '更新时间',
    `deleter` Nullable(String) COMMENT '删除人',
    `source_species` Nullable(String) COMMENT '来源物种',
    `organ_tissue_type` Nullable(String) COMMENT '器官/组织类型',
    `sample_morphology` Nullable(String) COMMENT '样本形态特征',
    `external_id` Nullable(String) COMMENT '外部标识码',
    `storage_condition` Nullable(String) COMMENT '储存条件',
    `storage_method` Nullable(String) COMMENT '储存方式',
    `contagious` Nullable(String) COMMENT '有无传染性（未知=0,无=1,有=2）',
    `clinical_typing_info` Nullable(String) COMMENT '临床分型信息',
    `expiry_date` Nullable(String) COMMENT '失效日期',
    `sample_weight` Nullable(String) COMMENT '样本重量',
    `bio_safety_level` Nullable(String) COMMENT '生物安全等级（未知=0, BSL-1=1, BSL-2=2, BSL-3=3）',
    `collection_time` Nullable(String) COMMENT '采集时间',
    `collection_method` Nullable(String) COMMENT '采集方式',
    `receive_time` Nullable(String) COMMENT '接收时间',
    `attachments` Nullable(String) COMMENT '附件',
    `block_id` Nullable(String),
    `run_id` Nullable(String),
    `antigen_code` Nullable(String),
    `antigen_cn` Nullable(String),
    `antigen_description` Nullable(String),
    `antigen_pro_info` Nullable(String),
    `pro_application_time` Nullable(String),
    `antigens_sequence` Nullable(String),
    `benchmark_antibody1_no` Nullable(String),
    `benchmark_antibody1_name` Nullable(String),
    `benchmark_antibody1_sequence` Nullable(String),
    `benchmark_antibody2_no` Nullable(String),
    `benchmark_antibody2_name` Nullable(String),
    `benchmark_antibody2_sequence` Nullable(String),
    `expiry_status` Nullable(String) COMMENT '过期状态',
    `deprecate_reason` Nullable(String) COMMENT '废弃原因',
    `source_node_id` Nullable(String) COMMENT '来源节点ID',
    `source_node_name` Nullable(String) COMMENT '来源节点名称',
    `source_node_status` Nullable(String) COMMENT '来源节点状态'
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'sample_antigen', 'postgres', 'I6Yvg/GD61UjyJsES5Q') COMMENT '抗原样本信息表';


-- 源表：public.sample_cell
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_sample_cell
(
    `sample_id` String COMMENT '主键ID',
    `source` Nullable(String) COMMENT '来源',
    `current_status` Nullable(String) COMMENT '状态',
    `barcode` Nullable(String) COMMENT '条形码',
    `sample_name` Nullable(String) COMMENT '样本名称',
    `sample_type` Nullable(String) COMMENT '样本类型',
    `concentration` Nullable(Decimal(15,6)) COMMENT '浓度值',
    `concentration_unit` Nullable(String) COMMENT '基础浓度单位',
    `concentration_unit_display` Nullable(String) COMMENT '展示浓度单位',
    `sample_volume` Nullable(Decimal(15,6)) COMMENT '体积值',
    `volume_unit` Nullable(String) COMMENT '基础体积单位',
    `volume_unit_display` Nullable(String) COMMENT '展示体积单位',
    `mass` Nullable(Decimal(15,6)) COMMENT '质量值',
    `mass_unit` Nullable(String) COMMENT '基础质量单位',
    `mass_unit_display` Nullable(String) COMMENT '展示质量单位',
    `harvesting_time` Nullable(DateTime) COMMENT '收获时间',
    `harvesting_person` Nullable(String) COMMENT '收获人员',
    `plate_id` Nullable(String) COMMENT '所在板ID',
    `well` Nullable(String) COMMENT '所在孔号',
    `storage_location` Nullable(String) COMMENT '存储位置',
    `project_id` Nullable(String) COMMENT '项目ID',
    `project_no` Nullable(String) COMMENT '项目编号',
    `species` Nullable(String) COMMENT '物种',
    `passage_no` Nullable(Int32) COMMENT '传代次数',
    `doubling_time` Nullable(Decimal(10,2)) COMMENT '倍增时间（小时）',
    `viability` Nullable(Decimal(15,2)) COMMENT '活率（百分比）',
    `total_cell_concentration` Nullable(Decimal(15,2)) COMMENT '总细胞浓度',
    `live_cell_concentration` Nullable(Decimal(15,2)) COMMENT '活细胞浓度',
    `diameter` Nullable(Decimal(8,3)) COMMENT '直径（微米）',
    `creator` String COMMENT '创建人',
    `created_time` Nullable(DateTime) COMMENT '创建时间',
    `is_deleted` Nullable(UInt8) COMMENT '是否删除：0-否，1-是',
    `deleted_time` Nullable(DateTime) COMMENT '删除时间',
    `updater` Nullable(String) COMMENT '更新人',
    `updated_time` Nullable(DateTime) COMMENT '更新时间',
    `deleter` Nullable(String) COMMENT '删除人',
    `source_species` Nullable(String) COMMENT '来源物种',
    `organ_tissue_type` Nullable(String) COMMENT '器官/组织类型',
    `sample_morphology` Nullable(String) COMMENT '样本形态特征',
    `external_id` Nullable(String) COMMENT '外部标识码',
    `storage_condition` Nullable(String) COMMENT '储存条件',
    `storage_method` Nullable(String) COMMENT '储存方式',
    `contagious` Nullable(String) COMMENT '有无传染性（未知=0,无=1,有=2）',
    `clinical_typing_info` Nullable(String) COMMENT '临床分型信息',
    `expiry_date` Nullable(String) COMMENT '失效日期',
    `sample_weight` Nullable(String) COMMENT '样本重量',
    `bio_safety_level` Nullable(String) COMMENT '生物安全等级（未知=0, BSL-1=1, BSL-2=2, BSL-3=3）',
    `collection_time` Nullable(String) COMMENT '采集时间',
    `collection_method` Nullable(String) COMMENT '采集方式',
    `receive_time` Nullable(String) COMMENT '接收时间',
    `attachments` Nullable(String) COMMENT '附件',
    `block_id` Nullable(String),
    `run_id` Nullable(String),
    `source_node_id` Nullable(String) COMMENT '来源节点ID',
    `source_node_name` Nullable(String) COMMENT '来源节点名称',
    `source_node_status` Nullable(String) COMMENT '来源节点状态',
    `expiry_status` Nullable(String) COMMENT '过期状态',
    `deprecate_reason` Nullable(String) COMMENT '废弃原因'
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'sample_cell', 'postgres', 'I6Yvg/GD61UjyJsES5Q') COMMENT '细胞样本信息表';


-- 源表：public.sample_plasmid
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_sample_plasmid
(
    `sample_id` String COMMENT '主键ID',
    `source` Nullable(String) COMMENT '来源',
    `current_status` Nullable(String) COMMENT '状态',
    `barcode` Nullable(String) COMMENT '条形码',
    `sample_name` Nullable(String) COMMENT '样本名称',
    `sample_type` Nullable(String) COMMENT '样本类型',
    `concentration` Nullable(Decimal(15,6)) COMMENT '浓度值',
    `concentration_unit` Nullable(String) COMMENT '基础浓度单位',
    `concentration_unit_display` Nullable(String) COMMENT '展示浓度单位',
    `sample_volume` Nullable(Decimal(15,6)) COMMENT '体积值',
    `volume_unit` Nullable(String) COMMENT '基础体积单位',
    `volume_unit_display` Nullable(String) COMMENT '展示体积单位',
    `mass` Nullable(Decimal(15,6)) COMMENT '质量值',
    `mass_unit` Nullable(String) COMMENT '基础质量单位',
    `mass_unit_display` Nullable(String) COMMENT '展示质量单位',
    `harvesting_time` Nullable(DateTime) COMMENT '收获时间',
    `harvesting_person` Nullable(String) COMMENT '收获人员',
    `plate_id` Nullable(String) COMMENT '所在板ID',
    `well` Nullable(String) COMMENT '所在孔号',
    `storage_location` Nullable(String) COMMENT '存储位置',
    `project_id` Nullable(String) COMMENT '项目ID',
    `project_no` Nullable(String) COMMENT '项目编号',
    `a260_280` Nullable(Decimal(15,2)) COMMENT 'A260/280比值',
    `a260_230` Nullable(Decimal(15,2)) COMMENT 'A260/230比值',
    `creator` String COMMENT '创建人',
    `created_time` Nullable(DateTime) COMMENT '创建时间',
    `is_deleted` Nullable(UInt8) COMMENT '是否删除：0-否，1-是',
    `deleted_time` Nullable(DateTime) COMMENT '删除时间',
    `updater` Nullable(String) COMMENT '更新人',
    `updated_time` Nullable(DateTime) COMMENT '更新时间',
    `deleter` Nullable(String) COMMENT '删除人',
    `source_species` Nullable(String) COMMENT '来源物种',
    `organ_tissue_type` Nullable(String) COMMENT '器官/组织类型',
    `sample_morphology` Nullable(String) COMMENT '样本形态特征',
    `external_id` Nullable(String) COMMENT '外部标识码',
    `storage_condition` Nullable(String) COMMENT '储存条件',
    `storage_method` Nullable(String) COMMENT '储存方式',
    `contagious` Nullable(String) COMMENT '有无传染性（未知=0,无=1,有=2）',
    `clinical_typing_info` Nullable(String) COMMENT '临床分型信息',
    `expiry_date` Nullable(String) COMMENT '失效日期',
    `sample_weight` Nullable(String) COMMENT '样本重量',
    `bio_safety_level` Nullable(String) COMMENT '生物安全等级（未知=0, BSL-1=1, BSL-2=2, BSL-3=3）',
    `collection_time` Nullable(String) COMMENT '采集时间',
    `collection_method` Nullable(String) COMMENT '采集方式',
    `receive_time` Nullable(String) COMMENT '接收时间',
    `attachments` Nullable(String) COMMENT '附件',
    `block_id` Nullable(String),
    `run_id` Nullable(String),
    `source_node_id` Nullable(String) COMMENT '来源节点ID',
    `source_node_name` Nullable(String) COMMENT '来源节点名称',
    `source_node_status` Nullable(String) COMMENT '来源节点状态',
    `expiry_status` Nullable(String) COMMENT '过期状态',
    `deprecate_reason` Nullable(String) COMMENT '废弃原因',
    `batch_no` Nullable(String),
    `molecule_name` Nullable(String),
    `chain_name` Nullable(String),
    `chain_type` Nullable(String),
    `is_correct` Nullable(String),
    `sanger_result` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'sample_plasmid', 'postgres', 'I6Yvg/GD61UjyJsES5Q') COMMENT '质粒样本信息表';


-- 源表：public.sample_protein
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_sample_protein
(
    `sample_id` String COMMENT '主键ID',
    `source` Nullable(String) COMMENT '来源',
    `current_status` Nullable(String) COMMENT '状态',
    `barcode` Nullable(String) COMMENT '条形码',
    `sample_name` Nullable(String) COMMENT '样本名称',
    `sample_type` Nullable(String) COMMENT '样本类型',
    `concentration` Nullable(Decimal(15,6)) COMMENT '浓度值',
    `concentration_unit` Nullable(String) COMMENT '基础浓度单位',
    `concentration_unit_display` Nullable(String) COMMENT '展示浓度单位',
    `sample_volume` Nullable(Decimal(15,6)) COMMENT '体积值',
    `volume_unit` Nullable(String) COMMENT '基础体积单位',
    `volume_unit_display` Nullable(String) COMMENT '展示体积单位',
    `mass` Nullable(Decimal(15,6)) COMMENT '质量值',
    `mass_unit` Nullable(String) COMMENT '基础质量单位',
    `mass_unit_display` Nullable(String) COMMENT '展示质量单位',
    `harvesting_time` Nullable(DateTime) COMMENT '收获时间',
    `harvesting_person` Nullable(String) COMMENT '收获人员',
    `plate_id` Nullable(String) COMMENT '所在板ID',
    `well` Nullable(String) COMMENT '所在孔号',
    `storage_location` Nullable(String) COMMENT '存储位置',
    `project_id` Nullable(String) COMMENT '项目ID',
    `project_no` Nullable(String) COMMENT '项目编号',
    `mw` Nullable(Decimal(10,4)) COMMENT 'mw',
    `pi` Nullable(Decimal(10,4)) COMMENT 'pi',
    `ec` Nullable(Decimal(10,4)) COMMENT 'ec',
    `creator` String COMMENT '创建人',
    `created_time` Nullable(DateTime) COMMENT '创建时间',
    `is_deleted` Nullable(UInt8) COMMENT '是否删除：0-否，1-是',
    `deleted_time` Nullable(DateTime) COMMENT '删除时间',
    `updater` Nullable(String) COMMENT '更新人',
    `updated_time` Nullable(DateTime) COMMENT '更新时间',
    `deleter` Nullable(String) COMMENT '删除人',
    `source_species` Nullable(String) COMMENT '来源物种',
    `organ_tissue_type` Nullable(String) COMMENT '器官/组织类型',
    `sample_morphology` Nullable(String) COMMENT '样本形态特征',
    `external_id` Nullable(String) COMMENT '外部标识码',
    `storage_condition` Nullable(String) COMMENT '储存条件',
    `storage_method` Nullable(String) COMMENT '储存方式',
    `contagious` Nullable(String) COMMENT '有无传染性（未知=0,无=1,有=2）',
    `clinical_typing_info` Nullable(String) COMMENT '临床分型信息',
    `expiry_date` Nullable(String) COMMENT '失效日期',
    `sample_weight` Nullable(String) COMMENT '样本重量',
    `bio_safety_level` Nullable(String) COMMENT '生物安全等级（未知=0, BSL-1=1, BSL-2=2, BSL-3=3）',
    `collection_time` Nullable(String) COMMENT '采集时间',
    `collection_method` Nullable(String) COMMENT '采集方式',
    `receive_time` Nullable(String) COMMENT '接收时间',
    `attachments` Nullable(String) COMMENT '附件',
    `block_id` Nullable(String),
    `run_id` Nullable(String),
    `source_node_id` Nullable(String) COMMENT '来源节点ID',
    `source_node_name` Nullable(String) COMMENT '来源节点名称',
    `source_node_status` Nullable(String) COMMENT '来源节点状态',
    `expiry_status` Nullable(String) COMMENT '过期状态',
    `deprecate_reason` Nullable(String) COMMENT '废弃原因'
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'sample_protein', 'postgres', 'I6Yvg/GD61UjyJsES5Q') COMMENT '蛋白样本信息表';


-- 源表：public.sds_page
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_sds_page
(
    `id` String,
    `lane` Nullable(Int32),
    `barcode` Nullable(String),
    `product_name` Nullable(String),
    `purity` Nullable(Decimal(5,2)),
    `run_id` Nullable(String),
    `block_id` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'sds_page', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.serial_number_sequence
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_serial_number_sequence
(
    `id` Int64 COMMENT '主键ID',
    `module_code` String COMMENT '模块',
    `seq_date` String COMMENT '流水日期',
    `seq_value` Int32 COMMENT '流水值',
    `updated_time` DateTime COMMENT '修改日期'
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'serial_number_sequence', 'postgres', 'I6Yvg/GD61UjyJsES5Q') COMMENT '流水号表';


-- 源表：public.silver_layer_ai_seq_screening
CREATE TABLE IF NOT EXISTS workflow_prod.silver_layer_ai_seq_screening
(
    `id` String,
    `antigen_no` Nullable(String),
    `raw_clonotype_id` Nullable(String),
    `barcode` Nullable(String),
    `cdr1_range_igh` Nullable(String),
    `cdr1_range_igk` Nullable(String),
    `cdr1_range_igl` Nullable(String),
    `cdr2_range_igh` Nullable(String),
    `cdr2_range_igk` Nullable(String),
    `cdr2_range_igl` Nullable(String),
    `cdr3_range_igh` Nullable(String),
    `cdr3_range_igk` Nullable(String),
    `cdr3_range_igl` Nullable(String),
    `merged_aa_igh` Nullable(String),
    `merged_aa_igk` Nullable(String),
    `merged_aa_igl` Nullable(String),
    `frequency` Nullable(String),
    `proportion` Nullable(String),
    `antibody_id` Nullable(String),
    `sequencing_batch` Nullable(String),
    `run_id` Nullable(String),
    `block_id` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'silver_layer_ai_seq_screening', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.silver_layer_bcr_sequencing
CREATE TABLE IF NOT EXISTS workflow_prod.silver_layer_bcr_sequencing
(
    `id` String,
    `sequencing_batch` Nullable(String),
    `antigen_no` Nullable(String),
    `animal_no` Nullable(String),
    `sorting_time` Nullable(String),
    `library_construction_time` Nullable(String),
    `library_construction_quality_report` Nullable(String),
    `bcr_sequencing_provider` Nullable(String),
    `raw_data_size` Nullable(String),
    `storage_path` Nullable(String),
    `md5` Nullable(String),
    `sequencing_report_time` Nullable(String),
    `sequencing_report` Nullable(String),
    `filtered_contig` Nullable(String),
    `clonoypes` Nullable(String),
    `run_id` Nullable(String),
    `block_id` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'silver_layer_bcr_sequencing', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.silver_layer_bli_testing
CREATE TABLE IF NOT EXISTS workflow_prod.silver_layer_bli_testing
(
    `id` String,
    `antigen_no` Nullable(String),
    `bli_batch` Nullable(String),
    `loading_sample_id` Nullable(String),
    `kd` Nullable(String),
    `ka` Nullable(String),
    `kdis` Nullable(String),
    `response` Nullable(String),
    `full_r_2` Nullable(String),
    `run_id` Nullable(String),
    `block_id` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'silver_layer_bli_testing', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.silver_layer_custom_table
CREATE TABLE IF NOT EXISTS workflow_prod.silver_layer_custom_table
(
    `id` String,
    `c1` Nullable(String),
    `c2` Nullable(String),
    `c3` Nullable(String),
    `c4` Nullable(String),
    `c5` Nullable(String),
    `c6` Nullable(String),
    `c7` Nullable(String),
    `c8` Nullable(String),
    `c9` Nullable(String),
    `c10` Nullable(String),
    `run_id` Nullable(String),
    `block_id` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'silver_layer_custom_table', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.silver_layer_experiment
CREATE TABLE IF NOT EXISTS workflow_prod.silver_layer_experiment
(
    `experiment_id` String COMMENT '实验唯一ID',
    `experiment_no` String COMMENT '实验编号',
    `experiment_name` String COMMENT '实验名称',
    `description` Nullable(String) COMMENT '实验描述',
    `project_id` String COMMENT '关联项目ID',
    `experiment_type` Int16 COMMENT '实验类型：0未知 1DNA测序 2RNA分析 3质谱分析 4细胞实验 5生信分析',
    `status` Int16 COMMENT '实验状态：0未知 1准备中 2进行中 3已完成 4已终止',
    `user_id` String COMMENT '操作人ID',
    `sample_ids` Array(String) COMMENT '关联样本ID列表',
    `device_used` Array(String) COMMENT '主要仪器设备列表',
    `start_date` Nullable(Date) COMMENT '实验开始日期',
    `end_date` Nullable(Date) COMMENT '实际结束日期',
    `report` Nullable(String) COMMENT '实验报告',
    `create_time` DateTime COMMENT '创建时间（上海时区）',
    `update_time` DateTime COMMENT '最后更新时间（上海时区）',
    `engine_instance_id` Nullable(String) COMMENT '引擎流程实例ID',
    `creator` Nullable(String) COMMENT '创建人',
    `updater` Nullable(String) COMMENT '修改人',
    `deleter` Nullable(String) COMMENT '删除人',
    `is_deleted` Nullable(UInt8) COMMENT '是否删除：0-否，1-是',
    `deleted_time` Nullable(DateTime) COMMENT '删除时间',
    `workflow_template_id` String COMMENT '业务流模板ID',
    `start_time` Nullable(DateTime),
    `end_time` Nullable(DateTime),
    `aborted_reason` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'silver_layer_experiment', 'postgres', 'I6Yvg/GD61UjyJsES5Q') COMMENT '实验实体表';


-- 源表：public.silver_layer_expression_and_purification
CREATE TABLE IF NOT EXISTS workflow_prod.silver_layer_expression_and_purification
(
    `id` String,
    `antibody_name` Nullable(String),
    `plate_id` Nullable(String),
    `well_id` Nullable(String),
    `expression_cell` Nullable(String),
    `expression_volume` Nullable(Decimal(15,4)),
    `antibody_concentration` Nullable(Decimal(15,4)),
    `volume` Nullable(Decimal(15,4)),
    `total_amount` Nullable(Decimal(15,4)),
    `titer` Nullable(Decimal(15,4)),
    `yield` Nullable(Decimal(15,4)),
    `buffer` Nullable(String),
    `transfection_date` Nullable(DateTime),
    `purification_date` Nullable(DateTime),
    `batch_number` Nullable(String),
    `run_id` Nullable(String),
    `block_id` Nullable(String),
    `transfection_batch` Nullable(String) COMMENT '转染批次'
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'silver_layer_expression_and_purification', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.silver_layer_facs_sorting
CREATE TABLE IF NOT EXISTS workflow_prod.silver_layer_facs_sorting
(
    `id` String,
    `antigen_no` Nullable(String),
    `animal_no` Nullable(String),
    `sorting_time` Nullable(String),
    `facs_record` Nullable(String),
    `sorting_reagents` Nullable(String),
    `cell_viability_activity_assay` Nullable(String),
    `target_cell_purity` Nullable(String),
    `run_id` Nullable(String),
    `block_id` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'silver_layer_facs_sorting', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.silver_layer_ic50_testing
CREATE TABLE IF NOT EXISTS workflow_prod.silver_layer_ic50_testing
(
    `id` String,
    `sample_name` Nullable(String),
    `ec50` Nullable(Decimal(15,4)),
    `span` Nullable(Decimal(15,4)),
    `attachment` Nullable(String),
    `run_id` Nullable(String),
    `block_id` Nullable(String),
    `detection_time` Nullable(DateTime),
    `detection_batch` Nullable(String) COMMENT '检测批次'
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'silver_layer_ic50_testing', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.silver_layer_immunization_test_bleed
CREATE TABLE IF NOT EXISTS workflow_prod.silver_layer_immunization_test_bleed
(
    `id` String,
    `antigen_no` Nullable(String),
    `immunogen` Nullable(String),
    `animal_no` Nullable(String),
    `strain` Nullable(String),
    `route` Nullable(String),
    `adjuvant` Nullable(String),
    `dosage` Nullable(String),
    `immunization1` Nullable(String),
    `immunization2` Nullable(String),
    `immunization3` Nullable(String),
    `immunization4` Nullable(String),
    `immunization5` Nullable(String),
    `immunization6` Nullable(String),
    `test_bleed_date_2` Nullable(String),
    `test_bleed_date_3` Nullable(String),
    `test_bleed_date_4` Nullable(String),
    `test_bleed_date_5` Nullable(String),
    `serum_titer_assay` Nullable(String),
    `spleen` Nullable(String),
    `run_id` Nullable(String),
    `block_id` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'silver_layer_immunization_test_bleed', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.silver_layer_in_vitro_testing
CREATE TABLE IF NOT EXISTS workflow_prod.silver_layer_in_vitro_testing
(
    `id` String,
    `antigen_no` Nullable(String),
    `antibody_id` Nullable(String),
    `assay_batch` Nullable(String),
    `cell_binding_assay_time` Nullable(String),
    `cell_binding_ec50` Nullable(String),
    `cell_binding_span` Nullable(String),
    `non_specific_binding_assay_time` Nullable(String),
    `non_specific_binding_mfi` Nullable(String),
    `cell_function_assay_time` Nullable(String),
    `cell_function_ec50` Nullable(String),
    `cell_function_span` Nullable(String),
    `run_id` Nullable(String),
    `block_id` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'silver_layer_in_vitro_testing', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.silver_layer_molecule_chain_info
CREATE TABLE IF NOT EXISTS workflow_prod.silver_layer_molecule_chain_info
(
    `id` String,
    `molecule_name` Nullable(String),
    `chain_name` Nullable(String),
    `light_chain_subtype` Nullable(String),
    `chain_type` Nullable(String),
    `sequence` Nullable(String),
    `variable_region_aa_seq` Nullable(String),
    `constant_region_tag_aa_seq` Nullable(String),
    `extinction_coefficient` Nullable(Decimal(10,6)),
    `stock_vector_name` Nullable(String),
    `stock_vector_no` Nullable(String),
    `optimized_species` Nullable(String),
    `start_codon_seq` Nullable(String),
    `start_codon_dna_seq` Nullable(String),
    `variable_region_dna_seq` Nullable(String),
    `constant_region_tag_dna_seq` Nullable(String),
    `plasmid_name` Nullable(String),
    `signal_peptide_aa_seq` Nullable(String),
    `signal_peptide_dna_seq` Nullable(String),
    `kozak_seq` Nullable(String),
    `target_gene_full_aa_seq` Nullable(String),
    `target_gene_full_dna_seq` Nullable(String),
    `cloning_enzyme` Nullable(String),
    `linear_vector_enzyme_site_size` Nullable(String),
    `pcr_size_bp` Nullable(Int32),
    `resistance` Nullable(String),
    `run_id` Nullable(String),
    `block_id` Nullable(String),
    `sequence_length` Nullable(Int32),
    `sequence_for_synthesis` Nullable(String),
    `plasmid_sequence` Nullable(String),
    `plasmid_map` Nullable(String),
    `sequencing_batch` Nullable(String),
    `homology_arm_f` Nullable(String),
    `homology_arm_r` Nullable(String),
    `antigen_no` Nullable(String) COMMENT '抗原编号',
    `design_batch` Nullable(String) COMMENT '改造批次'
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'silver_layer_molecule_chain_info', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.silver_layer_primer_return_info
CREATE TABLE IF NOT EXISTS workflow_prod.silver_layer_primer_return_info
(
    `id` String,
    `primer_return_table` Nullable(String),
    `synthesis_batch_no` Nullable(String),
    `target_conc` Nullable(Decimal(12,4)),
    `add_water_vol` Nullable(Decimal(12,4)),
    `run_id` Nullable(String),
    `block_id` Nullable(String),
    `return_time` Nullable(DateTime),
    `antigen_no` Nullable(String) COMMENT '抗原编号'
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'silver_layer_primer_return_info', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.silver_layer_protocol
CREATE TABLE IF NOT EXISTS workflow_prod.silver_layer_protocol
(
    `protocol_id` String COMMENT '实验流程编号',
    `experiment_id` String COMMENT '实验唯一ID',
    `title` String COMMENT '标题',
    `description` Nullable(String) COMMENT '实验流程描述',
    `steps` Array(String) COMMENT '实验步骤',
    `status` Nullable(String) COMMENT '状态',
    `p_protocol_ids` Array(String) COMMENT '父节点流程编号',
    `version` String COMMENT '版本号',
    `metadata` Nullable(String) COMMENT '扩展元数据(JSON)',
    `creator` Nullable(String) COMMENT '创建人',
    `updater` Nullable(String) COMMENT '更新人',
    `create_time` DateTime COMMENT '创建时间（上海时区）',
    `update_time` DateTime COMMENT '最后更新时间（上海时区）',
    `task_status` Nullable(String) COMMENT '任务状态',
    `task_temporary_data` Nullable(String),
    `run_id` Nullable(String),
    `assign` Nullable(String),
    `engine_task_id` Nullable(String),
    `workflow_node_id` Nullable(String) COMMENT '业务流节点ID',
    `run_message` Nullable(String) COMMENT '运行消息',
    `end_time` Nullable(DateTime) COMMENT '结束时间',
    `engine_instance_id` Nullable(String) COMMENT '流程实例ID',
    `task_def_key` Nullable(String) COMMENT 'BPMN 节点 KEY',
    `revision` Int32,
    `node_execution_type` Nullable(String),
    `actual_execution_mode` Nullable(String),
    `run_start_time` Nullable(DateTime)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'silver_layer_protocol', 'postgres', 'I6Yvg/GD61UjyJsES5Q') COMMENT '实验流程实体表';


-- 源表：public.silver_layer_rec_plasmid_const
CREATE TABLE IF NOT EXISTS workflow_prod.silver_layer_rec_plasmid_const
(
    `id` String,
    `chain_gene_name` Nullable(String),
    `single_clone_culture_temp` Nullable(Decimal(15,2)),
    `single_clone_culture_time` Nullable(Decimal(15,2)),
    `bacterial_culture_temp` Nullable(Decimal(15,2)),
    `bacterial_culture_time` Nullable(Decimal(15,2)),
    `bacterial_culture_speed` Nullable(Decimal(15,2)),
    `bacterial_culture_volume` Nullable(Decimal(15,2)),
    `run_id` Nullable(String),
    `block_id` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'silver_layer_rec_plasmid_const', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.silver_layer_record_cell_count
CREATE TABLE IF NOT EXISTS workflow_prod.silver_layer_record_cell_count
(
    `id` String COMMENT '主键ID',
    `barcode` Nullable(String) COMMENT '条形码',
    `sample_name` Nullable(String) COMMENT '样本名称',
    `species` Nullable(String) COMMENT '物种',
    `viability` Nullable(Decimal(5,2)) COMMENT '活率（百分比）',
    `total_cell_concentration` Nullable(Decimal(15,2)) COMMENT '总细胞浓度',
    `live_cell_concentration` Nullable(Decimal(15,2)) COMMENT '活细胞浓度',
    `diameter` Nullable(Decimal(8,3)) COMMENT '直径（微米）',
    `testing_time` Nullable(DateTime) COMMENT '检测时间',
    `creator` Nullable(String) COMMENT '创建人',
    `created_time` Nullable(DateTime),
    `updater` Nullable(String),
    `updated_time` Nullable(DateTime),
    `is_deleted` Nullable(UInt8),
    `deleted_time` Nullable(DateTime),
    `deleter` Nullable(String),
    `block_id` Nullable(String),
    `run_id` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'silver_layer_record_cell_count', 'postgres', 'I6Yvg/GD61UjyJsES5Q') COMMENT '细胞计数信息表';


-- 源表：public.silver_layer_record_centrifuge
CREATE TABLE IF NOT EXISTS workflow_prod.silver_layer_record_centrifuge
(
    `id` String COMMENT '主键ID',
    `temperature` Nullable(Decimal(5,2)) COMMENT '离心温度（℃）',
    `speed` Nullable(Decimal(10,2)) COMMENT '转速（rpm）',
    `centrifugal_force` Nullable(Decimal(5,2)) COMMENT '离心力（xg）',
    `duration` Nullable(Decimal(10,2)) COMMENT '离心时间（分钟）',
    `creator` Nullable(String) COMMENT '创建人',
    `created_time` Nullable(DateTime),
    `updater` Nullable(String),
    `updated_time` Nullable(DateTime),
    `is_deleted` Nullable(UInt8),
    `deleted_time` Nullable(DateTime),
    `deleter` Nullable(String),
    `run_id` Nullable(String),
    `block_id` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'silver_layer_record_centrifuge', 'postgres', 'I6Yvg/GD61UjyJsES5Q') COMMENT '离心机运行记录表';


-- 源表：public.silver_layer_record_culture
CREATE TABLE IF NOT EXISTS workflow_prod.silver_layer_record_culture
(
    `id` String COMMENT '主键ID',
    `speed` Nullable(Decimal(5,2)) COMMENT '转速（rpm）',
    `duration` Nullable(Decimal(5,2)) COMMENT '时间（h）',
    `temperature` Nullable(Decimal(5,2)) COMMENT '温度（℃）',
    `humidity` Nullable(Decimal(5,2)) COMMENT '湿度（%）',
    `co2_concentration` Nullable(Decimal(5,2)) COMMENT 'CO2浓度（%）',
    `creator` Nullable(String) COMMENT '创建人',
    `created_time` Nullable(DateTime),
    `updater` Nullable(String),
    `updated_time` Nullable(DateTime),
    `is_deleted` Nullable(UInt8),
    `deleted_time` Nullable(DateTime),
    `deleter` Nullable(String),
    `block_id` Nullable(String),
    `run_id` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'silver_layer_record_culture', 'postgres', 'I6Yvg/GD61UjyJsES5Q') COMMENT '培养记录表';


-- 源表：public.silver_layer_record_microplate_assay
CREATE TABLE IF NOT EXISTS workflow_prod.silver_layer_record_microplate_assay
(
    `id` String COMMENT '主键ID',
    `barcode` Nullable(String) COMMENT '条形码',
    `sample_name` Nullable(String) COMMENT '样本名称',
    `plate` Nullable(String) COMMENT '孔板',
    `well` Nullable(String) COMMENT '孔位',
    `od` Nullable(Decimal(15,4)) COMMENT '吸光度值',
    `testing_time` Nullable(DateTime) COMMENT '检测时间',
    `creator` Nullable(String) COMMENT '创建人',
    `created_time` Nullable(DateTime),
    `updater` Nullable(String),
    `updated_time` Nullable(DateTime),
    `is_deleted` Nullable(UInt8),
    `deleted_time` Nullable(DateTime),
    `deleter` Nullable(String),
    `run_id` Nullable(String),
    `block_id` Nullable(String),
    `testing_batch` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'silver_layer_record_microplate_assay', 'postgres', 'I6Yvg/GD61UjyJsES5Q') COMMENT '酶标仪检测信息表';


-- 源表：public.silver_layer_record_move_sample
CREATE TABLE IF NOT EXISTS workflow_prod.silver_layer_record_move_sample
(
    `id` String COMMENT '主键ID',
    `sample_name` Nullable(String) COMMENT '样本名称',
    `source_plate` Nullable(String) COMMENT '源板',
    `source_well` Nullable(String) COMMENT '源孔位',
    `target_plate` Nullable(String) COMMENT '目标板',
    `target_well` Nullable(String) COMMENT '目标孔位',
    `product_name` Nullable(String) COMMENT '产物名称',
    `block_id` Nullable(String),
    `run_id` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'silver_layer_record_move_sample', 'postgres', 'I6Yvg/GD61UjyJsES5Q') COMMENT '转孔记录表';


-- 源表：public.silver_layer_role
CREATE TABLE IF NOT EXISTS workflow_prod.silver_layer_role
(
    `id` String COMMENT '主键ID',
    `role_name` String COMMENT '角色名称',
    `role_status` Int16 COMMENT '角色状态',
    `creator` String COMMENT '创建人',
    `created_time` Nullable(DateTime) COMMENT '创建时间',
    `is_deleted` Nullable(UInt8) COMMENT '是否删除：0-否，1-是',
    `deleted_time` Nullable(DateTime) COMMENT '删除时间',
    `updater` Nullable(String) COMMENT '更新人',
    `updated_time` Nullable(DateTime) COMMENT '更新时间',
    `deleter` Nullable(String) COMMENT '删除人'
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'silver_layer_role', 'postgres', 'I6Yvg/GD61UjyJsES5Q') COMMENT '角色表';


-- 源表：public.silver_layer_sample_antigen
CREATE TABLE IF NOT EXISTS workflow_prod.silver_layer_sample_antigen
(
    `sample_id` String COMMENT '主键ID',
    `source` Nullable(String) COMMENT '来源',
    `current_status` String COMMENT '状态',
    `barcode` String COMMENT '条形码',
    `sample_name` String COMMENT '抗原编号',
    `sample_type` String COMMENT '样本类型',
    `concentration` Nullable(Decimal(15,6)) COMMENT '浓度值',
    `concentration_unit` Nullable(String) COMMENT '基础浓度单位',
    `concentration_unit_display` Nullable(String) COMMENT '展示浓度单位',
    `sample_volume` Nullable(Decimal(15,6)) COMMENT '体积值',
    `volume_unit` Nullable(String) COMMENT '基础体积单位',
    `volume_unit_display` Nullable(String) COMMENT '展示体积单位',
    `mass` Nullable(Decimal(15,6)) COMMENT '质量值',
    `mass_unit` Nullable(String) COMMENT '基础质量单位',
    `mass_unit_display` Nullable(String) COMMENT '展示质量单位',
    `harvesting_time` Nullable(DateTime) COMMENT '收获时间',
    `harvesting_person` Nullable(String) COMMENT '收获人员',
    `plate_id` Nullable(String) COMMENT '所在板ID',
    `well` Nullable(String) COMMENT '所在孔号',
    `storage_location` Nullable(String) COMMENT '存储位置',
    `project_id` Nullable(String) COMMENT '项目ID',
    `project_no` Nullable(String) COMMENT '项目编号',
    `antigen_code` Nullable(String) COMMENT '名称',
    `antigen_cn` Nullable(String) COMMENT '中文名称',
    `antigen_description` Nullable(String) COMMENT '抗原简介',
    `antigen_pro_info` Nullable(String) COMMENT '抗原采购信息',
    `pro_application_time` Nullable(String) COMMENT '采购申请时间',
    `antigens_sequence` Nullable(String) COMMENT '免疫抗原序列',
    `benchmark_antibody1_no` Nullable(String) COMMENT 'Benchmark抗体1编号',
    `benchmark_antibody1_name` Nullable(String) COMMENT 'Benchmark抗体1名称',
    `benchmark_antibody1_sequence` Nullable(String) COMMENT 'Benchmark抗体1序列',
    `benchmark_antibody2_no` Nullable(String) COMMENT 'Benchmark抗体2编号',
    `benchmark_antibody2_name` Nullable(String) COMMENT 'Benchmark抗体2名称',
    `benchmark_antibody2_sequence` Nullable(String) COMMENT 'Benchmark抗体2序列',
    `creator` String COMMENT '创建人',
    `created_time` Nullable(DateTime) COMMENT '创建时间',
    `is_deleted` Nullable(UInt8) COMMENT '是否删除：0-否，1-是',
    `deleted_time` Nullable(DateTime) COMMENT '删除时间',
    `updater` Nullable(String) COMMENT '更新人',
    `updated_time` Nullable(DateTime) COMMENT '更新时间',
    `deleter` Nullable(String) COMMENT '删除人',
    `source_species` Nullable(String) COMMENT '来源物种',
    `organ_tissue_type` Nullable(String) COMMENT '器官/组织类型',
    `sample_morphology` Nullable(String) COMMENT '样本形态特征',
    `external_id` Nullable(String) COMMENT '外部标识码',
    `storage_condition` Nullable(String) COMMENT '储存条件',
    `storage_method` Nullable(String) COMMENT '储存方式',
    `contagious` Nullable(String) COMMENT '有无传染性（未知=0,无=1,有=2）',
    `clinical_typing_info` Nullable(String) COMMENT '临床分型信息',
    `expiry_date` Nullable(String) COMMENT '失效日期',
    `sample_weight` Nullable(String) COMMENT '样本重量',
    `bio_safety_level` Nullable(String) COMMENT '生物安全等级（未知=0, BSL-1=1, BSL-2=2, BSL-3=3）',
    `collection_time` Nullable(String) COMMENT '采集时间',
    `collection_method` Nullable(String) COMMENT '采集方式',
    `receive_time` Nullable(String) COMMENT '接收时间',
    `attachments` Nullable(String) COMMENT '附件',
    `deprecate_reason` Nullable(String),
    `run_id` Nullable(String),
    `block_id` Nullable(String),
    `source_node_name` Nullable(String),
    `source_node_status` Nullable(String),
    `expiry_status` Nullable(String),
    `source_node_id` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'silver_layer_sample_antigen', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.silver_layer_sample_cell
CREATE TABLE IF NOT EXISTS workflow_prod.silver_layer_sample_cell
(
    `sample_id` String COMMENT '主键ID',
    `source` Nullable(String) COMMENT '来源',
    `current_status` Nullable(String) COMMENT '状态',
    `barcode` Nullable(String) COMMENT '条形码',
    `sample_name` Nullable(String) COMMENT '样本名称',
    `sample_type` Nullable(String) COMMENT '样本类型',
    `concentration` Nullable(Decimal(15,6)) COMMENT '浓度值',
    `concentration_unit` Nullable(String) COMMENT '基础浓度单位',
    `concentration_unit_display` Nullable(String) COMMENT '展示浓度单位',
    `sample_volume` Nullable(Decimal(15,6)) COMMENT '体积值',
    `volume_unit` Nullable(String) COMMENT '基础体积单位',
    `volume_unit_display` Nullable(String) COMMENT '展示体积单位',
    `mass` Nullable(Decimal(15,6)) COMMENT '质量值',
    `mass_unit` Nullable(String) COMMENT '基础质量单位',
    `mass_unit_display` Nullable(String) COMMENT '展示质量单位',
    `harvesting_time` Nullable(DateTime) COMMENT '收获时间',
    `harvesting_person` Nullable(String) COMMENT '收获人员',
    `plate_id` Nullable(String) COMMENT '所在板ID',
    `well` Nullable(String) COMMENT '所在孔号',
    `storage_location` Nullable(String) COMMENT '存储位置',
    `project_id` Nullable(String) COMMENT '项目ID',
    `project_no` Nullable(String) COMMENT '项目编号',
    `species` Nullable(String) COMMENT '物种',
    `passage_no` Nullable(Int32) COMMENT '传代次数',
    `doubling_time` Nullable(Decimal(10,2)) COMMENT '倍增时间（小时）',
    `viability` Nullable(Decimal(15,2)) COMMENT '活率（百分比）',
    `total_cell_concentration` Nullable(Decimal(15,2)) COMMENT '总细胞浓度',
    `live_cell_concentration` Nullable(Decimal(15,2)) COMMENT '活细胞浓度',
    `diameter` Nullable(Decimal(8,3)) COMMENT '直径（微米）',
    `creator` String COMMENT '创建人',
    `created_time` Nullable(DateTime) COMMENT '创建时间',
    `is_deleted` Nullable(UInt8) COMMENT '是否删除：0-否，1-是',
    `deleted_time` Nullable(DateTime) COMMENT '删除时间',
    `updater` Nullable(String) COMMENT '更新人',
    `updated_time` Nullable(DateTime) COMMENT '更新时间',
    `deleter` Nullable(String) COMMENT '删除人',
    `source_species` Nullable(String) COMMENT '来源物种',
    `organ_tissue_type` Nullable(String) COMMENT '器官/组织类型',
    `sample_morphology` Nullable(String) COMMENT '样本形态特征',
    `external_id` Nullable(String) COMMENT '外部标识码',
    `storage_condition` Nullable(String) COMMENT '储存条件',
    `storage_method` Nullable(String) COMMENT '储存方式',
    `contagious` Nullable(String) COMMENT '有无传染性（未知=0,无=1,有=2）',
    `clinical_typing_info` Nullable(String) COMMENT '临床分型信息',
    `expiry_date` Nullable(String) COMMENT '失效日期',
    `sample_weight` Nullable(String) COMMENT '样本重量',
    `bio_safety_level` Nullable(String) COMMENT '生物安全等级（未知=0, BSL-1=1, BSL-2=2, BSL-3=3）',
    `collection_time` Nullable(String) COMMENT '采集时间',
    `collection_method` Nullable(String) COMMENT '采集方式',
    `receive_time` Nullable(String) COMMENT '接收时间',
    `attachments` Nullable(String) COMMENT '附件',
    `run_id` Nullable(String),
    `block_id` Nullable(String),
    `source_node_name` Nullable(String) COMMENT '来源节点名称',
    `source_node_status` Nullable(String) COMMENT '来源节点状态',
    `expiry_status` Nullable(String) COMMENT '过期状态',
    `deprecate_reason` Nullable(String) COMMENT '废弃原因',
    `source_node_id` Nullable(String) COMMENT '来源节点ID'
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'silver_layer_sample_cell', 'postgres', 'I6Yvg/GD61UjyJsES5Q') COMMENT '细胞样本信息表';


-- 源表：public.silver_layer_sample_plasmid
CREATE TABLE IF NOT EXISTS workflow_prod.silver_layer_sample_plasmid
(
    `sample_id` String COMMENT '主键ID',
    `source` Nullable(String) COMMENT '来源',
    `current_status` Nullable(String) COMMENT '状态',
    `barcode` Nullable(String) COMMENT '条形码',
    `sample_name` Nullable(String) COMMENT '样本名称',
    `sample_type` Nullable(String) COMMENT '样本类型',
    `concentration` Nullable(Decimal(15,6)) COMMENT '浓度值',
    `concentration_unit` Nullable(String) COMMENT '基础浓度单位',
    `concentration_unit_display` Nullable(String) COMMENT '展示浓度单位',
    `sample_volume` Nullable(Decimal(15,6)) COMMENT '体积值',
    `volume_unit` Nullable(String) COMMENT '基础体积单位',
    `volume_unit_display` Nullable(String) COMMENT '展示体积单位',
    `mass` Nullable(Decimal(15,6)) COMMENT '质量值',
    `mass_unit` Nullable(String) COMMENT '基础质量单位',
    `mass_unit_display` Nullable(String) COMMENT '展示质量单位',
    `harvesting_time` Nullable(DateTime) COMMENT '收获时间',
    `harvesting_person` Nullable(String) COMMENT '收获人员',
    `plate_id` Nullable(String) COMMENT '所在板ID',
    `well` Nullable(String) COMMENT '所在孔号',
    `storage_location` Nullable(String) COMMENT '存储位置',
    `project_id` Nullable(String) COMMENT '项目ID',
    `project_no` Nullable(String) COMMENT '项目编号',
    `a260_280` Nullable(Decimal(15,2)) COMMENT 'A260/280比值',
    `a260_230` Nullable(Decimal(15,2)) COMMENT 'A260/230比值',
    `creator` String COMMENT '创建人',
    `created_time` Nullable(DateTime) COMMENT '创建时间',
    `is_deleted` Nullable(UInt8) COMMENT '是否删除：0-否，1-是',
    `deleted_time` Nullable(DateTime) COMMENT '删除时间',
    `updater` Nullable(String) COMMENT '更新人',
    `updated_time` Nullable(DateTime) COMMENT '更新时间',
    `deleter` Nullable(String) COMMENT '删除人',
    `source_species` Nullable(String) COMMENT '来源物种',
    `organ_tissue_type` Nullable(String) COMMENT '器官/组织类型',
    `sample_morphology` Nullable(String) COMMENT '样本形态特征',
    `external_id` Nullable(String) COMMENT '外部标识码',
    `storage_condition` Nullable(String) COMMENT '储存条件',
    `storage_method` Nullable(String) COMMENT '储存方式',
    `contagious` Nullable(String) COMMENT '有无传染性（未知=0,无=1,有=2）',
    `clinical_typing_info` Nullable(String) COMMENT '临床分型信息',
    `expiry_date` Nullable(String) COMMENT '失效日期',
    `sample_weight` Nullable(String) COMMENT '样本重量',
    `bio_safety_level` Nullable(String) COMMENT '生物安全等级（未知=0, BSL-1=1, BSL-2=2, BSL-3=3）',
    `collection_time` Nullable(String) COMMENT '采集时间',
    `collection_method` Nullable(String) COMMENT '采集方式',
    `receive_time` Nullable(String) COMMENT '接收时间',
    `attachments` Nullable(String) COMMENT '附件',
    `block_id` Nullable(String),
    `run_id` Nullable(String),
    `source_node_name` Nullable(String) COMMENT '来源节点名称',
    `source_node_status` Nullable(String) COMMENT '来源节点状态',
    `expiry_status` Nullable(String) COMMENT '过期状态',
    `deprecate_reason` Nullable(String) COMMENT '废弃原因',
    `source_node_id` Nullable(String) COMMENT '来源节点ID',
    `batch_no` Nullable(String),
    `molecule_name` Nullable(String),
    `chain_name` Nullable(String),
    `chain_type` Nullable(String),
    `is_correct` Nullable(String),
    `sanger_result` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'silver_layer_sample_plasmid', 'postgres', 'I6Yvg/GD61UjyJsES5Q') COMMENT '质粒样本信息表';


-- 源表：public.silver_layer_sample_protein
CREATE TABLE IF NOT EXISTS workflow_prod.silver_layer_sample_protein
(
    `sample_id` String COMMENT '主键ID',
    `source` Nullable(String) COMMENT '来源',
    `current_status` Nullable(String) COMMENT '状态',
    `barcode` Nullable(String) COMMENT '条形码',
    `sample_name` Nullable(String) COMMENT '样本名称',
    `sample_type` Nullable(String) COMMENT '样本类型',
    `concentration` Nullable(Decimal(15,6)) COMMENT '浓度值',
    `concentration_unit` Nullable(String) COMMENT '基础浓度单位',
    `concentration_unit_display` Nullable(String) COMMENT '展示浓度单位',
    `sample_volume` Nullable(Decimal(15,6)) COMMENT '体积值',
    `volume_unit` Nullable(String) COMMENT '基础体积单位',
    `volume_unit_display` Nullable(String) COMMENT '展示体积单位',
    `mass` Nullable(Decimal(15,6)) COMMENT '质量值',
    `mass_unit` Nullable(String) COMMENT '基础质量单位',
    `mass_unit_display` Nullable(String) COMMENT '展示质量单位',
    `harvesting_time` Nullable(DateTime) COMMENT '收获时间',
    `harvesting_person` Nullable(String) COMMENT '收获人员',
    `plate_id` Nullable(String) COMMENT '所在板ID',
    `well` Nullable(String) COMMENT '所在孔号',
    `storage_location` Nullable(String) COMMENT '存储位置',
    `project_id` Nullable(String) COMMENT '项目ID',
    `project_no` Nullable(String) COMMENT '项目编号',
    `mw` Nullable(Decimal(10,4)) COMMENT 'mw',
    `pi` Nullable(Decimal(10,4)) COMMENT 'pi',
    `ec` Nullable(Decimal(10,4)) COMMENT 'ec',
    `creator` String COMMENT '创建人',
    `created_time` Nullable(DateTime) COMMENT '创建时间',
    `is_deleted` Nullable(UInt8) COMMENT '是否删除：0-否，1-是',
    `deleted_time` Nullable(DateTime) COMMENT '删除时间',
    `updater` Nullable(String) COMMENT '更新人',
    `updated_time` Nullable(DateTime) COMMENT '更新时间',
    `deleter` Nullable(String) COMMENT '删除人',
    `source_species` Nullable(String) COMMENT '来源物种',
    `organ_tissue_type` Nullable(String) COMMENT '器官/组织类型',
    `sample_morphology` Nullable(String) COMMENT '样本形态特征',
    `external_id` Nullable(String) COMMENT '外部标识码',
    `storage_condition` Nullable(String) COMMENT '储存条件',
    `storage_method` Nullable(String) COMMENT '储存方式',
    `contagious` Nullable(String) COMMENT '有无传染性（未知=0,无=1,有=2）',
    `clinical_typing_info` Nullable(String) COMMENT '临床分型信息',
    `expiry_date` Nullable(String) COMMENT '失效日期',
    `sample_weight` Nullable(String) COMMENT '样本重量',
    `bio_safety_level` Nullable(String) COMMENT '生物安全等级（未知=0, BSL-1=1, BSL-2=2, BSL-3=3）',
    `collection_time` Nullable(String) COMMENT '采集时间',
    `collection_method` Nullable(String) COMMENT '采集方式',
    `receive_time` Nullable(String) COMMENT '接收时间',
    `attachments` Nullable(String) COMMENT '附件',
    `block_id` Nullable(String),
    `run_id` Nullable(String),
    `source_node_name` Nullable(String) COMMENT '来源节点名称',
    `source_node_status` Nullable(String) COMMENT '来源节点状态',
    `expiry_status` Nullable(String) COMMENT '过期状态',
    `deprecate_reason` Nullable(String) COMMENT '废弃原因',
    `source_node_id` Nullable(String) COMMENT '来源节点ID'
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'silver_layer_sample_protein', 'postgres', 'I6Yvg/GD61UjyJsES5Q') COMMENT '蛋白样本信息表';


-- 源表：public.silver_layer_solubility_testing
CREATE TABLE IF NOT EXISTS workflow_prod.silver_layer_solubility_testing
(
    `id` String,
    `testing_batch` Nullable(String),
    `sample_name` Nullable(String),
    `solubility` Nullable(Decimal(15,4)),
    `detection_time` Nullable(DateTime),
    `attachment` Nullable(String),
    `run_id` Nullable(String),
    `block_id` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'silver_layer_solubility_testing', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.silver_layer_sop
CREATE TABLE IF NOT EXISTS workflow_prod.silver_layer_sop
(
    `id` String COMMENT 'Primary Key',
    `sop_code` Nullable(String) COMMENT 'SOP编号',
    `sop_name` Nullable(String) COMMENT 'SOP名称',
    `sop_link` Nullable(String) COMMENT 'SOP链接',
    `block_id` Nullable(String),
    `run_id` Nullable(String),
    `creator` Nullable(String),
    `created_time` Nullable(DateTime),
    `updater` Nullable(String),
    `updated_time` Nullable(DateTime),
    `is_deleted` Nullable(UInt8),
    `deleted_time` Nullable(DateTime),
    `deleter` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'silver_layer_sop', 'postgres', 'I6Yvg/GD61UjyJsES5Q') COMMENT 'SOP信息表';


-- 源表：public.silver_layer_tm_testing
CREATE TABLE IF NOT EXISTS workflow_prod.silver_layer_tm_testing
(
    `id` String,
    `testing_batch` Nullable(String),
    `sample_name` Nullable(String),
    `tm` Nullable(Decimal(15,4)),
    `detection_time` Nullable(DateTime),
    `attachment` Nullable(String),
    `run_id` Nullable(String),
    `block_id` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'silver_layer_tm_testing', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.silver_layer_user
CREATE TABLE IF NOT EXISTS workflow_prod.silver_layer_user
(
    `user_id` String COMMENT '人员ID（唯一标识）',
    `user_name` String COMMENT '姓名',
    `department` Nullable(String) COMMENT '所属部门',
    `user_role` String,
    `role` String COMMENT '角色：研究员/助理/软件测试人员/等',
    `status` String COMMENT '状态：在职/离职',
    `phone` Nullable(String) COMMENT '手机号',
    `email` Nullable(String) COMMENT '邮箱',
    `create_time` DateTime COMMENT '创建时间（上海时区）',
    `update_time` DateTime COMMENT '最后更新时间（上海时区）',
    `password` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'silver_layer_user', 'postgres', 'I6Yvg/GD61UjyJsES5Q') COMMENT '人员实体表';


-- 源表：public.workflow_attachment
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_workflow_attachment
(
    `id` String,
    `attachment` Nullable(String),
    `block_id` Nullable(String),
    `run_id` Nullable(String),
    `creator` Nullable(String),
    `created_time` Nullable(DateTime),
    `updater` Nullable(String),
    `updated_time` Nullable(DateTime),
    `is_deleted` Nullable(UInt8),
    `deleted_time` Nullable(DateTime)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'workflow_attachment', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.workflow_autobio_data
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_workflow_autobio_data
(
    `id` String,
    `table_name` Nullable(String),
    `query_sql` Nullable(String),
    `topic_name` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'workflow_autobio_data', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.workflow_data_job
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_workflow_data_job
(
    `id` String,
    `run_id` Nullable(String),
    `status` Nullable(String),
    `created_time` Nullable(DateTime),
    `statistics` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'workflow_data_job', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.workflow_data_transform_rule
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_workflow_data_transform_rule
(
    `id` String,
    `model_id` Nullable(String),
    `model_feild_key` Nullable(String),
    `table_name` Nullable(String),
    `feild_name` Nullable(String),
    `task_type` Nullable(String),
    `value_method` Nullable(String),
    `transform_rule` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'workflow_data_transform_rule', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.workflow_edge
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_workflow_edge
(
    `id` String COMMENT '主键ID',
    `edge_key` String COMMENT '边名称',
    `template_id` String,
    `source_node_id` String COMMENT 'source 节点ID',
    `source_handle` String COMMENT 'source 连接点ID',
    `target_node_id` String COMMENT 'target 节点ID',
    `target_handle` String COMMENT 'target 连接点ID',
    `data` Nullable(String) COMMENT '业务数据',
    `source` Nullable(String),
    `target` Nullable(String),
    `semantic_type` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'workflow_edge', 'postgres', 'I6Yvg/GD61UjyJsES5Q') COMMENT '工作流模板连线表';


-- 源表：public.workflow_file
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_workflow_file
(
    `id` String,
    `original_file_name` Nullable(String),
    `object_name` Nullable(String),
    `file_type` Nullable(String),
    `bucket` Nullable(String),
    `creator` Nullable(String),
    `created_time` Nullable(DateTime)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'workflow_file', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.workflow_import_template
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_workflow_import_template
(
    `id` String,
    `template_name` Nullable(String),
    `file_id` Nullable(String),
    `model_id` Nullable(String),
    `model_name` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'workflow_import_template', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.workflow_model
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_workflow_model
(
    `id` String,
    `model_name` Nullable(String),
    `model_type` Nullable(String),
    `status` Nullable(String),
    `model_fields` Nullable(String),
    `model_primary_keys` Nullable(String),
    `creator` Nullable(String),
    `created_time` Nullable(DateTime),
    `updater` Nullable(String),
    `updated_time` Nullable(DateTime),
    `is_deleted` Nullable(UInt8),
    `deleted_time` Nullable(DateTime),
    `deleter` Nullable(String),
    `model_group` Nullable(String),
    `model_strategy` Nullable(String),
    `model_icon` Nullable(String),
    `model_tag` Nullable(String),
    `publisher` Nullable(String),
    `model_description` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'workflow_model', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.workflow_model_group
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_workflow_model_group
(
    `id` String,
    `group_name` String,
    `group_color` Nullable(String),
    `group_order` Nullable(Int32)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'workflow_model_group', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.workflow_node
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_workflow_node
(
    `id` String COMMENT '主键ID',
    `node_key` String COMMENT '节点key，唯一值',
    `type` String COMMENT '节点类型(task=任务节点)',
    `task_type` Nullable(String) COMMENT '任务类型(manual=手动，autobio=autobio)',
    `template_id` String COMMENT '模板ID',
    `node_template_id` Nullable(String) COMMENT '业务模板ID',
    `position` Nullable(String) COMMENT '画布信息',
    `data` Nullable(String) COMMENT '业务参数信息'
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'workflow_node', 'postgres', 'I6Yvg/GD61UjyJsES5Q') COMMENT '工作流模板节点信息表';


-- 源表：public.workflow_node_context
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_workflow_node_context
(
    `id` String,
    `experiment_id` Nullable(String),
    `protocol_id` Nullable(String),
    `context_data` String,
    `node_id` Nullable(String),
    `created_time` DateTime,
    `node_template_id` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'workflow_node_context', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.workflow_node_template
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_workflow_node_template
(
    `id` String,
    `template_name` Nullable(String),
    `template_type` Nullable(String),
    `status` Nullable(String),
    `template_group` Nullable(String),
    `blocks` Nullable(String),
    `execution` Nullable(String),
    `created_time` Nullable(DateTime),
    `creator` Nullable(String),
    `updater` Nullable(String),
    `updated_time` Nullable(DateTime),
    `is_deleted` Nullable(UInt8),
    `deleted_time` Nullable(DateTime),
    `deleter` Nullable(String),
    `disable_reason` Nullable(String),
    `publish_time` Nullable(DateTime)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'workflow_node_template', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.workflow_rich_text
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_workflow_rich_text
(
    `id` String,
    `rich_text` Nullable(String),
    `run_id` Nullable(String),
    `block_id` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'workflow_rich_text', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.workflow_sample_tracking
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_workflow_sample_tracking
(
    `id` String,
    `ancestor_id` Nullable(String),
    `descendant_id` Nullable(String),
    `depth` Nullable(Int32)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'workflow_sample_tracking', 'postgres', 'I6Yvg/GD61UjyJsES5Q');


-- 源表：public.workflow_template
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_workflow_template
(
    `id` String COMMENT '主键ID',
    `template_name` String COMMENT '模板名称',
    `status` Int16 COMMENT '模板状态(草稿=0，已发布=1，待审核=2，审核通过=3，审核拒绝=4，废弃=5)',
    `template_group` Nullable(String) COMMENT '工作流模板组',
    `publish_time` Nullable(DateTime) COMMENT '发布时间',
    `remark` Nullable(String) COMMENT '备注',
    `creator` Nullable(String) COMMENT '创建人',
    `created_time` Nullable(DateTime) COMMENT '创建时间',
    `updater` Nullable(String) COMMENT '更新人',
    `updated_time` Nullable(DateTime) COMMENT '更新时间',
    `is_deleted` Nullable(UInt8) COMMENT '是否删除：0-否，1-是',
    `deleted_time` Nullable(DateTime) COMMENT '删除时间',
    `deleter` Nullable(String) COMMENT '删除人',
    `deprecated_reason` Nullable(String)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'workflow_template', 'postgres', 'I6Yvg/GD61UjyJsES5Q') COMMENT '工作流模板表';


-- 源表：public.workflow_textarea
CREATE TABLE IF NOT EXISTS workflow_prod.bronze_layer_workflow_textarea
(
    `id` String,
    `content` Nullable(String),
    `block_id` Nullable(String),
    `run_id` Nullable(String),
    `creator` Nullable(String),
    `created_time` Nullable(DateTime),
    `updater` Nullable(String),
    `updated_time` Nullable(DateTime),
    `is_deleted` Nullable(UInt8),
    `deleted_time` Nullable(DateTime)
)
ENGINE = PostgreSQL('10.10.2.15', 'labillion-workflow', 'workflow_textarea', 'postgres', 'I6Yvg/GD61UjyJsES5Q');

