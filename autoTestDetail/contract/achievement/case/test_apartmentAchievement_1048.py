# -*- coding:utf8 -*-

import time

from assertpy import assert_that as asserts
from selenium.webdriver.common.keys import Keys

from common import sqlbase, page
from common.base import log, Base
from common.interface import createCustomer, createApartmentContract, addHouseContractAndFitment, audit, auditType, \
    auditStatus
from contract.achievement.page import apartmentAchievementPage
from contract.apartmentContract.page import apartmentContractEndPage
from contract.houseContract.page import houseContractPage


@log
def test_1048():
    """修改前合同终止结算日期"""

    # describe：修改前合同终止结算日期
    # data：1、业绩审核状态为待审核；2、业绩对应的合同有前合同，且前合同有终止结算；3、前合同终止日期之后无资源划转；4、记录原业绩中的委托核算周期和差价业绩；5、终止结算日期不在委托合同免租期内；
    # result：1、新业绩中委托核算周期比原来多1天；2、新的差价业绩与原来的值不同；

    fileName = 'apartmentAchievement_1048'

    with Base() as base:
        # 创建委托合同和出租合同
        houseSql = sqlbase.serach(
            "select house_id,residential_id,building_id,house_code from house where deleted=0 and city_code=330100 order by rand() limit 1")  # 获取随机开发房源
        houseInfo = {'houseID': houseSql[0], 'residentialID': houseSql[1], 'buildingID': houseSql[2],'houseCode': houseSql[3]}
        dateInfo = sqlbase.serach("select date(sysdate()),DATE_SUB(date(sysdate()),INTERVAL 1 year) ,DATE_SUB(date(sysdate()),INTERVAL 11 MONTH) ,DATE_ADD(date(sysdate()),INTERVAL 1 YEAR) ,"
                                  "DATE_ADD(date(sysdate()),INTERVAL 15 MONTH) ,DATE_SUB(date(sysdate()),INTERVAL 1 MONTH),DATE_SUB(date(sysdate()),INTERVAL 20 DAY),"
                                  "DATE_SUB(date(DATE_ADD(date(sysdate()),INTERVAL 1 YEAR)),INTERVAL 1 DAY ) from dual ")  # 日期元素
        apartmentId = addHouseContractAndFitment(apartment_type='MANAGE', entrust_type='SHARE', sign_date=dateInfo[1],
                                                 owner_sign_date=dateInfo[1], entrust_start_date=dateInfo[1],
                                                 entrust_end_date=dateInfo[7], delay_date=dateInfo[4],
                                                 free_start_date=dateInfo[1], free_end_date=dateInfo[2],
                                                 first_pay_date=dateInfo[1], second_pay_date=dateInfo[2],
                                                 rent=3000, parking=100, year_service_fee=500, payment_cycle='MONTH',
                                                 fitment_start_date=dateInfo[1], fitment_end_date=dateInfo[2], rooms=3,
                                                 fitmentCost=88888,houseInfo=houseInfo)
        rentPriceInfo = sqlbase.serach("select rent_price,date(sysdate()) from apartment where apartment_id='%s'" % apartmentId)
        rentPrice = float(rentPriceInfo[0])
        customer = createCustomer()
        apartmentContractInfoF = createApartmentContract(apartement_id=apartmentId, customerInfo=customer,
                                                        rent_price=rentPrice, sign_date=dateInfo[2],
                                                        rent_start_date=dateInfo[2], rent_end_date=dateInfo[7],
                                                        deposit=rentPrice, payment_cycle='MONTH')
        apartmentContractNumF = apartmentContractInfoF['contractNum']
        apartmentContractIdF = apartmentContractInfoF['contractID']
        # 第一份合同审核
        audit(apartmentContractIdF,auditType.apartmentContract,auditStatus.chuShen,auditStatus.fuShen)
        # base.open(page.apartmentContractPage, apartmentContractPage.searchContractMould['tr_contract'])
        # base.input_text(apartmentContractPage.searchContractMould['contract_num_loc'], apartmentContractNumF)  # 输入合同编号
        # base.click(apartmentContractPage.searchContractMould['search_button_loc'])
        # base.staleness_of(apartmentContractPage.searchContractMould['tr_contract'])
        # base.dblclick(apartmentContractPage.searchContractMould['tr_contract'])  # 双击第一条数据
        # # 打开详情页需要加载，但DOM其实已经加载完仍旧无法点击，此处加5秒等待
        # for i in range(5):
        #     try:
        #         base.click(apartmentContractPage.addApartmentContractMould['tab_info_loc'], index=4)  # 租客详情
        #         break
        #     except:
        #         time.sleep(1)
        # # 初审
        # base.click(apartmentContractPage.addApartmentContractMould['chushen_loc'])  # 初审
        # base.click(apartmentContractPage.addApartmentContractMould['contract_audit_confirm'])  # 确定
        # base.staleness_of(apartmentContractPage.searchContractMould['tr_contract'])  # 等待列表刷新
        # base.dblclick(apartmentContractPage.searchContractMould['tr_contract'])  # 双击第一条数据
        # for i in range(5):
        #     try:
        #         base.click(apartmentContractPage.addApartmentContractMould['tab_info_loc'], index=4)  # 租客详情
        #         break
        #     except:
        #         time.sleep(1)
        # # 复审
        # base.click(apartmentContractPage.addApartmentContractMould['fushen_loc'])  # 复审
        # base.click(apartmentContractPage.addApartmentContractMould['contract_audit_confirm'])  # 确定
        # base.staleness_of(apartmentContractPage.searchContractMould['tr_contract'])  # 等待列表刷新
        #终止结算
        base.open(page.apartmentContractPage, apartmentContractEndPage.addContractEndMould['tr_contract'])
        base.input_text(apartmentContractEndPage.addContractEndMould['contract_num_loc'], apartmentContractNumF)  # 输入合同编
        base.click(apartmentContractEndPage.addContractEndMould['search_button_loc'])  # 搜索
        base.staleness_of(apartmentContractEndPage.addContractEndMould['tr_contract'])  # 等待列表刷新
        base.context_click(apartmentContractEndPage.addContractEndMould['tr_contract'])  # 右击第一条数据
        base.click(apartmentContractEndPage.addContractEndMould['end_button_loc'], index=1)  # 终止结算
        base.click(apartmentContractEndPage.addContractEndMould['now_end_loc'])  # 立即终止
        base.input_text(apartmentContractEndPage.addContractEndMould['end_reason_loc'], u'承租周期已完')  # 终止原因
        endNum = 'AutoACE' + '-' + time.strftime('%m%d%H%M')
        base.type_date(apartmentContractEndPage.typeMould['end_date'], dateInfo[5])  # 终止日期：合同到期日
        base.type_select(apartmentContractEndPage.typeMould['end_type'], 'OWNER_DEFAULT')  # 退租
        base.input_text(apartmentContractEndPage.addContractEndMould['end_num_loc'], endNum)  # 终止协议号
        base.type_select(apartmentContractEndPage.typeMould['receipt_type_loc'], 'PAYER')  # 承租人
        base.type_select(apartmentContractEndPage.typeMould['pay_type_loc'], 'PERSONAL')  # 个人
        base.input_text(apartmentContractEndPage.addContractEndMould['receipt_num_loc'], '123456789')  # 收款卡号
        base.send_keys(apartmentContractEndPage.addContractEndMould['receipt_num_loc'], Keys.ENTER)
        base.click(houseContractPage.addHouseContractMould['close_loc'])  # 确认无误
        base.dblclick(apartmentContractEndPage.addContractEndMould['weiyuejin_loc'], index=12)  # 违约金
        base.input_text(apartmentContractEndPage.addContractEndMould['receivable_money_loc'], '888.88')  # 应收违约金
        base.input_text(apartmentContractEndPage.addContractEndMould['payable_money_loc'], '666.66')  # 应退违约金
        base.upload_file(apartmentContractEndPage.addContractEndMould['add_end_image_loc'],
                         'C:\Users\Public\Pictures\Sample Pictures\jsp.jpg')  # 传图
        base.wait_element(apartmentContractEndPage.addContractEndMould['end_image_loc'])
        base.input_text(apartmentContractEndPage.addContractEndMould['remark_loc'], 'AutoTest')  # 备注
        base.click(apartmentContractEndPage.addContractEndMould['submit_button'])  # 提交
        base.check_submit()  # 等待提交完成
        apartmentStatusSql = "select * from apartment where rent_status='WAITING_RENT' and apartment_id='%s' " % apartmentId
        base.diffAssert(lambda test: asserts(sqlbase.waitData(apartmentStatusSql, 1)).is_true(), 1048,
                        u'%s:房源ID %s 未释放' % (fileName, apartmentId))
        # 第二份出租合同
        customer = createCustomer()
        apartmentContractInfoS = createApartmentContract(apartement_id=apartmentId, customerInfo=customer,
                                                         rent_price=rentPrice, sign_date=dateInfo[0],
                                                         rent_start_date=dateInfo[0], rent_end_date=dateInfo[7],
                                                         deposit=rentPrice, payment_cycle='MONTH')
        apartmentContractNumS = apartmentContractInfoS['contractNum']
        achievementSql = "select profits_fee from apartment_contract_achievement where contract_num='%s' and deleted=0 and accounting_num=1" % apartmentContractNumS
        base.diffAssert(lambda test: asserts(sqlbase.waitData(achievementSql, 1)).is_true(), 1048,
                        u'%s:出租合同 %s 业绩生成异常' % (fileName, apartmentContractNumS))
        # 获取当前的核算收进价和差价业绩
        base.open(page.apartmentAchievementPage, apartmentAchievementPage.searchContractMould['tr_contract'])
        base.click(apartmentAchievementPage.searchContractMould['reset_button_loc'])  # 重置
        base.input_text(apartmentAchievementPage.searchContractMould['contract_num_loc'],apartmentContractNumS)  # 输入合同号
        base.click(apartmentAchievementPage.searchContractMould['search_button_loc'])  # 查找
        base.staleness_of(apartmentAchievementPage.searchContractMould['tr_contract'])  # 等待第一条数据刷新
        base.dblclick(apartmentAchievementPage.searchContractMould['tr_contract'],
                      checkLoc=apartmentAchievementPage.detailAchievementMoudle['contract_num_loc'])  # 点击第一条数据等待详情页面完全显示
        accountingmonthOld = base.script(
            "var a = $('#house_contract_table tbody > tr >td:nth-child(9)').text();return a", True)
        profits_fee_old = sqlbase.serach(achievementSql)[0]
        # 修改前合同终止结算日期
        base.open(page.contractEndPage, apartmentContractEndPage.searchMould['tr_contract_end'])
        base.input_text(apartmentContractEndPage.searchMould['contract_num_loc'], apartmentContractNumF)
        base.click(apartmentContractEndPage.searchMould['search_button_loc'])
        base.staleness_of(apartmentContractEndPage.searchMould['tr_contract_end'])
        base.dblclick(apartmentContractEndPage.searchMould['tr_contract_end'],
                      checkLoc=apartmentContractEndPage.addContractEndMould['apartment_num_loc'])
        time.sleep(3)
        base.type_date(apartmentContractEndPage.typeMould['end_date'], dateInfo[6])  # 终止日期：合同到期日
        base.click(apartmentContractEndPage.addContractEndMould['save_button'])  # 保存
        base.check_submit()
        # 获取最新的核算收进价和差价业绩
        base.open(page.apartmentAchievementPage, apartmentAchievementPage.searchContractMould['tr_contract'])
        base.click(apartmentAchievementPage.searchContractMould['reset_button_loc'])  # 重置
        time.sleep(10)
        base.input_text(apartmentAchievementPage.searchContractMould['contract_num_loc'], apartmentContractNumS)  # 输入合同号
        base.click(apartmentAchievementPage.searchContractMould['search_button_loc'])  # 查找
        base.staleness_of(apartmentAchievementPage.searchContractMould['tr_contract'])  # 等待第一条数据刷新
        base.dblclick(apartmentAchievementPage.searchContractMould['tr_contract'],
                      checkLoc=apartmentAchievementPage.detailAchievementMoudle['contract_num_loc'])  # 点击第一条数据等待详情页面完全显示
        accountingmonthNew = base.script(
            "var a = $('#house_contract_table tbody > tr >td:nth-child(9)').text();return a", True)
        profits_fee_new = sqlbase.serach(achievementSql)[0]
        base.diffAssert(lambda test: asserts(accountingmonthNew).is_not_equal_to(accountingmonthOld), 1048,
                        u'%s:出租合同 %s 对应前合同终止日期修改后业绩中核算收进价异常，修改前 %s 修改后 %s' % (fileName, apartmentContractNumS, accountingmonthOld, accountingmonthNew))
        base.diffAssert(lambda test: asserts(profits_fee_new).is_not_equal_to(profits_fee_old), 1048,
                        u'%s:出租合同 %s 对应委托成本修改后业绩中差价业绩异常，修改前 %s 修改后 %s' % (fileName, apartmentContractNumS, profits_fee_old, profits_fee_new))

test_1048()