# -*- coding:utf8 -*-

import datetime
import time

from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.apartmentContract.page import apartmentContractPage
from contract.earnest import earnestPage


@log
def earnestSignContract():
    """下定管理页面定金确认后签约合同"""

    # describe： 下定管理页面定金确认后签约合同
    # data：下定状态为待签
    # result：未确认的确认成功后，签约出租合同成功，审核通过

    sql = "SELECT earnest.sign_status,earnest.earnest_code,earnest.earnest_money,apartment.apartment_code,earnest.confirm_status FROM earnest ,apartment " \
          "WHERE earnest.room_id = apartment.room_id and earnest.sign_status = 'WAITING_SIGN' and earnest.earnest_money>'100' and earnest.deleted=0 order by rand() limit 1"
    if sqlbase.get_count(sql) ==0:
        consoleLog(u'SQL查询失败！','w')
        consoleLog(u'执行SQL：%s' % sql.encode('utf-8'))
        return
    result = sqlbase.serach(sql)

    with Base() as base:
        base.open(page.earnestPage, earnestPage.searchMouid['tr_contract'])
        base.input_text(earnestPage.searchMouid['earnest_code_loc'], result[1])  # 输入定金编号
        consoleLog(u'获取房源编号:%s ；定金编号：%s ；' % (result[3], result[1]))
        base.click(earnestPage.searchMouid['search_button_loc'])  # 搜索
        base.staleness_of(earnestPage.searchMouid['tr_contract'])  # 等待列表刷新
        if result[4] == 'N':#未确认的需要确认
            base.click(earnestPage.searchMouid['confirm_button_loc'])#确认
            base.input_text(earnestPage.confirmMould['earnest_money_loc'], result[2])#输入金额
            base.type_select(earnestPage.confirmMould['payway'],'ALIPAY')#收款方式
            base.input_text(earnestPage.confirmMould['name_loc'],u'Autotest')#收据名字
            base.type_select(earnestPage.confirmMould['company'],'ISZTECH')#收款公司
            base.type_date(earnestPage.confirmMould['receipt_date'],datetime.date.today())#收款日期
            base.click(earnestPage.confirmMould['submit_loc'])#提交
            base.check_submit()

        base.click(earnestPage.searchMouid['sign_loc'])  # 点击签约
        randomHouseContract = sqlbase.serach(
            "SELECT entrust_start_date,entrust_end_date,date(sysdate()),date_add(date(sysdate()), interval 1 DAY) from house_contract,apartment "
            "where  house_contract.house_id=apartment.house_id and apartment.apartment_code= '%s'" %result[3].encode('utf-8'))
        contractNum = 'AutoTest' + '-' + time.strftime('%m%d%H%M')
        base.input_text(apartmentContractPage.addApartmentContractMould['contract_num_loc'], contractNum)  # 合同编号
        base.type_date(apartmentContractPage.typeMould['sign_date'], randomHouseContract[2])  # 签约日期
        base.type_date(apartmentContractPage.typeMould['rent_start_date'], randomHouseContract[2])  # 承租起算日
        base.type_date(apartmentContractPage.typeMould['rent_end_date'], randomHouseContract[1])  # 承租到期日
        base.input_text(apartmentContractPage.addApartmentContractMould['deposit_loc'], 1234)  # 押金
        base.type_select(apartmentContractPage.typeMould['payment_type'], 'NORMAL')  # 正常付款
        base.type_select(apartmentContractPage.typeMould['payment_cycle'], 'TOW_MONTH')  # 二月付
        # base.input_text(ApartmentContractPage.addApartmentContractMould['rent_strategy_price_loc'],4321)     #月租金：需求变更，单条情况下无需手动录入
        # base.type_date(ApartmentContractPage.typeMould['rent_strategy_end_loc'],'2018-08-08')    #租金策略结束日：不知道为什么自动化打开的DOM和正常情况下的DOM不一样，所以直接用jquery赋值
        js = "$('#contract_strategy_table > table > tbody > tr > td:nth-child(8) > input').val('%s')" % \
             randomHouseContract[1]
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
        base.input_text(apartmentContractPage.addApartmentContractMould['sign_name_loc'], 'AutoTest')  # 签约人姓名
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
            "AND apartment_contract.house_id = apartment.house_id  AND apartment_contract.contract_num = '%s'AND apartment_contract.audit_status='AUDIT'" \
            "and apartment_contract.contract_type = 'NEWSIGN' AND apartment_contract.is_active='Y' "%contractNum
        if sqlbase.get_count(contractAdd)==1:#数据检查
            consoleLog(u'出租合同：%s 新增成功' % contractNum)
        else:
            consoleLog(u'合同新增失败',level='e')
            consoleLog(u'执行SQL：%s' % contractAdd.encode('utf-8'))
            return

        # 审核出租合同
        base.open(page.apartmentContractPage, apartmentContractPage.searchContractMould['tr_contract'])
        base.input_text(apartmentContractPage.searchContractMould['contract_num_loc'], contractNum)  # 输入合同编号
        base.click(apartmentContractPage.searchContractMould['search_button_loc'])  # 搜索
        base.staleness_of(apartmentContractPage.searchContractMould['tr_contract'])  # 等待列表刷新
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
        contractAud="SELECT DISTINCT apartment_contract.contract_num FROM apartment_contract , house ,apartment WHERE apartment_contract.house_id = house.house_id " \
            "AND apartment_contract.house_id = apartment.house_id  AND apartment_contract.contract_num = '%s'AND apartment_contract.audit_status='APPROVED'" \
            "and apartment_contract.contract_type = 'NEWSIGN' AND apartment_contract.is_active='Y' "%contractNum
        if sqlbase.get_count(contractAud)==1:#数据检查
            consoleLog(u'出租合同：%s 新增审核通过' % contractNum)
        else:
            consoleLog(u'合同新增审核失败',level='e')
            consoleLog(u'执行SQL：%s' % contractAud.encode('utf-8'))
            return

earnestSignContract()
