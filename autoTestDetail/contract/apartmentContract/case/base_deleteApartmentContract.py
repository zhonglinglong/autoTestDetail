# -*- coding:utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from common.base import log,consoleLog,Base,get_conf
from common import page
from contract.apartmentContract.page import apartmentContractPage
from common import sqlbase


@log
def deleteApartmentContract():
    """删除出租合同"""
    try:
        base=Base()
        base.open(page.apartmentContractPage, apartmentContractPage.searchContractMould['tr_contract'], havaFrame=False)
        #配置文件读取合同编号信息
        contractNum = get_conf('apartmentContractInfo', 'contractnum')
        sql = "SELECT * from apartment_contract where contract_num = '%s' and deleted = 0" % contractNum.encode('utf-8')
        if sqlbase.get_count(sql) > 0:
            base.input_text(apartmentContractPage.searchContractMould['contract_num_loc'], contractNum.decode('utf-8'))
            base.click(apartmentContractPage.searchContractMould['search_button_loc'])
            base.staleness_of(apartmentContractPage.searchContractMould['tr_contract'])
            base.script("$('#data_perm_btn').click()")
            base.click(apartmentContractPage.addApartmentContractMould['delete_button_confirm'])
            base.check_submit()
            consoleLog(u'出租合同 %s 删除成功' % contractNum)
        else:
            consoleLog(u'未找到出租合同 %s ，跳过删除用例' % contractNum)

    finally:
        base.driver.quit()

deleteApartmentContract()
