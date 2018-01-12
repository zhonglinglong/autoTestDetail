# -*- coding:utf8 -*-
import time

from selenium.webdriver.common.keys import Keys

from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.apartmentContract.page import apartmentContractPage
from contract.apartmentContract.page import apartmentContractEndPage
from assertpy import assert_that as asserts

@log
def test_1016():
    """出租合同正退终止结算"""

    # describe：检测合同终止为正退,初审复审反审驳回删除
    # data：1.合同已复审2.合同不是已续
    # result：终止结算提交成功，驳回初审复审反审删除成功

    fileName = 'apartmentContract_1016'
    contractSql = "SELECT contract_num,rent_end_date from apartment_contract where deleted = 0 and city_code = 330100 and audit_status = 'APPROVED' and contract_status = 'EFFECTIVE' " \
                    "and contract_type = 'NEWSIGN' and entrust_type = 'SHARE' and payment_type<>'NETWORKBANK' order by rand() limit 1"
    if sqlbase.get_count(contractSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % contractSql)
        return
    info = sqlbase.serach(contractSql)
    contractNum = info[0]
    consoleLog(u'%s:取随机出租合同 %s 做正退终止' % (fileName, contractNum))

    with Base() as base:
        base.open(page.apartmentContractPage, apartmentContractEndPage.addContractEndMould['tr_contract'])
        base.input_text(apartmentContractEndPage.addContractEndMould['contract_num_loc'], contractNum)  # 输入合同编
        base.click(apartmentContractEndPage.addContractEndMould['search_button_loc'])  # 搜索
        base.staleness_of(apartmentContractEndPage.addContractEndMould['tr_contract'])  # 等待列表刷新
        base.context_click(apartmentContractEndPage.addContractEndMould['tr_contract'])  # 右击第一条数据
        base.click(apartmentContractEndPage.addContractEndMould['end_button_loc'], index=1)  # 终止结算
        base.click(apartmentContractEndPage.addContractEndMould['now_end_loc'])  # 立即终止
        base.input_text(apartmentContractEndPage.addContractEndMould['end_reason_loc'], u'承租周期已完')  # 终止原因
        endNum = 'AutoACE' + '-' + time.strftime('%m%d%H%M')
        base.type_date(apartmentContractEndPage.typeMould['end_date'], info[1])  # 终止日期：承租到期日
        base.type_select(apartmentContractEndPage.typeMould['end_type'], 'RETREATING')  # 正退租
        base.type_select(apartmentContractEndPage.typeMould['receipt_type_loc'], 'PAYER')  # 承租人
        base.type_select(apartmentContractEndPage.typeMould['pay_type_loc'], 'PERSONAL')  # 个人
        base.input_text(apartmentContractEndPage.addContractEndMould['receipt_num_loc'], '123456789')  # 收款卡号
        base.send_keys(apartmentContractEndPage.addContractEndMould['receipt_num_loc'], Keys.ENTER)
        base.click(apartmentContractEndPage.addContractEndMould['cardconfirm_close_loc'])  # 银行卡确认无误
        base.dblclick(apartmentContractEndPage.addContractEndMould['weiyuejin_loc'], index=12)  # 违约金
        base.input_text(apartmentContractEndPage.addContractEndMould['receivable_money_loc'], '888.88')  # 应收违约金
        base.input_text(apartmentContractEndPage.addContractEndMould['payable_money_loc'], '999.99')  # 应退违约金
        base.input_text(apartmentContractEndPage.addContractEndMould['remark_loc'], 'AutoTest')  # 备注
        base.click(apartmentContractEndPage.addContractEndMould['submit_button'])  # 提交
        base.check_submit()  # 等待提交完成
        contractEndAdd = "SELECT ace.end_contract_num FROM apartment_contract ac,apartment_contract_end ace WHERE ac.contract_id = ace.contract_id " \
                         "and ace.audit_status='NO_AUDIT' AND ace.end_type='RETREATING'and ace.deleted=0 and ac.contract_num='%s'" % contractNum
        base.diffAssert(lambda test: asserts(sqlbase.waitData(contractEndAdd,1)).is_true(), 1016,
                        u'%s:出租合同 %s 终止结算新增异常，执行SQL：%s' % (fileName, contractNum, contractEndAdd))
        base.open(page.contractEndPage, apartmentContractEndPage.searchMould['tr_contract_end'], havaFrame=False)
        base.input_text(apartmentContractEndPage.searchMould['contract_num_loc'], contractNum)  # 输入合同号
        base.click(apartmentContractEndPage.searchMould['search_button_loc'])  # 搜索
        base.staleness_of(apartmentContractEndPage.searchMould['tr_contract_end'])  # 等待列表刷新
        base.dblclick(apartmentContractEndPage.searchMould['tr_contract_end'])  # 双击第一条数据
        # 驳回
        base.click(apartmentContractEndPage.addContractEndMould['bohui_loc'])  # 驳回
        base.input_text(apartmentContractEndPage.addContractEndMould['contract_audit_content'], u'AutoTest') #驳回意见
        base.click(apartmentContractEndPage.addContractEndMould['contract_audit_confirm'])  # 确定
        base.check_submit()
        base.dblclick(apartmentContractEndPage.searchMould['tr_contract_end'])  # 双击第一条数据
        # 初审
        base.click(apartmentContractEndPage.addContractEndMould['chushen_loc'])  # 初审
        base.click(apartmentContractEndPage.addContractEndMould['contract_audit_confirm'])  # 确定
        base.check_submit()
        base.dblclick(apartmentContractEndPage.searchMould['tr_contract_end'])  # 双击第一条数据
        # 复审
        base.click(apartmentContractEndPage.addContractEndMould['fushen_loc'])  # 复审
        base.click(apartmentContractEndPage.addContractEndMould['contract_audit_confirm'])  # 确定
        base.check_submit()
        contractEndAud = "SELECT ace.audit_status FROM apartment_contract ac,apartment_contract_end ace WHERE ac.contract_id = ace.contract_id " \
                         "AND ace.end_type='RETREATING'and ace.deleted=0 and ac.contract_num='%s'" % contractNum
        contractEndStatus = sqlbase.serach(contractEndAud)[0]
        base.diffAssert(lambda test: asserts(contractEndStatus).is_equal_to('REVIEW'), 1016,
                        u'%s:出租合同 %s 终止结算状态异常，期望值 REVIEW 实际值 %s' % (fileName, contractNum, contractEndStatus))
        # 反审
        base.dblclick(apartmentContractEndPage.searchMould['tr_contract_end'])  # 双击第一条数据
        base.click(apartmentContractEndPage.addContractEndMould['fanshen_loc'])  # 反审
        base.input_text(apartmentContractEndPage.addContractEndMould['contract_audit_content'], u'AutoTest')  # 反审意见
        base.click(apartmentContractEndPage.addContractEndMould['contract_audit_confirm'])  # 确定
        base.check_submit()
        contractEndRaud = "SELECT ace.audit_status FROM apartment_contract ac,apartment_contract_end ace WHERE ac.contract_id = ace.contract_id " \
                         "AND ace.end_type='RETREATING' and ace.deleted=0 and ac.contract_num='%s'" % contractNum
        contractEndRaudStatus = sqlbase.serach(contractEndRaud)[0]
        base.diffAssert(lambda test: asserts(contractEndRaudStatus).is_equal_to('NO_AUDIT'), 1016,
                        u'%s:出租合同 %s 终止结算状态异常，期望值 NO_AUDIT 实际值 %s' % (fileName, contractNum, contractEndRaudStatus))
        base.click(apartmentContractEndPage.addContractEndMould['delete_button'])
        base.click(apartmentContractEndPage.addContractEndMould['delete_button_confirm'])
        base.check_submit()
        # 终止结算检查
        contractEndDeSql = "select * from apartment_contract_end ace inner join apartment_contract ac on ace.contract_id=ac.contract_id and ac.contract_num='%s' where ace.deleted=1 and " \
                           "ace.end_type='RETREATING'" % contractNum
        base.diffAssert(lambda test: asserts(sqlbase.waitData(contractEndDeSql,1)).is_true(), 1016,
                        u'%s:出租合同 %s 终止结算删除异常，执行SQL：%s' % (fileName, contractNum, contractEndDeSql))

test_1016()