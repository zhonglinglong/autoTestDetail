# -*- coding:utf8 -*-

import time
from selenium.common.exceptions import InvalidElementStateException
from assertpy import assert_that as asserts
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.apartmentContract.page import apartmentContractPage

@log
def test_1006():
    """出租合同审核"""

    # describe：合同正常初审、复审
    # data：未初审的合同
    # result：1、初审后可以修改详情2、复审后不可以修改详情3、复审通过

    fileName = 'apartmentContract_1006'
    contractSql = "SELECT ac.contract_num,cp.urgent_customer_name,cp.customer_name from apartment_contract ac inner join customer_person cp on ac.person_id=cp.person_id " \
                  "inner join query_apartment_contract qac on ac.contract_num=qac.contract_num where ac.deleted = 0 and ac.city_code = '330100' and ac.entrust_type='SHARE' " \
                  "and ac.audit_status = 'AUDIT' and ac.contract_status = 'EFFECTIVE' and ac.deleted=0 and ac.payment_type='NORMAL' ORDER BY RAND() LIMIT 1"
    if sqlbase.get_count(contractSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % contractSql)
        return
    info = sqlbase.serach(contractSql)
    contractNum = info[0]
    consoleLog(u'%s:取随机合同 %s 做合同审核' % (fileName, contractNum))

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
        base.staleness_of(apartmentContractPage.searchContractMould['tr_contract'])  # 等待列表刷新
        base.dblclick(apartmentContractPage.searchContractMould['tr_contract'])  # 双击第一条数据
        for i in range(5):
            try:
                base.click(apartmentContractPage.addApartmentContractMould['tab_info_loc'], index=4)  # 租客详情
                break
            except:
                time.sleep(1)
        # 复审
        newUrgentName = u'NewUrgent'
        base.input_text(apartmentContractPage.addApartmentContractMould['urgent_customer_name_loc'], newUrgentName)  # 修改联系人
        base.click(apartmentContractPage.addApartmentContractMould['fushen_loc'])  # 复审
        base.click(apartmentContractPage.addApartmentContractMould['contract_audit_confirm'])  # 确定
        base.staleness_of(apartmentContractPage.searchContractMould['tr_contract'])  # 等待列表刷新
        # 审核状态检查
        contractAudit = "select ac.contract_num,cp.urgent_customer_name from apartment_contract ac ,customer_person cp where ac.person_id=cp.person_id AND ac.contract_num = '%s'AND ac.audit_status='APPROVED' " \
                        "and ac.is_active='Y' " % (contractNum)
        base.diffAssert(lambda test: asserts(sqlbase.waitData(contractAudit, 1)).is_true(), 1006,
                        u'%s:出租合同 %s 审核异常，执行SQL:%s' % (fileName, contractNum, contractAudit))
        # 紧急联系人检查
        realUrgentName = sqlbase.serach(contractAudit)[1]
        base.diffAssert(lambda test: asserts(realUrgentName).is_equal_to(newUrgentName), 1006,
                        u'%s:出租合同 %s 紧急联系人修改异常，期望值 %s 实际值 %s' % (fileName, contractNum, newUrgentName, realUrgentName))

        base.dblclick(apartmentContractPage.searchContractMould['tr_contract'])  # 双击第一条数据
        for i in range(5):
            try:
                base.click(apartmentContractPage.addApartmentContractMould['tab_info_loc'], index=4)  # 租客详情
                break
            except:
                time.sleep(1)
        try:
            base.input_text(apartmentContractPage.addApartmentContractMould['urgent_customer_name_loc'], 'AutoTest')  # 修改联系人
        except InvalidElementStateException:
            consoleLog(u'复审状态的合同紧急联系人无法编辑')

test_1006()