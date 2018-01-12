# -*- coding:utf8 -*-

import time
from assertpy import assert_that as asserts
from common import sqlbase, page
from common.base import log, consoleLog, Base
from common.interface import createCustomer, createApartmentContract, addHouseContractAndFitment, audit, auditType, \
    auditStatus
from contract.achievement.page import apartmentAchievementPage
from contract.apartmentContract.page import apartmentContractPage

@log
def test_1057():
    """已审核的业绩修改出租合同租金价格"""

    # describe：在委托合同详情中，修改业绩核算周期对应时间段的出租合同租金价格，已审核的业绩数据不变
    # data：1、业绩审核状态为待审核；1、业绩状态为已审核；3、提前记录原业绩中的核算出租和差价业绩；
    # result：1、业绩中所有字段都不发生变化；

    fileName = 'apartmentAchievement_1057'

    with Base() as base:
        # 创建委托合同和出租合同
        houseSql = sqlbase.serach(
            "select house_id,residential_id,building_id,house_code from house where deleted=0 and city_code=330100 order by rand() limit 1")  # 获取随机开发房源
        houseInfo = {'houseID': houseSql[0], 'residentialID': houseSql[1], 'buildingID': houseSql[2],'houseCode': houseSql[3]}
        dateInfo = sqlbase.serach("select date(sysdate()),date_add(date(sysdate()),INTERVAL 1 day),date_add(date(sysdate()),interval 2 year),date_add(date(sysdate()),interval 27 month),"
                                  "date_add(date(sysdate()),INTERVAL 1 month),date_add(date(sysdate()),INTERVAL 6 month),date_add(date(sysdate()),INTERVAL 3 month) from dual")  # 日期元素
        apartmentId = addHouseContractAndFitment(apartment_type='MANAGE', entrust_type='SHARE', sign_date=dateInfo[0],
                                                 owner_sign_date=dateInfo[0], entrust_start_date=dateInfo[0],
                                                 entrust_end_date=dateInfo[2], delay_date=dateInfo[3],
                                                 free_start_date=dateInfo[0], free_end_date=dateInfo[4],
                                                 first_pay_date=dateInfo[0], second_pay_date=dateInfo[4],
                                                 rent=3000, parking=100, year_service_fee=500, payment_cycle='MONTH',
                                                 fitment_start_date=dateInfo[0], fitment_end_date=dateInfo[4], rooms=3,
                                                 fitmentCost=88888,houseInfo=houseInfo)
        houseContractInfo = sqlbase.serach("select hc.contract_num,hc.contract_id from house_contract hc inner join apartment a on a.house_id = hc.house_id and a.apartment_id='%s' where hc.audit_status='AUDIT' " % apartmentId)
        houseContractId = houseContractInfo[1]
        rentPriceInfo = sqlbase.serach("select rent_price,date(sysdate()) from apartment where apartment_id='%s'" % apartmentId)
        rentPrice = float(rentPriceInfo[0])
        customer = createCustomer()
        apartmentContractInfo = createApartmentContract(apartement_id=apartmentId, customerInfo=customer,
                                                        rent_price=rentPrice, sign_date=dateInfo[0],
                                                        rent_start_date=dateInfo[1], rent_end_date=dateInfo[5],#承租6个月
                                                        deposit=rentPrice, payment_cycle='MONTH')
        apartmentContractNum = apartmentContractInfo['contractNum']
        apartmentContractId = apartmentContractInfo['contractID']
        achievementSql = "select substring_index(house_code,'-',1) from apartment_contract_achievement where contract_num='%s'and deleted=0" % apartmentContractNum
        base.diffAssert(lambda test: asserts(sqlbase.waitData(achievementSql, 1)).is_true(), 1057,
                        u'%s:合同 %s 对应业绩生成异常' % (fileName, apartmentContractNum))
        # 委托合同审核
        audit(houseContractId, auditType.houseContract,auditStatus.chuShen,auditStatus.fuShen)
        # 出租合同审核
        audit(apartmentContractId, auditType.apartmentContract,auditStatus.chuShen,auditStatus.fuShen)
        # 业绩检查
        achievementsqlb = "select aca.is_active,aca.audit_status,aca.contract_audit_status,aca.profits_fee,aca.achievementRent from apartment_contract_achievement aca " \
                          "inner join apartment a on a.apartment_code=aca.house_code and a.apartment_id='%s' where aca.contract_num='%s' and aca.deleted=0 and aca.is_active='Y'" % (apartmentId, apartmentContractNum)
        base.diffAssert(lambda test: asserts(sqlbase.waitData(achievementsqlb, 1)).is_true(), 1057,
                        u'%s:合同 %s 对应业绩生效异常' % (fileName, apartmentContractNum))
        profits_feeOld = sqlbase.serach(achievementsqlb)[3]  # 差价业绩
        achievementRentOld = sqlbase.serach(achievementsqlb)[4]  # 核算出租价
        # 获取当前的核算收进价和差价业绩并审核
        base.open(page.apartmentAchievementPage, apartmentAchievementPage.searchContractMould['tr_contract'])
        base.click(apartmentAchievementPage.searchContractMould['reset_button_loc'])  # 重置
        base.input_text(apartmentAchievementPage.searchContractMould['contract_num_loc'], apartmentContractNum)  # 输入合同号
        base.click(apartmentAchievementPage.searchContractMould['search_button_loc'])  # 查找
        base.staleness_of(apartmentAchievementPage.searchContractMould['tr_contract'])  # 等待第一条数据刷新
        base.dblclick(apartmentAchievementPage.searchContractMould['tr_contract'],
                      checkLoc=apartmentAchievementPage.detailAchievementMoudle['contract_num_loc'])  # 点击第一条数据等待详情页面完全显示
        base.click(apartmentAchievementPage.detailAchievementMoudle['audit_button_loc'])
        base.input_text(apartmentAchievementPage.detailAchievementMoudle['contract_audit_content'], 'ok')
        base.click(apartmentAchievementPage.detailAchievementMoudle['contract_audit_confirm'])
        base.check_submit()
        # 反审出租合同并修改租金
        audit(apartmentContractId, auditType.apartmentContract, auditStatus.fanShen)
        base.open(page.apartmentContractPage, apartmentContractPage.searchContractMould['tr_contract'])
        base.input_text(apartmentContractPage.searchContractMould['contract_num_loc'], apartmentContractNum)  # 输入合同编号
        base.click(apartmentContractPage.searchContractMould['search_button_loc'])
        base.staleness_of(apartmentContractPage.searchContractMould['tr_contract'])
        base.dblclick(apartmentContractPage.searchContractMould['tr_contract'],
                      checkLoc=apartmentContractPage.addApartmentContractMould['contract_num_loc'])  # 双击第一条数据
        # base.click(apartmentContractPage.addApartmentContractMould['rent_strategy1_end_loc'])
        base.script("$('#contract_strategy_table > table > tbody > tr > td:nth-child(8) > input').click()")
        base.type_date(apartmentContractPage.addApartmentContractMould['rent_strategy1_end_loc'],dateInfo[6])
        base.click(apartmentContractPage.addApartmentContractMould['rent_strategy_menu_loc'])
        base.input_text(apartmentContractPage.addApartmentContractMould['rent_strategy2_money_loc'], 3000)
        base.type_date(apartmentContractPage.addApartmentContractMould['rent_strategy2_end_loc'], dateInfo[5])
        base.click(apartmentContractPage.addApartmentContractMould['save_button'])
        base.check_submit()
        # 数据库获取最新的核算收进价和差价业绩
        time.sleep(10)
        achievementInfoSql = "select profits_fee,rent_cost,end_time,achievementRent from apartment_contract_achievement where contract_num='%s' and deleted=0"%apartmentContractNum
        achievementInfo = sqlbase.serach(achievementInfoSql)
        achievementRent = achievementInfo[3]  # 核算出租价
        profits_fee = achievementInfo[0]  # 差价业绩
        base.diffAssert(lambda test: asserts(achievementRent).is_equal_to(achievementRentOld), 1057,
                        u'%s:出租合同 %s 业绩对应委托成本修改后已审核业绩中核算收进价异常，修改前 %s 修改后 %s' % (fileName, apartmentContractNum, achievementRentOld, achievementRent))
        base.diffAssert(lambda test: asserts(profits_fee).is_equal_to(profits_feeOld), 1057,
                        u'%s:出租合同 %s 业绩对应委托成本修改后已审核业绩中差价业绩异常，修改前 %s 修改后 %s' % (fileName, apartmentContractNum, profits_feeOld, profits_fee))

test_1057()