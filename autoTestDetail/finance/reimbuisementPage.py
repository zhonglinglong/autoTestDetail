# -*- coding:utf8 -*-
from selenium.webdriver.common.by import By

searchMould = {
        'residential_name' : (By.ID,'residential_name_search'),
        'search_button' : (By.ID,'search_btn'),
        'expenseNum_loc' : (By.ID,'expense_num_search'), #报销编号
        'tr_reimbuisement' : (By.CSS_SELECTOR,'tr[datagrid-row-index="0"]')
    }
editMould = {
        'reset_button' : (By.CSS_SELECTOR,'[onclick="ReimbursementExpense.reset(0)"]'), #重置
        'delete_button' : (By.CSS_SELECTOR,'[onclick="ReimbursementExpense.delDialog(0)"]'),    #删除
        'alert_confirm': (By.CSS_SELECTOR, '.dialog-button.messager-button > a:nth-child(1) > span'),
        'payment_button' : (By.CSS_SELECTOR,'[onclick="ReimbursementExpense.receivableDialog(0)"]'),   #付款index=0为操作列，1为右键
        'payment_type' : (By.CSS_SELECTOR,'input#complete_type'), #付款方式index=0为现金，1为银行转账
        'payment_remark' : (By.CSS_SELECTOR,'#remark + span > input:nth-child(1)'), #付款备注
        'payment_save' : (By.ID,'form_btn'),  #付款保存
        'payment_audit': (By.CSS_SELECTOR, 'button[onclick="Expense.end()"]'),  # 付款审核
        'payment_audit_save': (By.CSS_SELECTOR, '.panel.window.messager-window > div:nth-child(3) > a:nth-child(1)'),  # 付款审核保存
        # 审核相关
        'chushen_loc': (By.CSS_SELECTOR, 'button[status="PASS"]'),  # 初审
        'fushen_loc': (By.CSS_SELECTOR, 'button[status="REVIEW"]'),  # 复审
        'bohui_loc': (By.CSS_SELECTOR, 'button[status="RE_JECT"]'),  # 驳回
        'fanshen_loc' : (By.CSS_SELECTOR,'button[status="REAUDIT"]'), #反审
        'audit_content': (By.ID, 'iszCommonWorkflowContext'),  # 审核意见
        'audit_confirm': (By.ID, 'iszCommonWorkflowPageSure'),  # 审核确认
        'save_button' : ()
    }

