# -*- coding:utf8 -*-

import time
from assertpy import assert_that as asserts
from selenium.webdriver.common.keys import Keys
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.achievement.page import apartmentAchievementPage
from contract.apartmentContract.page import apartmentContractEndPage

@log
def test_1076():
    """修改出租终止类型退租变转租"""

    # describe：出租合同转租终止结算改成退租，修改转租费输入6666，同步到业绩中
    # data：1、出租终止类型为转租；2、出租终止结算未复审；3、业绩状态未审核；
    # result：1、业绩金额变为6666；2、业绩违约类型变为转租；3、分成人业绩同步变化；4、预估业绩排行榜同步更新；

    fileName = 'apartmentAchievement_1076'
    contractSql = "SELECT contract_num,rent_end_date,date(sysdate()) from apartment_contract where deleted = 0 and city_code = 330100 and audit_status = 'APPROVED' and contract_status = 'EFFECTIVE' " \
                    "and contract_type = 'NEWSIGN' and entrust_type = 'SHARE' and payment_type<>'NETWORKBANK' and rent_end_date>DATE_ADD(date(SYSDATE()),INTERVAL 1 MONTH)order by rand() limit 1"
    if sqlbase.get_count(contractSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % contractSql)
        return
    info = sqlbase.serach(contractSql)
    contractNum = info[0]
    consoleLog(u'%s:取随机出租合同 %s 做退租终止改转租终止' % (fileName, contractNum))

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
        base.dblclick(apartmentContractEndPage.addContractEndMould['weiyuejin_loc'], index=12)  # 违约金
        base.input_text(apartmentContractEndPage.addContractEndMould['receivable_money_loc'], breach_money)  # 应收违约金
        base.dblclick(apartmentContractEndPage.addContractEndMould['weiyuejin_loc'], index=21)  # 转租费
        base.input_text(apartmentContractEndPage.addContractEndMould['zhuanzu_money_loc'], zhuanzu_money)  # 应收转租金
        base.upload_file(apartmentContractEndPage.addContractEndMould['add_end_image_loc'],'C:\Users\Public\Pictures\Sample Pictures\jsp.jpg')  # 传图
        base.wait_element(apartmentContractEndPage.addContractEndMould['end_image_loc'])
        base.input_text(apartmentContractEndPage.addContractEndMould['remark_loc'], 'AutoTest')  # 备注
        base.click(apartmentContractEndPage.addContractEndMould['submit_button'])  # 提交
        base.check_submit()  # 等待提交完成
        # 违约业绩检查
        breachAchievementSql = "select is_active,accounting_money,achieve_id from breach_achievement where breach_num='%s' and deleted=0 and breach_type='OWNER_DEFAULT_BREACH'" % contractNum
        if sqlbase.waitData(breachAchievementSql, 1):
            breachAchievementInfo = sqlbase.serach(breachAchievementSql)
            base.diffAssert(lambda test: asserts(breachAchievementInfo[1]).is_equal_to(breach_money), 1076,
                            u'%s:出租合同 %s 转租违约业绩金额异常，期望值 %s 实际值 %s' % (fileName, contractNum, breach_money, breachAchievementInfo[1]))
        else:
            consoleLog(u'%s:出租合同 %s 转租终止生成违约业绩异常，执行SQL：%s' % (fileName, contractNum, breachAchievementSql))
        #修改终止结算类型和转租费
        base.open(page.contractEndPage, apartmentContractEndPage.searchMould['tr_contract_end'])
        base.input_text(apartmentContractEndPage.searchMould['contract_num_loc'], contractNum)  # 输入合同号
        base.click(apartmentContractEndPage.searchMould['search_button_loc'])  # 搜索
        base.staleness_of(apartmentContractEndPage.searchMould['tr_contract_end'])  # 等待列表刷新
        base.dblclick(apartmentContractEndPage.searchMould['tr_contract_end'])  # 双击第一条数据
        zhuanzu_money_new = '6666.00'
        base.input_text(apartmentContractEndPage.addContractEndMould['remark_loc'], 'AutoTest2')  # 备注
        base.dblclick(apartmentContractEndPage.addContractEndMould['weiyuejin_loc'], index=21)  # 转租费
        base.type_select(apartmentContractEndPage.typeMould['end_type'], 'CORPORATE_DEFAULT')  # 改成转租
        base.input_text(apartmentContractEndPage.addContractEndMould['zhuanzu_money_loc'], zhuanzu_money_new)  # 应收转租金
        base.click(apartmentContractEndPage.addContractEndMould['save_button']) # 保存
        base.check_submit()
        breachAchievementNewSql = "select is_active,accounting_money,achieve_id from breach_achievement where breach_num='%s' and deleted=0 and breach_type='CUSTOMER_SUBLET'" % contractNum
        if sqlbase.waitData(breachAchievementNewSql, 1):
            breachAchievementNewInfo = sqlbase.serach(breachAchievementNewSql)
            base.diffAssert(lambda test: asserts(breachAchievementNewInfo[1]).is_equal_to(zhuanzu_money_new), 1076,
                            u'%s:出租合同 %s 违约业绩金额异常，期望值 %s 实际值 %s' % (fileName, contractNum, zhuanzu_money_new, breachAchievementNewInfo[1]))
        else:
            consoleLog(u'%s:出租合同 %s 退租终止违约修改成转租并修改转租费后业绩异常，执行SQL：%s' % (fileName, contractNum, breachAchievementSql))
        breachAchievementNew = breachAchievementNewInfo[1]
        base.diffAssert(lambda test: asserts(breachAchievementNew).is_equal_to(str(zhuanzu_money_new)), 1076,
                        u'%s:出租合同 %s 退租终止违约修改成转租并修改转租费后，违约业绩异常，期望值 %s 实际值 %s' % (fileName, contractNum, zhuanzu_money_new, breachAchievementNew))
        # base.diffAssert(lambda test: asserts(personAchievementNew).is_not_equal_to(personAchievementOld), 1076,
        #                 u'%s:出租合同 %s 退租终止违约修改成转租并修改转租费后，违约业绩分成明细异常，期望值不为 %s 实际值 %s' % (fileName, contractNum, personAchievementOld, personAchievementNew))

        # 业绩分成明细表（预估业绩排行榜数据取值表,检查违约业绩同步更新到预估业绩排行榜）
        breahAchievementDetailSql = "select ca.receivable from contract_achievement ca inner join contract_achievement_detail cad on ca.achieve_id=cad.achieve_id inner join breach_achievement ba " \
                                    "on ba.achieve_id=ca.achieve_id and ba.breach_type='CUSTOMER_SUBLET' and ba.deleted=0 and ba.breach_num='%s' " \
                                    "where ca.contract_category='CUSTOMER_SUBLET' and ca.deleted=0 " % contractNum
        prebreachAchievement = sqlbase.serach(breahAchievementDetailSql)[0]
        base.diffAssert(lambda test: asserts(prebreachAchievement).is_equal_to(str(zhuanzu_money_new)), 1076,
                        u'%s:出租合同 %s 退租终止违约修改成转租并修改转租费后,业绩分成明细业绩金额异常，实际值 %s 期望值 %s' % (fileName, contractNum, prebreachAchievement, zhuanzu_money_new))

test_1076()