# -*- coding:utf8 -*-

import time
from assertpy import assert_that as asserts
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.houseContract.page import houseContractEndPage

@log
def test_1110():
    """委托终止结算已审核删除"""

    # describe：委托终止结算已审核的删除失败
    # data：1、委托终止结算已审核
    # result：1、删除失败

    fileName = 'apartmentContract_1110'
    contractSql = "select hc.contract_num from house_contract_end hce,house_contract hc where hc.contract_id=hce.contract_id and hce.deleted=0 and hce.audit_status='REVIEW' " \
                  "and hc.city_code=330100  order by rand() limit 1"
    if sqlbase.get_count(contractSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % contractSql)
        return
    info = sqlbase.serach(contractSql)
    contractNum = info[0]
    consoleLog(u'%s:取合同 %s 终止结算做审核' % (fileName, contractNum))

    with Base() as base:
        # 删除终止结算
        base.open(page.contractEndPage, houseContractEndPage.searchMould['contract_search_button_loc'])
        base.click(houseContractEndPage.addContractEndMould['tab_info'], index=1)
        base.input_text(houseContractEndPage.searchMould['end_contract_num_loc'], contractNum)
        base.click(houseContractEndPage.searchMould['end_search_button_loc'])
        base.staleness_of(houseContractEndPage.searchMould['tr_contract_end'])
        base.click(houseContractEndPage.addContractEndMould['delete_button'])
        base.click(houseContractEndPage.addContractEndMould['delete_button_confirm'])
        time.sleep(1)
        message = base.script(
            "var a = $('.panel.window.messager-window>div:nth-child(2)>div:nth-child(2)').text();return a",
            True)  # 获取提示信息
        messagehope = u'终止结算已审核，不可删除'
        base.diffAssert(lambda test: asserts(message).contains(messagehope),1110,
                        u'%s:委托合同 %s 终止结算异常，期望值 %s 实际值 %s' % (fileName, contractNum, messagehope, message))
test_1110()