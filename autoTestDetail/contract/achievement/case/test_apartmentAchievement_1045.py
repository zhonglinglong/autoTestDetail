# -*- coding:utf8 -*-
import time
from assertpy import assert_that as asserts

from common import sqlbase, page
from common.base import log, Base
from common.interface import createCustomer, createApartmentContract, addHouseContractAndFitment
from contract.apartmentContract.page import apartmentContractPage


@log
def test_1045():
    """修改出租合同租金"""

    # describe：在出租合同详情中，修改业绩核算周期对应时间段的出租合同租金策略中的租金,业绩发生变化
    # data：1、业绩审核状态为待审核；2、委托合同状态为待审核或者已初审；3、提前记录原业绩中的核算出租价和差价业绩；
    # result：1、新产生的业绩中核算出租价与原记录不同；2、新的差价业绩与原来的值不同；

    fileName = 'apartmentAchievement_1045'

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
        rentPriceInfo = sqlbase.serach("select rent_price,date(sysdate()) from apartment where apartment_id='%s'" % apartmentId)
        rentPrice = float(rentPriceInfo[0])
        customer = createCustomer()
        apartmentContractInfo = createApartmentContract(apartement_id=apartmentId, customerInfo=customer,
                                                        rent_price=rentPrice, sign_date=dateInfo[0],
                                                        rent_start_date=dateInfo[1], rent_end_date=dateInfo[5],  # 承租6个月
                                                        deposit=rentPrice, payment_cycle='MONTH')
        apartmentContractNum = apartmentContractInfo['contractNum']
        # 业绩检查
        achievementsql = "select aca.is_active,aca.audit_status,aca.contract_audit_status,aca.profits_fee,aca.achievementRent from apartment_contract_achievement aca " \
                          "inner join apartment a on a.apartment_code=aca.house_code and a.apartment_id='%s' where aca.contract_num='%s' and aca.deleted=0" % (
                          apartmentId, apartmentContractNum)
        base.diffAssert(lambda test: asserts(sqlbase.waitData(achievementsql, 1)).is_true(), 1057,
                        u'%s:合同 %s 对应业绩生成异常' % (fileName, apartmentContractNum))
        profits_feeOld = sqlbase.serach(achievementsql)[3]  # 差价业绩
        achievementRentOld = sqlbase.serach(achievementsql)[4]  # 核算出租价
        # 修改出租合同租金策略
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
        # # 获取最新的核算收进价和差价业绩
        time.sleep(10)
        achievementInfoNew = sqlbase.serach(achievementsql)
        profits_fee_new = achievementInfoNew[3]  # 差价业绩
        achievementRent_new = achievementInfoNew[4]  # 核算出租价
        base.diffAssert(lambda test: asserts(achievementRent_new).is_not_equal_to(achievementRentOld), 1045,
                        u'%s:出租合同 %s 对应租金策略修改后业绩中核算出租业绩异常，修改前 %s 修改后 %s' % (fileName, apartmentContractNum, achievementRent_new, achievementRentOld))
        base.diffAssert(lambda test: asserts(profits_fee_new).is_not_equal_to(profits_feeOld), 1045,
                        u'%s:出租合同 %s 对应委托成本修改后业绩中差价业绩异常，修改前 %s 修改后 %s' % (fileName, apartmentContractNum, profits_feeOld, profits_fee_new))

test_1045()