# -*- coding:utf8 -*-
from selenium.webdriver.common.by import By


searchContractMould = {
        'contract_num_loc' : (By.CSS_SELECTOR,'#search_contract_num + span>input'),   #出租合同号
        'search_address_loc':(By.CSS_SELECTOR,'#search_address + span>input'),
        'breach_num_loc':(By.CSS_SELECTOR,'#search_breach_num +span>input'),  # 违约业绩页面合同号
        'contract_type_loc':'#search_contract_type',  # 业绩类型
        'rent_type_loc':'#search_rent_type',  # 承租类别
        'breach_type_loc':'#search_breach_type',  # 违约类别
        'category_loc':'#search_contract_category',  # 分类
        'search_button_loc' : (By.ID,'search_btn'),   #搜索
        'reset_button_loc':(By.ID,'reset_btn'),#重置
        'tr_contract' : (By.CSS_SELECTOR,'tr[datagrid-row-index="0"]'),#列表页第一行
        'tr2_contract' : (By.CSS_SELECTOR,'tr[datagrid-row-index="1"]'),#列表页第二行
        'contract_num_hefa_loc': (By.CSS_SELECTOR, '#search_other + span>input'),  # 核发排行榜出租合同号
    }
detailAchievementMoudle = {
        'contract_num_loc':(By.CSS_SELECTOR,'#apartment_contract_table td:nth-child(1)>div'),#出租合同号
        'breach_num_loc':(By.CSS_SELECTOR,'#loss_info td:nth-child(2)>div'),#违约合同号
        'resave_loc':(By.ID,'form_resave'),
        'audit_button_loc':(By.ID,'current_audit_general_button'),#审核
        'save_button_loc':(By.ID,'form_save'),  # 保存
        'fanshen_button_loc':(By.ID,'current_audit_general_button') , # 反审
        'cancel_button_loc':(By.ID,'cancel_button'),  # 取消
        'contract_audit_content':(By.ID,'iszCommonWorkflowContext'),#审核意见
        'contract_audit_confirm':(By.ID,'iszCommonWorkflowPageSure'),#审核确定
        'accounting_time_loc':('[datagrid-row-index=0] [field="accounting_time"] td>input',
                                        '[datagrid-row-index=1] [field="accounting_time"] td>input',
                                        '[datagrid-row-index=2] [field="accounting_time"] td>input',
                                        '[datagrid-row-index=3] [field="accounting_time"] td>input',
                                        '[datagrid-row-index=4] [field="accounting_time"] td>input'),  # 核发月份
}
