# -*- coding:utf8 -*-

import time
from assertpy import assert_that as asserts
from common import sqlbase, page
from common.base import log, consoleLog, Base
from common.interface import createCustomer, createApartmentContract, addHouseContractAndFitment, audit, auditType, \
    auditStatus
from contract.achievement.page import apartmentAchievementPage
from fitment import designSharePage

@log
def test_1058():
    """修改房源的装修成本"""

    # describe：在设计工程中修改房源的装修成本，对应业绩装修成本改变
    # data：1、业绩审核状态为待审核；2、委托合同状态为待审核或者已初审；3、提前记录原业绩中的核算收进价和差价业绩；
    # result：1、新产生的业绩中核算收进价与原记录不同；2、新的差价业绩与原来的值不同；

    fileName = 'apartmentAchievement_1058'

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
        base.diffAssert(lambda test: asserts(sqlbase.waitData(achievementSql, 1)).is_true(), 1058,
                        u'%s:合同 %s 对应业绩生成异常' % (fileName, apartmentContractNum))
        houseCode = sqlbase.serach(achievementSql)[0]
        # 委托合同审核
        audit(houseContractId,auditType.houseContract,auditStatus.chuShen,auditStatus.fuShen)
        # 出租合同审核
        audit(apartmentContractId,auditType.apartmentContract,auditStatus.chuShen,auditStatus.fuShen)
        # 业绩检查
        achievementsqlb = "select aca.is_active,aca.audit_status,aca.contract_audit_status,aca.profits_fee,aca.decorate_cost from apartment_contract_achievement aca " \
                          "inner join apartment a on a.apartment_code=aca.house_code and a.apartment_id='%s' where aca.contract_num='%s' and aca.deleted=0 and aca.is_active='Y'" % (apartmentId, apartmentContractNum)
        base.diffAssert(lambda test: asserts(sqlbase.waitData(achievementsqlb, 1)).is_true(), 1058,
                        u'%s:合同 %s 对应业绩生效异常' % (fileName, apartmentContractNum))
        profits_feeOld = sqlbase.serach(achievementsqlb)[3]  # 差价业绩
        decorate_costOld = sqlbase.serach(achievementsqlb)[4]  # 装修成本
        # 获取当前的核算收进价和差价业绩并审核
        base.open(page.apartmentAchievementPage, apartmentAchievementPage.searchContractMould['tr_contract'])
        base.click(apartmentAchievementPage.searchContractMould['reset_button_loc'])  # 重置
        base.input_text(apartmentAchievementPage.searchContractMould['contract_num_loc'], apartmentContractNum)  # 输入合同号
        base.click(apartmentAchievementPage.searchContractMould['search_button_loc'])  # 查找
        base.staleness_of(apartmentAchievementPage.searchContractMould['tr_contract'])  # 等待第一条数据刷新
        base.dblclick(apartmentAchievementPage.searchContractMould['tr_contract'],
                      checkLoc=apartmentAchievementPage.detailAchievementMoudle['contract_num_loc'])  # 点击第一条数据等待详情页面完全显示
        base.click(apartmentAchievementPage.detailAchievementMoudle['audit_button_loc'])
        base.input_text(apartmentAchievementPage.detailAchievementMoudle['contract_audit_content'],'ok')
        base.click(apartmentAchievementPage.detailAchievementMoudle['contract_audit_confirm'])
        base.check_submit()
        # 修改装修成本
        base.open(page.designManageSharePage, designSharePage.searchMould['tr_contract'])
        base.input_text(designSharePage.searchMould['residential_name_loc'], houseCode)
        base.click(designSharePage.searchMould['search_btn_loc'])
        base.staleness_of(designSharePage.searchMould['tr_contract'])
        base.context_click(designSharePage.searchMould['tr_contract'])
        base.click(designSharePage.designShareMould['design_btn_2'], index=0)
        time.sleep(2)
        base.input_text(designSharePage.designShareMould['total_cost'], '68888.00')
        base.click(designSharePage.designShareMould['save_btn_2'])
        base.check_submit()
        # 数据库获取最新的核算收进价和差价业绩
        time.sleep(10)
        achievementInfoSql = "select profits_fee,rent_cost,end_time,achievementRent,decorate_cost from apartment_contract_achievement where contract_num='%s' and deleted=0"%apartmentContractNum
        achievementInfo = sqlbase.serach(achievementInfoSql)
        decorate_cost = achievementInfo[4]  # 装修成本
        profits_fee = achievementInfo[0]  # 差价业绩
        base.diffAssert(lambda test: asserts(decorate_cost).is_equal_to(decorate_costOld),1058,
                        u'%s:出租合同 %s 业绩对应委托成本修改后已审核业绩中核算收进价异常，修改前 %s 修改后 %s' % (fileName, apartmentContractNum, decorate_costOld, decorate_cost))
        base.diffAssert(lambda test: asserts(profits_fee).is_equal_to(profits_feeOld),1058,
                        u'%s:出租合同 %s 业绩对应委托成本修改后已审核业绩中差价业绩异常，修改前 %s 修改后 %s' % (fileName, apartmentContractNum, profits_feeOld, profits_fee))

test_1058()