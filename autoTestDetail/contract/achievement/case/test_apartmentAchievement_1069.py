# -*- coding:utf8 -*-

import datetime
from assertpy import assert_that as asserts
from selenium.webdriver.common.by import By
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.apartmentContract.page import apartmentContractPage
from contract.earnest import earnestPage
from customer import customerPage


@log
def test_1069():
    """下定违约业绩生成"""

    # describe：下定违约生成违约业绩
    # data：1、定金状态已确认；2、签约状态为待签；3、违约金大于0；
    # result：1、下定违约提交后，生成未生效的违约业绩；2、业绩同步到预估业绩排行榜；

    fileName = 'apartmentAchievement_1069'
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
    earnestMoney = apartmentinfo[4] if float(apartmentinfo[4]) > 1000.00 else '1000.00'
    apartmentCode = apartmentinfo[0]
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
        base.type_select(customerPage.listMould['customer_status_loc'], 'EFFECTIVE')
        base.click(customerPage.listMould['search_button'])
        base.staleness_of(customerPage.listMould['tr_customer'])  # 搜索等待列表刷新
        customerCode = base.script(
             "var a = $('[datagrid-row-index=\"0\"] > [field=\"customer_num\"] > div > font').text();return a",
             True)  # 获取第一条数据编号
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
        # 定金确认
        base.open(page.earnestPage, earnestPage.searchMouid['tr_contract'])
        base.input_text(earnestPage.searchMouid['apartment_code_loc'], apartmentCode)  # 输入房源编号
        base.click(earnestPage.searchMouid['search_button_loc'])  # 搜索
        base.staleness_of(earnestPage.searchMouid['tr_contract'])  # 等待列表刷新
        base.click(earnestPage.searchMouid['confirm_button_loc'])  # 确认
        base.input_text(earnestPage.confirmMould['earnest_money_loc'], earnestMoney)  # 输入金额
        base.type_select(earnestPage.confirmMould['payway'], 'ALIPAY')  # 收款方式
        base.input_text(earnestPage.confirmMould['name_loc'], 'Autotest')  # 收据名字
        base.type_select(earnestPage.confirmMould['company'], 'ISZTECH')  # 收款公司
        base.type_date(earnestPage.confirmMould['receipt_date'], datetime.date.today())  # 收款日期
        base.click(earnestPage.confirmMould['submit_loc'])  # 提交
        base.check_submit()
        # 违约提交
        base.click(earnestPage.searchMouid['breach_loc'])  # 点击违约
        base.input_text(earnestPage.confirmMould['breach_reason_loc'], u'autotest')  # 输入原因
        base.input_text(earnestPage.confirmMould['breach_money_loc'], 2000)  # 输入违约金额
        base.click(earnestPage.confirmMould['submit_loc'])  # 提交
        # 违约业绩生效检查
        breachAchievementActiveSql = "select is_active,achieve_id from breach_achievement where object_type='EARNEST_BREACH' and apartment_code='%s' and deleted=0" % apartmentCode
        if sqlbase.waitData(breachAchievementActiveSql,1):
            breachAchievementInfo = sqlbase.serach(breachAchievementActiveSql)
            base.diffAssert(lambda test: asserts(breachAchievementInfo[0]).is_equal_to('N'), 1069,
                            u'%s:房源 %s 下定违约违约业绩状态异常，期望值 N 实际值 %s' % (fileName, apartmentCode, breachAchievementInfo[0]))
        else:
            consoleLog(u'%s:房源 %s 下定违约违约业绩生成异常'%(fileName, apartmentCode),'e')
        # 业绩分成明细表（预估业绩排行榜数据取值表,检查违约业绩更新到预估业绩排行榜）
        breahAchievementDetailSql = "select * from contract_achievement ca inner join contract_achievement_detail cad on ca.achieve_id=cad.achieve_id where ca.contract_category='EARNEST_BREACH' " \
                                    "and ca.deleted=0 and ca.achieve_id='%s'" % breachAchievementInfo[1]
        achievementDetialConunt = sqlbase.get_count(breahAchievementDetailSql)
        base.diffAssert(lambda test: asserts(achievementDetialConunt).is_not_equal_to(0), 1069,
                        u'%s:房源 %s 下定违约违约业绩分成明细异常' % (fileName, apartmentCode))

test_1069()