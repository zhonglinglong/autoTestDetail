# -*- coding:utf8 -*-
import time

import time
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.houseContract.page import houseContractPage
from assertpy import assert_that as asserts

@log
def test_1031():
    """有有效出租合同的委托合同删除"""

    # describe：有有效出租合同的委托合同不能删除
    # data：1、委托合同状态为有效；2、委托合同下有至少一个有效状态的出租合同；
    # result：删除失败，提示有关联的出租合同不能删除

    fileName = 'houseContract_1031'
    contractSql = "select hc.contract_num ,h.house_code from house_contract hc inner join house h on h.house_id=hc.house_id where  EXISTS (select * from apartment_contract ac " \
                  "where hc.house_id=ac.house_id and ac.is_active='Y' and ac.deleted=0 )and hc.is_active='Y' and hc.deleted=0 and hc.city_code=330100  order by rand() limit 1"
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
        base.wait_element(houseContractPage.addHouseContractMould['message_loc'])  # 等待提示出现
        time.sleep(1)
        message = base.script(
            "var a = $('.panel.window.messager-window>div:nth-child(2)>div:nth-child(2)').text();return a",
            True)  # 获取提示信息
        messagehope = u'有关联的出租合同不能删除.'
        base.diffAssert(lambda test: asserts(message).is_equal_to(messagehope),1031,
                        u'%s:合同 %s 删除异常,期望信息"%s"实际信息"%s"' % (fileName, contractNum, messagehope, message))

test_1031()