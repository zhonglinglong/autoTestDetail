# -*- coding:utf8 -*-

import time
from assertpy import assert_that as asserts
from selenium.webdriver.common.keys import Keys
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from common.interface import auditType, audit, auditStatus, createApartmentContract, createCustomer, \
    addHouseContractAndFitment
from contract.achievement.page import apartmentAchievementPage
from contract.apartmentContract.page import apartmentContractEndPage
from finance import apartmentContractReceivablePage


@log
def test_1138():
    """扣回业绩失效"""

    # describe：已生效且已审核的扣回业绩删除终止结算后业绩失效
    # data：1、业绩已审核；2、终止结算未复审；
    # result：1、业绩变成已失效；2、状态同步到预估业绩排行榜；

    fileName = 'apartmentAchievement_1138'

    with Base() as base:
        # 创建委托合同和出租合同
        houseSql = sqlbase.serach(
            "select house_id,residential_id,building_id,house_code from house where deleted=0 and city_code=330100 order by rand() limit 1")  # 获取随机开发房源
        houseInfo = {'houseID': houseSql[0], 'residentialID': houseSql[1], 'buildingID': houseSql[2], 'houseCode': houseSql[3]}
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
        houseContractInfo = sqlbase.serach("select hc.contract_num,hc.contract_id from house_contract hc inner join apartment a on a.house_id = hc.house_id and a.apartment_id='%s' "
                                           "where hc.audit_status='AUDIT' " % apartmentId)
        houseContractId = houseContractInfo[1]
        rentPriceInfo = sqlbase.serach("select rent_price,date(sysdate()) from apartment where apartment_id='%s'" % apartmentId)
        rentPrice = float(rentPriceInfo[0])
        customer = createCustomer()
        apartmentContractInfo = createApartmentContract(apartement_id=apartmentId, customerInfo=customer,
                                                        rent_price=rentPrice, sign_date=dateInfo[0],
                                                        rent_start_date=dateInfo[1], rent_end_date=dateInfo[5],  # 承租6个月
                                                        deposit=rentPrice, payment_cycle='MONTH')
        apartmentContractNum = apartmentContractInfo['contractNum']
        apartmentContractId = apartmentContractInfo['contractID']
        # 委托合同审核
        audit(houseContractId,auditType.houseContract,auditStatus.chuShen,auditStatus.fuShen)
        # 出租合同审核
        audit(apartmentContractId,auditType.apartmentContract,auditStatus.chuShen,auditStatus.fuShen)
        # 出租合同应收
        base.open(page.apartmentContractPayPage, apartmentContractReceivablePage.searchMould['tr_receviable_loc'])
        base.click(apartmentContractReceivablePage.searchMould['reset_button'])
        base.staleness_of(apartmentContractReceivablePage.searchMould['tr_receviable_loc'])
        base.input_text(apartmentContractReceivablePage.searchMould['contractNum_loc'],apartmentContractNum)
        base.click(apartmentContractReceivablePage.searchMould['search_button'])
        base.staleness_of(apartmentContractReceivablePage.searchMould['tr_receviable_loc'])
        moneyType = {u'首期管家服务费':int(0.07*rentPrice) , u'中介服务费':1000 , u'首期租金':int(rentPrice) , u'押金':int(rentPrice)}
        for i in range(3):
            moneyType_row = base.script("var a = $('[datagrid-row-index=\"%s\"] > [field=\"money_type\"] > div').text();return a" % i, True)
            base.click(apartmentContractReceivablePage.searchMould['receviabl_button'][i])
            base.input_text(apartmentContractReceivablePage.detailMould['receipts_money_loc'], moneyType[moneyType_row])
            base.click(apartmentContractReceivablePage.detailMould['receipts_type'])
            base.type_date(apartmentContractReceivablePage.detailMould['receipts_date_loc'], rentPriceInfo[1])
            base.input_text(apartmentContractReceivablePage.detailMould['alipay_card_loc'], '13676595110')
            base.input_text(apartmentContractReceivablePage.detailMould['operation_total_loc'], moneyType[moneyType_row])
            base.click(apartmentContractReceivablePage.detailMould['save_button'])
            base.check_submit()
            base.click(apartmentContractReceivablePage.detailMould['print_btn_close'])
            time.sleep(1)
        # 出单业绩生效检查
        achievementsql = "select aca.is_active,aca.audit_status,aca.contract_audit_status from apartment_contract_achievement aca inner join apartment a " \
                         "on a.apartment_code=aca.house_code and a.apartment_id='%s' where aca.contract_num='%s' and aca.deleted=0 and aca.is_active='Y'" \
                         "and aca.accounting_time is not null" % (apartmentId, apartmentContractNum)
        base.diffAssert(lambda test: asserts(sqlbase.waitData(achievementsql, 1)).is_true(), 1138,
                        u'%s:出租合同 %s 业绩生效异常，执行SQL:%s' % (fileName, apartmentContractNum, achievementsql))
        # 终止结算
        deposit_money = '888.88'  # 应付押金
        breach_money = '666.66'  # 转租费
        base.open(page.apartmentContractPage, apartmentContractEndPage.addContractEndMould['tr_contract'])
        base.input_text(apartmentContractEndPage.addContractEndMould['contract_num_loc'], apartmentContractNum)  # 输入合同编
        base.click(apartmentContractEndPage.addContractEndMould['search_button_loc'])  # 搜索
        base.staleness_of(apartmentContractEndPage.addContractEndMould['tr_contract'])  # 等待列表刷新
        base.context_click(apartmentContractEndPage.addContractEndMould['tr_contract'])  # 右击第一条数据
        base.click(apartmentContractEndPage.addContractEndMould['end_button_loc'], index=1)  # 终止结算
        base.click(apartmentContractEndPage.addContractEndMould['now_end_loc'])  # 立即终止
        base.input_text(apartmentContractEndPage.addContractEndMould['end_reason_loc'], u'退租')  # 终止原因
        endNum = 'AutoACE' + '-' + time.strftime('%m%d%H%M')
        base.type_date(apartmentContractEndPage.typeMould['end_date'], dateInfo[0])  # 终止日期：当天
        base.type_select(apartmentContractEndPage.typeMould['end_type'], 'OWNER_DEFAULT')  # 退租
        base.input_text(apartmentContractEndPage.addContractEndMould['end_num_loc'], endNum)  # 终止协议号
        base.type_select(apartmentContractEndPage.typeMould['receipt_type_loc'], 'PAYER')  # 承租人
        base.type_select(apartmentContractEndPage.typeMould['pay_type_loc'], 'PERSONAL')  # 个人
        base.input_text(apartmentContractEndPage.addContractEndMould['receipt_num_loc'], '123456789')  # 收款卡号
        base.send_keys(apartmentContractEndPage.addContractEndMould['receipt_num_loc'], Keys.ENTER)
        base.click(apartmentContractEndPage.addContractEndMould['cardconfirm_close_loc'])  # 银行卡确认无误
        base.dblclick(apartmentContractEndPage.addContractEndMould['project_type_loc'], index=1)  # 租金
        base.input_text(apartmentContractEndPage.addContractEndMould['payable_deposit_loc'], deposit_money)  # 应退押金：终止收支类型为收入才能删除
        base.dblclick(apartmentContractEndPage.addContractEndMould['project_type_loc'], index=12)  # 违约金
        base.input_text(apartmentContractEndPage.addContractEndMould['receivable_money_loc'], breach_money)  # 应收违约金
        base.upload_file(apartmentContractEndPage.addContractEndMould['add_end_image_loc'],
                         'C:\Users\Public\Pictures\Sample Pictures\jsp.jpg')  # 传图
        base.wait_element(apartmentContractEndPage.addContractEndMould['end_image_loc'])
        base.input_text(apartmentContractEndPage.addContractEndMould['remark_loc'], 'AutoTest')  # 备注
        base.click(apartmentContractEndPage.addContractEndMould['submit_button'])  # 提交
        base.check_submit()  # 等待提交完成
        # 终止结算审核
        contractEndAdd="SELECT ace.end_id FROM apartment_contract ac,apartment_contract_end ace WHERE ac.contract_id = ace.contract_id and ace.audit_status='NO_AUDIT' " \
                       "AND ace.end_type='OWNER_DEFAULT'and ace.deleted=0 and ace.end_contract_num='%s'" % endNum
        apartmentContractEndId = sqlbase.serach(contractEndAdd)[0]
        audit(apartmentContractEndId, auditType.apartmentContractEnd, auditStatus.chuShen, auditStatus.fuShen)
        # 扣回业绩检查
        backAchievementSql = "select is_active,achieve_id,accounting_time from back_achievement where contract_num='%s' and deleted=0 and contract_end_type='OWNER_DEFAULT' " \
                             "and is_active='Y'" % apartmentContractNum
        base.diffAssert(lambda test: asserts(sqlbase.waitData(backAchievementSql, 1)).is_true(), 1138,
                        u'%s:出租合同 %s 扣回业绩生效异常，执行SQL：%s' % (fileName, apartmentContractNum, backAchievementSql))
        # 业绩审核
        base.open(page.backAchievementPage, apartmentAchievementPage.searchContractMould['tr_contract'])
        base.click(apartmentAchievementPage.searchContractMould['reset_button_loc'])  # 重置
        time.sleep(10)  # 等待重新核算更新数据
        base.input_text(apartmentAchievementPage.searchContractMould['contract_num_loc'], apartmentContractNum)  # 输入合同号
        base.click(apartmentAchievementPage.searchContractMould['search_button_loc'])  # 查找
        base.staleness_of(apartmentAchievementPage.searchContractMould['tr_contract'])  # 等待第一条数据刷新
        base.dblclick(apartmentAchievementPage.searchContractMould['tr_contract'],
                      checkLoc=apartmentAchievementPage.detailAchievementMoudle['contract_num_loc'])  # 点击第一条数据等待详情页面完全显示
        base.click(apartmentAchievementPage.detailAchievementMoudle['audit_button_loc'])
        base.input_text(apartmentAchievementPage.detailAchievementMoudle['contract_audit_content'], 'ok')
        base.click(apartmentAchievementPage.detailAchievementMoudle['contract_audit_confirm'])
        base.check_submit()
        # 删除终止结算
        audit(apartmentContractEndId, auditType.apartmentContractEnd, auditStatus.fanShen)
        base.open(page.contractEndPage, apartmentContractEndPage.searchMould['tr_contract_end'])
        base.input_text(apartmentContractEndPage.searchMould['contract_num_loc'], apartmentContractNum)  # 输入合同号
        base.click(apartmentContractEndPage.searchMould['search_button_loc'])  # 搜索
        base.staleness_of(apartmentContractEndPage.searchMould['tr_contract_end'])  # 等待列表刷新
        base.click(apartmentContractEndPage.addContractEndMould['delete_button'])
        base.click(apartmentContractEndPage.addContractEndMould['delete_button_confirm'])
        base.check_submit()
        # 终止结算删除后
        backAchievementDelSql = "select is_active,achieve_id,accounting_time from back_achievement where contract_num='%s' and deleted=0 and contract_end_type='OWNER_DEFAULT' " \
                                "and is_active='INVALID'" % apartmentContractNum
        base.diffAssert(lambda test: asserts(sqlbase.waitData(backAchievementDelSql, 1)).is_true(), 1138,
                        u'%s:出租合同 %s 扣回业绩审核删除终止结算后业绩异常，执行SQL：%s' % (fileName, apartmentContractNum, backAchievementDelSql))

        # 业绩分成明细表（预估业绩排行榜数据取值表,检查扣回业绩同步更新到预估业绩排行榜）
        breahAchievementDetailSql = "select ca.receivable,ca.is_active from contract_achievement ca inner join contract_achievement_detail cad on ca.achieve_id=cad.achieve_id inner " \
                                    "join back_achievement ba on ba.achieve_id=ca.achieve_id and ba.contract_end_type='OWNER_DEFAULT' and ba.deleted=0 and ba.contract_num='%s' " \
                                    "where ca.contract_category='OWNER_DEFAULT_BACK' and ca.deleted=0" % apartmentContractNum
        breachAchievementStatus = sqlbase.serach(breahAchievementDetailSql)[1]
        base.diffAssert(lambda test: asserts(breachAchievementStatus).is_equal_to('INVALID'), 1138,
                        u'%s:出租合同 %s 退租扣回业绩审核删除终止结算后,业绩分成明细业绩状态异常，期望值 INVALID 实际值 %s' % (fileName, apartmentContractNum, breachAchievementStatus))

test_1138()