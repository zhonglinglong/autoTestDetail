# -*- coding:utf8 -*-

import time
from assertpy import assert_that as asserts
from common import sqlbase, page
from common.base import log, consoleLog, Base
from common.interface import createCustomer, createApartmentContract, addHouseContractAndFitment, audit, auditType, \
    auditStatus
from contract.achievement.page import apartmentAchievementPage
from contract.houseContract.page import houseContractPage

@log
def test_1056():
    """已审核的业绩修改委托合同免租期"""

    # describe：在委托合同详情中，修改业绩核算周期对应时间段的委托合同租免租期，已审核的业绩数据不变
    # data：1、业绩审核状态为待审核；1、业绩状态为已审核；3、提前记录原业绩中的核算收进价和差价业绩；
    # result：1、业绩中所有字段都不发生变化；

    fileName = 'apartmentAchievement_1056'

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
        base.diffAssert(lambda test: asserts(sqlbase.waitData(achievementSql, 1)).is_true(), 1056,
                        u'%s:合同 %s 对应业绩生成异常' % (fileName, apartmentContractNum))
        houseCode = sqlbase.serach(achievementSql)[0]
        # 委托合同审核
        audit(houseContractId,auditType.houseContract,auditStatus.chuShen,auditStatus.fuShen)
        # 出租合同审核
        audit(apartmentContractId,auditType.apartmentContract,auditStatus.chuShen,auditStatus.fuShen)
        # 业绩检查
        achievementsqlb = "select aca.is_active,aca.audit_status,aca.contract_audit_status,aca.profits_fee,aca.rent_cost from apartment_contract_achievement aca " \
                          "inner join apartment a on a.apartment_code=aca.house_code and a.apartment_id='%s' where aca.contract_num='%s' and aca.deleted=0 and aca.is_active='Y'" % (apartmentId, apartmentContractNum)
        base.diffAssert(lambda test: asserts(sqlbase.waitData(achievementsqlb, 1)).is_true(), 1056,
                        u'%s:合同 %s 对应业绩生效异常' % (fileName, apartmentContractNum))
        profits_feeOld = sqlbase.serach(achievementsqlb)[3]  # 差价业绩
        accountingCostOld = sqlbase.serach(achievementsqlb)[4]  # 核算收进价
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
        # 反审委托合同修改租金免租期并且复审
        audit(houseContractId, auditType.houseContract, auditStatus.fanShen)
        base.open(page.entrustContractPage, houseContractPage.contractSearchMould['tr_contract'])
        base.input_text(houseContractPage.contractSearchMould['residential_name_loc'], houseCode)
        base.click(houseContractPage.contractSearchMould['search_button_loc'])  # 搜索
        base.staleness_of(houseContractPage.contractSearchMould['tr_contract'])  # 等待列表刷新
        base.dblclick(houseContractPage.contractSearchMould['tr_contract'],
                      checkLoc=houseContractPage.addHouseContractMould['contract_num_loc'])  # 双击第一条数据
        time.sleep(3)
        base.script("$('#contract_strategy_table0 tr>td:nth-child(11)>input').click()")
        base.script("$('#contract_strategy_table0 tr>td:nth-child(11)>input').datebox('setValue','%s')" % dateInfo[6])
        base.click(houseContractPage.addHouseContractMould['page1_save_button'])  # 保存
        try:
            base.check_submit()
        except:
            message = base.script(
                "var a=$('.panel.window.messager-window>div:nth-child(2)>div:nth-child(2)').text();return a", True)
            messagehope = u'用户数据已经被其他用户更新'
            if messagehope in message:
                base.click(houseContractPage.addHouseContractMould['message_close_loc'])  # 关闭提示
                base.click(houseContractPage.addHouseContractMould['page1_save_button'])  # 保存
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
        # 数据库获取最新的核算收进价和差价业绩
        time.sleep(10)
        achievementInfoSql = "select profits_fee,rent_cost,end_time,achievementRent from apartment_contract_achievement where contract_num='%s' and deleted=0"%apartmentContractNum
        achievementInfo = sqlbase.serach(achievementInfoSql)
        rent_cost = achievementInfo[1]  # 核算收进价
        profits_fee = achievementInfo[0]  # 差价业绩
        base.diffAssert(lambda test: asserts(rent_cost).is_equal_to(accountingCostOld),1056,
                        u'%s:出租合同 %s 业绩对应委托成本修改后已审核业绩中核算收进价异常，修改前 %s 修改后 %s' % (fileName, apartmentContractNum, accountingCostOld, rent_cost))
        base.diffAssert(lambda test: asserts(profits_fee).is_equal_to(profits_feeOld),1056,
                        u'%s:出租合同 %s 业绩对应委托成本修改后已审核业绩中差价业绩异常，修改前 %s 修改后 %s' % (fileName, apartmentContractNum, profits_feeOld, profits_fee))


test_1056()