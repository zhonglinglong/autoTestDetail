# -*- coding:utf8 -*-

import time
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.apartmentContract.page import apartmentContractEndPage
from assertpy import assert_that as asserts

@log
def test_1017():
    """已终止合同发起结算"""

    # describe：已终止合同不能重复发起结算
    # data：合同已终止
    # result：终止结算提交失败

    fileName = 'apartmentContract_1017'
    contractSql = "select contract_num from apartment_contract where contract_status in ('COLLECTHOUSE','CORPORATE_DEFAULT','OWNER_DEFAULT','RETREATING','FORRENT') " \
                  "and city_code=330100 and deleted=0 and entrust_type='SHARE' order by rand() limit 1"
    if sqlbase.get_count(contractSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % contractSql)
        return
    info = sqlbase.serach(contractSql)
    contractNum = info[0]
    consoleLog(u'%s:取随机出租合同 %s 做终止' % (fileName, contractNum))

    with Base() as base:
        base.open(page.apartmentContractPage, apartmentContractEndPage.addContractEndMould['tr_contract'])
        base.input_text(apartmentContractEndPage.addContractEndMould['contract_num_loc'], contractNum)  # 输入合同编
        base.click(apartmentContractEndPage.addContractEndMould['search_button_loc'])  # 搜索
        base.staleness_of(apartmentContractEndPage.addContractEndMould['tr_contract'])  # 等待列表刷新
        base.context_click(apartmentContractEndPage.addContractEndMould['tr_contract'])  # 右击第一条数据
        base.click(apartmentContractEndPage.addContractEndMould['end_button_loc'], index=1)  # 终止结算
        time.sleep(1)
        message = base.script(
            "var a = $('.bootstrap-growl.alert.alert-info.alert-dismissible').text();return a",
            True)  # 获取提示信息
        messagehope = u'该合同已终止'
        base.diffAssert(lambda test: asserts(message).contains(messagehope),1017,
                        u'%s:出租合同 %s 终止结算异常，期望值 %s 实际值 %s' % (fileName, contractNum, messagehope, message))

test_1017()