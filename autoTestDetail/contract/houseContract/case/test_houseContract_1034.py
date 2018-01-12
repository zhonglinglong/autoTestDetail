# -*- coding:utf8 -*-

from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.houseContract.page import houseContractPage
from assertpy import assert_that as asserts

@log
def test_1034():
    """有效委托合同正常删除"""

    # describe：有效合同正常删除
    # data：1、委托合同状态为有效；2、委托合同下没有有效状态的出租合同；
    # result：委托合同删除成功；

    fileName = 'houseContract_1034'
    # contractSql = "select hc.contract_num,h.house_code from house_contract hc inner join house h on h.house_id=hc.house_id where not EXISTS (select * from apartment_contract ac " \
    #               "where hc.house_id=ac.house_id) and hc.is_active='Y' and hc.deleted=0 and hc.city_code=330100  order by rand() limit 1"
    contractSql = "select hc.contract_num,h.house_code from house_contract hc inner join house h on h.house_id=hc.house_id where not EXISTS (select * from house_contract_pay hcp " \
                  "where hc.contract_id=hcp.contract_id and hcp.deleted=0) and not EXISTS (select * from apartment_contract ac where hc.house_id=ac.house_id)and hc.is_active='Y' " \
                  "and hc.deleted=0 and hc.city_code=330100"
    if sqlbase.get_count(contractSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % contractSql)
        return
    contractInfo = sqlbase.serach(contractSql)
    contractNum = contractInfo[0]
    consoleLog(u'%s:取委托合同 %s 做删除' % (fileName, contractNum))

    with Base() as base:
        base.open(page.entrustContractPage, houseContractPage.contractSearchMould['tr_contract'])
        base.input_text(houseContractPage.contractSearchMould['residential_name_loc'], contractInfo[1])
        base.input_text(houseContractPage.contractSearchMould['contract_num_loc'], contractNum)
        base.click(houseContractPage.contractSearchMould['search_button_loc'])
        base.staleness_of(houseContractPage.contractSearchMould['tr_contract'])
        base.click(houseContractPage.addHouseContractMould['delete_button'])
        base.click(houseContractPage.addHouseContractMould['delete_button_confirm'])
        base.check_submit()
        # 合同状态检查
        contractSqlb = "select * from house_contract where deleted=1 and contract_num='%s'" % contractNum
        base.diffAssert(lambda test: asserts(sqlbase.waitData(contractSqlb,1)).is_true(),1034,
                        u'%s:委托合同 %s 删除异常,执行SQL：%s"' % (fileName, contractNum, contractSqlb))

test_1034()