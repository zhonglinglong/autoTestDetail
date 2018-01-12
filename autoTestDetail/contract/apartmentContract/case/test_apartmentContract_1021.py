# -*- coding:utf8 -*-

import datetime
import time

from selenium.webdriver.common.keys import Keys

from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.apartmentContract.page import apartmentContractEndPage
from assertpy import assert_that as asserts

@log
def test_1021():
    """出租合同转租终止"""

    # describe：检测预约终止结算功能
    # data：1.合同已复审2.合同不是已续3.终止类型为转租
    # result：终止结算提交成功

    fileName = 'apartmentContract_1021'
    contractSql = "SELECT contract_num,rent_end_date from apartment_contract where deleted = 0 and city_code = 330100 and audit_status = 'APPROVED' and contract_status = 'EFFECTIVE' " \
          "and contract_type = 'NEWSIGN' and entrust_type = 'SHARE' and payment_type<>'NETWORKBANK' order by rand() limit 1"
    if sqlbase.get_count(contractSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % contractSql)
        return
    info = sqlbase.serach(contractSql)
    contractNum = info[0]
    consoleLog(u'%s:取随机出租合同 %s 做转租终止' % (fileName, contractNum))

    with Base() as base:
        base.open(page.apartmentContractPage, apartmentContractEndPage.addContractEndMould['tr_contract'])
        base.input_text(apartmentContractEndPage.addContractEndMould['contract_num_loc'], contractNum)  # 输入合同编号
        today = datetime.date.today()
        base.click(apartmentContractEndPage.addContractEndMould['search_button_loc'])  # 搜索
        base.staleness_of(apartmentContractEndPage.addContractEndMould['tr_contract'])  # 等待列表刷新
        base.context_click(apartmentContractEndPage.addContractEndMould['tr_contract'])  # 右击第一条数据
        base.click(apartmentContractEndPage.addContractEndMould['end_button_loc'], index=1)  # 终止结算
        base.click(apartmentContractEndPage.addContractEndMould['now_end_loc'])  # 立即终止
        base.input_text(apartmentContractEndPage.addContractEndMould['end_reason_loc'], u'退租')  # 终止原因
        base.type_date(apartmentContractEndPage.typeMould['end_date'], today)  # 终止日期：当天
        endNum = 'AutoACE' + '-' + time.strftime('%m%d%H%M')
        base.type_select(apartmentContractEndPage.typeMould['end_type'], 'CORPORATE_DEFAULT')  # 转租
        base.input_text(apartmentContractEndPage.addContractEndMould['end_num_loc'], endNum)  # 终止协议号
        base.type_select(apartmentContractEndPage.typeMould['receipt_type_loc'], 'PAYER')  # 承租人
        base.type_select(apartmentContractEndPage.typeMould['pay_type_loc'], 'PERSONAL')  # 个人
        base.input_text(apartmentContractEndPage.addContractEndMould['receipt_num_loc'], '123456789')  # 收款卡号
        base.send_keys(apartmentContractEndPage.addContractEndMould['receipt_num_loc'], Keys.ENTER)
        base.click(apartmentContractEndPage.addContractEndMould['cardconfirm_close_loc'])  # 银行卡确认无误
        base.dblclick(apartmentContractEndPage.addContractEndMould['weiyuejin_loc'], index=12)  # 违约金
        base.input_text(apartmentContractEndPage.addContractEndMould['receivable_money_loc'], '888.88')  # 应收违约金
        base.input_text(apartmentContractEndPage.addContractEndMould['payable_money_loc'], '666.66')  # 应退违约金
        base.upload_file(apartmentContractEndPage.addContractEndMould['add_end_image_loc'],
                         'C:\Users\Public\Pictures\Sample Pictures\jsp.jpg')  # 传图
        base.wait_element(apartmentContractEndPage.addContractEndMould['end_image_loc'])
        base.input_text(apartmentContractEndPage.addContractEndMould['remark_loc'], 'AutoTest')  # 备注
        base.script('$("#form_submit_btn").click()')  # 提交
        base.check_submit()  # 等待提交完成
        contractEndAdd="SELECT * FROM apartment_contract ac,apartment_contract_end ace WHERE ac.contract_id = ace.contract_id and ace.audit_status='NO_AUDIT' " \
                       "AND ace.end_type='CORPORATE_DEFAULT'and ace.deleted=0 and ace.end_contract_num='%s'" % endNum
        base.diffAssert(lambda test: asserts(sqlbase.waitData(contractEndAdd, 1)).is_true(), 1021,
                        u'%s:出租合同 %s 预约终止结算新增异常，执行SQL：%s' % (fileName, contractNum, contractEndAdd))

test_1021()