# -*- coding:utf8 -*-
from common.base import log,consoleLog,Base,set_conf,get_conf
from common import page
from common import sqlbase
import time
from house.apartment   import  apartmentPage

@log
def addReimbursement():
    """新增报销单"""
    try:
        base=Base()
        base.open(page.apartmentPage, apartmentPage.apartmentMould['tr_apartment'])

        # 配置文件中读取房源
        apartmentCode = get_conf('houseInfo', 'apartmentcode')
        consoleLog(u'确认房源 %s 是否存在' % apartmentCode)
        sql = "SELECT * from apartment where apartment_code = '%s' and deleted = 0 and is_active = 'Y'" % apartmentCode.encode('utf-8')
        if sqlbase.get_count(sql) > 0:
            base.input_text(apartmentPage.apartmentMould['residential_name'], apartmentCode)


        else:
            sql = "SELECT apartment_code from apartment where deleted = 0 and is_active = 'Y' and city_code = '330100' LIMIT 1"
            apartmentCode = sqlbase.serach(sql)[0]
            base.input_text(apartmentPage.apartmentMould['residential_name'], apartmentCode)
        base.click(apartmentPage.apartmentMould['search_btn'])
        base.staleness_of(apartmentPage.apartmentMould['tr_apartment'])
        base.click(apartmentPage.apartmentMould['details_btn'])
        base.click(apartmentPage.apartmentMould['expense_btn'])
        # 报销费用
        base.input_text(apartmentPage.apartmentMould['memo'], u'报销单自动化测试备注')
        base.type_select(apartmentPage.typeMould['item_type'], 'WATER')
        base.type_select(apartmentPage.typeMould['bear_type'], 'COMPANY')
        base.input_text(apartmentPage.apartmentMould['amount'], '666')
        base.type_date(apartmentPage.typeMould['start_date'], u'2017-08-08')
        base.type_date(apartmentPage.typeMould['end_date'], u'2017-08-28')
        base.type_select(apartmentPage.typeMould['vacant'], 'Y')
        base.type_select(apartmentPage.typeMould['first'], 'Y')
        base.type_select(apartmentPage.typeMould['source_bear_id'], 'AutoTest-13666666665')
        # 报销人
        base.type_select(apartmentPage.typeMould['moneytype'], 'CUSTOMER_AGENT_PYMENT')
        base.type_select(apartmentPage.typeMould['customer_name'], 'AutoTest')
        base.type_select(apartmentPage.typeMould['customer_bank_location'], 'ABC')
        base.type_select(apartmentPage.typeMould['bank_card'], '6228481561239334717')
        # base.input_text(base.apartmentMould['brepay_company'],u'杭州爱上租科技有限公司')
        base.click(apartmentPage.apartmentMould['submit_btn'])
        base.check_submit()
        consoleLog(u'房源 %s 的报销单新增成功' % apartmentCode)
        sql = "SELECT expense_num from reimbursement_expense where apartment_id = (SELECT apartment_id from apartment where apartment_code = '%s')" % apartmentCode.encode('utf-8')
        consoleLog(u'记录房源 %s 的报销编号' % apartmentCode)
        num = sqlbase.serach(sql)[0]

        #写入配置文件
        set_conf('houseInfo', apartmentReimbursementNum=num)
    finally:
        base.driver.quit()

addReimbursement()