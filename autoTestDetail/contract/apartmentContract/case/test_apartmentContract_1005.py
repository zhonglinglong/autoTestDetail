# -*- coding:utf8 -*-
import time
from selenium.webdriver.common.by import By
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.apartmentContract.page import apartmentContractPage
from assertpy import assert_that as asserts

@log
def test_1005():
    """未定价房源签约"""

    # describe：房源签完委托合同未定价，合同签约失败
    # data：未定价的房源
    # result：签约失败

    fileName = 'apartmentContract_1005'
    randomApartment = "SELECT a.apartment_code,a.apartment_id,hc.contract_num,hc.contract_id FROM apartment a INNER JOIN house_contract hc " \
                      "ON hc.contract_id = a.house_contract_id AND hc.is_active = 'Y' AND hc.deleted = 0 AND hc.audit_status='APPROVED' AND hc.contract_status = 'EFFECTIVE' " \
                      "INNER JOIN fitment_house fh on fh.house_id=hc.house_id AND fh.fitment_status='HANDOVER' inner join query_apartment qa on qa.apartment_code=a.apartment_code " \
                      "WHERE a.deleted = 0 AND a.rent_price IS NULL AND a.city_code = 330100 AND hc.entrust_type = 'SHARE' AND a.rent_status='WAITING_RENT'ORDER BY RAND() LIMIT 1"
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
        base.dblclick(apartmentContractPage.customerSignMould['apartment_loc'])  # 对查询结果的第一条房源数据双击发起签约
        time.sleep(1)
        message = base.script(
            "var a = $('.bootstrap-growl.alert.alert-info.alert-dismissible').text();return a", True)
        messsagehope = u'房源未定价，找房源方'
        base.diffAssert(lambda test: asserts(message).contains(messsagehope), 1005,
                        u'%s:未定价房源 %s 签约异常' % (fileName, apartmentCode))

test_1005()