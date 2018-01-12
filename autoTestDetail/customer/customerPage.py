# -*- coding:utf8 -*-
from selenium.webdriver.common.by import By


listMould = {
        'customer_name_search' : (By.ID,'customer_code_name_mobile_search'),
        'search_button' : (By.ID,'search_btn'),
        'close_box_loc':(By.CSS_SELECTOR, '.panel.window > div:nth-child(1) > div.panel-tool > a'),  # 关闭弹窗
        'add_customer_loc' : (By.ID,'customerAdd'),
        'delete_button' : (By.ID,'del_btn'),
        'alert_confirm': (By.CSS_SELECTOR, '.dialog-button.messager-button > a:nth-child(1) > span'),
        'tr_customer': (By.CSS_SELECTOR, '[datagrid-row-index="0"]'),
        'allot_customer' : (By.CSS_SELECTOR,'.panel-tool-close'),
        'customer_status_loc':'#customer_status_search',
        'book_loc': (By.CSS_SELECTOR, '[datagrid-row-index="0"]>td[field="manage"]>div>button:nth-child(2)'), #下定
        'earnest_money_loc':(By.CSS_SELECTOR,'#earnest_money + span>input'),  # 定金
        'property_address':(By.CSS_SELECTOR,'#a_property_address>a'),  # 选择房源
        'submit_button':(By.CSS_SELECTOR,'#base_button .search-button-wrapper')  # 提交
    }
addCustomerMould = {
        #租客信息
        'customer_name_loc' : (By.CSS_SELECTOR,'#customer_name + span > input:nth-child(1)'),  #姓名
        'customer_phone_loc' : (By.CSS_SELECTOR,'#phone + span > input:nth-child(1)'),    #手机号
        'customer_gender_loc' : (By.CSS_SELECTOR,'[name="gender"]'),    #性别 0男 1女 2未知
        'customer_marriage_loc' : (By.CSS_SELECTOR,'[name = "marriage"]'),  #婚姻 0未婚 1已婚 2未知
        'customer_email_loc' : (By.CSS_SELECTOR,'#email + span > input:nth-child(1)'),  #邮箱
        'customer_wechat_loc': (By.CSS_SELECTOR, '#wechat + span > input:nth-child(1)'),  # 邮箱
        'rent_price_min_loc': (By.CSS_SELECTOR, '#rent_from_price + span > input:nth-child(1)'),  #求租最小价
        'rent_price_max_loc': (By.CSS_SELECTOR, '#rent_to_price + span > input:nth-child(1)'),  # 求租最大价
        #求租需求
        'rent_people_loc': (By.CSS_SELECTOR, '#rent_people + span > input:nth-child(1)'),  # 入住人数
        'area_loc': (By.CSS_SELECTOR, '#area + span > input:nth-child(1)'),  # 求租面积
        'rent_other': (By.ID, 'rent_other'),  # 其他需求

        'submit_loc' : (By.ID,'form_btn')   #提交
    }
typeMould = {
        #租客信息
        'constellation' : '#constellation',     #星座
        'education': '#education',  # 学历
        'customer_from': '#customer_from',  # 来源
        #求租需求
        'rent_class': '#rent_class',  # 求租等级
        'rent_type': '#rent_type',  # 求租类型
        'rent_use': '#rent_use',  # 求租用途
        'rent_fitment': '#rent_fitment',  # 装修情况
        'rent_area_code': '#rent_area_code',  # 求租城区
        'rent_business_circle': '#rent_business_circle_ids',  # 求租商圈
        'rent_date': '#rent_date'  # 希望入住日
    }