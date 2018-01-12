# -*- coding:utf8 -*-
from selenium.webdriver.common.by import By

searchMould = {
        'residential_name' : (By.ID,'residential_name_search'),
        'contractNum_loc': (By.ID,'contract_num_search'),
        'search_button' : (By.ID,'search_btn'),
        'reset_button': (By.ID,'reset_btn'),
        'tr_receviable_loc' : (By.CSS_SELECTOR,'tr[datagrid-row-index="0"]'),
        'receviabl_button': [(By.CSS_SELECTOR,'[onclick="ContractReceivable.receivableDialog(0)"]'),  # 第一个收款
        (By.CSS_SELECTOR,'[onclick="ContractReceivable.receivableDialog(1)"]'),  # 第二个收款
        (By.CSS_SELECTOR,'[onclick="ContractReceivable.receivableDialog(2)"]')],  # 第三个收款
        '': (),
        '': (),
        '': (),
        '': (),
        '': (),
        '': (),
        '': (),
        '': (),
        '': (),


    }
detailMould = {
        'receipts_money_loc': (By.CSS_SELECTOR,'#receipts_money + span >input'),
        'alipay_card_loc': (By.CSS_SELECTOR,'#alipay_card + span >input'),
        'operation_total_loc': (By.CSS_SELECTOR,'#operation_total + span >input'),
        'receipts_date_loc': '#receipts_date',
        'banktrans_date_loc':'#BANKTRANSFER #receipts_date',
        'receipts_cardtrans_loc': (By.CSS_SELECTOR,'input#receipts_type:nth-child(3)'),#银行卡转账
        'bank_name_loc':'#bank_name', #银行名称
        'card_num_loc':(By.CSS_SELECTOR,'#bank_card_last_four+span>input'),#卡号后四位
        'receipts_type': (By.CSS_SELECTOR,'input#receipts_type:nth-child(5)'),#支付宝
        'save_button':(By.ID,'form_btn'),
        'print_btn_close': (By.ID,'print_btn_close'),
        '': (),
        '': (),
        '': (),
        '': (),
        '': (),
        '': (),
    }