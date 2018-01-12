# -*- coding:utf8 -*-

import time

from selenium.webdriver.common.by import By

from common import page
from common import sqlbase
from common.base import log, consoleLog, Base, get_conf, set_conf
from contract.apartmentContract.page import apartmentContractPage


@log
def addApartmentContract():
    """新增出租合同"""
    try:
        base=Base()
        base.open(page.customerListPage, apartmentContractPage.customerSignMould['tr_customer'], havaFrame=False)
        #配置文件读取租客信息
        customerName = get_conf('customerInfo', 'customerName')
        contractNum = 'AutoTest' + '-' + time.strftime('%m%d-%H%M%S')
        testCustomer = "SELECT * from customer where customer_name = '%s' and deleted = 0" % customerName.encode('utf-8')

        if sqlbase.get_count(testCustomer) != 0:
            try:
                base.input_text(apartmentContractPage.customerSignMould['search_customer_name_loc'], customerName)#输入租客姓名
            except:
                base.click((By.CSS_SELECTOR, '.panel.window > div:nth-child(1) > div.panel-tool > a'))  # 可能会有分配租客的弹窗出现，此为关闭
                base.input_text(apartmentContractPage.customerSignMould['search_customer_name_loc'], customerName)#输入租客姓名
        else:
            try:
                base.click(
                    (By.CSS_SELECTOR, '.panel.window > div:nth-child(1) > div.panel-tool > a'))  # 可能会有分配租客的弹窗出现，此为关闭
            except:
                pass
            customerCode = base.script("var a = $('[datagrid-row-index=\"0\"] > [field=\"customer_num\"] > div > font').text();return a",True).decode('utf-8')
            consoleLog(u'使用随机租客 %s 签约承租合同' % customerCode, level='e')
            base.find_element(*apartmentContractPage.customerSignMould['search_customer_name_loc']).clear()
        base.click(apartmentContractPage.customerSignMould['search_button_loc'])  #查询
        base.staleness_of(apartmentContractPage.customerSignMould['tr_customer'])  #等待数据刷新
        base.script("$('button#edit_btn')[2].click()")  # 点击列表页第一行的签约
        # 此处为从配置文件中查询房源
        apartmentCode = get_conf('houseInfo', 'apartmentCode')
        consoleLog(u'查询配置文件测试房源数据：%s' % apartmentCode)
        testApartment = "SELECT rent_type from apartment where apartment_code = '%s' and deleted = 0 and rent_status = 'WAITING_RENT' " \
                        "and is_active = 'Y' and rent_price > 0" % apartmentCode.encode('utf-8')

        if sqlbase.get_count(testApartment) != 0:
            consoleLog(u'查询配置文件测试房源对应委托合同的委托周期')
            testHouseContract = "SELECT entrust_start_date,entrust_end_date,date(sysdate()) from house_contract where contract_num = '%s'" % get_conf(
                'houseContractInfo', 'contractNum').encode('utf-8')
            set_conf('apartmentContractInfo', signDate=sqlbase.serach(testHouseContract)[2],
                     rentStartDate=sqlbase.serach(testHouseContract)[2], rentEndDate=sqlbase.serach(testHouseContract)[1])
            if sqlbase.serach(testApartment)[0] == 'SHARE' or sqlbase.serach(testApartment)[0] == 'share':  #查询结果为合租房源
                base.click(apartmentContractPage.customerSignMould['share'])  #点合租
                base.input_text(apartmentContractPage.customerSignMould['search_apartment_loc'], apartmentCode)  #房源编号
                base.click(apartmentContractPage.customerSignMould['house_search_btn'])  #搜索
            else:
                base.input_text(apartmentContractPage.customerSignMould['search_apartment_loc'], apartmentCode) #不点合租直接输房源编号
                base.click(apartmentContractPage.customerSignMould['house_search_btn'])  #搜索
        else:
            consoleLog(u'查询配置文件没有签约过承租合同的有效的合租房源')
            randomApartment = "SELECT a.apartment_code,a.apartment_id,hc.contract_num,hc.contract_id FROM apartment a INNER JOIN house_contract hc " \
                              "ON hc.contract_id = a.house_contract_id AND hc.is_active = 'Y' AND hc.deleted = 0 AND hc.contract_status = 'EFFECTIVE' WHERE a.deleted = 0 " \
                              "AND a.rent_price > 0 AND a.city_code = 330100 AND hc.entrust_type = 'SHARE' AND NOT EXISTS ( SELECT 1 FROM apartment_contract_relation " \
                              "WHERE room_id IS NOT NULL AND room_id = a.room_id ) AND NOT EXISTS ( SELECT 1 FROM apartment_contract_relation " \
                              "WHERE room_id IS NULL AND house_id = a.house_id ) ORDER BY RAND() LIMIT 1"
            info = sqlbase.serach(randomApartment)
            apartmentCode = info[0]
            consoleLog(u'使用随机房源 %s 签约承租合同' % apartmentCode, level='w')
            base.click(apartmentContractPage.customerSignMould['share'])  #点合租
            base.input_text(apartmentContractPage.customerSignMould['search_apartment_loc'], info[0])  #房源编号
            base.click(apartmentContractPage.customerSignMould['house_search_btn'])  #搜索
            #将随机取得数据写入配置文件备用
            set_conf('houseInfo', apartmentCode=info[0], apartmentID=info[1])
            set_conf('houseContractInfo', contractnum=info[2], contractid=info[3])

            consoleLog(u'查询随机房源 %s 对应委托合同的委托周期' % apartmentCode)
            randomHouseContract = sqlbase.serach("SELECT entrust_start_date,entrust_end_date,date(sysdate()) from house_contract where contract_num = '%s'" % info[2].encode('utf-8'))
            # 将随机取得数据写入配置文件备用
            set_conf('apartmentContractInfo', signDate=randomHouseContract[2], rentStartDate=randomHouseContract[2], rentEndDate=randomHouseContract[1])

        base.staleness_of(apartmentContractPage.customerSignMould['apartment_loc'])
        base.dblclick(apartmentContractPage.customerSignMould['apartment_loc'],
                      checkLoc=apartmentContractPage.addApartmentContractMould['contract_num_loc'])  # 对查询结果的第一条房源数据双击发起签约
        base.input_text(apartmentContractPage.addApartmentContractMould['contract_num_loc'], contractNum)  # 合同编号
        #读取配置文件中预存的数据内容
        signDate = get_conf('apartmentContractInfo', 'signDate')
        rentStartDate = get_conf('apartmentContractInfo', 'rentStartDate')
        rentEndDate = get_conf('apartmentContractInfo', 'rentEndDate')

        base.type_date(apartmentContractPage.typeMould['sign_date'], signDate)  # 签约日期
        base.type_date(apartmentContractPage.typeMould['rent_start_date'], rentStartDate)  # 承租起算日
        base.type_date(apartmentContractPage.typeMould['rent_end_date'], rentEndDate)  # 承租到期日
        base.input_text(apartmentContractPage.addApartmentContractMould['deposit_loc'], 1234)
        base.type_select(apartmentContractPage.typeMould['payment_type'], 'NORMAL')  # 正常付款
        base.type_select(apartmentContractPage.typeMould['payment_cycle'], 'TOW_MONTH')  # 二月付
        # base.input_text(ApartmentContractPage.addApartmentContractMould['rent_strategy_price_loc'],4321)     #月租金：需求变更，单条情况下无需手动录入
        # base.type_date(ApartmentContractPage.typeMould['rent_strategy_end_loc'],'2018-08-08')    #租金策略结束日：不知道为什么自动化打开的DOM和正常情况下的DOM不一样，所以直接用jquery赋值
        js = "$('#contract_strategy_table > table > tbody > tr > td:nth-child(8) > input').val('%s')" % rentEndDate
        base.script(js)
        base.click(apartmentContractPage.addApartmentContractMould['rent_strategy_contain_loc'])  # 月租金包含按钮
        base.type_select(apartmentContractPage.typeMould['contain_fee_type'], 'PARKING')  # 包含车位费
        base.input_text(apartmentContractPage.addApartmentContractMould['contain_fee_loc'], 123)  # 车位费
        base.click(apartmentContractPage.addApartmentContractMould['contain_fee_save_loc'])  # 保存包含
        base.input_text(apartmentContractPage.addApartmentContractMould['agent_fee_loc'], 234)  # 中介服务费
        base.input_text(apartmentContractPage.addApartmentContractMould['remark_loc'], 'this is autotest date')  # 备注
        base.click(apartmentContractPage.addApartmentContractMould['next_loc_1'])  #第一页下一步
        base.click(apartmentContractPage.addApartmentContractMould['next_loc_2'])  #第二页下一步
        # 租客详情
        base.input_text(apartmentContractPage.addApartmentContractMould['sign_name_loc'], 'AutoTest')  #签约人姓名
        base.type_select(apartmentContractPage.typeMould['sign_id_type'], 'IDNO')  #证件类型
        base.input_text(apartmentContractPage.addApartmentContractMould['sign_id_no_loc'], '42062119910828541X')  #身份证
        base.input_text(apartmentContractPage.addApartmentContractMould['sign_phone_loc'], '15168368432')  #手机号
        base.input_text(apartmentContractPage.addApartmentContractMould['sign_address_loc'], u'浙江省杭州市滨江区六和路368号海创基地南楼三层') #地址
        base.type_select(apartmentContractPage.typeMould['sign_is_customer'], 'Y')  #为承租人
        base.input_text(apartmentContractPage.addApartmentContractMould['urgent_customer_name_loc'], 'AutoTest')  #紧急联系人
        base.input_text(apartmentContractPage.addApartmentContractMould['urgent_phone_loc'], '13666666666') #紧急联系人号码
        base.type_select(apartmentContractPage.typeMould['urgent_card_type'], 'IDNO') #紧急联系人证件类型
        base.input_text(apartmentContractPage.addApartmentContractMould['urgent_id_card_loc'], '42062119910828541X')  #紧急联系人证件号码
        base.input_text(apartmentContractPage.addApartmentContractMould['urgent_postal_address_loc'], u'浙江省杭州市滨江区六和路368号海创基地南楼三层') #紧急联系人地址
        base.type_select(apartmentContractPage.typeMould['customer_type'], 'EMPLOYEE')  #租客类型
        base.type_select(apartmentContractPage.typeMould['gender'], 'MALE')
        base.type_select(apartmentContractPage.typeMould['education'], 'BACHELOR')
        base.input_text(apartmentContractPage.addApartmentContractMould['trade_loc'], u'计算机软件')
        base.input_text(apartmentContractPage.addApartmentContractMould['email_loc'], 'wujun@ishangzu.com')
        base.type_select(apartmentContractPage.typeMould['yesNo'], 'Y')
        base.click(apartmentContractPage.addApartmentContractMould['add_person_loc'])
        base.input_text(apartmentContractPage.addApartmentContractMould['person_name_loc'], 'test')
        base.type_select(apartmentContractPage.typeMould['cardType'], 'PASSPORT')
        base.input_text(apartmentContractPage.addApartmentContractMould['person_cardType_loc'], 'abcdefghijk')
        base.type_select(apartmentContractPage.typeMould['sex'], 'MALE')
        base.input_text(apartmentContractPage.addApartmentContractMould['person_phone_loc'], '13777777777')
        base.type_date(apartmentContractPage.typeMould['staydate'], '2017-08-08')
        base.click(apartmentContractPage.addApartmentContractMould['submit_loc'])
        base.check_submit()
        consoleLog(u'出租合同：%s 新增成功' % contractNum)
        sql = "select contract_id from apartment_contract where contract_num = '%s'" % contractNum
        set_conf('apartmentContractInfo', contractnum=contractNum, contractid=sqlbase.serach(sql)[0])

    finally:
        base.driver.quit()

addApartmentContract()
