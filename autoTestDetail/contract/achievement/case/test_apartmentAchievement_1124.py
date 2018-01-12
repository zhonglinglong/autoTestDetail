# -*- coding:utf8 -*-

import time
from assertpy import assert_that as asserts
from selenium.webdriver.common.keys import Keys
from common import sqlbase, page
from common.base import log, consoleLog, Base
from common.interface import createCustomer, createApartmentContract, audit, auditType, auditStatus
from contract.achievement.page import apartmentAchievementPage
from contract.apartmentContract.page import apartmentContractEndPage
from finance import apartmentContractReceivablePage

@log
def test_1067():
    """扣回业绩由未生效变成生效"""

    # describe： 核发月份条件满足后生成核发月份
    # data：1、业绩违约类别为退租、换租、收房、转租；2、业绩状态为未生效且未审核；3、正常出房业绩条件全部达成；4、出租终止结算未复审；
    # result：1、业绩状态变为生效；2、业绩产生核发月份；3、业绩状态和核发月份同步更新到预估业绩排行榜；4、生效业绩加入核发业绩排行榜；

    fileName = 'apartmentAchievement_1067'
    randomApartment = "SELECT a.apartment_code,a.apartment_id,hc.contract_num,hc.contract_id FROM apartment a INNER JOIN house_contract hc " \
                      "ON hc.contract_id = a.house_contract_id AND hc.is_active = 'Y' AND hc.deleted = 0 AND hc.audit_status='APPROVED' AND hc.contract_status = 'EFFECTIVE' " \
                      "INNER JOIN fitment_house fh on fh.house_id=hc.house_id AND fh.fitment_status='HANDOVER' WHERE a.deleted = 0 " \
                      "AND a.rent_price > 0 AND a.city_code = 330100 AND hc.entrust_type = 'SHARE' AND a.rent_status='WAITING_RENT'" \
                      "AND hc.real_due_date>date_add(date(sysdate()), interval 1 YEAR) ORDER BY RAND() LIMIT 1"
    if sqlbase.get_count(randomApartment) == 0:
        consoleLog(u'%s:SQL查无数据！'% fileName, 'w')
        consoleLog(u'执行SQL：%s' % randomApartment)
        return
    info = sqlbase.serach(randomApartment)
    apartmentCode = info[0]
    apartmentId = info[1]
    consoleLog(u'%s:使用房源 %s 签约出租合同做退租违约' % (fileName,apartmentCode))
    dateInfo = sqlbase.serach(
        "SELECT entrust_start_date,entrust_end_date,date(sysdate()),date_add(date(sysdate()), interval 1 DAY),date_add(date(sysdate()), interval 6 month) "
        "from house_contract where contract_num = '%s'" % info[2])  # 获取时间元素

    with Base() as base:

        customer = createCustomer()
        rentPriceInfo = sqlbase.serach("select rent_price,date(sysdate()) from apartment where apartment_id='%s'" % apartmentId)
        rentPrice = float(rentPriceInfo[0])
        apartmentContractInfo = createApartmentContract(apartement_id=apartmentId, customerInfo=customer,
                                                        rent_price=rentPrice, sign_date=dateInfo[2],
                                                        rent_start_date=dateInfo[3], rent_end_date=dateInfo[4],
                                                        deposit=rentPrice, payment_cycle='MONTH')
        apartmentContractNum = apartmentContractInfo['contractNum']
        apartmentContractId = apartmentContractInfo['contractID']
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
        # 出房业绩达成检查
        achievementsql = "select aca.is_active,aca.audit_status,aca.accounting_time,aca.achievement_id from apartment_contract_achievement aca inner join apartment a " \
                         "on a.apartment_code=aca.house_code where contract_num='%s' and a.apartment_code='%s'and aca.deleted=0 and aca.is_active='Y' and aca.accounting_time " \
                         "is not null" % (apartmentContractNum, apartmentCode)
        base.diffAssert(lambda test: asserts(sqlbase.waitData(achievementsql, 1)).is_true(), 1067,
                        u'%s:出租合同 %s 出房业绩生效异常，执行SQL：%s' % (fileName, apartmentContractNum, achievementsql))
        # 出租合同终止结算
        breach_money = '888.88'  # 应收违约金
        zhuanzu_money = '666.66'  # 转租费
        base.open(page.apartmentContractPage, apartmentContractEndPage.addContractEndMould['tr_contract'])
        base.input_text(apartmentContractEndPage.addContractEndMould['contract_num_loc'], apartmentContractNum)  # 输入合同编
        base.click(apartmentContractEndPage.addContractEndMould['search_button_loc'])  # 搜索
        base.staleness_of(apartmentContractEndPage.addContractEndMould['tr_contract'])  # 等待列表刷新
        base.context_click(apartmentContractEndPage.addContractEndMould['tr_contract'])  # 右击第一条数据
        base.click(apartmentContractEndPage.addContractEndMould['end_button_loc'], index=1)  # 终止结算
        base.click(apartmentContractEndPage.addContractEndMould['now_end_loc'])  # 立即终止
        base.input_text(apartmentContractEndPage.addContractEndMould['end_reason_loc'], u'退租')  # 终止原因
        endNum = 'AutoACE' + '-' + time.strftime('%m%d%H%M')
        base.type_date(apartmentContractEndPage.typeMould['end_date'], info[2])  # 终止日期：当天
        base.type_select(apartmentContractEndPage.typeMould['end_type'], 'OWNER_DEFAULT')  # 退租
        base.input_text(apartmentContractEndPage.addContractEndMould['end_num_loc'], endNum)  # 终止协议号
        base.type_select(apartmentContractEndPage.typeMould['receipt_type_loc'], 'PAYER')  # 承租人
        base.type_select(apartmentContractEndPage.typeMould['pay_type_loc'], 'PERSONAL')  # 个人
        base.input_text(apartmentContractEndPage.addContractEndMould['receipt_num_loc'], '123456789')  # 收款卡号
        base.send_keys(apartmentContractEndPage.addContractEndMould['receipt_num_loc'], Keys.ENTER)
        base.click(apartmentContractEndPage.addContractEndMould['cardconfirm_close_loc'])  # 银行卡确认无误
        base.dblclick(apartmentContractEndPage.addContractEndMould['weiyuejin_loc'], index=12)  # 违约金
        base.input_text(apartmentContractEndPage.addContractEndMould['receivable_money_loc'], breach_money)  # 应收违约金
        base.dblclick(apartmentContractEndPage.addContractEndMould['weiyuejin_loc'], index=21)  # 转租费
        base.input_text(apartmentContractEndPage.addContractEndMould['zhuanzu_money_loc'], zhuanzu_money)  # 应收转租金
        base.upload_file(apartmentContractEndPage.addContractEndMould['add_end_image_loc'],
                         'C:\Users\Public\Pictures\Sample Pictures\jsp.jpg')  # 传图
        base.wait_element(apartmentContractEndPage.addContractEndMould['end_image_loc'])
        base.input_text(apartmentContractEndPage.addContractEndMould['remark_loc'], 'AutoTest')  # 备注
        base.click(apartmentContractEndPage.addContractEndMould['submit_button'])  # 提交
        base.check_submit()  # 等待提交完成
        contractEndAdd = "SELECT ace.end_contract_num,ace.end_id FROM apartment_contract ac,apartment_contract_end ace WHERE ac.contract_id = ace.contract_id " \
                         "and ace.audit_status='NO_AUDIT' AND ace.end_type='OWNER_DEFAULT'and ace.deleted=0 and ac.contract_num='%s'" % apartmentContractNum
        base.diffAssert(lambda test: asserts(sqlbase.waitData(contractEndAdd, 1)).is_true(), 1067,
                        u'%s:出租合同 %s 终止结算新增异常，执行SQL：%s' % (fileName, apartmentContractNum, contractEndAdd))
        apartmentContractEndId = sqlbase.serach(contractEndAdd)[1]
        audit(apartmentContractEndId, auditType.apartmentContractEnd, auditStatus.chuShen, auditStatus.fuShen)  # 终止结算审核

        # 扣回业绩生效检查
        backAchievementSql = "select is_active,achieve_id,accounting_time from back_achievement where contract_num='%s' and deleted=0 and contract_end_type='OWNER_DEFAULT' " \
                             "and accounting_time is not null" % apartmentContractNum
        if sqlbase.waitData(backAchievementSql, 1):
            backAchievementInfo = sqlbase.serach(backAchievementSql)
        else:
            consoleLog(u'%s:出租合同 %s 退租终止生成扣回业绩异常，执行SQL：%s' % (fileName, apartmentContractNum, backAchievementSql))

        # 业绩分成明细表（预估业绩排行榜数据取值表,检查违约业绩同步更新到预估业绩排行榜）
        backAchievementDetailSql = "select date_format(ca.achievement_month,'%%Y-%%m') from contract_achievement ca inner join apartment_contract ac on ac.contract_id=ca.contract_id and ca.achieve_id='%s' inner join contract_achievement_detail cad " \
                                   "on cad.achieve_id=ca.achieve_id where ca.deleted=0 and ca.contract_category='OWNER_DEFAULT_BACK'" % backAchievementInfo[1]
        achievementDetialConunt = sqlbase.get_count(backAchievementDetailSql)
        base.diffAssert(lambda test: asserts(sqlbase.serach(backAchievementDetailSql)[0]).is_equal_to(backAchievementInfo[2]), 1167,
                        u'%s:出租合同 %s 退租终止扣回业绩分成明细核发月份生成异常' % (fileName, apartmentContractNum))

        # 核发业绩排行榜检查
        base.open(page.achievementListPage, apartmentAchievementPage.searchContractMould['tr_contract'])
        base.click(apartmentAchievementPage.searchContractMould['reset_button_loc'])  # 重置
        base.staleness_of(apartmentAchievementPage.searchContractMould['tr_contract'])
        base.input_text(apartmentAchievementPage.searchContractMould['contract_num_hefa_loc'], apartmentContractNum)  # 输入合同号
        base.type_select(apartmentAchievementPage.searchContractMould['category_loc'], 'OWNER_DEFAULT_BACK')  # 分类：退租扣回
        base.click(apartmentAchievementPage.searchContractMould['search_button_loc'])  # 查找
        base.staleness_of(apartmentAchievementPage.searchContractMould['tr_contract'])  # 等待第一条数据刷新
        for i in range(achievementDetialConunt):
            achievement_month = base.script(
                "var a = $('[datagrid-row-index=\"%s\"] > [field=\"achievement_month\"] > div').text();return a" % i, True)
            base.diffAssert(lambda test: asserts(achievement_month).is_equal_to(backAchievementInfo[2]), 1067,
                            u'%s:出租合同 %s 对应退租终止违约业绩有核发月份的同步到核发业绩排行榜异常' % (fileName, apartmentContractNum))

test_1067()