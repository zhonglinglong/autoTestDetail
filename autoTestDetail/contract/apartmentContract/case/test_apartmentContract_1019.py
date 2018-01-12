# -*- coding:utf8 -*-

import time
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.apartmentContract.page import apartmentContractEndPage,apartmentContractPage
from assertpy import assert_that as asserts

@log
def test_1019():
    """未复审出租合同发起结算"""

    # describe：未复审合同不能发起结算
    # data：未复审出租合同
    # result：终止失败

    fileName = 'apartmentContract_1019'
    contractSql = "select contract_num from apartment_contract where contract_status='CONTINUED' " \
                  "and city_code=330100 and deleted=0 and entrust_type='SHARE' ORDER BY RAND() LIMIT 1"
    if sqlbase.get_count(contractSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % contractSql)
        return
    info = sqlbase.serach(contractSql)
    contractNum = info[0]
    consoleLog(u'%s:取随机已续合同 %s 做合同终止' % (fileName, contractNum))

    with Base() as base:
        base.open(page.apartmentContractPage, apartmentContractPage.searchContractMould['tr_contract'])
        base.input_text(apartmentContractPage.searchContractMould['contract_num_loc'], contractNum)  # 输入合同编号
        base.click(apartmentContractPage.searchContractMould['search_button_loc'])
        base.staleness_of(apartmentContractPage.searchContractMould['tr_contract'])
        base.click(apartmentContractEndPage.addContractEndMould['end_button_loc'])  # 终止结算
        time.sleep(1)
        message = base.script(
            "var a = $('.bootstrap-growl.alert.alert-info.alert-dismissible').text();return a",
            True)  # 获取提示信息
        messagehope = u'续签的合同不能终止结算'
        base.diffAssert(lambda test: asserts(message).contains(messagehope), 1019,
                        u'%s:出租合同 %s 终止结算异常，期望值 %s 实际值 %s' % (fileName, contractNum, messagehope, message))

test_1019()