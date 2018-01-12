# -*- coding:utf8 -*-

import datetime,time
from assertpy import assert_that as asserts
from selenium.webdriver.common.by import By
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.achievement.page import apartmentAchievementPage
from contract.apartmentContract.page import apartmentContractPage
from contract.earnest import earnestPage
from customer import customerPage

@log
def test_1096():
    """下定违约业绩审核后修改违约金额"""

    # describe：下定违约业绩审核后修改违约金额
    # data：1、违约金列表中记录未审核；2、业绩状态已审核；
    # result：1、业绩不发生变化

    fileName = 'apartmentAchievement_1096'
    apartmentSql = "SELECT a.apartment_code,a.apartment_id,hc.contract_num,hc.contract_id,a.rent_price FROM apartment a INNER JOIN house_contract hc " \
                   "ON hc.contract_id = a.house_contract_id AND hc.is_active = 'Y' AND hc.deleted = 0 AND hc.audit_status='APPROVED' AND hc.contract_status = 'EFFECTIVE' " \
                   "INNER JOIN fitment_house fh on fh.house_id=hc.house_id AND fh.fitment_status='HANDOVER' WHERE a.deleted = 0 " \
                   "AND a.rent_price > 0 AND a.city_code = 330100 AND hc.entrust_type = 'SHARE' AND a.rent_status='WAITING_RENT' AND hc.apartment_type='BRAND' " \
                   "AND hc.real_due_date>date_add(date(sysdate()), interval 2 YEAR) ORDER BY RAND() LIMIT 1"
    if sqlbase.get_count(apartmentSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % apartmentSql)
        return
    apartmentinfo = sqlbase.serach(apartmentSql)
    apartmentCode = apartmentinfo[0]
    earnestMoney = apartmentinfo[4] if float(apartmentinfo[4]) > 1000.00 else '1000.00'
    consoleLog(u'%s:取随机转租房源 %s 做下定' % (fileName, apartmentCode))

    with Base() as base:
        # 下定
        base.open(page.customerListPage, customerPage.listMould['tr_customer'])
        try:
             base.find_element(By.ID, 'search_btn').click()
             base.staleness_of(customerPage.listMould['tr_customer'])  # 搜索等待列表刷新
        except:
             base.click(
                 (By.CSS_SELECTOR, '.panel.window > div:nth-child(1) > div.panel-tool > a'))  # 可能会有分配租客的弹窗出现，此为关闭
        base.type_select(customerPage.listMould['customer_status_loc'],'EFFECTIVE')
        base.click(customerPage.listMould['search_button'])
        base.staleness_of(customerPage.listMould['tr_customer'])  # 搜索等待列表刷新
        customerCode = base.script(
             "var a = $('[datagrid-row-index=\"0\"] > [field=\"customer_num\"] > div > font').text();return a", True)  # 获取第一条数据编号
        base.input_text(customerPage.listMould['customer_name_search'], customerCode)
        base.click(customerPage.listMould['search_button'])
        base.staleness_of(customerPage.listMould['tr_customer'])  # 搜索等待列表刷新
        base.click(customerPage.listMould['book_loc'])  # 下定
        base.input_text(customerPage.listMould['earnest_money_loc'], earnestMoney)  # 定金
        base.click(customerPage.listMould['property_address'])  # 选择房源
        base.click(apartmentContractPage.customerSignMould['share'])  # 点合租
        base.input_text(apartmentContractPage.customerSignMould['search_apartment_loc'], apartmentCode)  # 房源编号
        base.click(apartmentContractPage.customerSignMould['house_search_btn'])  # 搜索
        base.staleness_of(apartmentContractPage.customerSignMould['apartment_loc'])
        base.dblclick(apartmentContractPage.customerSignMould['apartment_loc'])  # 选择房源
        base.upload_file(apartmentContractPage.customerSignMould['add_image_loc'],
                         'C:\Users\Public\Pictures\Sample Pictures\jsp.jpg')  # 传图
        base.wait_element(apartmentContractPage.customerSignMould['image_loc'])
        base.click(customerPage.listMould['submit_button'])  # 提交
        base.check_submit()
        #定金确认
        base.open(page.earnestPage, earnestPage.searchMouid['tr_contract'])
        base.input_text(earnestPage.searchMouid['apartment_code_loc'], apartmentCode)  # 输入房源编号
        base.click(earnestPage.searchMouid['search_button_loc'])  # 搜索
        base.staleness_of(earnestPage.searchMouid['tr_contract'])  # 等待列表刷新
        base.click(earnestPage.searchMouid['confirm_button_loc'])  # 确认
        base.input_text(earnestPage.confirmMould['earnest_money_loc'], earnestMoney)  # 输入金额
        base.type_select(earnestPage.confirmMould['payway'], 'ALIPAY')  # 收款方式
        base.input_text(earnestPage.confirmMould['name_loc'], 'Autotest')  # 收据名字
        base.type_select(earnestPage.confirmMould['company'], 'ISZTECH')  # 收款公司
        base.type_date(earnestPage.confirmMould['receipt_date'],datetime.date.today())  # 收款日期
        base.click(earnestPage.confirmMould['submit_loc'])  # 提交
        base.check_submit()
        # 违约提交
        base.click(earnestPage.searchMouid['breach_loc'])  # 点击违约
        base.input_text(earnestPage.confirmMould['breach_reason_loc'], u'autotest')  # 输入原因
        base.input_text(earnestPage.confirmMould['breach_money_loc'],earnestMoney)  # 输入违约金额
        base.click(earnestPage.confirmMould['submit_loc'])  # 提交
        base.check_submit()
        # 定金转入违约金审核
        base.open(page.depositToBreachPage, earnestPage.depositToBreachMould['tr_earnest'])
        base.input_text(earnestPage.depositToBreachMould['address_search_loc'], apartmentCode)
        base.click(earnestPage.depositToBreachMould['search_button'])
        base.staleness_of(earnestPage.depositToBreachMould['tr_earnest'])
        base.click(earnestPage.depositToBreachMould['audit_button'])
        base.input_text(earnestPage.depositToBreachMould['earnest_money_loc'], earnestMoney)
        base.click(earnestPage.depositToBreachMould['payment_way_loc'])
        base.type_date(earnestPage.depositToBreachMould['receipt_date_loc'], datetime.date.today())
        base.type_select(earnestPage.depositToBreachMould['company_loc'], 'ISZTECH')
        base.input_text(earnestPage.depositToBreachMould['alipay_card_loc'], '13676595110')
        base.input_text(earnestPage.depositToBreachMould['operation_total_loc'], earnestMoney)
        base.input_text(earnestPage.depositToBreachMould['remark_loc'], 'AutoTest')
        base.click(earnestPage.depositToBreachMould['shenhe_loc'])
        base.check_submit()
        # 业绩生效并产生核发月份检查
        breachAchievementActiveSql = "select accounting_time,achieve_id from breach_achievement where apartment_code='%s' and deleted=0 and breach_type='EARNEST_BREACH' " \
                                     "and is_active='Y'" % apartmentCode
        if sqlbase.waitData(breachAchievementActiveSql, 1):
            breachAchievementInfo = sqlbase.serach(breachAchievementActiveSql)
            base.diffAssert(lambda test: asserts(breachAchievementInfo[0]).is_not_empty(), 1096,
                            u'%s:房源 %s 下定违约违约业绩生效核发月份生成异常' % (fileName, apartmentCode))
        else:
            consoleLog(u'%s:房源 %s 下定违约违约违约业绩生效异常' % (fileName, apartmentCode),'e')
        # 业绩审核
        base.open(page.defaultAchievementPage, apartmentAchievementPage.searchContractMould['tr_contract'])
        base.click(apartmentAchievementPage.searchContractMould['reset_button_loc'])  # 重置
        time.sleep(10)  # 等待重新核算更新数据
        base.input_text(apartmentAchievementPage.searchContractMould['search_address_loc'], apartmentCode)  # 输入房源编号
        base.type_select(apartmentAchievementPage.searchContractMould['breach_type_loc'],'EARNEST_BREACH')  # 下定违约
        base.click(apartmentAchievementPage.searchContractMould['search_button_loc'])  # 查找
        base.staleness_of(apartmentAchievementPage.searchContractMould['tr_contract'])  # 等待第一条数据刷新
        base.dblclick(apartmentAchievementPage.searchContractMould['tr_contract'],
                      checkLoc=apartmentAchievementPage.detailAchievementMoudle['breach_num_loc'])  # 点击第一条数据等待详情页面完全显示
        base.click(apartmentAchievementPage.detailAchievementMoudle['audit_button_loc'])
        base.input_text(apartmentAchievementPage.detailAchievementMoudle['contract_audit_content'], 'ok')
        base.click(apartmentAchievementPage.detailAchievementMoudle['contract_audit_confirm'])
        base.check_submit()
        # 违约金审核重置
        base.open(page.depositToBreachPage, earnestPage.depositToBreachMould['tr_earnest'])
        base.input_text(earnestPage.depositToBreachMould['address_search_loc'], apartmentCode)
        base.click(earnestPage.depositToBreachMould['search_button'])
        base.staleness_of(earnestPage.depositToBreachMould['tr_earnest'])
        base.click(earnestPage.depositToBreachMould['reset_loc'])  # 重置
        base.click(earnestPage.depositToBreachMould['confirm_loc'])  # 确定
        base.check_submit()
        # 修改违约金额
        base.open(page.earnestBreachPage,earnestPage.searchMouid['tr_contract'])
        base.input_text(earnestPage.searchMouid['apartment_code_loc'], apartmentCode)  # 输入房源编号
        base.click(earnestPage.searchMouid['search_button_loc'])  # 搜索
        base.staleness_of(earnestPage.searchMouid['tr_contract'])  # 等待列表刷新
        base.dblclick(earnestPage.searchMouid['tr_contract'])
        time.sleep(2)
        base.input_text(earnestPage.confirmMould['breach_reason_loc'], u'修改违约金额')
        earnestMoneyNew = str(float(earnestMoney)+100)
        base.input_text(earnestPage.confirmMould['breach_money_loc'], earnestMoneyNew)
        base.click(earnestPage.confirmMould['submit_loc'])
        base.check_submit()

        # 修改违约金后业绩信息检查
        time.sleep(10)
        breachAchievementSql = "select is_active,achieve_id,accounting_money from breach_achievement where object_type='EARNEST_BREACH' and apartment_code='%s' and deleted=0 " \
                               "and is_active='Y'" % apartmentCode
        breachAchievementInfoNew = sqlbase.serach(breachAchievementSql)
        base.diffAssert(lambda test: asserts(breachAchievementInfoNew[2]).is_equal_to(earnestMoney), 1096,
                        u'%s:房源 %s 下定违约修改后违约业绩金额异常,期望值 %s 实际值 %s' % (fileName, apartmentCode, earnestMoney, breachAchievementInfoNew[2]))

        # 业绩分成明细表（预估业绩排行榜数据取值表,检查违约业绩更新到预估业绩排行榜）
        breahAchievementDetailSql = "select ca.share_achieve from contract_achievement ca inner join contract_achievement_detail cad on ca.achieve_id=cad.achieve_id where " \
                                    "ca.contract_category='EARNEST_BREACH' and ca.deleted=0 and ca.achieve_id='%s'" % breachAchievementInfoNew[1]
        achievementDetialInfo = sqlbase.serach(breahAchievementDetailSql)
        base.diffAssert(lambda test: asserts(achievementDetialInfo[0]).is_equal_to(earnestMoney), 1096,
                        u'%s:房源 %s 下定违约违约业绩分成明细异常,期望值 %s 实际值 %s' % (fileName, apartmentCode, earnestMoney, achievementDetialInfo[0]))

test_1096()