# -*- coding:utf8 -*-
import time
from assertpy import assert_that as asserts
from common import sqlbase, page
from common.base import log, consoleLog, Base
from common.interface import addHouseContractAndFitment, createCustomer, createApartmentContract, auditType, \
    auditStatus, audit
from contract.achievement.page import apartmentAchievementPage
from contract.apartmentContract.page import apartmentContractPage

@log
def test_1053():
    """生效业绩变为已失效"""

    # describe： 删除业绩对应的出租合同，业绩状态变为已失效；
    # data：1、业绩审核状态为已审核；2、业绩状态为生效；3、出租合同未终止结算且未续签
    # result：1、业绩状态变为已失效；2、业绩已失效状态同步到预估业绩排行榜和核发业绩排行榜；

    fileName = 'apartmentAchievement_1053'

    with Base() as base:
        #创建房源，委托合同
        dateSql = "select date(sysdate()),date_add(date(sysdate()),INTERVAL 1 day),date_add(date(sysdate()),interval 1 year),date_add(date(sysdate()),interval 3 year),date_add(date(sysdate()),INTERVAL 1 month) from dual"
        dateInfo = sqlbase.serach(dateSql)
        apartmentId = addHouseContractAndFitment(apartment_type='MANAGE', entrust_type='SHARE', sign_date=dateInfo[0],
                                                 owner_sign_date=dateInfo[0], entrust_start_date=dateInfo[0],
                                                 entrust_end_date=dateInfo[3], delay_date=dateInfo[3],
                                                 free_start_date=dateInfo[0], free_end_date=dateInfo[4],
                                                 first_pay_date=dateInfo[0], second_pay_date=dateInfo[4],
                                                 rent=1234, parking=123, year_service_fee=321, payment_cycle='MONTH',
                                                 fitment_start_date=dateInfo[0], fitment_end_date=dateInfo[4], rooms=3,
                                                 fitmentCost=88888)
        houseContractInfo = sqlbase.serach("select hc.contract_num,hc.contract_id from house_contract hc inner join apartment a on a.house_id = hc.house_id and a.apartment_id='%s' where hc.audit_status='AUDIT' " % apartmentId)
        houseContractNum = houseContractInfo[0]
        houseContractId = houseContractInfo[1]
        #创建租客，出租合同
        customer = createCustomer()
        apartmentContractInfo = createApartmentContract(apartement_id=apartmentId, customerInfo=customer,
                                                        rent_price=5500, sign_date=dateInfo[0],
                                                        rent_start_date=dateInfo[1], rent_end_date=dateInfo[2],
                                                        deposit=2000, payment_cycle='MONTH')
        apartmentContractNum = apartmentContractInfo['contractNum']
        apartmentContractId = apartmentContractInfo['contractID']
        #业绩检查
        achievementsqla = "select aca.is_active,aca.audit_status,aca.accounting_time from apartment_contract_achievement aca " \
                          "inner join apartment a on a.apartment_code=aca.house_code and a.apartment_id='%s' where aca.contract_num='%s' and aca.deleted=0" % (apartmentId,apartmentContractNum)
        if sqlbase.waitData(achievementsqla,1):
            achievementinfo = sqlbase.serach(achievementsqla)
            base.diffAssert(lambda test: asserts(achievementinfo[0]).is_equal_to('N'), 1053,
                            u'%s:合同 %s 对应业绩生效状态异常，期望值 N 实际值 %s' % (fileName, apartmentContractNum, achievementinfo[0]))
            base.diffAssert(lambda test: asserts(achievementinfo[1]).is_equal_to('AUDIT'), 1053,
                            u'%s:合同 %s 对应业绩审核状态异常, 期望值 AUDIT 实际值 %s' % (fileName, apartmentContractNum, achievementinfo[1]))
        else:
            consoleLog(u'%s:合同 %s 对应业绩生成异常' % (fileName, apartmentContractNum),'e')
            consoleLog(u'执行SQL:%s' % achievementsqla)
        #委托合同审核
        audit(houseContractId,auditType.houseContract,auditStatus.chuShen,auditStatus.fuShen)
        #出租合同审核
        audit(apartmentContractId,auditType.apartmentContract,auditStatus.chuShen,auditStatus.fuShen)
        # 业绩检查
        achievementsqlb = "select aca.is_active,aca.audit_status,aca.contract_audit_status from apartment_contract_achievement aca inner join apartment a " \
                          "on a.apartment_code=aca.house_code and a.apartment_id='%s' where aca.contract_num='%s' and aca.deleted=0 and aca.is_active='Y'" % (apartmentId, apartmentContractNum)
        base.diffAssert(lambda test: asserts(sqlbase.waitData(achievementsqlb, 1)).is_true(), 1053,
                        u'%s:合同 %s 对应业绩生效异常' % (fileName, apartmentContractNum))
        #业绩审核
        base.open(page.apartmentAchievementPage, apartmentAchievementPage.searchContractMould['tr_contract'])
        base.click(apartmentAchievementPage.searchContractMould['reset_button_loc'])  # 重置
        base.input_text(apartmentAchievementPage.searchContractMould['contract_num_loc'], apartmentContractNum)  # 输入合同号
        base.type_select(apartmentAchievementPage.searchContractMould['contract_type_loc'], 'NEWSIGN')  # 承租类型
        base.click(apartmentAchievementPage.searchContractMould['search_button_loc'])  # 查找
        base.staleness_of(apartmentAchievementPage.searchContractMould['tr_contract'])  # 等待第一条数据刷新
        base.dblclick(apartmentAchievementPage.searchContractMould['tr_contract'],
                      checkLoc=apartmentAchievementPage.detailAchievementMoudle['contract_num_loc'])  # 点击第一条数据等待详情页面完全显示
        base.click(apartmentAchievementPage.detailAchievementMoudle['audit_button_loc'])
        base.input_text(apartmentAchievementPage.detailAchievementMoudle['contract_audit_content'], 'ok')
        base.click(apartmentAchievementPage.detailAchievementMoudle['contract_audit_confirm'])
        base.check_submit()
        achievementStatus = "select * from apartment_contract_achievement where is_active='Y' and audit_status='APPROVED' AND deleted=0 and accounting_num=1 " \
                            "and city_code=330100 and contract_num='%s'" % apartmentContractNum
        base.diffAssert(lambda test: asserts(sqlbase.waitData(achievementStatus, 1)).is_true(), 1053,
                        u'%s:合同 %s 对应业绩审核异常' % (fileName, apartmentContractNum))
        # 出租合同反审后删除
        audit(apartmentContractId, auditType.apartmentContract, auditStatus.fanShen)
        base.open(page.apartmentContractPage, apartmentContractPage.searchContractMould['tr_contract'])
        base.input_text(apartmentContractPage.searchContractMould['contract_num_loc'], apartmentContractNum)  # 输入合同编号
        base.click(apartmentContractPage.searchContractMould['search_button_loc'])
        base.staleness_of(apartmentContractPage.searchContractMould['tr_contract'])
        base.context_click(apartmentContractPage.searchContractMould['tr_contract'])
        base.click(apartmentContractPage.searchContractMould['delete_loc'])
        base.click(apartmentContractPage.addApartmentContractMould['delete_button_confirm'])
        base.check_submit()
        # 预估业绩排行榜
        time.sleep(10)
        chievementDetailSql = "select ca.receivable,ca.is_active from contract_achievement ca inner join contract_achievement_detail cad on ca.achieve_id=cad.achieve_id " \
                              "inner join apartment_contract_achievement aca on aca.achievement_id=ca.achieve_id and aca.deleted=0 and aca.contract_num='%s' where ca.contract_type='NORMAL' " \
                              "and ca.deleted=0" % apartmentContractNum
        breachAchievementStatus = sqlbase.serach(chievementDetailSql)[1]
        base.diffAssert(lambda test: asserts(breachAchievementStatus).is_equal_to('INVALID'), 1053,
                        u'%s:出租合同 %s 业绩分成明细业绩状态异常，期望值 INVALID 实际值 %s' % (fileName, apartmentContractNum, breachAchievementStatus))

test_1053()