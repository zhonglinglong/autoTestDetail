# -*- coding:utf8 -*-

import time
from assertpy import assert_that as asserts
from selenium.webdriver.common.keys import Keys
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.apartmentContract.page import apartmentContractEndPage

@log
def test_1089():
    """出租违约业绩删除"""

    # describe：出租违约业绩生成后删除终止结算，未审核的违约业绩会删除，同步到预估业绩排行榜
    # data：1、业绩状态未审核；2、终止结算未复审；
    # result：1、违约业绩删除；2、预估业绩排行榜中业绩删除；

    fileName = 'apartmentAchievement_1089'
    contractSql = "SELECT contract_num,rent_end_date,date(sysdate()) from apartment_contract where deleted = 0 and city_code = 330100 and audit_status = 'APPROVED' and contract_status = 'EFFECTIVE' " \
                    "and contract_type = 'NEWSIGN' and entrust_type = 'SHARE' and payment_type<>'NETWORKBANK' and rent_end_date>DATE_ADD(date(SYSDATE()),INTERVAL 1 MONTH)order by rand() limit 1"
    if sqlbase.get_count(contractSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % contractSql)
        return
    info = sqlbase.serach(contractSql)
    contractNum = info[0]
    consoleLog(u'%s:取随机出租合同 %s 做退租终止' % (fileName, contractNum))

    with Base() as base:
        breach_money = '888.88'  # 应收违约金
        zhuanzu_money = '999.99'  # 转租费
        base.open(page.apartmentContractPage, apartmentContractEndPage.addContractEndMould['tr_contract'])
        base.input_text(apartmentContractEndPage.addContractEndMould['contract_num_loc'], contractNum)  # 输入合同编
        base.click(apartmentContractEndPage.addContractEndMould['search_button_loc'])  # 搜索
        base.staleness_of(apartmentContractEndPage.addContractEndMould['tr_contract'])  # 等待列表刷新
        base.context_click(apartmentContractEndPage.addContractEndMould['tr_contract'])  # 右击第一条数据
        base.click(apartmentContractEndPage.addContractEndMould['end_button_loc'], index=1)  # 终止结算
        base.click(apartmentContractEndPage.addContractEndMould['now_end_loc'])  # 立即终止
        base.input_text(apartmentContractEndPage.addContractEndMould['end_reason_loc'], u'退租')  # 终止原因
        endNum = 'AutoACE' + '-' + time.strftime('%m%d%H%M')
        base.type_date(apartmentContractEndPage.typeMould['end_date'], info[2])  # 终止日期：当天
        base.type_select(apartmentContractEndPage.typeMould['end_type'], 'OWNER_DEFAULT')  # 退租
        base.input_text(apartmentContractEndPage.addContractEndMould['end_num_loc'], endNum)  # 终止协议号
        base.type_select(apartmentContractEndPage.typeMould['receipt_type_loc'], 'PAYER')  # 承租人
        base.type_select(apartmentContractEndPage.typeMould['pay_type_loc'], 'PERSONAL')  # 个人
        base.input_text(apartmentContractEndPage.addContractEndMould['receipt_num_loc'], '123456789')  # 收款卡号
        base.send_keys(apartmentContractEndPage.addContractEndMould['receipt_num_loc'], Keys.ENTER)
        base.click(apartmentContractEndPage.addContractEndMould['cardconfirm_close_loc'])  # 银行卡确认无误
        base.dblclick(apartmentContractEndPage.addContractEndMould['project_type_loc'], index=1)  # 租金
        base.input_text(apartmentContractEndPage.addContractEndMould['payable_deposit_loc'], '2000.00')  # 应退押金 终止收支类型为收入才能删除
        base.dblclick(apartmentContractEndPage.addContractEndMould['project_type_loc'], index=12)  # 违约金
        base.input_text(apartmentContractEndPage.addContractEndMould['receivable_money_loc'], breach_money)  # 应收违约金
        base.dblclick(apartmentContractEndPage.addContractEndMould['project_type_loc'], index=21)  # 转租费
        base.input_text(apartmentContractEndPage.addContractEndMould['zhuanzu_money_loc'], zhuanzu_money)  # 应收转租金
        base.upload_file(apartmentContractEndPage.addContractEndMould['add_end_image_loc'],
                         'C:\Users\Public\Pictures\Sample Pictures\jsp.jpg')  # 传图
        base.wait_element(apartmentContractEndPage.addContractEndMould['end_image_loc'])
        base.input_text(apartmentContractEndPage.addContractEndMould['remark_loc'], 'AutoTest')  # 备注
        base.click(apartmentContractEndPage.addContractEndMould['submit_button'])  # 提交
        base.check_submit()  # 等待提交完成
        # 违约业绩检查
        breachAchievementSql = "select is_active,accounting_money,achieve_id from breach_achievement where breach_num='%s' and deleted=0 and breach_type='OWNER_DEFAULT_BREACH'" % contractNum
        if sqlbase.waitData(breachAchievementSql,1):
            breachAchievementInfo = sqlbase.serach(breachAchievementSql)
        else:
            consoleLog(u'%s:出租合同 %s 退租终止生成违约业绩异常，执行SQL：%s' % (fileName, contractNum, breachAchievementSql))
        # 删除终止结算
        base.open(page.contractEndPage, apartmentContractEndPage.searchMould['tr_contract_end'])
        base.input_text(apartmentContractEndPage.searchMould['contract_num_loc'], contractNum)
        base.click(apartmentContractEndPage.searchMould['search_button_loc'])
        base.staleness_of(apartmentContractEndPage.searchMould['tr_contract_end'])
        base.click(apartmentContractEndPage.addContractEndMould['delete_button'])
        base.click(apartmentContractEndPage.addContractEndMould['delete_button_confirm'])
        base.check_submit()
        # 检查业绩删除
        breachAchievementDelSql = "select is_active,accounting_money,achieve_id from breach_achievement where achieve_id='%s' and deleted=0 and breach_type='OWNER_DEFAULT_BREACH'" % breachAchievementInfo[2]
        achievementDelConunt = sqlbase.get_count(breachAchievementDelSql)
        base.diffAssert(lambda test: asserts(achievementDelConunt).is_equal_to(0), 1089,
                        u'%s:出租合同 %s 违约业绩删除异常，执行SQL：%s' % (fileName, contractNum, breachAchievementDelSql))
        # 业绩分成明细表（预估业绩排行榜数据取值表,检查违约业绩同步更新到预估业绩排行榜）
        breahAchievementDetailSql = "select * from contract_achievement_detail where achieve_id='%s' and deleted=0" % breachAchievementInfo[2]
        achievementDetialDelConunt = sqlbase.get_count(breahAchievementDetailSql)
        base.diffAssert(lambda test: asserts(achievementDetialDelConunt).is_equal_to(0), 1089,
                        u'%s:出租合同 %s 违约业绩分成明细删除异常' % (fileName, contractNum))

test_1089()