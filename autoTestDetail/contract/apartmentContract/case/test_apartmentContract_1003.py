# -*- coding:utf8 -*-

import time
from selenium.webdriver.common.by import By
from assertpy import assert_that as asserts
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.apartmentContract.page import apartmentContractPage


@log
def test_1003():
    """出租合同起算日小于委托合同签约日"""

    # describe：出租合同承租起算日不在委托合同周期内，合同签约失败
    # data：出租合同起算日小于委托合同签约日
    # result：签约失败

    fileName = 'apartmentContract_1003'
    randomApartment = "SELECT a.apartment_code,a.apartment_id,hc.contract_num,hc.contract_id FROM apartment a INNER JOIN house_contract hc ON hc.contract_id = a.house_contract_id AND hc.is_active = 'Y' " \
                      "AND hc.deleted = 0 AND hc.contract_status = 'EFFECTIVE'WHERE a.deleted = 0 AND a.rent_price > 0 AND a.city_code = 330100 AND hc.entrust_type = 'SHARE' AND a.rent_status='WAITING_RENT'" \
                      "AND hc.apartment_type='BRAND'AND hc.sign_date>date_sub(date(sysdate()), interval 6 month) and not EXISTS (select * from apartment_contract ac,apartment_contract_relation acr " \
                      "where ac.contract_id=acr.contract_id and a.apartment_id=acr.apartment_id) and EXISTS (select * from query_apartment qa where qa.apartment_code=a.apartment_code) ORDER BY RAND() LIMIT 1"
    if sqlbase.get_count(randomApartment) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % randomApartment)
        return
    info = sqlbase.serach(randomApartment)
    apartmentCode = info[0]
    consoleLog(u'%s:使用房源 %s 签约出租合同' % (fileName, apartmentCode))

    with Base() as base:
        base.open(page.customerListPage, apartmentContractPage.customerSignMould['tr_customer'])
        try:
            base.find_element(By.ID, 'search_btn').click()
            base.staleness_of(apartmentContractPage.customerSignMould['tr_customer'])  # 搜索等待列表刷新
        except:
            base.click((By.CSS_SELECTOR, '.panel.window > div:nth-child(1) > div.panel-tool > a'))  # 可能会有分配租客的弹窗出现，此为关闭
        customerCode = base.script(
            "var a = $('[datagrid-row-index=\"0\"] > [field=\"customer_num\"] > div > font').text();return a",
            True)  # 获取第一条数据编号
        base.input_text(apartmentContractPage.customerSignMould['search_customer_name_loc'], customerCode)
        base.click(apartmentContractPage.customerSignMould['search_button_loc'])
        base.staleness_of(apartmentContractPage.customerSignMould['tr_customer'])
        base.script("$('button#edit_btn')[2].click()")  # 点击列表页第一行的签约
        base.click(apartmentContractPage.customerSignMould['share'])  # 点合租
        base.input_text(apartmentContractPage.customerSignMould['search_apartment_loc'], apartmentCode)  # 房源编号
        base.click(apartmentContractPage.customerSignMould['house_search_btn'])
        base.staleness_of(apartmentContractPage.customerSignMould['apartment_loc'])
        try:
            base.dblclick(apartmentContractPage.customerSignMould['apartment_loc'],
                          checkLoc=apartmentContractPage.addApartmentContractMould[
                              'contract_num_loc'])  # 对查询结果的第一条房源数据双击发起签约
        except:
            base.click(apartmentContractPage.customerSignMould['newsign_button_loc'])  # 新签
        contractNum = 'AutoTest' + '-' + time.strftime('%m%d%H%M%S')  # 定义合同编号
        randomHouseContract = sqlbase.serach(
            "SELECT entrust_start_date,entrust_end_date,date(sysdate()),date_add(date(sysdate()), interval 1 DAY),date_sub(date(sysdate()), interval 6 month) "
            "from house_contract where contract_num = '%s'" % info[2])  # 获取房源合同时间元素
        base.input_text(apartmentContractPage.addApartmentContractMould['contract_num_loc'], contractNum)  # 合同编号
        base.type_date(apartmentContractPage.typeMould['sign_date'], randomHouseContract[4])  # 签约日期
        base.type_date(apartmentContractPage.typeMould['rent_start_date'], randomHouseContract[4])  # 承租起算日
        base.type_date(apartmentContractPage.typeMould['rent_end_date'], randomHouseContract[2])  # 承租到期日
        time.sleep(3)
        message = base.script("var a = $('.panel.window.messager-window>div:nth-child(2)>div:nth-child(2)').text();return a", True)
        if message is not None:
            messagehope = u'承租开始日期没到委托合同开始日'
            base.diffAssert(lambda test: asserts(message).is_equal_to(messagehope), 1003,
                            u'%s:出租合同 %s 新增提交异常，期望值 %s 实际值 %s' % (fileName, contractNum, messagehope, message))
        else:
            consoleLog(u'%s：页面信息获取失败' % fileName, 'e')

test_1003()