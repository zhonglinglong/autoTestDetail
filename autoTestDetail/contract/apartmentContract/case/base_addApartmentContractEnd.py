# -*- coding:utf8 -*-

from common import page
from common import sqlbase
from common.base import log, consoleLog, Base, get_conf, set_conf
from contract.apartmentContract.page import apartmentContractEndPage


@log
def addApartmentContract():
    """新增出租合同终止结算"""
    try:
        base=Base()
        base.open(page.apartmentContractPage, apartmentContractEndPage.addContractEndMould['tr_contract'], havaFrame=False)
        #配置文件读取合同信息
        contractNum = get_conf('apartmentContractInfo', 'contractnum')
        endDate = None
        sql = "SELECT rent_end_date from apartment_contract where contract_num = '%s' and deleted = 0" % contractNum.encode(
            'utf-8')
        if sqlbase.get_count(sql) > 0:
            base.input_text(apartmentContractEndPage.addContractEndMould['contract_num_loc'], contractNum)
            endDate = sqlbase.serach(sql)[0]
        else:
            sql = "SELECT contract_num,rent_end_date from apartment_contract where deleted = 0 and city_code = 330100 and audit_status = 'APPROVED' and contract_status = 'EFFECTIVE' " \
                  "and contract_type = 'NEWSIGN' and entrust_type = 'SHARE' limit 1"
            if sqlbase.get_count(sql) > 0:
                info = sqlbase.serach(sql)
                contractNum = info[0]
                endDate = info[1]
                consoleLog(u'未找到测试合同，随机使用合同 %s 做新增终止结算用例' % contractNum, level='w')
                base.input_text(apartmentContractEndPage.addContractEndMould['contract_num_loc'], contractNum)
                set_conf('apartmentContractInfo', contractnum=contractNum)
            else:
                consoleLog(u'未找到符合条件的可以做终止的出租合同，跳过出租合同终止步骤', level='w')
                return
        base.click(apartmentContractEndPage.addContractEndMould['search_button_loc'])
        base.staleness_of(apartmentContractEndPage.addContractEndMould['tr_contract'])
        base.context_click(apartmentContractEndPage.addContractEndMould['tr_contract'])
        base.click(apartmentContractEndPage.addContractEndMould['end_button_loc'], index=1)
        base.click(apartmentContractEndPage.addContractEndMould['now_end_loc'])
        base.input_text(apartmentContractEndPage.addContractEndMould['receipt_num_loc'], 'AutoTest')
        base.type_date(apartmentContractEndPage.typeMould['end_date'], endDate)
        base.input_text(apartmentContractEndPage.addContractEndMould['end_reason_loc'], u'承租周期已完')
        base.type_select(apartmentContractEndPage.typeMould['end_type'], 'RETREATING')  # 正退
        base.type_select(apartmentContractEndPage.typeMould['receipt_type_loc'], 'PAYER')  # 承租人
        base.input_text(apartmentContractEndPage.addContractEndMould['bank_loc'], u'中国银行')
        base.dblclick(apartmentContractEndPage.addContractEndMould['weiyuejin_loc'], index=12)
        base.input_text(apartmentContractEndPage.addContractEndMould['receivable_money_loc'], '888.88')
        base.input_text(apartmentContractEndPage.addContractEndMould['payable_money_loc'], '666.66')
        base.input_text(apartmentContractEndPage.addContractEndMould['remark_loc'], 'AutoTest')
        # base.click(base.addContractEndMould['submit_loc'])     #不知道这步为什么会报错，改用js执行
        base.script('$("#form_submit_btn").click()')
        base.check_submit()
        consoleLog(u'出租合同 %s 终止结算新增成功' % contractNum)
    finally:
        base.driver.quit()

addApartmentContract()
