# -*- coding:utf8 -*-

import time

from assertpy import assert_that as asserts

from common import sqlbase, page
from common.base import log, Base
from common.interface import createCustomer, createApartmentContract, addHouseContractAndFitment
from contract.houseContract.page import houseContractPage


@log
def test_1044():
    """修改委托合同租金"""

    # describe：在委托合同详情中，修改业绩核算周期对应时间段的委托合同租金策略中的租金，业绩中对应发生变化
    # data：1、业绩审核状态为待审核；2、委托合同状态为待审核或者已初审；3、提前记录原业绩中的核算收进价和差价业绩；
    # result：1、新产生的业绩中核算收进价与原记录不同；2、新的差价业绩与原来的值不同；

    fileName = 'apartmentAchievement_1044'

    with Base() as base:
        # 创建委托合同和出租合同
        houseSql = sqlbase.serach(
            "select house_id,residential_id,building_id,house_code from house where deleted=0 and city_code=330100 order by rand() limit 1")  # 获取随机开发房源
        houseInfo = {'houseID': houseSql[0], 'residentialID': houseSql[1], 'buildingID': houseSql[2],'houseCode': houseSql[3]}
        dateInfo = sqlbase.serach("select date(sysdate()),date_add(date(sysdate()),INTERVAL 1 day),date_add(date(sysdate()),interval 2 year),date_add(date(sysdate()),interval 27 month),"
                                  "date_add(date(sysdate()),INTERVAL 1 month),date_add(date(sysdate()),INTERVAL 6 month) from dual")  # 日期元素
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
        achievementsql = "select substring_index(aca.house_code,'-',1),aca.is_active,aca.audit_status,aca.contract_audit_status,aca.profits_fee,aca.rent_cost from apartment_contract_achievement aca " \
                          "inner join apartment a on a.apartment_code=aca.house_code and a.apartment_id='%s' where aca.contract_num='%s' and aca.deleted=0" % (
                          apartmentId, apartmentContractNum)
        base.diffAssert(lambda test: asserts(sqlbase.waitData(achievementsql, 1)).is_true(), 1057,
                        u'%s:合同 %s 对应业绩生成异常' % (fileName, apartmentContractNum))
        profits_feeOld = sqlbase.serach(achievementsql)[4]  # 差价业绩
        rent_cost_old = sqlbase.serach(achievementsql)[5]  # 核算收进价
        houseCode = sqlbase.serach(achievementsql)[0]
        # 修改租金策略并且复审
        base.open(page.entrustContractPage, houseContractPage.contractSearchMould['tr_contract'])
        # base.input_text(houseContractPage.contractSearchMould['contract_num_loc'], info[2])
        base.input_text(houseContractPage.contractSearchMould['residential_name_loc'], houseCode)
        base.click(houseContractPage.contractSearchMould['search_button_loc'])  # 搜索
        base.staleness_of(houseContractPage.contractSearchMould['tr_contract'])  # 等待列表刷新
        base.dblclick(houseContractPage.contractSearchMould['tr_contract'],
                      checkLoc=houseContractPage.addHouseContractMould['contract_num_loc'])  # 双击第一条数据
        base.click(houseContractPage.addHouseContractMould['contract_strategy1.1_loc'])
        base.input_text(houseContractPage.addHouseContractMould['contract_strategy1_loc'], 4000)  # 第一年租金策略
        base.click(houseContractPage.addHouseContractMould['page1_save_button'])  # 保存
        for i in range(3):
            try:
                base.check_submit()
                break
            except:
                message = base.script(
                    "var a=$('.panel.window.messager-window>div:nth-child(2)>div:nth-child(2)').text();return a", True)
                messagehope = u'用户数据已经被其他用户更新'
                if messagehope in message:
                    base.click(houseContractPage.addHouseContractMould['message_close_loc'])  # 关闭提示
                    base.click(houseContractPage.addHouseContractMould['rent_save_button'])  # 保存
                    base.check_submit()
        # 委托合同复审
        base.click(houseContractPage.addHouseContractMould['tab_info_loc'], index=1)  # 租金页面
        base.click(houseContractPage.addHouseContractMould['rent_detail_selectAll'])  # 全选
        base.click(houseContractPage.addHouseContractMould['rent_audit_loc'])  # 审核
        base.click(houseContractPage.addHouseContractMould['audit_pass_loc'])  # 通过
        base.click(houseContractPage.addHouseContractMould['rent_audit_confirm'])  # 确认
        # 初审
        base.click(houseContractPage.addHouseContractMould['tab_info_loc'], index=3)  # 最后一页
        time.sleep(2)
        base.script('$("button[status=\'PASS\']")[2].click()')  # 初审
        base.click(houseContractPage.addHouseContractMould['contract_audit_confirm'])  # 确认
        for i in range(3):
            try:
                base.staleness_of(houseContractPage.contractSearchMould['tr_contract'])  # 等待数据刷新
                break
            except:
                message = base.script(
                    "var a=$('.panel.window.messager-window>div:nth-child(2)>div:nth-child(2)').text();return a", True)
                messagehope = u'用户数据已经被其他用户更新'
                if messagehope in message:
                    base.click(houseContractPage.addHouseContractMould['message_close_loc'])  # 关闭提示
                    base.click(houseContractPage.addHouseContractMould['contract_audit_confirm'])  # 确认
                    base.staleness_of(houseContractPage.contractSearchMould['tr_contract'])  # 等待数据刷新
        # 复审
        base.dblclick(houseContractPage.contractSearchMould['tr_contract'],
                      checkLoc=houseContractPage.addHouseContractMould['contract_num_loc'])  # 双击第一条数据
        base.click(houseContractPage.addHouseContractMould['tab_info_loc'], index=3)  # 最后一页
        time.sleep(2)
        base.script('$("button[status=\'APPROVED\']")[1].click()')  # 复审
        base.click(houseContractPage.addHouseContractMould['rentdif_cofirm_loc'])  # 租金策略不同提示确定
        base.click(houseContractPage.addHouseContractMould['contract_audit_confirm'])  # 确认
        for i in range(3):
            try:
                base.check_submit()
                break
            except:
                message = base.script(
                    "var a=$('.panel.window.messager-window>div:nth-child(2)>div:nth-child(2)').text();return a", True)
                messagehope = u'用户数据已经被其他用户更新'
                if messagehope in message:
                    base.click(houseContractPage.addHouseContractMould['message_close_loc'])  # 关闭提示
                    base.click(houseContractPage.addHouseContractMould['contract_audit_confirm'])  # 确认
                    base.check_submit()
        #获取最新业绩信息
        time.sleep(10)
        profits_feeNew = sqlbase.serach(achievementsql)[4]
        rent_cost_new = sqlbase.serach(achievementsql)[5]
        base.diffAssert(lambda test:asserts(rent_cost_new).is_not_equal_to(rent_cost_old),1044,
                        u'%s:出租合同 %s 对应委托成本修改后业绩中核算收进价异常，修改前 %s 修改后 %s' % (fileName, apartmentContractNum, rent_cost_old, rent_cost_new))
        base.diffAssert(lambda test: asserts(profits_feeNew).is_not_equal_to(profits_feeOld),1044,
                        u'%s:出租合同 %s 对应委托成本修改后业绩中差价业绩异常，修改前 %s 修改后 %s' % (fileName, apartmentContractNum,profits_feeOld, profits_feeNew))

test_1044()