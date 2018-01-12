# -*- coding:utf8 -*-

import time

from assertpy import assert_that as asserts

from common import sqlbase, page
from common.base import log, consoleLog, Base
from common.interface import createCustomer, createApartmentContract, auditType, audit, auditStatus
from contract.achievement.page import apartmentAchievementPage
from finance import apartmentContractReceivablePage


@log
def test_1043():
    """手工修改核发月份"""

    # describe： 手工修改核发月份,对应业绩记录核发月份发生改变
    # data：1、业绩审核状态为待审核；2、业绩核发月份字段不为空；
    # result：1、修改后的核发月份同步到预估业绩排行榜；2、修改后的核发月份同步到核发业绩排行榜；3、出单业绩列表页中显示修改后的核发月份，取分成记录中最早的月份；

    fileName = 'apartmentAchievement_1043'
    randomApartment = "SELECT a.apartment_code,a.apartment_id,hc.contract_num,hc.contract_id FROM apartment a INNER JOIN house_contract hc " \
                      "ON hc.contract_id = a.house_contract_id AND hc.is_active = 'Y' AND hc.deleted = 0 AND hc.audit_status='APPROVED' AND hc.contract_status = 'EFFECTIVE' " \
                      "INNER JOIN fitment_house fh on fh.house_id=hc.house_id AND fh.fitment_status='HANDOVER' WHERE a.deleted = 0 " \
                      "AND a.rent_price > 0 AND a.city_code = 330100 AND hc.entrust_type = 'SHARE' AND a.rent_status='WAITING_RENT'" \
                      "AND hc.real_due_date>date_add(date(sysdate()), interval 1 YEAR) ORDER BY RAND() LIMIT 1"
    if sqlbase.get_count(randomApartment) == 0:
        consoleLog(u'%s:SQL查无数据！'% fileName, 'w')
        consoleLog(u'执行SQL：%s' % randomApartment)
        return
    info = sqlbase.serach(randomApartment)
    apartmentCode = info[0]
    apartmentId = info[1]
    dateInfo = sqlbase.serach(
        "select 1,2,date(sysdate()),date_add(date(sysdate()), interval 1 DAY),date_add(date(sysdate()), interval 6 month),DATE_FORMAT(DATE_ADD(sysdate(),INTERVAL 1	MONTH),'%Y-%m') from dual")
    consoleLog(u'%s:使用房源 %s 签约出租合同' % (fileName,apartmentCode))

    with Base() as base:
        # 创建委托和出租合同
        customer = createCustomer()
        rentPriceInfo = sqlbase.serach("select rent_price from apartment where apartment_id='%s'" % apartmentId)[0]
        rentPrice = float(rentPriceInfo)
        apartmentContractInfo = createApartmentContract(apartement_id=apartmentId, customerInfo=customer,
                                                        rent_price=rentPrice, sign_date=dateInfo[2],
                                                        rent_start_date=dateInfo[3], rent_end_date=dateInfo[4],
                                                        deposit=rentPrice, payment_cycle='MONTH')
        apartmentContractNum = apartmentContractInfo['contractNum']
        apartmentContractId =  apartmentContractInfo['contractID']
        # 出租合同审核
        audit(apartmentContractId, auditType.apartmentContract, auditStatus.chuShen, auditStatus.fuShen)
        # 出租合同应收
        base.open(page.apartmentContractPayPage, apartmentContractReceivablePage.searchMould['tr_receviable_loc'])
        base.click(apartmentContractReceivablePage.searchMould['reset_button'])
        base.staleness_of(apartmentContractReceivablePage.searchMould['tr_receviable_loc'])
        base.input_text(apartmentContractReceivablePage.searchMould['contractNum_loc'], apartmentContractNum)
        base.click(apartmentContractReceivablePage.searchMould['search_button'])
        base.staleness_of(apartmentContractReceivablePage.searchMould['tr_receviable_loc'])
        moneyType = {u'首期管家服务费':int(0.07*rentPrice) , u'中介服务费':1000 , u'首期租金':int(rentPrice) , u'押金':int(rentPrice)}
        for i in range(3):
            moneyType_row = base.script("var a = $('[datagrid-row-index=\"%s\"] > [field=\"money_type\"] > div').text();return a" % i, True)
            base.click(apartmentContractReceivablePage.searchMould['receviabl_button'][i])
            base.input_text(apartmentContractReceivablePage.detailMould['receipts_money_loc'], moneyType[moneyType_row])
            base.click(apartmentContractReceivablePage.detailMould['receipts_type'])
            base.type_date(apartmentContractReceivablePage.detailMould['receipts_date_loc'], dateInfo[2])
            base.input_text(apartmentContractReceivablePage.detailMould['alipay_card_loc'], '13676595110')
            base.input_text(apartmentContractReceivablePage.detailMould['operation_total_loc'], moneyType[moneyType_row])
            base.click(apartmentContractReceivablePage.detailMould['save_button'])
            base.check_submit()
            base.click(apartmentContractReceivablePage.detailMould['print_btn_close'])
            time.sleep(1)
        # 业绩检查
        achievementSql = "select aca.is_active,aca.audit_status,aca.accounting_time,aca.achievement_id from apartment_contract_achievement aca inner join apartment a on" \
                         " a.apartment_code=aca.house_code where contract_num='%s' and a.apartment_code='%s'and aca.deleted=0 and aca.accounting_time is not " \
                         "null" % (apartmentContractNum, apartmentCode)
        base.diffAssert(lambda test: asserts(sqlbase.waitData(achievementSql, 1)).is_true(), 1043,
                        u'%s:合同 %s 对应业绩核发月份异常' % (fileName, apartmentContractNum))
        achievementInfo = sqlbase.serach(achievementSql)
        achievementDetialConunt = sqlbase.get_count(
            "select * from apartment_contract_achievement_detail where achievement_id='%s'" % achievementInfo[3])  # 业绩分成条数
        # 修改核发月份
        base.open(page.apartmentAchievementPage, apartmentAchievementPage.searchContractMould['tr_contract'])
        base.click(apartmentAchievementPage.searchContractMould['reset_button_loc'])  # 重置
        base.input_text(apartmentAchievementPage.searchContractMould['contract_num_loc'], apartmentContractNum)  # 输入合同号
        base.click(apartmentAchievementPage.searchContractMould['search_button_loc'])  # 查找
        base.staleness_of(apartmentAchievementPage.searchContractMould['tr_contract'])  # 等待第一条数据刷新
        base.dblclick(apartmentAchievementPage.searchContractMould['tr_contract'],
                      checkLoc=apartmentAchievementPage.detailAchievementMoudle['contract_num_loc'])  # 点击第一条数据等待详情页面完全显示
        for i in range(achievementDetialConunt):
            base.type_date(apartmentAchievementPage.detailAchievementMoudle['accounting_time_loc'][i], dateInfo[5])  # 修改核发月份到下个月
        base.click(apartmentAchievementPage.detailAchievementMoudle['save_button_loc'])
        base.check_submit()
        # 出租合同业绩分成明细表（检查出单业绩对应核发月份是否修改）
        time.sleep(5)
        apartmentContractAchievementSql = "select accounting_time from apartment_contract_achievement_detail where deleted=0 and achievement_id='%s'" % achievementInfo[3]
        accountingTime = sqlbase.serach(apartmentContractAchievementSql)[0]
        base.diffAssert(lambda test: asserts(accountingTime).is_equal_to(dateInfo[5]), 1043,
                        u'%s:出租合同 %s 对应出租业绩分成记录核发月份修改异常,修改后期望值 %s 实际值 %s' % (fileName, apartmentContractNum, dateInfo[5], accountingTime))

        # 业绩分成明细表（预估业绩排行榜数据取值表,检查核发月份同步更新到预估业绩排行榜）
        contractAchievementSql = "select achievement_month from contract_achievement_detail where deleted=0 and achieve_id='%s'" % (achievementInfo[3])
        achievementDetial = sqlbase.serach(contractAchievementSql)
        base.diffAssert(lambda test: asserts(achievementDetial[0]).is_equal_to(dateInfo[5]),1043,
                        u'%s:出租合同 %s 对应业绩分成明细核发月份修改异常,修改后期望值 %s 实际值 %s' % (fileName, apartmentContractNum, dateInfo[5], achievementDetial[0]))

        # 核发业绩排行榜核发月份检查
        base.open(page.achievementListPage, apartmentAchievementPage.searchContractMould['tr_contract'])
        base.click(apartmentAchievementPage.searchContractMould['reset_button_loc'])  # 重置
        base.staleness_of(apartmentAchievementPage.searchContractMould['tr_contract'])
        base.input_text(apartmentAchievementPage.searchContractMould['contract_num_hefa_loc'], apartmentContractNum)  # 输入合同号
        base.click(apartmentAchievementPage.searchContractMould['search_button_loc'])  # 查找
        base.staleness_of(apartmentAchievementPage.searchContractMould['tr_contract'])  # 等待第一条数据刷新
        time.sleep(3)
        for i in range(achievementDetialConunt):
            achievement_month = base.script(
                "var a = $('[datagrid-row-index=\"%s\"] > [field=\"achievement_month\"] > div').text();return a" % i,
                True)
            base.diffAssert(lambda test: asserts(achievement_month).is_equal_to(dateInfo[5]), 1043,
                            u'%s:出租合同 %s 对应业绩修改核发月份的同步到核发业绩排行榜异常，期望值 %s 实际值 %s' % (fileName, apartmentContractNum, dateInfo[5], achievement_month,))

test_1043()