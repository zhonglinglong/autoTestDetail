# -*- coding:utf8 -*-

import time
from selenium.webdriver.common.by import By
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.apartmentContract.page import apartmentContractPage
from assertpy import assert_that as asserts

@log
def test_1011():
    """出租合同月付不打折，半年付打0.985折，年付打0.97折"""

    # describe： 合同周期为一年半，选择付款方式年付、半年付、月付，对应有不同的折扣
    # data：房源为整租，品牌公寓，合同周期为一年半
    # result：1.合同创建成功2.年付时，租金、服务费打0.97折3.半年付时，租金、服务费打0.985折4.月付时，租金、服务费不打折

    # 获取随机房源
    fileName = 'apartmentContract_1011'
    randomApartment = "SELECT a.apartment_code,a.apartment_id,hc.contract_num,hc.contract_id,a.rent_price FROM apartment a INNER JOIN house_contract hc " \
                      "ON hc.contract_id = a.house_contract_id AND hc.is_active = 'Y' AND hc.deleted = 0 AND hc.audit_status='APPROVED' AND hc.contract_status = 'EFFECTIVE' " \
                      "INNER JOIN fitment_house fh on fh.house_id=hc.house_id AND fh.fitment_status='HANDOVER' WHERE a.deleted = 0 " \
                      "AND a.rent_price > 0 AND a.city_code = 330100 AND hc.entrust_type = 'ENTIRE' AND a.rent_status='WAITING_RENT' AND hc.apartment_type='BRAND' " \
                      "AND hc.real_due_date>date_add(date(sysdate()), interval 18 month) ORDER BY RAND() LIMIT 1"
    if sqlbase.get_count(randomApartment) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % randomApartment)
        return
    info = sqlbase.serach(randomApartment)
    apartmentCode = info[0]
    rent_price = info[4]

    with Base() as base:
        base.open(page.customerListPage, apartmentContractPage.customerSignMould['tr_customer'])
        try:
            base.find_element(By.ID,'search_btn').click()
            base.staleness_of(apartmentContractPage.customerSignMould['tr_customer']) #搜索等待列表刷新
        except:
            base.click((By.CSS_SELECTOR, '.panel.window > div:nth-child(1) > div.panel-tool > a'))  # 可能会有分配租客的弹窗出现，此为关闭
        customerCode = base.script(
            "var a = $('[datagrid-row-index=\"0\"] > [field=\"customer_num\"] > div > font').text();return a",
            True)  # 获取第一条数据编号
        base.input_text(apartmentContractPage.customerSignMould['search_customer_name_loc'], customerCode)
        base.click(apartmentContractPage.customerSignMould['search_button_loc'])
        base.staleness_of(apartmentContractPage.customerSignMould['tr_customer'])
        base.script("$('button#edit_btn')[2].click()")  # 点击列表页第一行的签约
        consoleLog(u'%s:使用房源 %s 签约出租合同' % (fileName, apartmentCode))
        base.input_text(apartmentContractPage.customerSignMould['search_apartment_loc'], apartmentCode)  # 房源编号
        base.click(apartmentContractPage.customerSignMould['house_search_btn'])  # 搜索
        base.staleness_of(apartmentContractPage.customerSignMould['entire_apartment_loc'])  # 搜索等待列表刷新
        try:
            base.dblclick(apartmentContractPage.customerSignMould['entire_apartment_loc'],
                          checkLoc=apartmentContractPage.addApartmentContractMould['contract_num_loc'])  # 对查询结果的第一条房源数据双击发起签约
        except:
            base.click(apartmentContractPage.customerSignMould['newsign_button_loc'])  # 新签
        contractNum = 'AutoTest' + '-' + time.strftime('%m%d%H%M%S')  # 定义合同编号
        randomHouseContract = sqlbase.serach(
            "SELECT entrust_start_date,entrust_end_date,date(sysdate()),date_add(date(sysdate()), interval 1 DAY),date_add(date(sysdate()), interval 18 month) "
            "from house_contract where contract_num = '%s'" % info[2])  # 获取房源合同时间元素
        base.input_text(apartmentContractPage.addApartmentContractMould['contract_num_loc'], contractNum)  # 合同编号
        base.type_date(apartmentContractPage.typeMould['sign_date'], randomHouseContract[2])  # 签约日期
        base.type_date(apartmentContractPage.typeMould['rent_start_date'], randomHouseContract[3])  # 承租起算日
        base.type_date(apartmentContractPage.typeMould['rent_end_date'], randomHouseContract[4])  # 承租到期日
        base.input_text(apartmentContractPage.addApartmentContractMould['deposit_loc'], 1234)  # 押金
        base.type_select(apartmentContractPage.typeMould['payment_type'], 'NORMAL')  # 正常付款
        base.type_select(apartmentContractPage.typeMould['payment_cycle'], 'MONTH')  # 月付
        base.click(apartmentContractPage.addApartmentContractMould['rent_strategy_price_loc'])
        rent_money_month = base.script(
            "var a = $('#contract_strategy_table tr>td:nth-child(6)>span>input').val();return a",
            True)  # 获取第一条数据编号
        base.diffAssert(lambda test: asserts(rent_money_month).is_equal_to(rent_price),1011,
                        u'%s:出租合同租金月付时显示异常，期望值 %s 实际值 %s' % (fileName, rent_price, rent_money_month))
        base.type_select(apartmentContractPage.typeMould['payment_cycle'], 'HALF_YEAR')  # 半年付
        base.click(apartmentContractPage.addApartmentContractMould['rent_strategy_price_loc'])
        rent_money_halfyear = base.script(
            "var a = $('#contract_strategy_table tr>td:nth-child(6)>span>input').val();return a",
            True)  # 获取第一条数据编号
        base.diffAssert(lambda test: asserts(rent_money_halfyear).is_equal_to(str('%.2f' % (float(rent_price)*0.985))), 1011,
                        u'%s:出租合同租金半年付时显示异常，期望值 %s 实际值 %s' % (fileName, str('%.2f' % (float(rent_price)*0.985)), rent_money_halfyear))
        base.type_select(apartmentContractPage.typeMould['payment_cycle'], 'ONE_YEAR')  # 一年付
        base.click(apartmentContractPage.addApartmentContractMould['rent_strategy_price_loc'])
        rent_money_year = base.script(
            "var a = $('#contract_strategy_table tr>td:nth-child(6)>span>input').val();return a",
            True)  # 获取第一条数据编号
        base.diffAssert(lambda test: asserts(rent_money_year).is_equal_to(str('%.2f' % (float(rent_price) * 0.97))), 1011,
                        u'%s:出租合同租金年付时显示异常，期望值 %s 实际值 %s' % (fileName, str('%.2f' % (float(rent_price) * 0.97)), rent_money_year))

test_1011()