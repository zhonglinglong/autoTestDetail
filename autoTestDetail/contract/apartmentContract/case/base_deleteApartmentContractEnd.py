# -*- coding:utf8 -*-

from common import page
from common import sqlbase
from common.base import log, consoleLog, Base, get_conf
from contract.apartmentContract.page import apartmentContractEndPage


@log
def auditApartmentContract():
    """删除核出租合同终止结算"""
    try:
        base=Base()
        base.open(page.contractEndPage, apartmentContractEndPage.searchMould['tr_contract_end'], havaFrame=False)
        contractNum = get_conf('apartmentContractInfo', 'contractnum')
        sql = "SELECT * from apartment_contract where contract_num = '%s' and deleted = 0 and contract_status != 'EFFECTIVE'" % contractNum.encode(
            'utf-8')
        if sqlbase.get_count(sql) > 0:
            base.input_text(apartmentContractEndPage.searchMould['contract_num_loc'], contractNum)
        else:
            consoleLog(u'未找到出租合同终止结算的测试数据，跳过删除用例', level='w')
            return
        base.click(apartmentContractEndPage.searchMould['search_button_loc'])
        base.staleness_of(apartmentContractEndPage.searchMould['tr_contract_end'])
        base.click(apartmentContractEndPage.addContractEndMould['delete_button'])
        base.click(apartmentContractEndPage.addContractEndMould['delete_button_confirm'])
        base.check_submit()
        consoleLog(u'出租合同 %s 终止结算删除成功' % contractNum)
    finally:
        base.driver.quit()

auditApartmentContract()
