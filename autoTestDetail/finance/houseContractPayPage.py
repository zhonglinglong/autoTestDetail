# -*- coding:utf8 -*-

from common.base import Base
from common import page
from selenium.webdriver.common.by import By


class HouseContractPayPage(Base):
    searchMould = {
        'contract_num' : (By.ID,'contract_num_search'),
        'search_btn' : (By.ID,'search_btn'),
        'tr_houseContractPay': (By.CSS_SELECTOR, 'tr[datagrid-row-index="0"]')
    }
    editMould = {
        'payment_button': (By.CSS_SELECTOR, '[onclick="ReimbursementExpense.receivableDialog(0)"]'),    # 付款index=0为操作列，1为右键
        'payment_type': (By.CSS_SELECTOR, 'input#complete_type'),  # 付款方式index=0为现金，1为银行转账
        'payment_remark': (By.CSS_SELECTOR, '#remark + span > input:nth-child(1)'),  # 付款备注
        'payment_save': (By.ID, 'form_btn'),  # 付款保存
    }