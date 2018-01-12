# -*- coding:utf8 -*-

from selenium.webdriver.common.by import By


apartmentMould = {
        #搜索出需要的房源
        'tr_house': (By.CSS_SELECTOR, 'tr[datagrid-row-index="0"]'),
        'residential_name': (By.ID,'residential_name_house_code_search'),#搜索栏物业地址
        'search_btn' : (By.ID,'search_btn'),#搜索按钮
        'details_btn' : (By.CSS_SELECTOR,'[onclick="Apartment.dialog(\'edit\',0)"]'),#详情
        'tr_apartment' : (By.CSS_SELECTOR,'tr[datagrid-row-index="0"]'),
        #详情界面
        'make_price_btn' : (By.ID,'btn_make_price'),#定价按钮
        'apartment_info_loc':(By.ID,'share_base_apartment'), #房源信息
        'dealtype_loc':'#dealtype',  #  处理状态
        #定价界面
        'entire_rent_price': (By.CSS_SELECTOR,'#rent_price + span >input:nth-child(1)'),#整租-月租金 index=1
        'share_rent_price' : (By.CSS_SELECTOR,'td[field=rent_price] > div > span >input:nth-child(1)'), #合租-月租金 多房间下为数组，个数为房间数量
        'save_btn' : (By.CSS_SELECTOR,'#base_button > div > p > button:nth-child(2)'),#保存
        'form_btn' : (By.ID,'form_btn'), #保存
        'expense_btn' : (By.CSS_SELECTOR,'#base_button > div > button:nth-child(6)'),#报销
        'amount' : (By.CSS_SELECTOR,'#projectAllExpense > div > table > tbody > tr:nth-child(3) > td:nth-child(5) > span > input'),#报销金额
        'brepay_company': (By.CSS_SELECTOR,'#repay_company + span > input:nth-child(1)'), # 还款公司
        'memo': (By.ID,'memo'),  # 备注
        'submit_btn': (By.ID,'submit_btn')  # 提交
    }
typeMould = {
        'item_type' : '#projectAllExpense > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > input ',#报销项目
        'bear_type' : '#projectAllExpense > div > table > tbody > tr:nth-child(3) > td:nth-child(2) > input ',#承担方
        'start_date' : '#projectAllExpense > div > table > tbody > tr:nth-child(3) > td:nth-child(6) > input:nth-child(1)',#费用周期开始
        'end_date' : '#projectAllExpense > div > table > tbody > tr:nth-child(3) > td:nth-child(6) > input:nth-child(3)',#费用周期结算
        'vacant' : '#projectAllExpense > div > table > tbody > tr:nth-child(3) > td:nth-child(8) > input',#空置期
        'first' : '#projectAllExpense > div > table > tbody > tr:nth-child(3) > td:nth-child(9) > input',#首次
        'source_bear_id' : '#projectAllExpense > div > table > tbody > tr:nth-child(3) > td:nth-child(10) > span > input:nth-child(1)',#房源方
        'moneytype' : '#moneytype ',#收借款类别
        'customer_name' : '#bank_name ',#姓名
        'customer_bank_location' : '#bank_location ',#开户银行
        'bank_card' : '#bank_card  '#银行卡号
    }
