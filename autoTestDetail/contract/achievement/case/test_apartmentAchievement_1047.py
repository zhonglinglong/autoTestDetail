# -*- coding:utf8 -*-

import time

from assertpy import assert_that as asserts

from common import sqlbase, page
from common.base import log, Base
from common.interface import createCustomer, createApartmentContract, addHouseContractAndFitment
from fitment import designSharePage


@log
def test_1047():
    """修改装修成本"""

    # describe：在设计工程中修改房源的装修成本，对应业绩装修成本改变
    # data：1、业绩审核状态为待审核；2、委托合同状态为待审核或者已初审；3、提前记录原业绩中的核算收进价和差价业绩；
    # result：1、新产生的业绩中核算收进价与原记录不同；2、新的差价业绩与原来的值不同；

    fileName = 'apartmentAchievement_1047'

    with Base() as base:
        # 创建委托合同和出租合同
        houseSql = sqlbase.serach(
            "select house_id,residential_id,building_id,house_code from house where deleted=0 and city_code=330100 order by rand() limit 1")  # 获取随机开发房源
        houseInfo = {'houseID': houseSql[0], 'residentialID': houseSql[1], 'buildingID': houseSql[2],'houseCode': houseSql[3]}
        dateInfo = sqlbase.serach("select date(sysdate()),date_add(date(sysdate()),INTERVAL 1 day),date_add(date(sysdate()),interval 2 year),date_add(date(sysdate()),interval 27 month),"
                                  "date_add(date(sysdate()),INTERVAL 1 month),date_add(date(sysdate()),INTERVAL 6 month),date_add(date(sysdate()),INTERVAL 10 day) from dual")  # 日期元素
        apartmentId = addHouseContractAndFitment(apartment_type='MANAGE', entrust_type='SHARE', sign_date=dateInfo[0],
                                                 owner_sign_date=dateInfo[0], entrust_start_date=dateInfo[0],
                                                 entrust_end_date=dateInfo[2], delay_date=dateInfo[3],
                                                 free_start_date=dateInfo[0], free_end_date=dateInfo[4],
                                                 first_pay_date=dateInfo[0], second_pay_date=dateInfo[4],
                                                 rent=3000, parking=100, year_service_fee=500, payment_cycle='MONTH',
                                                 fitment_start_date=dateInfo[0], fitment_end_date=dateInfo[4], rooms=3,
                                                 fitmentCost=88888,houseInfo=houseInfo)
        rentPriceInfo = sqlbase.serach("select rent_price,date(sysdate()) from apartment where apartment_id='%s'" % apartmentId)
        rentPrice = float(rentPriceInfo[0])
        customer = createCustomer()
        apartmentContractInfo = createApartmentContract(apartement_id=apartmentId, customerInfo=customer,
                                                        rent_price=rentPrice, sign_date=dateInfo[0],
                                                        rent_start_date=dateInfo[1], rent_end_date=dateInfo[5],  # 承租6个月
                                                        deposit=rentPrice, payment_cycle='MONTH')
        apartmentContractNum = apartmentContractInfo['contractNum']
        # 业绩检查
        achievementSql = "select substring_index(aca.house_code,'-',1),aca.is_active,aca.audit_status,aca.contract_audit_status,aca.profits_fee,aca.decorate_cost from apartment_contract_achievement aca " \
                          "inner join apartment a on a.apartment_code=aca.house_code and a.apartment_id='%s' where aca.contract_num='%s' and aca.deleted=0" % (
                          apartmentId, apartmentContractNum)
        base.diffAssert(lambda test: asserts(sqlbase.waitData(achievementSql, 1)).is_true(), 1047,
                        u'%s:合同 %s 业绩生成异常' % (fileName, apartmentContractNum))
        achievementInfo = sqlbase.serach(achievementSql)
        profits_fee_old = achievementInfo[4]  # 差价业绩
        decorate_cost_old = achievementInfo[5]  # 装修成本
        houseCode = achievementInfo[0]
        # 修改装修成本
        base.open(page.designManageSharePage,designSharePage.searchMould['tr_contract'])
        base.input_text(designSharePage.searchMould['residential_name_loc'], houseCode)
        base.click(designSharePage.searchMould['search_btn_loc'])
        base.staleness_of(designSharePage.searchMould['tr_contract'])
        base.context_click(designSharePage.searchMould['tr_contract'])
        base.click(designSharePage.designShareMould['design_btn_2'], index=0)
        time.sleep(2)
        base.input_text(designSharePage.designShareMould['total_cost'], '68888.00')
        base.click(designSharePage.designShareMould['save_btn_2'])
        base.check_submit()
        # 获取最新的核算收进价和差价业绩
        time.sleep(10)
        achievementInfoNew = sqlbase.serach(achievementSql)
        profits_fee_new = achievementInfoNew[4]  # 差价业绩
        decorate_cost_new = achievementInfoNew[5]  # 装修成本
        base.diffAssert(lambda test:asserts(decorate_cost_new).is_not_equal_to(decorate_cost_old), 1047,
                        u'%s:出租合同 %s 对应装修成功修改后业绩中核算收进价异常，修改前 %s 修改后 %s' % (fileName, apartmentContractNum, decorate_cost_old, decorate_cost_new))
        base.diffAssert(lambda test: asserts(profits_fee_new).is_not_equal_to(profits_fee_old), 1047,
                        u'%s:出租合同 %s 对应委托成本修改后业绩中差价业绩异常，修改前 %s 修改后 %s' % (fileName, apartmentContractNum,profits_fee_old, profits_fee_new))

test_1047()