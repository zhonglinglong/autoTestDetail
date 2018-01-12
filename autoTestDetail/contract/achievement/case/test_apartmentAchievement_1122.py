# -*- coding:utf8 -*-

import time
from assertpy import assert_that as asserts
from selenium.webdriver.common.keys import Keys
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.apartmentContract.page import apartmentContractEndPage

@log
def test_1122():
    """换租生成扣回业绩"""

    # describe：出租合同换租终止结算生成扣回业绩，记录同步到预估业绩排行榜
    # data：1、出租合同状态为有效；2、出租合同审核状态为已复审；
    # result：1、合同状态变为换租；2、生成一条扣回业绩，状态为未生效；3、扣回业绩分成记录插入到预估业绩排行榜；

    fileName = 'apartmentAchievement_1122'
    contractSql = "SELECT contract_num,rent_end_date,date(sysdate()) from apartment_contract where deleted = 0 and city_code = 330100 and audit_status = 'APPROVED' and contract_status = 'EFFECTIVE' " \
                    "and contract_type = 'NEWSIGN' and entrust_type = 'SHARE' and payment_type<>'NETWORKBANK' and rent_end_date>DATE_ADD(date(SYSDATE()),INTERVAL 1 MONTH)order by rand() limit 1"
    if sqlbase.get_count(contractSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % contractSql)
        return
    info = sqlbase.serach(contractSql)
    contractNum = info[0]
    consoleLog(u'%s:取随机出租合同 %s 做换租终止' % (fileName, contractNum))

    with Base() as base:
        breach_money = '888.88'  # 应收违约金
        zhuanzu_money = '666.66'  # 转租费
        base.open(page.apartmentContractPage, apartmentContractEndPage.addContractEndMould['tr_contract'])
        base.input_text(apartmentContractEndPage.addContractEndMould['contract_num_loc'], contractNum)  # 输入合同编
        base.click(apartmentContractEndPage.addContractEndMould['search_button_loc'])  # 搜索
        base.staleness_of(apartmentContractEndPage.addContractEndMould['tr_contract'])  # 等待列表刷新
        base.context_click(apartmentContractEndPage.addContractEndMould['tr_contract'])  # 右击第一条数据
        base.click(apartmentContractEndPage.addContractEndMould['end_button_loc'], index=1)  # 终止结算
        base.click(apartmentContractEndPage.addContractEndMould['now_end_loc'])  # 立即终止
        base.input_text(apartmentContractEndPage.addContractEndMould['end_reason_loc'], u'换租')  # 终止原因
        endNum = 'AutoACE' + '-' + time.strftime('%m%d%H%M')
        base.type_date(apartmentContractEndPage.typeMould['end_date'], info[2])  # 终止日期：当天
        base.type_select(apartmentContractEndPage.typeMould['end_type'], 'FORRENT')  # 换租
        base.input_text(apartmentContractEndPage.addContractEndMould['end_num_loc'], endNum)  # 终止协议号
        base.type_select(apartmentContractEndPage.typeMould['receipt_type_loc'], 'PAYER')  # 承租人
        base.type_select(apartmentContractEndPage.typeMould['pay_type_loc'], 'PERSONAL')  # 个人
        base.input_text(apartmentContractEndPage.addContractEndMould['receipt_num_loc'], '123456789')  # 收款卡号
        base.send_keys(apartmentContractEndPage.addContractEndMould['receipt_num_loc'], Keys.ENTER)
        base.click(apartmentContractEndPage.addContractEndMould['cardconfirm_close_loc'])  # 银行卡确认无误
        base.dblclick(apartmentContractEndPage.addContractEndMould['weiyuejin_loc'], index=12)  # 违约金
        base.input_text(apartmentContractEndPage.addContractEndMould['receivable_money_loc'], breach_money)  # 应收违约金
        base.dblclick(apartmentContractEndPage.addContractEndMould['weiyuejin_loc'], index=21)  # 转租费
        base.input_text(apartmentContractEndPage.addContractEndMould['zhuanzu_money_loc'], zhuanzu_money)  # 应收转租金
        base.upload_file(apartmentContractEndPage.addContractEndMould['add_end_image_loc'],
                         'C:\Users\Public\Pictures\Sample Pictures\jsp.jpg')  # 传图
        base.wait_element(apartmentContractEndPage.addContractEndMould['end_image_loc'])
        base.input_text(apartmentContractEndPage.addContractEndMould['remark_loc'], 'AutoTest')  # 备注
        base.click(apartmentContractEndPage.addContractEndMould['submit_button'])  # 提交
        base.check_submit()  # 等待提交完成
        contractEndAdd = "SELECT ace.end_contract_num FROM apartment_contract ac,apartment_contract_end ace WHERE ac.contract_id = ace.contract_id " \
                         "and ace.audit_status='NO_AUDIT' AND ace.end_type='FORRENT'and ace.deleted=0 and ac.contract_num='%s'" % contractNum
        base.diffAssert(lambda test: asserts(sqlbase.waitData(contractEndAdd,1)).is_true(),1122,
                        u'%s:出租合同 %s 终止结算新增异常，执行SQL：%s' % (fileName, contractNum, contractEndAdd))
        #合同状态检查
        contractStatus = sqlbase.serach("select contract_status from apartment_contract where deleted = 0 and contract_num='%s' " % contractNum)[0]
        base.diffAssert(lambda test: asserts(contractStatus).is_equal_to('FORRENT'), 1122,
                        u'%s:出租合同 %s 终止结算后状态异常异常，期望值 FORRENT 实际值 %s' % (fileName, contractNum, contractStatus))
        #扣回业绩检查
        backAchievementSql = "select is_active,achieve_id,accounting_time from back_achievement where contract_num='%s' and deleted=0 and contract_end_type='FORRENT' " % contractNum
        if sqlbase.waitData(backAchievementSql,1):
            backAchievementInfo = sqlbase.serach(backAchievementSql)
            base.diffAssert(lambda test: asserts(backAchievementInfo[0]).is_equal_to('N'), 1122,
                            u'%s:出租合同 %s 换租扣回业绩状态异常，期望值 N 实际值 %s' % (fileName, contractNum, backAchievementInfo[0]))
            # base.diffAssert(lambda test: asserts(breachAchievementInfo[1]).is_equal_to(breach_money), 1122,
            #                 u'%s:出租合同 %s 换租扣回业绩金额异常，期望值 %s 实际值 %s' % (fileName, contractNum, breach_money, breachAchievementInfo[1]))
        else:
            consoleLog(u'%s:出租合同 %s 换租终止生成扣回业绩异常，执行SQL：%s' % (fileName, contractNum, backAchievementSql))

        # 业绩分成明细表（预估业绩排行榜数据取值表,检查扣回业绩同步更新到预估业绩排行榜）
        backAchievementDetailSql = "select * from contract_achievement ca inner join apartment_contract ac on ac.contract_id=ca.contract_id and ca.achieve_id='%s' where ca.deleted=0 " \
                                   "and ca.contract_category='FORRENT_BACK'" % backAchievementInfo[1]
        achievementDetialConunt = sqlbase.get_count(backAchievementDetailSql)
        base.diffAssert(lambda test: asserts(achievementDetialConunt).is_not_equal_to(0), 1122,
                        u'%s:出租合同 %s 换租终止扣回业绩分成明细异常' % (fileName, contractNum))

test_1122()