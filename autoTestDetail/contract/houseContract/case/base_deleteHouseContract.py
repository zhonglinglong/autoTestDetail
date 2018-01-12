# -*- coding:utf8 -*-

from common import page
from common import sqlbase
from common.base import log, consoleLog, Base, get_conf
from contract.houseContract.page import houseContractPage


@log
def addHouseContact():
    """审核委托合同"""
    try:
        base=Base()
        base.open(page.entrustContractPage, houseContractPage.contractSearchMould['tr_contract'], havaFrame=False)
        #配置文件读取合同编号
        contractNum = get_conf('houseContractInfo', 'contractNum')
        sql = "SELECT * from house_contract WHERE contract_num = '%s' and deleted = 0" % contractNum.encode('utf-8')
        if sqlbase.get_count(sql) != 0:
            base.input_text(houseContractPage.contractSearchMould['contract_num_loc'], contractNum)
            base.click(houseContractPage.contractSearchMould['search_button_loc'])
            base.staleness_of(houseContractPage.contractSearchMould['tr_contract'])
            base.click(houseContractPage.addHouseContractMould['delete_button'])
            base.click(houseContractPage.addHouseContractMould['delete_button_confirm'])
            base.check_submit()
            consoleLog(u'委托合同删除成功')
        else:
            consoleLog(u'未找到委托合同 %s，略过删除功能' % contractNum)
    finally:
        base.driver.quit()

addHouseContact()
