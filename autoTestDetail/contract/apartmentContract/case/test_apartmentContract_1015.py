# -*- coding:utf8 -*-

import time
from assertpy import assert_that as asserts
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.apartmentContract.page import apartmentContractPage

@log
def test_1015():
    """出租合同反审"""

    # describe：出租合同反审后初审复审
    # data：已复审的出租合同
    # result：1.反审成功2.初审成功3.复审成功

    fileName = 'apartmentContract_1015'
    contractSql = "SELECT ac.contract_num,cp.urgent_customer_name,cp.customer_name from apartment_contract ac inner join customer_person cp on ac.person_id=cp.person_id " \
                  "where ac.deleted = 0 and ac.city_code = '330100' and ac.entrust_type='SHARE' and ac.audit_status = 'APPROVED' and ac.contract_status = 'EFFECTIVE' " \
                  "and ac.deleted=0 and payment_type='NORMAL' ORDER BY RAND() LIMIT 1"
    if sqlbase.get_count(contractSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % contractSql)
        return
    info = sqlbase.serach(contractSql)
    contractNum = info[0]
    consoleLog(u'%s:取随机已复审合同 %s 做合同反审' % (fileName, contractNum))

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
        # 反审
        base.click(apartmentContractPage.addApartmentContractMould['fanshen_loc'])  # 反审
        base.input_text(apartmentContractPage.addApartmentContractMould['contract_audit_content'], u'自动化反审意见')
        base.click(apartmentContractPage.addApartmentContractMould['contract_audit_confirm'])  # 确定
        base.check_submit()
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
        base.staleness_of(apartmentContractPage.searchContractMould['tr_contract'])  # 等待列表刷新
        base.dblclick(apartmentContractPage.searchContractMould['tr_contract'])  # 双击第一条数据
        for i in range(5):
            try:
                base.click(apartmentContractPage.addApartmentContractMould['tab_info_loc'], index=4)  # 租客详情
                break
            except:
                time.sleep(1)
        # 复审
        base.click(apartmentContractPage.addApartmentContractMould['fushen_loc'])  # 复审
        base.click(apartmentContractPage.addApartmentContractMould['contract_audit_confirm'])  # 确定
        base.staleness_of(apartmentContractPage.searchContractMould['tr_contract'])  # 等待列表刷新
        # 审核状态检查
        contractAuditSql ="select audit_status from apartment_contract where is_active='Y' and deleted=0 and contract_num='%s'" % contractNum
        contractAuditStatus = sqlbase.serach(contractAuditSql)[0]
        base.diffAssert(lambda test: asserts(contractAuditStatus).is_equal_to('APPROVED'),1015,
                        u'%s:出租合同 %s 审核后状态异常，期望值 APPROVED 实际值 %s' % (fileName, contractNum, contractAuditStatus))

test_1015()