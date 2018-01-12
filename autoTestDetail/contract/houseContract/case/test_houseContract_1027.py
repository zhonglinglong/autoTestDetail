# -*- coding:utf8 -*-
import time

from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.houseContract.page import houseContractPage
from assertpy import assert_that as asserts

@log
def test_1027():
    """已续的合同不能续签"""

    # describe：已续的合同续签失败
    # data：原合同状态为已续
    # result：续签失败，提示已续的合同无法续签

    fileName = 'houseContract_1027'
    contractSql = "select contract_num from house_contract where contract_status='CONTINUED' AND is_active='Y' and deleted=0 order by rand() limit 1"
    if sqlbase.get_count(contractSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % contractSql)
        return
    contractNum = sqlbase.serach(contractSql)[0]
    consoleLog(u'%s:取已续签委托合同 %s 做续签' % (fileName, contractNum))

    with Base() as base:
        base.open(page.entrustContractPage, houseContractPage.contractSearchMould['tr_contract'])
        base.input_text(houseContractPage.contractSearchMould['contract_num_loc'], contractNum)
        base.click(houseContractPage.contractSearchMould['search_button_loc'])  # 搜索
        base.staleness_of(houseContractPage.contractSearchMould['tr_contract'])  # 等待列表刷新
        base.click(houseContractPage.addHouseContractMould['continue_button'])  # 续签
        time.sleep(1)
        message = base.script(
            "var a = $('.bootstrap-growl.alert.alert-info.alert-dismissible').text();return a",
            True)  # 获取提示信息
        messagehope = u'已续的合同不能续签'
        base.diffAssert(lambda test: asserts(message).contains(messagehope),1027,
                        u'%s:已续委托合同 %s 续签异常,期望信息"%s"实际信息"%s"' % (fileName, contractNum, messagehope, message))

test_1027()