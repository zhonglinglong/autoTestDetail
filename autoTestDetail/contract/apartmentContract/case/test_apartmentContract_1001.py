# -*- coding:utf8 -*-

import time
from selenium.webdriver.common.by import By
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.apartmentContract.page import apartmentContractPage
from assertpy import assert_that as asserts

@log
def test_1001():
    """出租合同签约周期小于一个月"""

    # describe：检测出租合同是否可以小于一个月
    # data：房源为整租，服务公寓，合同周期小于一个月
    # result：1.合同创建成功2.生成出单业绩

    fileName = 'apartmentContract_1001'
    randomApartment = "SELECT a.apartment_code,a.apartment_id,hc.contract_num,hc.contract_id FROM apartment a INNER JOIN house_contract hc ON hc.contract_id = a.house_contract_id " \
                      "AND hc.is_active = 'Y' AND hc.deleted = 0 AND hc.audit_status='APPROVED' AND hc.contract_status = 'EFFECTIVE' inner join query_apartment qa on qa.apartment_code=a.apartment_code " \
                      "WHERE a.deleted = 0 AND a.rent_price > 0 AND a.city_code = 330100 AND hc.entrust_type = 'ENTIRE' AND a.rent_status='WAITING_RENT' AND hc.apartment_type='MANAGE' " \
                      "AND hc.real_due_date>date_add(date(sysdate()), interval 1 MONTH) ORDER BY RAND() LIMIT 1"
    if sqlbase.get_count(randomApartment) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % randomApartment)
        return
    info = sqlbase.serach(randomApartment)
    apartmentCode = info[0]
    consoleLog(u'%s:使用房源 %s 签约承租合同' % (fileName,apartmentCode))

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
        base.staleness_of(apartmentContractPage.customerSignMould['tr_customer'])  # 搜索等待列表刷新
        base.script("$('button#edit_btn')[2].click()")  # 点击列表页第一行的签约
        base.input_text(apartmentContractPage.customerSignMould['search_apartment_loc'], apartmentCode)  # 房源编号
        base.click(apartmentContractPage.customerSignMould['house_search_btn']) # 搜索
        base.staleness_of(apartmentContractPage.customerSignMould['entire_apartment_loc'])  # 搜索等待列表刷新
        try:
            base.dblclick(apartmentContractPage.customerSignMould['entire_apartment_loc'],
                          checkLoc=apartmentContractPage.addApartmentContractMould['contract_num_loc'])  # 对查询结果的第一条房源数据双击发起签约
        except:
            base.click(apartmentContractPage.customerSignMould['newsign_button_loc'])  # 新签
        # 获取房源合同时间元素
        randomHouseContract = sqlbase.serach(
            "SELECT entrust_start_date,entrust_end_date,date(sysdate()),date_add(date(sysdate()), interval 1 DAY),date_add(date(sysdate()), interval 15 DAY) "
            "from house_contract where contract_num = '%s'" % info[2])
        contractNum = 'AutoTest' + '-' + time.strftime('%m%d%H%M%S')
        base.input_text(apartmentContractPage.addApartmentContractMould['contract_num_loc'], contractNum)  # 合同编号
        base.type_date(apartmentContractPage.typeMould['sign_date'], randomHouseContract[2])  # 签约日期
        base.type_date(apartmentContractPage.typeMould['rent_start_date'], randomHouseContract[3])  # 承租起算日
        base.type_date(apartmentContractPage.typeMould['rent_end_date'], randomHouseContract[4])  # 承租到期日
        base.input_text(apartmentContractPage.addApartmentContractMould['deposit_loc'], 1234)  # 押金
        base.type_select(apartmentContractPage.typeMould['payment_type'], 'NORMAL')  # 正常付款
        base.type_select(apartmentContractPage.typeMould['payment_cycle'], 'ALL')  # 一次性付款
        js = "$('#contract_strategy_table > table > tbody > tr > td:nth-child(8) > input').val('%s')" % randomHouseContract[4]
        base.script(js)
        base.click(apartmentContractPage.addApartmentContractMould['rent_strategy_contain_loc'])  # 月租金包含按钮
        base.type_select(apartmentContractPage.typeMould['contain_fee_type'], 'PARKING')  # 包含车位费
        base.input_text(apartmentContractPage.addApartmentContractMould['contain_fee_loc'], 123)  # 车位费
        base.click(apartmentContractPage.addApartmentContractMould['contain_fee_save_loc'])  # 保存包含
        base.input_text(apartmentContractPage.addApartmentContractMould['agent_fee_loc'], 234)  # 中介服务费
        base.input_text(apartmentContractPage.addApartmentContractMould['remark_loc'], 'this is autotest date')  # 备注
        base.click(apartmentContractPage.addApartmentContractMould['next_loc_1'])  # 第一页下一步
        base.click(apartmentContractPage.addApartmentContractMould['next_loc_2'])  # 第二页下一步
        # 租客详情
        base.input_text(apartmentContractPage.addApartmentContractMould['sign_name_loc'], u'AutoTest')  # 签约人姓名
        base.type_select(apartmentContractPage.typeMould['sign_id_type'], 'IDNO')  # 证件类型
        base.input_text(apartmentContractPage.addApartmentContractMould['sign_id_no_loc'], '42062119910828541X')  # 身份证
        base.input_text(apartmentContractPage.addApartmentContractMould['sign_phone_loc'], '15168368432')  # 手机号
        base.input_text(apartmentContractPage.addApartmentContractMould['sign_address_loc'],
                        u'浙江省杭州市滨江区六和路368号海创基地南楼三层')  # 地址
        base.type_select(apartmentContractPage.typeMould['sign_is_customer'], 'Y')  # 为承租人
        base.input_text(apartmentContractPage.addApartmentContractMould['urgent_customer_name_loc'], 'AutoTest')  # 紧急联系人
        base.input_text(apartmentContractPage.addApartmentContractMould['urgent_phone_loc'], '13666666666')  # 紧急联系人号码
        base.type_select(apartmentContractPage.typeMould['urgent_card_type'], 'IDNO')  # 紧急联系人证件类型
        base.input_text(apartmentContractPage.addApartmentContractMould['urgent_id_card_loc'], '42062119910828541X')  # 紧急联系人证件号码
        base.input_text(apartmentContractPage.addApartmentContractMould['urgent_postal_address_loc'],
                        u'浙江省杭州市滨江区六和路368号海创基地南楼三层')  # 紧急联系人地址
        base.type_select(apartmentContractPage.typeMould['customer_type'], 'EMPLOYEE')  # 租客类型
        base.type_select(apartmentContractPage.typeMould['gender'], 'MALE')  # 租客性别
        base.type_select(apartmentContractPage.typeMould['education'], 'BACHELOR')  # 学历
        base.input_text(apartmentContractPage.addApartmentContractMould['trade_loc'], u'计算机软件')  # 行业
        base.input_text(apartmentContractPage.addApartmentContractMould['email_loc'], 'wujun@ishangzu.com')  # 邮件
        base.type_select(apartmentContractPage.typeMould['yesNo'], 'Y')  # 是否入住
        base.click(apartmentContractPage.addApartmentContractMould['add_person_loc'])  # 新增入住人
        base.input_text(apartmentContractPage.addApartmentContractMould['person_name_loc'], 'test')  # 入住人姓名
        base.type_select(apartmentContractPage.typeMould['cardType'], 'PASSPORT')  # 证件类型
        base.input_text(apartmentContractPage.addApartmentContractMould['person_cardType_loc'], 'abcdefghijk')  # 证件号
        base.type_select(apartmentContractPage.typeMould['sex'], 'MALE')  # 性别
        base.input_text(apartmentContractPage.addApartmentContractMould['person_phone_loc'], '13777777777')  # 号码
        base.type_date(apartmentContractPage.typeMould['staydate'], randomHouseContract[3])  # 入住日期
        base.click(apartmentContractPage.addApartmentContractMould['submit_loc'])  # 提交
        base.check_submit()  # 等待提交完成
        contractAdd = "select * from apartment a,apartment_contract ac ,apartment_contract_relation acr where a.apartment_id=acr.apartment_id and acr.contract_id=ac.contract_id " \
                      "and a.apartment_code='%s'AND ac.contract_num = '%s'AND ac.audit_status='AUDIT' and ac.contract_type = 'NEWSIGN' AND ac.entrust_type='ENTIRE' " \
                      "AND ac.is_active='Y' " % (apartmentCode, contractNum)
        base.diffAssert(lambda test: asserts(sqlbase.waitData(contractAdd, 1)).is_true(), 1001,
                        u'%s:出租合同 %s 新增失败，执行SQL:%s' % (fileName, contractNum, contractAdd))
        achievementsqla = "select * from apartment_contract_achievement where contract_num='%s' and is_active='N' and accounting_num=1 and audit_status='AUDIT' and deleted=0 " % contractNum
        base.diffAssert(lambda test:asserts(sqlbase.waitData(achievementsqla, 1)).is_true(), 1001,
                        u'%s:合同 %s 对应业绩未生成' % (fileName, contractNum))

test_1001()