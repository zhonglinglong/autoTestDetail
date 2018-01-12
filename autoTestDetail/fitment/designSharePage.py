# -*- coding:utf8 -*-
from selenium.webdriver.common.by import By

searchMould = {
        'contract_num_loc' : (By.ID,'contract_num_search'),
        'residential_name_loc' : (By.ID,'residential_name_search'),
        'fitment_status_search' : (By.ID,'fitment_status_search'),
        'search_btn_loc' : (By.ID,'search_btn_share'),
        'tr_contract' : (By.CSS_SELECTOR,'tr[datagrid-row-index="0"]')
    }
designShareMould = {
        #操作按钮
        'design_btn':(By.CSS_SELECTOR,"[onclick='ShareIndex.dialog(\"workBlank\",0)']"), #分割户型:index=0右侧、1右键
        'design_btn_1': (By.CSS_SELECTOR,"[onclick='ShareIndex.dialog(\"sendOrder\",0)']"), #派单:index=0右侧、1右键
        'design_btn_2': (By.CSS_SELECTOR,"[onclick='ManageShareIndex.dialog(\"manageShareClosingRoom\",0)']"), #交房:index=0右侧、1右键
        'config_selected_all' : (By.CSS_SELECTOR,'[onclick="ShareWorkBlank.selectAll(this);"]'),    #所有配置全选
        #新增房间
        'add_house_btn': (By.CSS_SELECTOR,'#design_share_panel > div:nth-child(7) > div > div > a'),#新增房间
        'room_area' : (By.CSS_SELECTOR,'#room_area + span > input:nth-child(1)'),#面积:index=0是房间1，=1是房间2
        'save_btn' : (By.ID,'form_btn_workBlank'), #保存
        #派单界面
        'save_btn_1': (By.ID, 'send_order_form_btn'),  # 保存
        #交房界面
        'total_cost': (By.CSS_SELECTOR,'#total_cost + span > input'),#装修总成本
        'save_btn_2': (By.ID,'closing_room_form_btn'),#保存
    }

typeMould = {
        'fitment_style' : '#fitment_style ',#装修风格
        'room1_no' : '#share_room_1 > table > tbody > tr > td > input#room_no',#房号
        'room2_no' : '#share_room_2 > table > tbody > tr > td > input#room_no',
        'room1_orientation' : '#share_room_1 > table > tbody > tr > td > input#room_orientation',#朝向
        'room2_orientation' : '#share_room_2 > table > tbody > tr > td > input#room_orientation',
        'fitment_uid' : '#fitment_uid',#施工专员
        'decorate_start_date' : '#decorate_start_date',#装修开工日
        'hard_delivery_date' : '#hard_delivery_date', #硬装交付日
        'set_delivery_date' : '#set_delivery_date', #整套交付日
    }








