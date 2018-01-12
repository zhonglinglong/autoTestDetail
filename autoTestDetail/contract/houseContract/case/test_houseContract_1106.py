# -*- coding:utf8 -*-

import time
from assertpy import assert_that as asserts
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.houseContract.page import houseContractEndPage


@log
def test_1106():
    """未复审委托合同做终止结算"""

    # describe：委托合同未复审无法做终止结算
    # data：1.委托合同未复审
    # result：1.终止结算失败

    fileName = 'apartmentContract_1106'
    contractSql = "select contract_num from house_contract where is_active='Y' and contract_status='EFFECTIVE' and audit_status<>'APPROVED' and deleted=0 and city_code=330100 order by rand() limit 1"
    if sqlbase.get_count(contractSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % contractSql)
        return
    info = sqlbase.serach(contractSql)
    contractNum = info[0]
    consoleLog(u'%s:取随机未复审委托合同 %s 做终止结算' % (fileName, contractNum))

    with Base() as base:
        base.open(page.entrustContractPage, houseContractEndPage.addContractEndMould['tr_contract'])
        base.input_text(houseContractEndPage.searchMould['contract_num_loc'], contractNum)  # 输入合同号
        base.click(houseContractEndPage.searchMould['contract_search_button_loc'])  # 搜索
        base.staleness_of(houseContractEndPage.addContractEndMould['tr_contract'])  # 等待数据刷新
        base.context_click(houseContractEndPage.addContractEndMould['tr_contract'])  # 右击第一条数据
        base.click(houseContractEndPage.addContractEndMould['end_button_loc'], index=1)  # 终止结算
        time.sleep(1)
        message = base.script(
            "var a = $('.panel.window.messager-window>div:nth-child(2)>div:nth-child(2)').text();return a",
            True)  # 获取提示信息
        messagehope = u'审核状态为“已审核”才可以发起终止结算'
        base.diffAssert(lambda test: asserts(message).is_equal_to(messagehope),1106,
                        u'%s:委托合同 %s 终止结算异常，期望值 %s 实际值 %s' % (fileName, contractNum, messagehope, message))

test_1106()