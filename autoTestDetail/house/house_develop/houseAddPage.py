# -*- coding:utf8 -*-

from selenium.webdriver.common.by import By

houseAddMould = {
    'test' : (By.ID,'form_btn'), #测试页面加载
    #基本信息
    'property_name': (By.CSS_SELECTOR, '#td_not_found > span > input'),  # 物业地址 ַ
    'property_name_click': (By.CSS_SELECTOR,'#house_develop_panel_form + div > div > div'),
    'building_name_search' : (By.CSS_SELECTOR,'#building_name_search + span > span + input'),
    'buidlding_click':(By.CSS_SELECTOR,'[style="display: block;"]'),
    'unit_search': (By.CSS_SELECTOR, '#unit_search + span > span + input'),
    'unit_click' : (By.CSS_SELECTOR,'[style="display: block;"]'),   #index = 1
    'house_no_search': (By.CSS_SELECTOR, '#house_no_search + span > span + input'),
    'house_no_click': (By.CSS_SELECTOR, '[style="display: block;"]'),  # index = 2
    'add_contact_btn' : (By.ID,'other_contact_btn'),    #新增联系方式
    'contact_people': (By.CSS_SELECTOR, '#contact + span > input'),  # 联系人
    'contact_tel1': (By.CSS_SELECTOR, '#contact_tel + span > input'),  # 联系方式
    'contact_tel2' : (By.CSS_SELECTOR,'#phone + span > input:nth-child(1)'),   #联系方式
    'save_contact_btn' : (By.ID,'contact_form_btn'),    #新增联系方式保存
    #出租信息
    'rental_price': (By.CSS_SELECTOR, '#rental_price + span > input '),# 意向租金
    #详细信息
    'build_area': (By.CSS_SELECTOR, '#build_area + span > input'),  # 面积
    'form_btn': (By.ID, 'form_btn')  # 保存
}

typeMould = {
    'residential' : '#residential_name_search', #楼盘
    'building': '#house_develop_panel_form + div + div > div > div',  # 栋座
    'unit': '#house_develop_panel_form + div + div + div > div > div',  # 单元
    'room_number': '#house_develop_panel_form + div + div + div + div > div >div',  # 房号
    'did' : '#did', #拓房部门
    'uid' : '#uid', #拓房人
    'house_status': 'body > div:nth-child(17) > div > div:nth-child(3)',  # 房源状态
    'remark': '#remark',  # 备注
    'source': '#source ', #房屋来源
    'rooms' : '#rooms ', #室
    'livings' : '#livings ',#厅
    'kitchens' : '#kitchens ',#厨
    'bathrooms' : '#bathrooms ',#卫
    'balconys' : '#balconys', #阳
    'orientation': '#orientation',  # 朝向
    'property_type': '#property_type',  # 物业类型
    'property_use': '#property_use',  # 物业用途
    'fitment_type': '#fitment_type',  # 装修情况
    'look_type': '#look_type',  # 看房方式
    'look_date': '#look_date',  # 可看房日期
}




