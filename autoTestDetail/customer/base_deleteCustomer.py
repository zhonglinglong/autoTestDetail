# -*- coding:utf8 -*-
from customer import customerPage
from common.base import log,consoleLog,get_conf,set_conf,Base
from common import page,sqlbase
import time
import random

@log
def deleteCustomer():
    """删除租前客户信息"""
    try:
        base=Base()
        base.open(page.customerListPage, customerPage.listMould['tr_customer'], havaFrame=False)
        #配置文件中读取租前客户信息
        customerName = get_conf('customerInfo', 'customerName')
        sql = "SELECT * from customer where customer_name = '%s' and deleted = 0" % customerName.encode('utf-8')

        if sqlbase.get_count(sql) > 0:
            base.input_text(customerPage.listMould['customer_name_search'], customerName)
            base.click(customerPage.listMould['search_button'])
            base.staleness_of(customerPage.listMould['tr_customer'])
            base.click(customerPage.listMould['delete_button'])
            base.click(customerPage.listMould['alert_confirm'])
            base.check_submit()
            consoleLog(u'租前客户 %s 删除成功' % customerName)
        else:
            consoleLog(u'未找到租前客户 %s，跳过删除' % customerName)
    finally:
        base.driver.quit()
        
deleteCustomer()