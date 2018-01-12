# -*- coding:utf8 -*-
import time

from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.apartmentContract.page import apartmentContractPage
from assertpy import assert_that as asserts

@log
def test_1012():
    """出租合同已有实收"""

    # describe：出租合同有实收不能删除
    # data：出租合同已有实收
    # result：删除失败

    fileName = 'apartmentContract_1012'
    contractSql = "select ac.contract_num from apartment_contract ac inner join apartment_contract_receipts acr on ac.contract_id=acr.contract_id " \
                  "where ac.deleted=0 and ac.is_active='Y'  and ac.city_code=330100 and ac.entrust_type='SHARE' ORDER BY RAND() LIMIT 1"
    if sqlbase.get_count(contractSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % contractSql)
        return
    info = sqlbase.serach(contractSql)
    contractNum = info[0]
    consoleLog(u'%s:取随机实收出租合同 %s 做合同删除' % (fileName, contractNum))

    with Base() as base:
        base.open(page.apartmentContractPage, apartmentContractPage.searchContractMould['tr_contract'])
        base.input_text(apartmentContractPage.searchContractMould['contract_num_loc'], contractNum)  # 输入合同编号
        base.click(apartmentContractPage.searchContractMould['search_button_loc'])
        base.staleness_of(apartmentContractPage.searchContractMould['tr_contract'])
        base.context_click(apartmentContractPage.searchContractMould['tr_contract'])
        base.click(apartmentContractPage.searchContractMould['delete_loc']) # 删除
        base.click(apartmentContractPage.addApartmentContractMould['delete_button_confirm'])
        base.wait_element(apartmentContractPage.searchContractMould['message_loc'])  # 等待提示出现
        time.sleep(1)
        message = base.script(
            "var a = $('.panel.window.messager-window>div:nth-child(2)>div:nth-child(2)').text();return a",
            True)  # 获取提示信息
        messagehope = u'请财务先重置并删除收款信息'
        base.diffAssert(lambda test: asserts(message).is_equal_to(messagehope),1012,
                        u'%s:出租合同 %s 删除异常，期望值 %s 实际值 %s' % (fileName, contractNum, messagehope, message))

test_1012()