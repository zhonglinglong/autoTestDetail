# -*- coding:utf8 -*-

from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.apartmentContract.page import apartmentContractPage
from assertpy import assert_that as asserts

@log
def test_1014():
    """正常出租合同删除"""

    # describe：正常出租合同删除
    # data：出租合同状态有效且没有实收
    # result：删除成功

    fileName = 'apartmentContract_1014'
    contractSql = "select ac.contract_num from apartment_contract ac where not EXISTS (select * from apartment_contract_receipts acr where ac.contract_id=acr.contract_id) " \
                  "and  ac.deleted=0 and ac.is_active='Y' and ac.city_code=330100 and ac.entrust_type='SHARE' and ac.contract_status='EFFECTIVE' ORDER BY RAND() LIMIT 1"
    if sqlbase.get_count(contractSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % contractSql)
        return
    info = sqlbase.serach(contractSql)
    contractNum = info[0]
    consoleLog(u'%s:取随机有效出租合同 %s 做合同删除' % (fileName, contractNum))

    with Base() as base:
        base.open(page.apartmentContractPage, apartmentContractPage.searchContractMould['tr_contract'])
        base.input_text(apartmentContractPage.searchContractMould['contract_num_loc'], contractNum)  # 输入合同编号
        base.click(apartmentContractPage.searchContractMould['search_button_loc'])
        base.staleness_of(apartmentContractPage.searchContractMould['tr_contract'])
        base.context_click(apartmentContractPage.searchContractMould['tr_contract'])
        base.click(apartmentContractPage.searchContractMould['delete_loc'])
        base.click(apartmentContractPage.addApartmentContractMould['delete_button_confirm'])
        base.check_submit()
        # 合同检查
        contractStatusSql = "select * from apartment_contract where deleted=1 and contract_num='%s' " % contractNum
        base.diffAssert(lambda test: asserts(sqlbase.waitData(contractStatusSql, 1)).is_true(), 1014,
                        u'%s:出租合同 %s 删除异常，执行SQL：%s' % (fileName, contractNum, contractStatusSql))

test_1014()