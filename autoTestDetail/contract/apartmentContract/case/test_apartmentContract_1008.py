# -*- coding:utf8 -*-

import time
from selenium.webdriver.common.by import By
from assertpy import assert_that as asserts
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.apartmentContract.page import apartmentContractPage
from customer import customerPage

@log
def test_1008():
    """客户转租房源签约"""

    # describe：不续可看的房源可以签约成功
    # data：1.房源为客户转租；
    # result：签约成功3.租前客户变为已签约

    fileName = 'apartmentContract_1008'
    apartmentSql = "select a.apartment_code,ac.contract_num,ac.real_due_date from apartment a inner join apartment_contract_relation acr " \
                   "on a.apartment_id=acr.apartment_id inner join apartment_contract ac on ac.contract_id = acr.contract_id and ac.is_active='Y' and ac.deleted=0 and ac.city_code=330100 " \
                   "and ac.contract_status ='EFFECTIVE' and ac.entrust_type='SHARE' and a.fitment_type is not Null inner join house_contract hc on hc.house_id=a.house_id " \
                   "and hc.entrust_end_date >DATE_ADD(ac.rent_end_date ,INTERVAL 2 month) and a.category='CUSTOM_RELET' ORDER BY RAND() LIMIT 1"
    if sqlbase.get_count(apartmentSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % apartmentSql)
        return
    apartmentinfo = sqlbase.serach(apartmentSql)
    apartmentCode = apartmentinfo[0]
    consoleLog(u'%s：取随机转租房源 %s 做新签' % (fileName, apartmentCode))

    with Base() as base:
         # 签约
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
             "var a = $('[datagrid-row-index=\"0\"] > [field=\"customer_num\"] > div > font').text();return a",
             True).decode('utf-8')  # 获取第一条数据编号
        base.input_text(customerPage.listMould['customer_name_search'], customerCode)
        base.click(customerPage.listMould['search_button'])
        base.staleness_of(customerPage.listMould['tr_customer'])  # 搜索等待列表刷新
        base.script("$('button#edit_btn')[2].click()")  # 点击列表页第一行的签约
        base.click(apartmentContractPage.customerSignMould['share'])  # 点合租
        base.input_text(apartmentContractPage.customerSignMould['search_apartment_loc'], apartmentCode)  # 房源编号
        base.click(apartmentContractPage.customerSignMould['house_search_btn'])
        base.staleness_of(apartmentContractPage.customerSignMould['apartment_loc'])
        base.dblclick(apartmentContractPage.customerSignMould['apartment_loc'])
        base.click(apartmentContractPage.customerSignMould['newsign_button_loc'])  # 新签
        # 获取时间元素
        randomHouseContract = sqlbase.serach(
            "SELECT date(sysdate()),date_add(date('%s'), interval 1 DAY),date_add(date('%s'), interval 2 month) from dual" % (apartmentinfo[2],apartmentinfo[2]))
        contractNum = 'AutoTest' + '-' + time.strftime('%m%d%H%M%S')
        base.input_text(apartmentContractPage.addApartmentContractMould['contract_num_loc'], contractNum)  # 合同编号
        base.type_date(apartmentContractPage.typeMould['sign_date'], randomHouseContract[0])  # 签约日期
        base.type_date(apartmentContractPage.typeMould['rent_end_date'], randomHouseContract[2])  # 承租到期日
        base.input_text(apartmentContractPage.addApartmentContractMould['deposit_loc'], 1234)  # 押金
        base.type_select(apartmentContractPage.typeMould['payment_type'], 'NORMAL')  # 正常付款
        base.type_select(apartmentContractPage.typeMould['payment_cycle'], 'ALL')  # 一次性付款
        js = "$('#contract_strategy_table > table > tbody > tr > td:nth-child(8) > input').val('%s')" % \
             randomHouseContract[2]
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
        base.input_text(apartmentContractPage.addApartmentContractMould['urgent_customer_name_loc'],
                        'AutoTest')  # 紧急联系人
        base.input_text(apartmentContractPage.addApartmentContractMould['urgent_phone_loc'], '13666666666')  # 紧急联系人号码
        base.type_select(apartmentContractPage.typeMould['urgent_card_type'], 'IDNO')  # 紧急联系人证件类型
        base.input_text(apartmentContractPage.addApartmentContractMould['urgent_id_card_loc'],
                        '42062119910828541X')  # 紧急联系人证件号码
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
        base.type_date(apartmentContractPage.typeMould['staydate'], randomHouseContract[1])  # 入住日期
        base.click(apartmentContractPage.addApartmentContractMould['submit_loc'])  # 提交
        base.check_submit()  # 等待提交完成
        # 合同检查
        contractAdd = "select * from apartment a,apartment_contract ac ,apartment_contract_relation acr where a.apartment_id=acr.apartment_id and acr.contract_id=ac.contract_id " \
                       "and a.apartment_code='%s'AND ac.contract_num = '%s'AND ac.audit_status='AUDIT' and ac.contract_type = 'NEWSIGN' AND ac.entrust_type='SHARE' " \
                       "AND ac.is_active='Y' " % (apartmentCode, contractNum)
        base.diffAssert(lambda test: asserts(sqlbase.waitData(contractAdd,1)).is_true(),1008,
                        u'%s:出租合同 %s 新增失败，执行SQL:%s' % (fileName, contractNum, contractAdd))
        # 租前客户状态检查
        customerstatusSql = "select customer_status from customer where customer_num='%s'" % customerCode
        customerStatus = sqlbase.serach(customerstatusSql)[0]
        base.diffAssert(lambda test: asserts(customerStatus).is_equal_to('SIGNED'), 1008,
                        u'%s:租前客户 %s 状态异常，期望值 SIGNED 实际值 %s' % (fileName, customerCode, customerStatus))

test_1008()