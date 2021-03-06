# -*- coding:utf8 -*-
import time

from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.houseContract.page import houseContractPage
from assertpy import assert_that as asserts
import time

@log
def test_1035():
    """已终止的合同不能删除"""

    # describe：已终止的合同不能删除
    # data：1、合同状态为公司违约或者业主违约或者正退；2.名下无出租合同
    # result：删除失败，委托合同为终止状态不能删除

    fileName = 'houseContract_1035'
    contractSql = "select hc.contract_num ,h.house_code from house_contract hc inner join house h on h.house_id=hc.house_id where hc.contract_status='OWNER_DEFAULT' " \
                  "and hc.deleted=0 and hc.city_code=330100 and not EXISTS (select * from apartment_contract ac where hc.house_id=ac.house_id)order by rand() limit 1"
    if sqlbase.get_count(contractSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % contractSql)
        return
    contractInfo = sqlbase.serach(contractSql)
    contractNum = contractInfo[0]
    consoleLog(u'%s:取已终止委托合同 %s 做删除' % (fileName, contractNum))

    with Base() as base:
        base.open(page.entrustContractPage, houseContractPage.contractSearchMould['tr_contract'])
        base.input_text(houseContractPage.contractSearchMould['residential_name_loc'], contractInfo[1])
        base.input_text(houseContractPage.contractSearchMould['contract_num_loc'], contractNum)
        base.click(houseContractPage.contractSearchMould['search_button_loc'])
        base.staleness_of(houseContractPage.contractSearchMould['tr_contract'])
        base.click(houseContractPage.addHouseContractMould['delete_button'])
        base.click(houseContractPage.addHouseContractMould['delete_button_confirm'])
        base.wait_element(houseContractPage.addHouseContractMould['message_loc'])  # 等待提示出现
        time.sleep(1)
        message = base.script(
            "var a = $('.panel.window.messager-window>div:nth-child(2)>div:nth-child(2)').text();return a",
            True)  # 获取提示信息
        messagehope = u'委托合同为终止状态不能删除.'
        base.diffAssert(lambda test: asserts(message).is_equal_to(messagehope),1035,
                        u'%s:已终止委托合同 %s 删除异常,期望信息"%s"实际信息"%s"' % (fileName, contractNum, messagehope, message))

test_1035()