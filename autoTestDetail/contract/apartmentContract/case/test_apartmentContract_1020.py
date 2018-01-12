# -*- coding:utf8 -*-

import datetime
from assertpy import assert_that as asserts
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.apartmentContract.page import apartmentContractEndPage

@log
def test_1020():
    """出租合同预约终止结算"""

    # describe：检测预约终止结算功能
    # data：1.合同已复审2.合同不是已续3.终止类型为退租
    # result：终止结算提交成功

    fileName = 'apartmentContract_1020'
    contractSql = "SELECT contract_num,rent_end_date from apartment_contract where deleted = 0 and city_code = 330100 and audit_status = 'APPROVED' and contract_status = 'EFFECTIVE' " \
          "and contract_type = 'NEWSIGN' and entrust_type = 'SHARE' and payment_type<>'NETWORKBANK' order by rand() limit 1"
    if sqlbase.get_count(contractSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % contractSql)
        return
    info = sqlbase.serach(contractSql)
    contractNum = info[0]
    consoleLog(u'%s:取随机出租合同 %s 做退租预终止' % (fileName, contractNum))

    with Base() as base:
        base.open(page.apartmentContractPage, apartmentContractEndPage.addContractEndMould['tr_contract'])
        base.input_text(apartmentContractEndPage.addContractEndMould['contract_num_loc'], contractNum)  # 输入合同编号
        today = datetime.date.today()
        base.click(apartmentContractEndPage.addContractEndMould['search_button_loc'])  # 搜索
        base.staleness_of(apartmentContractEndPage.addContractEndMould['tr_contract'])  # 等待列表刷新
        base.context_click(apartmentContractEndPage.addContractEndMould['tr_contract'])  # 右击第一条数据
        base.click(apartmentContractEndPage.addContractEndMould['end_button_loc'], index=1)  # 终止结算
        base.click(apartmentContractEndPage.addContractEndMould['before_end_loc'])  # 预约终止
        base.click(apartmentContractEndPage.addContractEndMould['before_end_continue_loc'])  # 继续
        base.wait_element(apartmentContractEndPage.addContractEndMould['apartment_num_loc'])
        base.type_select(apartmentContractEndPage.typeMould['end_type'], 'OWNER_DEFAULT')  # 退租
        base.type_date(apartmentContractEndPage.typeMould['end_date'], today)  # 终止日期：当天
        base.click(apartmentContractEndPage.addContractEndMould['submit_button_loc'])  # 提交
        base.check_submit()  # 等待提交完成
        contractEndAdd="SELECT * FROM apartment_contract ac,apartment_contract_end ace WHERE ac.contract_id = ace.contract_id and ace.audit_status='NO_AUDIT' " \
                       "AND ace.end_type='OWNER_DEFAULT'and ace.deleted=0 and ace.contract_end_type='PREEND' and ac.contract_num='%s'" % contractNum
        base.diffAssert(lambda test: asserts(sqlbase.waitData(contractEndAdd, 1)).is_true(), 1020,
                        u'%s:出租合同 %s 预约终止结算新增异常，执行SQL：%s' % (fileName, contractNum, contractEndAdd))

test_1020()