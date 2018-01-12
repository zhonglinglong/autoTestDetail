# -*- coding:utf8 -*-

import time

from selenium.webdriver.common.by import By

from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.apartmentContract.page import apartmentContractPage


@log
def test():
    """出租合同起算日在到期日与延长期之间"""

    # 待接口完善
    # describe：出租合同承租起算日在到期日与延长期之间，合同签约成功
    # data：出租合同起算日大于委托合同到期日小于委托合同延迟期
    # result：签约成功

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
        consoleLog(u'使用客户 %s 做合租合同签约' % customerCode)
        base.input_text(apartmentContractPage.customerSignMould['search_customer_name_loc'], customerCode)
        base.click(apartmentContractPage.customerSignMould['search_button_loc'])
        base.staleness_of(apartmentContractPage.customerSignMould['tr_customer'])
        base.script("$('button#edit_btn')[2].click()")  # 点击列表页第一行的签约
        # 获取随机房源
        randomApartment = "SELECT a.apartment_code,a.apartment_id,hc.contract_num,hc.contract_id FROM apartment a INNER JOIN house_contract hc " \
                          "ON hc.contract_id = a.house_contract_id AND hc.is_active = 'Y' AND hc.deleted = 0 AND hc.audit_status='APPROVED' AND hc.contract_status = 'EFFECTIVE'" \
                          "INNER JOIN fitment_house fh on fh.house_id=hc.house_id AND fh.fitment_status='HANDOVER' WHERE a.deleted = 0 " \
                          "AND a.rent_price > 0 AND a.city_code = 330100 AND hc.entrust_type = 'SHARE' AND a.rent_status='WAITING_RENT' " \
                          "AND hc.entrust_end_date<sysdate() ORDER BY RAND() LIMIT 1"
        if sqlbase.get_count(randomApartment) == 0:
            consoleLog(u'SQL查无数据！', level='w')
            consoleLog(u'执行SQL：%s' % randomApartment.encode('utf-8'))
            return
        info = sqlbase.serach(randomApartment)
        apartmentCode = info[0]
        consoleLog(u'使用房源 %s 签约出租合同' % apartmentCode)
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
            "SELECT entrust_start_date,entrust_end_date,date(sysdate()),date_add(date(entrust_end_date), interval 5 DAY),date_sub(date(delay_date), interval 5 day) from house_contract where contract_num = '%s'" %
            info[2].encode('utf-8'))  # 获取房源合同时间元素
        base.input_text(apartmentContractPage.addApartmentContractMould['contract_num_loc'], contractNum)  # 合同编号
        base.type_date(apartmentContractPage.typeMould['sign_date'], randomHouseContract[2])  # 签约日期
        base.type_date(apartmentContractPage.typeMould['rent_start_date'], randomHouseContract[3])  # 承租起算日
        base.type_date(apartmentContractPage.typeMould['rent_end_date'], randomHouseContract[4])  # 承租到期日
        message = base.script("var a = $('.panel.window.messager-window>div:nth-child(2)>div:nth-child(2)').text();return a",True).encode('utf-8')
        if message is not None:
            messagehope = u'承租开始日期没到委托合同开始日'.encode('utf-8')
            if message == messagehope:
                consoleLog(u'出租合同起算日小于委托合同签约日，出租合同签约失败')
            else:
                consoleLog(u'页面信息提示不正确','e')
        else:
            consoleLog(u'页面信息获取失败','e')

test()