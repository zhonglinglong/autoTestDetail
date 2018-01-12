# -*- coding:utf8 -*-

import time

from assertpy import assert_that as asserts

from common import sqlbase, page
from common.base import log, consoleLog, Base
from common.interface import createCustomer, createApartmentContract, audit, auditType, auditStatus
from contract.achievement.page import apartmentAchievementPage
from finance import apartmentContractReceivablePage


@log
def test_1042():
    """核发月份条件满足后生成核发月份"""

    # describe： 核发月份条件满足后生成核发月份
    # data：1、业绩审核状态为待审核；2、业绩核发月份字段为空；
    # result：1、业绩分成记录生成核发月份；2、列表页业绩记录产生核发月份；3、核发月份同步更新到预估业绩排行榜；4、有核发月份的业绩分成记录插入核发业绩排行榜；

    fileName = 'apartmentAchievement_1042'
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
    consoleLog(u'%s:使用房源 %s 签约出租合同' % (fileName,apartmentCode))
    dateInfo = sqlbase.serach(
        "SELECT entrust_start_date,entrust_end_date,date(sysdate()),date_add(date(sysdate()), interval 1 DAY),date_add(date(sysdate()), interval 6 month) "
        "from house_contract where contract_num = '%s'" % info[2])  # 获取时间元素

    with Base() as base:
        # 创建委托和出租合同
        customer = createCustomer()
        rentPriceInfo = sqlbase.serach("select rent_price,date(sysdate()) from apartment where apartment_id='%s'" % apartmentId)
        rentPrice = float(rentPriceInfo[0])
        apartmentContractInfo = createApartmentContract(apartement_id=apartmentId, customerInfo=customer,
                                                        rent_price=rentPrice, sign_date=dateInfo[2],
                                                        rent_start_date=dateInfo[3], rent_end_date=dateInfo[4],
                                                        deposit=rentPrice, payment_cycle='MONTH')
        apartmentContractNum = apartmentContractInfo['contractNum']
        apartmentContractId = apartmentContractInfo['contractID']
        # 出租合同审核
        audit(apartmentContractId, auditType.apartmentContract, auditStatus.chuShen, auditStatus.fuShen)
        contractAuditSql = "select audit_status from apartment_contract where is_active='Y' and deleted=0 and contract_num='%s'" % apartmentContractNum
        contractAuditStatus = sqlbase.serach(contractAuditSql)[0]
        base.diffAssert(lambda test: asserts(contractAuditStatus).is_equal_to('APPROVED'), 1042,
                        u'%s:出租合同 %s 审核后状态异常，期望值 APPROVED 实际值 %s' % (fileName, apartmentContractNum, contractAuditStatus))
        # 出租合同应收
        base.open(page.apartmentContractPayPage, apartmentContractReceivablePage.searchMould['tr_receviable_loc'])
        base.click(apartmentContractReceivablePage.searchMould['reset_button'])
        base.staleness_of(apartmentContractReceivablePage.searchMould['tr_receviable_loc'])
        base.input_text(apartmentContractReceivablePage.searchMould['contractNum_loc'],apartmentContractNum)
        base.click(apartmentContractReceivablePage.searchMould['search_button'])
        base.staleness_of(apartmentContractReceivablePage.searchMould['tr_receviable_loc'])
        moneyType = {u'首期管家服务费':int(0.07*rentPrice) , u'中介服务费':1000 , u'首期租金':int(rentPrice) , u'押金':int(rentPrice)}
        for i in range(3):
            moneyType_row = base.script("var a = $('[datagrid-row-index=\"%s\"] > [field=\"money_type\"] > div').text();return a" % i, True)
            base.click(apartmentContractReceivablePage.searchMould['receviabl_button'][i])
            base.input_text(apartmentContractReceivablePage.detailMould['receipts_money_loc'], moneyType[moneyType_row])
            base.click(apartmentContractReceivablePage.detailMould['receipts_type'])
            base.type_date(apartmentContractReceivablePage.detailMould['receipts_date_loc'], rentPriceInfo[1])
            base.input_text(apartmentContractReceivablePage.detailMould['alipay_card_loc'], '13676595110')
            base.input_text(apartmentContractReceivablePage.detailMould['operation_total_loc'], moneyType[moneyType_row])
            base.click(apartmentContractReceivablePage.detailMould['save_button'])
            base.check_submit()
            base.click(apartmentContractReceivablePage.detailMould['print_btn_close'])
            time.sleep(1)
        # 业绩检查
        achievementSql = "select aca.is_active,aca.audit_status,aca.accounting_time,aca.achievement_id from apartment_contract_achievement aca inner join apartment a on a.apartment_code=aca.house_code " \
                          "where contract_num='%s' and a.apartment_code='%s'and aca.deleted=0 and aca.accounting_time is not null" % (apartmentContractNum, apartmentCode)
        base.diffAssert(lambda test: asserts(sqlbase.waitData(achievementSql, 1)).is_true(), 1042,
                        u'%s:合同 %s 对应业绩核发月份异常' % (fileName, apartmentContractNum))
        achievementInfo = sqlbase.serach(achievementSql)
        base.diffAssert(lambda test: asserts(achievementInfo[0]).is_equal_to('Y'),1042,
                        u'%s:合同 %s 对应业绩生效状态异常，期望值 Y 实际值 %s' % (fileName, apartmentContractNum, achievementInfo[0]))
        base.diffAssert(lambda test: asserts(achievementInfo[1]).is_equal_to('AUDIT'),1042,
                        u'%s:合同 %s 对应业绩审核状态异常, 期望值 AUDIT 实际值 %s' % (fileName, apartmentContractNum, achievementInfo[1]))

        # 出租合同业绩分成明细表（检查业绩分成记录生成核发月份）
        apartmentContractAchievementSql = "select accounting_time from apartment_contract_achievement_detail where deleted=0 and achievement_id='%s'" % achievementInfo[3]
        base.diffAssert(lambda test: asserts(sqlbase.serach(apartmentContractAchievementSql)[0]).is_equal_to(achievementInfo[2]), 1042,
                        u'%s:出租合同 %s 对应业绩分成记录核发月份异常' % (fileName, apartmentContractNum))

        # 业绩分成明细表（预估业绩排行榜数据取值表,检查核发月份同步更新到预估业绩排行榜）
        contractAchievementSql = "select * from contract_achievement_detail where deleted=0 and achieve_id='%s' and achievement_month='%s'" % (achievementInfo[3], achievementInfo[2])
        achievementDetialConunt = sqlbase.get_count(contractAchievementSql)
        base.diffAssert(lambda test: asserts(achievementDetialConunt).is_not_equal_to(0), 1042,
                        u'%s:出租合同 %s 对应业绩分成明细异常' % (fileName, apartmentContractNum))

        # 核发业绩排行榜检查
        base.open(page.achievementListPage, apartmentAchievementPage.searchContractMould['tr_contract'])
        base.click(apartmentAchievementPage.searchContractMould['reset_button_loc'])  # 重置
        base.staleness_of(apartmentAchievementPage.searchContractMould['tr_contract'])
        base.input_text(apartmentAchievementPage.searchContractMould['contract_num_hefa_loc'], apartmentContractNum)  # 输入合同号
        base.click(apartmentAchievementPage.searchContractMould['search_button_loc'])  # 查找
        base.staleness_of(apartmentAchievementPage.searchContractMould['tr_contract'])  # 等待第一条数据刷新
        for i in range(achievementDetialConunt):
            achievement_month = base.script(
                "var a = $('[datagrid-row-index=\"%s\"] > [field=\"achievement_month\"] > div').text();return a" % i,True)
            base.diffAssert(lambda test: asserts(achievement_month).is_equal_to(achievementInfo[2]), 1042,
                            u'%s:出租合同 %s 对应业绩有核发月份的同步到核发业绩排行榜异常' % (fileName, apartmentContractNum))

test_1042()