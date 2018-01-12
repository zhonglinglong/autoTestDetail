# -*- coding:utf8 -*-

import time
from assertpy import assert_that as asserts
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.houseContract.page import houseContractPage

@log
def test_1025():
    """新签合同续签，委托周期连续"""

    # describe：新签合同续签，委托周期连续
    # data：1、原合同状态为有效；2、续签合同委托起算日为系统默认值；
    # result：1、续签合同创建成功；2、原合同状态变为已续；

    fileName = 'houseContract_1025'
    contractSql = "select contract_num,apartment_type,entrust_type,reform_way,sign_body,payment_cycle,rental_price,year_service_fee,entrust_end_date,date_ADD(date(entrust_end_date), interval 1 DAY)," \
                  "date_ADD(date(entrust_end_date), interval 2 YEAR),date_ADD(date(entrust_end_date), interval 1 MONTH),SYSDATE(),house_id,contract_id from house_contract where contract_type='NEWSIGN' " \
                  "and deleted=0 and city_code=330100 and is_active='Y'and contract_status='EFFECTIVE' order by rand() limit 1"
    if sqlbase.get_count(contractSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % contractSql)
        return
    contractInfo = sqlbase.serach(contractSql)
    contractNum = contractInfo[0];consoleLog(u'%s:取委托合同 %s 做续签' % (fileName, contractNum))
    housearea = sqlbase.serach("select build_area from house h,house_contract hc where h.house_id=hc.house_id and hc.house_id='%s'" % contractInfo[13])
    lordSql = "select * from house_contract_landlord hcl INNER JOIN  house_contract hc on hc.contract_id = hcl.contract_id where hc.contract_id='%s'" % contractInfo[14]
    lordExist = True if sqlbase.get_count(lordSql) != 0 else False

    with Base() as base:
        base.open(page.entrustContractPage, houseContractPage.contractSearchMould['tr_contract'])
        base.input_text(houseContractPage.contractSearchMould['contract_num_loc'], contractNum)
        base.click(houseContractPage.contractSearchMould['search_button_loc'])  # 搜索
        base.staleness_of(houseContractPage.contractSearchMould['tr_contract'])  # 等待列表刷新
        base.click(houseContractPage.addHouseContractMould['continue_button'])  # 续签
        base.click(houseContractPage.addHouseContractMould['pledge_loc'])  # 抵押情况
        base.input_text(houseContractPage.addHouseContractMould['inside_space_loc'], housearea)  # 面积
        base.type_select(houseContractPage.typeMould['apartment_type'], contractInfo[1])  # 服务公寓
        base.type_select(houseContractPage.typeMould['reform_way'], contractInfo[3])  # 不改造
        base.type_select(houseContractPage.typeMould['entrust_type'], contractInfo[2])  # 整租
        newContractNum = 'AutoTestHX' + '-' + time.strftime('%m%d%H%M%S')  # 定义合同编号
        base.input_text(houseContractPage.addHouseContractMould['contract_num_loc'], newContractNum)  # 输入合同编号
        base.click(houseContractPage.addHouseContractMould['oldcontract_loc'])  # 原合同不并入新合同
        base.type_select(houseContractPage.typeMould['sign_body'], contractInfo[4])  # 杭州爱上租科技有限公司
        base.type_date(houseContractPage.typeMould['sign_date'], contractInfo[8])  # 签约日期:原合同到期日期
        base.type_date(houseContractPage.typeMould['owner_sign_date'], contractInfo[8])  # 业主交房日期:原合同到期日期
        base.type_date(houseContractPage.typeMould['entrust_start_date'], contractInfo[9])  # 委托起算日:原合同到期第二天
        base.type_date(houseContractPage.typeMould['entrust_end_date'], contractInfo[10])  # 委托到期日:原合同到期后二年
        base.type_select(houseContractPage.typeMould['freeType'], 'STARTMONTH')  # 免租：无
        base.type_date(houseContractPage.typeMould['first_pay_date'], contractInfo[9])  # 首次付款日:原合同到期第二天
        base.type_date(houseContractPage.typeMould['second_pay_date'], contractInfo[11])  # 第二次付款日:原合同到期后一个月
        base.input_text(houseContractPage.addHouseContractMould['rent_loc'], contractInfo[6])  # 租金
        base.input_text(houseContractPage.addHouseContractMould['parking_loc'], 100)  # 停车费
        base.input_text(houseContractPage.addHouseContractMould['service_fee_loc'], contractInfo[7])  # 服务费
        base.click(houseContractPage.addHouseContractMould['payment_cycle_loc_1'])  # 付款周期
        base.click(houseContractPage.addHouseContractMould['payment_cycle_month_loc'])  # 月付
        base.click(houseContractPage.addHouseContractMould['next_loc_1'])  # 下一页
        base.click(houseContractPage.addHouseContractMould['next_loc_2'])  # 下一页
        if not lordExist:
            landlordName = 'AutoTest'
            base.click(houseContractPage.addHouseContractMould['addlandlord_button']) # 新增业主信息
            base.input_text(houseContractPage.addHouseContractMould['landlord_name_loc'], landlordName)
            base.type_select(houseContractPage.typeMould['ownerCardType'], 'IDNO')  # 身份证
            base.input_text(houseContractPage.addHouseContractMould['landlord_card_loc'], '42062119910828541X')
            base.click(houseContractPage.addHouseContractMould['landlord_name_loc'])
            base.input_text(houseContractPage.addHouseContractMould['landlord_phone_loc'], '13666666666')
            base.click(houseContractPage.addHouseContractMould['landlord_name_loc'])
            base.input_text(houseContractPage.addHouseContractMould['landlord_address_loc'], u'浙江省杭州市滨江区海创基地南楼三层')
        base.input_text(houseContractPage.addHouseContractMould['emergency_name_loc'], u'紧急联系人')
        base.input_text(houseContractPage.addHouseContractMould['emergency_phone_loc'], '13777777777')
        base.type_select(houseContractPage.typeMould['emergency_card_type'], 'IDNO')  # 身份证
        base.input_text(houseContractPage.addHouseContractMould['emergency_id_card_loc'], '411722197508214014')
        base.input_text(houseContractPage.addHouseContractMould['emergency_address_loc'], u'浙江省杭州市滨江区海创基地北楼四层')
        base.click(houseContractPage.addHouseContractMould['next_loc_3'])
        base.click(houseContractPage.addHouseContractMould['submit_loc'])
        base.check_submit()
        # 原合同状态已续检查
        contractSql = "select contract_status from house_contract where  contract_num='%s'" % contractNum
        base.diffAssert(lambda test: asserts(sqlbase.serach(contractSql)[0]).is_equal_to('CONTINUED'),1025,
                        u'%s:委托合同 %s 续签异常,期望值 CONTINUED 实际值 %s，执行SQL:%s' % (fileName, contractNum, sqlbase.serach(contractSql)[0], contractSql))

test_1025()