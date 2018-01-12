# -*- coding:utf8 -*-
from selenium.webdriver.common.by import By

searchMould = {
        'residentia_name_loc' : (By.ID,'residential_name_search'),
        'building_name_loc' : (By.ID,'building_name_search'),
        'unit_name_loc' : (By.ID,'unit_search'),
        'houseno_name_loc' : (By.ID,'house_no_search'),
        'search_button_loc' : (By.ID,'search_btn'),
        'tr_house' : (By.CSS_SELECTOR,'tr[datagrid-row-index="0"]')
    }
houseAuditPageloc = {
        'audit_btn': (By.ID, 'audit_btn'),  # 审核
        'department_did_loc' : '#residential_department_did',   #责任部门
        'cancel_btn': (By.ID, 'cancel_btn'),  # 审核通过
        'form_btn': (By.ID, 'form_btn'),  # 审核不通过
        'iszCommonWorkflowPageSure': (By.ID, 'iszCommonWorkflowPageSure'),  # 确定
    }
