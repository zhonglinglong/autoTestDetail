# -*- coding:utf8 -*-
import time

from common import sqlbase, page
from common.base import log, consoleLog, Base
from common.interface import addHouseContractAndFitment, createCustomer, createApartmentContract
from contract.achievement.page import apartmentAchievementPage
from contract.apartmentContract.page import apartmentContractPage
from assertpy import assert_that as asserts

@log
def test_1054():
    """出单业绩删除"""

    # describe： 删除业绩对应的出租合同，业绩状态变为已失效；
    # data：1、业绩审核状态为未审核；2、业绩状态为生效；3、出租合同未终止结算且未续签
    # result：11、业绩从出单业绩列表中删除；2、分成记录从预估业绩排行榜中删除；3、有核发月份的分成记录还需要从核发业绩排行榜中删除

    fileName = 'apartmentAchievement_1054'

    with Base() as base:
        # 创建房源，委托合同
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
        # 创建租客，出租合同
        customer = createCustomer()
        apartmentContractInfo = createApartmentContract(apartement_id=apartmentId, customerInfo=customer,
                                                        rent_price=5500, sign_date=dateInfo[0],
                                                        rent_start_date=dateInfo[1], rent_end_date=dateInfo[2],
                                                        deposit=2000, payment_cycle='MONTH')
        apartmentContractNum = apartmentContractInfo['contractNum']
        # 出租合同检查
        contractAdd = "select * from apartment a,apartment_contract ac ,apartment_contract_relation acr where a.apartment_id=acr.apartment_id and acr.contract_id=ac.contract_id " \
                      "and a.apartment_id='%s'AND ac.contract_num = '%s'AND ac.audit_status='AUDIT' and ac.contract_type = 'NEWSIGN' AND ac.entrust_type='SHARE' " \
                      "AND ac.is_active='Y' " % (apartmentId, apartmentContractNum)
        # 业绩检查
        achievementsqla = "select aca.is_active,aca.audit_status,aca.accounting_time from apartment_contract_achievement aca " \
                          "inner join apartment a on a.apartment_code=aca.house_code and a.apartment_id='%s' where aca.contract_num='%s' and aca.deleted=0" % (apartmentId,apartmentContractNum)
        base.diffAssert(lambda test: asserts(sqlbase.waitData(achievementsqla, 1)).is_true(), 1054,
                        u'%s:合同 %s 对应业绩生成异常' % (fileName, apartmentContractNum))
        # 删除出租合同
        base.open(page.apartmentContractPage, apartmentContractPage.searchContractMould['tr_contract'])
        base.input_text(apartmentContractPage.searchContractMould['contract_num_loc'], apartmentContractNum)  # 输入合同编号
        base.click(apartmentContractPage.searchContractMould['search_button_loc'])
        base.staleness_of(apartmentContractPage.searchContractMould['tr_contract'])
        base.context_click(apartmentContractPage.searchContractMould['tr_contract'])
        base.click(apartmentContractPage.searchContractMould['delete_loc'])
        base.click(apartmentContractPage.addApartmentContractMould['delete_button_confirm'])
        base.check_submit()
        time.sleep(10)
        achievementsqla = "select aca.is_active,aca.audit_status,aca.accounting_time from apartment_contract_achievement aca " \
                          "inner join apartment a on a.apartment_code=aca.house_code and a.apartment_id='%s' where aca.contract_num='%s' and aca.deleted=0" % (apartmentId,apartmentContractNum)
        base.diffAssert(lambda test: asserts(sqlbase.get_count(achievementsqla)).is_equal_to(0), 1054,
                        u'%s:合同 %s 对应业绩删除异常' % (fileName, apartmentContractNum))
        # 预估业绩排行榜
        base.open(page.achievementListPrePage, apartmentAchievementPage.searchContractMould['tr_contract'])
        base.click(apartmentAchievementPage.searchContractMould['reset_button_loc'])  # 重置
        base.staleness_of(apartmentAchievementPage.searchContractMould['tr_contract'])
        base.input_text(apartmentAchievementPage.searchContractMould['contract_num_hefa_loc'], apartmentContractNum)  # 输入合同号
        base.click(apartmentAchievementPage.searchContractMould['search_button_loc'])  # 查找
        try:
            base.wait_element(apartmentAchievementPage.searchContractMould['tr_contract'])
        except:
            achievementDetailCount = sqlbase.get_count(
                "select * from contract_achievement_detail acd inner join apartment_contract_achievement aca "
                "on aca.achievement_id=acd.achieve_id and aca.contract_num='%s' where acd.deleted=0" % apartmentContractNum)
            if achievementDetailCount == 0:
                consoleLog(u'%s:出租合同 %s 删除后分成记录从预估业绩排行榜中删除'% (fileName,apartmentContractNum))
test_1054()