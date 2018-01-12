# -*- coding:utf8 -*-
from customer import customerPage
from common.base import log,consoleLog,get_conf,set_conf,Base
from common import page,sqlbase
import time
import random

@log
def addCustomer():
    """新增租前客户信息"""
    try:
        base=Base()
        base.open(page.customerListPage, customerPage.listMould['add_customer_loc'], havaFrame=False)
        base.click(customerPage.listMould['add_customer_loc'])
        customerName = 'AutoTest' + '-' + time.strftime('%m%d-%H%M%S')
        base.input_text(customerPage.addCustomerMould['customer_name_loc'], customerName)
        prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
                   "153", "155", "156", "157", "158", "159", "186", "187", "188"]
        phone = random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))
        base.input_text(customerPage.addCustomerMould['customer_phone_loc'], phone)
        base.click(customerPage.addCustomerMould['customer_gender_loc'], index=1)
        base.click(customerPage.addCustomerMould['customer_marriage_loc'], index=1)
        base.input_text(customerPage.addCustomerMould['customer_email_loc'], 'mail@mail.com')
        base.input_text(customerPage.addCustomerMould['customer_wechat_loc'], 'AutoTest')
        base.type_select(customerPage.typeMould['constellation'], 'VIRGO')
        base.type_select(customerPage.typeMould['education'], 'BACHELOR')
        base.type_select(customerPage.typeMould['customer_from'], 'LOCAL58')
        # 求租需求
        base.type_select(customerPage.typeMould['rent_class'], 'CLASSA')  # 求租等级-A级
        base.type_select(customerPage.typeMould['rent_type'], 'GATHERHOUSE')  # 求租类型-不限
        base.type_select(customerPage.typeMould['rent_use'], 'RESIDENCE')  # 求租用途-住宅
        base.type_select(customerPage.typeMould['rent_fitment'], 'FITMENT_ROUGH')  # 装修情况-毛坯
        base.type_select(customerPage.typeMould['rent_area_code'], '330108')  # 求租城区-滨江
        base.type_select(customerPage.typeMould['rent_business_circle'], '4')  # 求租商圈-浦沿
        base.input_text(customerPage.addCustomerMould['rent_price_min_loc'], '1111')
        base.input_text(customerPage.addCustomerMould['rent_price_max_loc'], '2222')
        base.type_date(customerPage.typeMould['rent_date'], '2017-02-02')
        base.input_text(customerPage.addCustomerMould['rent_people_loc'], '3')
        base.input_text(customerPage.addCustomerMould['area_loc'], '88.88')
        base.input_text(customerPage.addCustomerMould['rent_other'], u'浙江省杭州市滨江区六和路368号海创基地南楼3E')
        base.click(customerPage.addCustomerMould['submit_loc'])
        base.check_submit()
        consoleLog(u'新增租客 %s 成功' % customerName)
        #将新增租客信息写入配置文件中
        set_conf('customerInfo', customerName=customerName)
        sql = "SELECT customer_id from customer where customer_name = '%s' and deleted = 0" % customerName.encode(
            'utf-8')
        set_conf('customerInfo', customerID=sqlbase.serach(sql)[0])
    finally:
        base.driver.quit()
        
addCustomer()