# -*- coding:utf8 -*-
import time

from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.apartmentContract.page import apartmentContractEndPage
from contract.apartmentContract.page import apartmentContractPage
from assertpy import assert_that as asserts

@log
def test_1022():
    """合同终止结算已复审删除"""

    # describe：合同终止结算已复审不能删除
    # data：合同终止结算已复审
    # result：删除失败

    fileName = 'apartmentContract_1022'
    contractSql = "select ac.contract_num from apartment_contract_end ace inner join apartment_contract ac on ace.contract_id=ac.contract_id " \
                  "and ac.city_code=330100 where ace.deleted=0 and ace.audit_status='REVIEW'  order by rand() limit 1"
    if sqlbase.get_count(contractSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % contractSql)
        return
    info = sqlbase.serach(contractSql)
    contractNum = info[0]
    consoleLog(u'%s:取随机终止结算合同 %s 做删除' % (fileName, contractNum))

    with Base() as base:
        base.open(page.contractEndPage, apartmentContractEndPage.searchMould['tr_contract_end'])
        base.input_text(apartmentContractEndPage.searchMould['contract_num_loc'], contractNum)
        base.click(apartmentContractEndPage.searchMould['search_button_loc'])
        base.staleness_of(apartmentContractEndPage.searchMould['tr_contract_end'])
        base.click(apartmentContractEndPage.addContractEndMould['delete_button'])
        base.click(apartmentContractEndPage.addContractEndMould['delete_button_confirm'])
        base.wait_element(apartmentContractPage.searchContractMould['message_loc'])  # 等待提示出现
        time.sleep(1)
        message = base.script(
            "var a = $('.panel.window.messager-window>div:nth-child(2)>div:nth-child(2)').text();return a",
            True)  # 获取提示信息
        messagehope = u'终止结算已审核，不可删除'
        base.diffAssert(lambda test: asserts(message).contains(messagehope),1022,
                        u'%s:出租合同 %s 终止结算删除异常，期望值 %s 实际值 %s' % (fileName, contractNum, messagehope, message))

test_1022()