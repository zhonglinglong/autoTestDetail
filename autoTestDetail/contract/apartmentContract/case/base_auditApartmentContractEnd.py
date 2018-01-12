# -*- coding:utf8 -*-

from common import page
from common import sqlbase
from common.base import log, consoleLog, Base, get_conf, set_conf
from contract.apartmentContract.page import apartmentContractEndPage


@log
def auditApartmentContract():
    """审核出租合同终止结算"""
    try:
        base=Base()
        base.open(page.contractEndPage, apartmentContractEndPage.searchMould['tr_contract_end'], havaFrame=False)
        #配置文件读取出租合同终止结算信息
        contractNum = get_conf('apartmentContractInfo', 'contractnum')
        sql = "SELECT * from apartment_contract where contract_num = '%s' and deleted = 0 and contract_status != 'EFFECTIVE'" % contractNum.encode(
            'utf-8')

        if sqlbase.get_count(sql) > 0:
            base.input_text(apartmentContractEndPage.searchMould['contract_num_loc'], contractNum)
        else:
            sql = "SELECT contract_num from apartment_contract act inner join apartment_contract_end ace on act.contract_id = ace.contract_id where ace.deleted = 0 " \
                  "and act.city_code = 330100 and ace.audit_status = 'NO_AUDIT' and act.contract_type = 'NEWSIGN' and act.entrust_type = 'SHARE' limit 1"
            if sqlbase.get_count(sql) > 0:
                contractNum = sqlbase.serach(sql)[0]
                consoleLog(u'未找到测试合同，随机使用合同 %s 做审核终止结算用例' % contractNum, level='w')
                base.input_text(apartmentContractEndPage.searchMould['contract_num_loc'], contractNum)
                set_conf('apartmentContractInfo', contractnum=contractNum)
            else:
                consoleLog(u'未找到符合条件的可以做终止的出租合同，跳过出租合同终止步骤', level='w')
                return
        base.click(apartmentContractEndPage.searchMould['search_button_loc'])
        base.staleness_of(apartmentContractEndPage.searchMould['tr_contract_end'])
        base.dblclick(apartmentContractEndPage.searchMould['tr_contract_end'])
        # 驳回
        base.click(apartmentContractEndPage.addContractEndMould['bohui_loc'])
        base.input_text(apartmentContractEndPage.addContractEndMould['contract_audit_content'], u'自动化测试审核数据')
        base.click(apartmentContractEndPage.addContractEndMould['contract_audit_confirm'])
        base.staleness_of(apartmentContractEndPage.searchMould['tr_contract_end'])
        # 初审
        base.dblclick(apartmentContractEndPage.searchMould['tr_contract_end'])
        base.click(apartmentContractEndPage.addContractEndMould['chushen_loc'])
        base.click(apartmentContractEndPage.addContractEndMould['contract_audit_confirm'])
        base.staleness_of(apartmentContractEndPage.searchMould['tr_contract_end'])
        base.dblclick(apartmentContractEndPage.searchMould['tr_contract_end'])
        # 复审
        base.click(apartmentContractEndPage.addContractEndMould['fushen_loc'])
        base.click(apartmentContractEndPage.addContractEndMould['contract_audit_confirm'])
        consoleLog(u'出租合同 %s 终止结算审核成功' % contractNum)

    finally:
        base.driver.quit()

auditApartmentContract()
