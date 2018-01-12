# -*- coding:utf8 -*-
from selenium.webdriver.common.by import By


searchContractMould = {
        'contract_num_loc' : (By.CSS_SELECTOR,'#search_panel>table>tbody>tr:nth-child(2)>td:nth-child(2)>span>input'),   #出租合同号
        'search_button_loc' : (By.ID,'search_btn'),   #搜索
        'reset_button_loc':(By.ID,'reset_btn'),#重置
        'tr_contract' : (By.CSS_SELECTOR,'tr[datagrid-row-index="0"]'),#列表页第一行
    }
detailAchievementMoudle = {
        'contract_num_loc':(By.CSS_SELECTOR,'#apartment_contract_table>table>tr>td>div'),#出租合同号
        'audit_button_loc':(By.ID,'current_audit_general_button'),#审核
        'contract_audit_content':(By.ID,'iszCommonWorkflowContext'),#审核意见
        'contract_audit_confirm':(By.ID,'iszCommonWorkflowPageSure'),#审核确定
        '':(),
}
