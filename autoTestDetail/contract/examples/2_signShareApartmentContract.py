# -*- coding:utf8 -*-

import time

from selenium.webdriver.common.by import By

from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.apartmentContract.page import apartmentContractPage


@log
def signShareApartmentContract():
    """客户合租合同签约审核主流程"""

    # describe： 客户合租合同签约审核主流程
    # data：有效的租前客户，有效已定价合租房源
    # result：新增合租合同成功，审核通过

    with Base() as base:
        base.open(page.customerListPage, apartmentContractPage.customerSignMould['tr_customer'])
        try:
            base.find_element(By.ID,'search_btn').click()
            base.staleness_of(apartmentContractPage.customerSignMould['tr_customer']) #搜索等待列表刷新
        except:
            base.click((By.CSS_SELECTOR, '.panel.window > div:nth-child(1) > div.panel-tool > a'))  # 可能会有分配租客的弹窗出现，此为关闭
        customerCode = base.script(
            "var a = $('[datagrid-row-index=\"0\"] > [field=\"customer_num\"] > div > font').text();return a",
            True).decode('utf-8')  # 获取第一条数据编号
        consoleLog(u'使用客户 %s 做合租合同签约'%customerCode)
        base.input_text(apartmentContractPage.customerSignMould['search_customer_name_loc'], customerCode)
        base.click(apartmentContractPage.customerSignMould['search_button_loc'])
        base.staleness_of(apartmentContractPage.customerSignMould['tr_customer'])
        base.script("$('button#edit_btn')[2].click()")  # 点击列表页第一行的签约
        # 获取随机房源
        randomApartment = "SELECT a.apartment_code,a.apartment_id,hc.contract_num,hc.contract_id FROM apartment a INNER JOIN house_contract hc " \
                          "ON hc.contract_id = a.house_contract_id AND hc.is_active = 'Y' AND hc.deleted = 0 AND hc.audit_status='APPROVED' AND hc.contract_status = 'EFFECTIVE' " \
                          "INNER JOIN fitment_house fh on fh.house_id=hc.house_id AND fh.fitment_status='HANDOVER' WHERE a.deleted = 0 " \
                          "AND a.rent_price > 0 AND a.city_code = 330100 AND hc.entrust_type = 'SHARE' AND NOT EXISTS ( SELECT 1 FROM apartment_contract_relation " \
                          "WHERE room_id IS NOT NULL AND room_id = a.room_id ) AND NOT EXISTS ( SELECT 1 FROM apartment_contract_relation " \
                          "WHERE room_id IS NULL AND house_id = a.house_id ) ORDER BY RAND() LIMIT 1"
        if sqlbase.get_count(randomApartment) ==0:
            consoleLog(u'SQL查无数据！',level='w')
            consoleLog(u'执行SQL：%s' % randomApartment.encode('utf-8'))
            return
        info = sqlbase.serach(randomApartment)
        apartmentCode = info[0]
        consoleLog(u'使用房源 %s 签约出租合同' % apartmentCode)
        base.click(apartmentContractPage.customerSignMould['share'])  # 点合租
        base.input_text(apartmentContractPage.customerSignMould['search_apartment_loc'], info[0])  # 房源编号
        base.click(apartmentContractPage.customerSignMould['house_search_btn'])
        base.staleness_of(apartmentContractPage.customerSignMould['apartment_loc'])
        base.dblclick(apartmentContractPage.customerSignMould['apartment_loc'],
                      checkLoc=apartmentContractPage.addApartmentContractMould['contract_num_loc'])  # 对查询结果的第一条房源数据双击发起签约
        contractNum = 'AutoTest' + '-' + time.strftime('%m%d%H%M')#定义合同编号
        randomHouseContract = sqlbase.serach(
            "SELECT entrust_start_date,entrust_end_date,date(sysdate()),date_add(date(sysdate()), interval 1 DAY) from house_contract where contract_num = '%s'" %info[2].encode('utf-8'))#获取房源合同时间元素
        base.input_text(apartmentContractPage.addApartmentContractMould['contract_num_loc'], contractNum)  # 合同编号
        base.type_date(apartmentContractPage.typeMould['sign_date'], randomHouseContract[2])  # 签约日期
        base.type_date(apartmentContractPage.typeMould['rent_start_date'], randomHouseContract[2])  # 承租起算日
        base.type_date(apartmentContractPage.typeMould['rent_end_date'], randomHouseContract[1])  # 承租到期日
        base.input_text(apartmentContractPage.addApartmentContractMould['deposit_loc'], 1234)#押金
        base.type_select(apartmentContractPage.typeMould['payment_type'], 'NORMAL')  # 正常付款
        base.type_select(apartmentContractPage.typeMould['payment_cycle'], 'TOW_MONTH')  # 二月付
        js = "$('#contract_strategy_table > table > tbody > tr > td:nth-child(8) > input').val('%s')" % randomHouseContract[1]
        base.script(js)  # 月租金
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
        base.type_date(apartmentContractPage.typeMould['staydate'], randomHouseContract[3])  # 入住日期
        base.click(apartmentContractPage.addApartmentContractMould['submit_loc'])  # 提交
        base.check_submit()  # 等待提交完成
        contractAdd="SELECT DISTINCT apartment_contract.contract_num FROM apartment_contract , house ,apartment WHERE apartment_contract.house_id = house.house_id " \
            "AND apartment_contract.house_id = apartment.house_id and apartment.apartment_code='%s'AND apartment_contract.contract_num = '%s'AND apartment_contract.audit_status='AUDIT'" \
            "and apartment_contract.contract_type = 'NEWSIGN' AND apartment_contract.entrust_type='SHARE' AND apartment_contract.is_active='Y' "%(apartmentCode,contractNum)
        if sqlbase.get_count(contractAdd)==1:#数据检查
            consoleLog(u'出租合同：%s 新增成功' % contractNum)
        else:
            consoleLog(u'合同新增失败',level='e')
            consoleLog(u'执行SQL:%s' % contractAdd.encode('utf-8'))
            return
        #生成业绩，且首条状态为未生效
        achievementsqla = "select * from apartment_contract_achievement where contract_num='%s' and is_active='N' and accounting_num=1 and audit_status='AUDIT' and deleted=0 " % contractNum.encode('utf-8')
        for i in range(5):
            if sqlbase.get_count(achievementsqla) == 1:
                consoleLog(u'合同 %s 对应业绩已生成且未生效' % contractNum)
                break
            else:
                time.sleep(10)
                if i == 4:
                    consoleLog(u'合同 %s 对应业绩未生成' % contractNum, 'e')
                    consoleLog(u'执行SQL:%s' % achievementsqla.encode('utf-8'))
                    return

        #审核出租合同
        base.open(page.apartmentContractPage, apartmentContractPage.searchContractMould['tr_contract'])
        base.input_text(apartmentContractPage.searchContractMould['contract_num_loc'], contractNum)  # 输入合同编号
        base.click(apartmentContractPage.searchContractMould['search_button_loc'])
        base.staleness_of(apartmentContractPage.searchContractMould['tr_contract'])
        base.dblclick(apartmentContractPage.searchContractMould['tr_contract'])  # 双击第一条数据
        # 打开详情页需要加载，但DOM其实已经加载完仍旧无法点击，此处加5秒等待
        for i in range(5):
            try:
                base.click(apartmentContractPage.addApartmentContractMould['tab_info_loc'], index=4)  # 租客详情
                break
            except:
                time.sleep(1)
        # 初审
        base.click(apartmentContractPage.addApartmentContractMould['chushen_loc'])  # 初审
        base.click(apartmentContractPage.addApartmentContractMould['contract_audit_confirm'])  # 确定
        base.staleness_of(apartmentContractPage.searchContractMould['tr_contract'])  # 等待列表刷新
        base.dblclick(apartmentContractPage.searchContractMould['tr_contract'])  # 双击第一条数据
        for i in range(5):
            try:
                base.click(apartmentContractPage.addApartmentContractMould['tab_info_loc'], index=4)  # 租客详情
                break
            except:
                time.sleep(1)
        # 复审
        base.click(apartmentContractPage.addApartmentContractMould['fushen_loc'])  # 复审
        base.click(apartmentContractPage.addApartmentContractMould['contract_audit_confirm'])  # 确定
        base.check_submit()  # 等待提交完成
        contractAudit = "SELECT DISTINCT apartment_contract.contract_num FROM apartment_contract , house ,apartment WHERE apartment_contract.house_id = house.house_id " \
              "AND apartment_contract.house_id = apartment.house_id and apartment.apartment_code='%s'AND apartment_contract.contract_num = '%s'AND apartment_contract.audit_status='APPROVED'" \
              "and apartment_contract.contract_type = 'NEWSIGN' AND apartment_contract.entrust_type='SHARE' AND apartment_contract.is_active='Y' " % (
              apartmentCode, contractNum)
        if sqlbase.get_count(contractAudit) == 1:#数据检查
            consoleLog(u'审核出租合同 %s 成功' % contractNum)
        else:
            consoleLog(u'合同审核失败', level='e')
            consoleLog(u'执行SQL:%s' % contractAudit.encode('utf-8'))
            return
        # 业绩变成已生效
        achievementsqlb = "select * from apartment_contract_achievement where contract_num='%s' and is_active='Y' and accounting_num=1 and audit_status='AUDIT' and deleted=0 " % contractNum.encode(
            'utf-8')
        for i in range(5):
            if sqlbase.get_count(achievementsqlb) == 1:
                consoleLog(u'合同 %s 对应业绩已生效' % contractNum)
                break
            else:
                time.sleep(10)
                if i == 4:
                    consoleLog(u'合同 %s 对应业绩未生效' % contractNum, 'e')
                    consoleLog(u'执行SQL:%s' % achievementsqlb.encode('utf-8'))
                    return

signShareApartmentContract()