# -*- coding:utf8 -*-

import time
from selenium.webdriver.common.by import By
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.apartmentContract.page import apartmentContractPage
from assertpy import assert_that as asserts

@log
def test_1007():
    """租合同周期在跟前合同的周期重叠"""

    # describe：租合同周期在跟前合同的周期重叠,提示时间段被占用
    # data：有过出租合同且当前状态为待租的房源，新增出租合同时间在前合同的承租周期内
    # result：合同创建失败

    fileName = 'apartmentContract_1007'
    searchSql = "SELECT a.apartment_code,hc.contract_num,ac.contract_num,date_sub(date(ac.real_due_date), interval 2 DAY) FROM apartment a INNER JOIN house_contract hc " \
                "ON hc.contract_id = a.house_contract_id AND hc.is_active = 'Y' AND hc.deleted = 0 AND hc.audit_status='APPROVED' AND hc.contract_status = 'EFFECTIVE'" \
                "INNER JOIN apartment_contract_relation acr  on a.apartment_id=acr.apartment_id INNER JOIN apartment_contract ac on ac.contract_id=acr.contract_id and ac.deleted=0 " \
                "WHERE a.apartment_id=acr.apartment_id and a.deleted = 0 AND a.rent_price > 0 AND a.city_code = 330100 AND hc.entrust_type = 'SHARE' AND a.rent_status='WAITING_RENT' order by rand() limit 1"
    if sqlbase.get_count(searchSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % searchSql)
        return
    info = sqlbase.serach(searchSql)
    apartmentCode = info[0]
    consoleLog(u'%s:取随机房源 %s 做签约' %(fileName, apartmentCode))
    signDate = info[3]

    with Base() as base:
        base.open(page.customerListPage, apartmentContractPage.customerSignMould['tr_customer'])
        try:
            base.find_element(By.ID, 'search_btn').click()
            base.staleness_of(apartmentContractPage.customerSignMould['tr_customer'])  # 搜索等待列表刷新
        except:
            base.click((By.CSS_SELECTOR, '.panel.window > div:nth-child(1) > div.panel-tool > a'))  # 可能会有分配租客的弹窗出现，此为关闭
        customerCode = base.script(
            "var a = $('[datagrid-row-index=\"0\"] > [field=\"customer_num\"] > div > font').text();return a",
            True).decode('utf-8')  # 获取第一条数据编号
        base.input_text(apartmentContractPage.customerSignMould['search_customer_name_loc'], customerCode)
        base.click(apartmentContractPage.customerSignMould['search_button_loc'])
        base.staleness_of(apartmentContractPage.customerSignMould['tr_customer'])
        base.script("$('button#edit_btn')[2].click()")  # 点击列表页第一行的签约
        consoleLog(u'使用房源 %s 签约出租合同' % apartmentCode)
        base.click(apartmentContractPage.customerSignMould['share'])  # 点合租
        base.input_text(apartmentContractPage.customerSignMould['search_apartment_loc'], apartmentCode)  # 房源编号
        base.click(apartmentContractPage.customerSignMould['house_search_btn'])
        base.staleness_of(apartmentContractPage.customerSignMould['apartment_loc'])
        base.dblclick(apartmentContractPage.customerSignMould['apartment_loc'])  # 对查询结果的第一条房源数据双击发起签约
        base.click(apartmentContractPage.customerSignMould['newsign_button_loc'])  # 新签
        contractNum = 'AutoTest' + '-' + time.strftime('%m%d%H%M%S')  # 定义合同编号
        randomHouseContract = sqlbase.serach(
            "SELECT entrust_start_date,entrust_end_date,date(sysdate()) from house_contract where contract_num = '%s'" % info[1])  # 获取房源合同时间元素
        base.input_text(apartmentContractPage.addApartmentContractMould['contract_num_loc'], contractNum)  # 合同编号
        base.type_date(apartmentContractPage.typeMould['sign_date'], signDate)  # 签约日期
        base.type_date(apartmentContractPage.typeMould['rent_start_date'], signDate)  # 承租起算日
        base.type_date(apartmentContractPage.typeMould['rent_end_date'], randomHouseContract[1])  # 承租到期日
        time.sleep(3)
        message = base.script(
            "var a = $('.panel.window.messager-window>div:nth-child(2)>div:nth-child(2)').text();return a",
            True)
        if message != '':
            messagehope = u'该时间段被合同号%s占用' % info[2]
            base.diffAssert(lambda test: asserts(message).is_equal_to(messagehope), 1007,
                            u'%s:页面信息提示不正确，期望值 %s 实际值 %s' % (fileName, messagehope, message))
        else:
            consoleLog(u'页面信息获取失败', 'e')
            return

test_1007()