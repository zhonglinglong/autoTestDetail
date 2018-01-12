# -*- coding:utf8 -*-

import time

from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.apartmentContract.page import apartmentContractEndPage,apartmentContractPage
from assertpy import assert_that as asserts

@log
def test_1018():
    """未复审出租合同发起结算"""

    # describe：未复审合同不能发起结算
    # data：未复审出租合同
    # result：终止失败

    fileName = 'apartmentContract_1018'
    contractSql = "SELECT ac.contract_num,cp.urgent_customer_name,cp.customer_name from apartment_contract ac inner join customer_person cp on ac.person_id=cp.person_id " \
                  "where ac.deleted = 0 and ac.city_code = '330100' and ac.entrust_type='SHARE' and ac.audit_status = 'AUDIT' and ac.contract_status = 'EFFECTIVE' " \
                  "and ac.deleted=0 and payment_type='NORMAL' ORDER BY RAND() LIMIT 1"
    if sqlbase.get_count(contractSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % contractSql)
        return
    info = sqlbase.serach(contractSql)
    contractNum = info[0]
    consoleLog(u'%s:取随机合同 %s 做合同终止' % (fileName, contractNum))

    with Base() as base:
        base.open(page.apartmentContractPage, apartmentContractPage.searchContractMould['tr_contract'])
        base.input_text(apartmentContractPage.searchContractMould['contract_num_loc'], contractNum)  # 输入合同编号
        base.click(apartmentContractPage.searchContractMould['search_button_loc'])
        base.staleness_of(apartmentContractPage.searchContractMould['tr_contract'])
        base.dblclick(apartmentContractPage.searchContractMould['tr_contract'])  # 双击第一条数据
        # 打开详情页需要加载，但DOM其实已经加载完仍旧无法点击，此处加5秒等待
        for i in range(5):
            try:
                base.click(apartmentContractPage.addApartmentContractMould['tab_info_loc'], index=4)  # 租客详情
                break
            except:
                time.sleep(1)
        # 初审
        base.click(apartmentContractPage.addApartmentContractMould['chushen_loc'])  # 初审
        base.click(apartmentContractPage.addApartmentContractMould['contract_audit_confirm'])  # 确定
        base.check_submit()
        base.click(apartmentContractEndPage.addContractEndMould['end_button_loc'])  # 终止结算
        time.sleep(1)
        message = base.script(
            "var a = $('.bootstrap-growl.alert.alert-info.alert-dismissible').text();return a",
            True)  # 获取提示信息
        messagehope = u'合同未复审不能终止结算'
        base.diffAssert(lambda test: asserts(message).contains(messagehope), 1018,
                        u'%s:出租合同 %s 终止结算异常，期望值 %s 实际值 %s' % (fileName, contractNum, messagehope, message))

test_1018()