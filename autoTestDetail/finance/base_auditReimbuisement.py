# -*- coding:utf8 -*-
from finance  import reimbuisementPage
from common.base import log,consoleLog,get_conf,set_conf,Base
from common import page,sqlbase
import time

@log
def auditReimbuisement():
    """审核报销单"""
    try:
        base=Base()
        base.open(page.reimbursementExpenseListPage, reimbuisementPage.searchMould['tr_reimbuisement'], havaFrame=False)
        #配置文件读取报销单信息
        expenseNum = get_conf('houseInfo', 'apartmentReimbursementNum')
        sql = "SELECT * from reimbursement_expense where expense_num = '%s' and deleted = 0" % expenseNum.encode(
            'utf-8')
        consoleLog(u'查询是否存在测试房源的报销单')

        if sqlbase.get_count(sql) > 0:
            base.input_text(reimbuisementPage.searchMould['expenseNum_loc'], expenseNum)
        else:
            sql = "SELECT rr.expense_num from reimbursement_expense rr INNER JOIN house hh on rr.house_id = hh.house_id where hh.city_code = 330100 " \
                  "and rr.deleted = 0 and rr.audit_status = 'NO_AUDIT' limit 1"
            consoleLog(u'未找到测试房源的报销单，随机查找报销单做审核操作')
            if sqlbase.get_count(sql) > 0:
                expenseNum = sqlbase.serach(sql)[0]
                base.input_text(reimbuisementPage.searchMould['expenseNum_loc'], expenseNum);consoleLog(u'输入报销单：%s' % expenseNum)
            else:
                consoleLog(u'未找到符合条件的报销单，跳过审核用例')
                return
        base.click(reimbuisementPage.searchMould['search_button'])
        base.staleness_of(reimbuisementPage.searchMould['tr_reimbuisement'])
        base.dblclick(reimbuisementPage.searchMould['tr_reimbuisement'])
        base.click(reimbuisementPage.editMould['bohui_loc'])
        base.input_text(reimbuisementPage.editMould['audit_content'], 'AutoTest')
        base.click(reimbuisementPage.editMould['audit_confirm'])
        base.staleness_of(reimbuisementPage.searchMould['tr_reimbuisement'])
        base.dblclick(reimbuisementPage.searchMould['tr_reimbuisement'])
        base.click(reimbuisementPage.editMould['chushen_loc'])
        base.click(reimbuisementPage.editMould['audit_confirm'])
        base.staleness_of(reimbuisementPage.searchMould['tr_reimbuisement'])
        base.dblclick(reimbuisementPage.searchMould['tr_reimbuisement'])
        base.click(reimbuisementPage.editMould['fushen_loc'])
        base.click(reimbuisementPage.editMould['audit_confirm'])
        base.check_submit()
        base.click(reimbuisementPage.editMould['payment_button'], index=0)
        base.click(reimbuisementPage.editMould['payment_type'], index=0)
        base.input_text(reimbuisementPage.editMould['payment_remark'], 'AutoTest')
        base.click(reimbuisementPage.editMould['payment_save'])
        base.staleness_of(reimbuisementPage.searchMould['tr_reimbuisement'])
        base.dblclick(reimbuisementPage.searchMould['tr_reimbuisement'])
        base.click(reimbuisementPage.editMould['payment_audit'])
        base.click(reimbuisementPage.editMould['payment_audit_save'])
        consoleLog(u'报销单 %s 审核成功' % expenseNum)
    finally:
        base.driver.quit()

auditReimbuisement()