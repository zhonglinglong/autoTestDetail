# -*- coding:utf8 -*-

import time

from assertpy import assert_that as asserts

from common import sqlbase, page
from common.base import log, Base
from common.interface import createCustomer, createApartmentContract, addHouseContractAndFitment
from contract.apartmentContract.page import apartmentContractPage


@log
def test_1050():
    """修改出租合同承租到期日-2"""

    # describe：在出租合同详情中，修改出租合同承租到期日减1天；业绩发生变化
    # data：1、业绩审核状态为待审核；2、合同生成多条业绩；3、记录原业绩中出租和委托核算周期及差价业绩；
    # result：1、最后一条业绩中出租和委托核算周期都减1天；2、最后一条业绩中差价业绩变化；3、其他业绩记录中数据不变；

    fileName = 'apartmentAchievement_1050'

    with Base() as base:
        # 创建委托合同和出租合同
        houseSql = sqlbase.serach(
            "select house_id,residential_id,building_id,house_code from house where deleted=0 and city_code=330100 order by rand() limit 1")  # 获取随机开发房源
        houseInfo = {'houseID': houseSql[0], 'residentialID': houseSql[1], 'buildingID': houseSql[2],'houseCode': houseSql[3]}
        dateInfo = sqlbase.serach("select date(sysdate()),date_add(date(sysdate()),INTERVAL 1 day),date_add(date(sysdate()),interval 2 year),date_add(date(sysdate()),interval 27 month),"
                                  "date_add(date(sysdate()),INTERVAL 1 month),date_add(date(sysdate()),INTERVAL 14 month),date_add(date(sysdate()),INTERVAL 3 month),"
                                  "DATE_SUB(date_add(date(sysdate()),INTERVAL 14 month),INTERVAL 1 DAY) from dual")  # 日期元素
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
                                                        rent_start_date=dateInfo[1], rent_end_date=dateInfo[5],  # 承租14个月
                                                        deposit=rentPrice, payment_cycle='MONTH')
        apartmentContractNum = apartmentContractInfo['contractNum']
        achievementSql = "select substring_index(house_code,'-',1) from apartment_contract_achievement where contract_num='%s' and deleted=0" % apartmentContractNum
        base.diffAssert(lambda test: asserts(sqlbase.waitData(achievementSql, 2)).is_true(), 1050,
                        u'%s：业绩生成异常' % fileName)
        # 获取第一条业绩信息
        achievement1Sql = "select start_time,end_time,profits_fee from apartment_contract_achievement where contract_num='%s' and deleted=0 and accounting_num=1" % apartmentContractNum
        achievement1Info = sqlbase.serach(achievement1Sql)
        accountingEndTime1_old = achievement1Info[1]
        profits_fee1_old = achievement1Info[2]
        # 获取第二条业绩信息
        achievement2Sql = "select start_time,end_time,profits_fee from apartment_contract_achievement where contract_num='%s' and deleted=0 and accounting_num=2" % apartmentContractNum
        achievement2Info = sqlbase.serach(achievement2Sql)
        accountingEndTime2_old = achievement2Info[1]
        profits_fee2_old = achievement2Info[2]
        base.open(page.apartmentContractPage, apartmentContractPage.searchContractMould['tr_contract'])
        base.input_text(apartmentContractPage.searchContractMould['contract_num_loc'], apartmentContractNum)  # 输入合同编号
        base.click(apartmentContractPage.searchContractMould['search_button_loc'])
        base.staleness_of(apartmentContractPage.searchContractMould['tr_contract'])
        base.dblclick(apartmentContractPage.searchContractMould['tr_contract'],
                      checkLoc=apartmentContractPage.addApartmentContractMould['contract_num_loc'])  # 双击第一条数据
        base.type_date(apartmentContractPage.typeMould['rent_end_date2'], dateInfo[7])  # 承租到期日
        base.type_select(apartmentContractPage.typeMould['payment_type'], 'NORMAL')  # 正常付款
        base.type_select(apartmentContractPage.typeMould['payment_cycle'], 'MONTH')  # 一次性付款
        base.script("$('#contract_strategy_table > table > tbody > tr > td:nth-child(8) > input').click()")
        base.type_date(apartmentContractPage.addApartmentContractMould['rent_strategy1_end_loc'], dateInfo[7])
        base.click(apartmentContractPage.addApartmentContractMould['save_button'])
        base.check_submit()
        #获取最新的核算收进价和差价业绩
        time.sleep(10)
        # 获取第一条业绩信息
        achievement1InfoNew = sqlbase.serach(achievement1Sql)
        accountingEndTime1_new = achievement1InfoNew[1]
        profits_fee1_new = achievement1InfoNew[2]
        # 获取第二条业绩信息
        achievement2InfoNew = sqlbase.serach(achievement2Sql)
        accountingEndTime2_new = achievement2InfoNew[1]
        profits_fee2_new = achievement2InfoNew[2]
        base.diffAssert(lambda test: asserts(accountingEndTime1_new).is_equal_to(accountingEndTime1_old), 1050,
                        u'%s:出租合同 %s 对应承租期修改后首条业绩中核算周期异常，修改前 %s 修改后 %s' % (fileName, apartmentContractNum, accountingEndTime1_old, accountingEndTime1_new))
        base.diffAssert(lambda test: asserts(profits_fee1_new).is_equal_to(profits_fee1_old), 1050,
                        u'%s:出租合同 %s 对应委托成本修改后首条业绩中差价业绩异常，修改前 %s 修改后 %s' % (fileName, apartmentContractNum, profits_fee1_old, profits_fee1_new))
        # 第二条业绩前后对比
        base.diffAssert(lambda test: asserts(accountingEndTime2_new).is_not_equal_to(accountingEndTime2_old), 1050,
                        u'%s:出租合同 %s 对应承租期修改后末条业绩中核算周期异常，修改前 %s 修改后 %s' % (fileName, apartmentContractNum, accountingEndTime2_old, accountingEndTime2_new))
        base.diffAssert(lambda test: asserts(profits_fee2_new).is_not_equal_to(profits_fee2_old), 1050,
                        u'%s:出租合同 %s 对应委托成本修改后末条业绩中差价业绩异常，修改前 %s 修改后 %s' % (fileName, apartmentContractNum, profits_fee2_old, profits_fee2_new))

test_1050()