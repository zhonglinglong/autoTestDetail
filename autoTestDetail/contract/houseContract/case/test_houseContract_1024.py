# -*- coding:utf8 -*-

import time
from assertpy import assert_that as asserts
from selenium.webdriver.common.keys import Keys

from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.houseContract.page import houseContractPage


@log
def test_1024():
    """特殊免租期委托合同创建"""

    # describe：开发自营房源列表中签约委托合同
    # data：1、委托周期三年，三年的租金要递增；2、免租类别选首月，免租开始日和免租到期日选择为2个月；3、委托类型服务整租；4、车位费和服务费不为0；
    # result：1、委托合同创建成功；2、委托合同应付中生成财务记录；3、房源状态变为自营待租；

    fileName = 'houseContract_1024'
    hosueSql = "select h.house_code,h.build_area,sysdate(),date_ADD(date(sysdate()), interval 1 DAY),date_ADD(date(sysdate()), interval 3 YEAR),date_ADD(date(sysdate()), interval 1 MONTH),date_ADD(date(sysdate()), interval 2 MONTH) " \
               "from house_rent hr INNER JOIN house h on h.house_id=hr.house_id and h.city_code=330100 and h.deleted=0 where hr.house_status='WAITING_RENT' order by rand() limit 1"
    if sqlbase.get_count(hosueSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % hosueSql)
        return
    contractInfo = sqlbase.serach(hosueSql)

    with Base() as base:
        base.open(page.devHousePage, houseContractPage.addHouseContractMould['edit_loc'])
        base.input_text(houseContractPage.houseSearchMould['residential_name_loc'], contractInfo[0])  # 输入房源编号
        base.click(houseContractPage.houseSearchMould['search_button_loc'])  # 搜索
        base.staleness_of(houseContractPage.houseSearchMould['tr_house'])  # 等待列表刷新
        base.click(houseContractPage.houseSearchMould['add_house_contract_button']) # 新增委托
        try:
            base.input_text(houseContractPage.addHouseContractMould['inside_space_loc'], contractInfo[1]) # 面积
        except:
            base.click(houseContractPage.addHouseContractMould['newsign_button'])  #新签
        base.input_text(houseContractPage.addHouseContractMould['inside_space_loc'], contractInfo[1]) # 面积
        base.type_select(houseContractPage.typeMould['property_type'], 'HAVECARD')  # 有产证商品房
        base.click(houseContractPage.addHouseContractMould['pledge_loc']) # 抵押情况
        base.type_select(houseContractPage.typeMould['apartment_type'], 'MANAGE')  # 服务公寓
        base.type_select(houseContractPage.typeMould['reform_way'], 'UNRRESTYLE')  # 不改造
        base.type_select(houseContractPage.typeMould['entrust_type'], 'ENTIRE')  # 整租
        contractNum = 'AutoTestH' + '-' + time.strftime('%m%d%H%M') # 定义合同编号
        base.input_text(houseContractPage.addHouseContractMould['contract_num_loc'], contractNum) # 输入合同编号
        base.type_select(houseContractPage.typeMould['sign_body'], 'ISZTECH')  # 杭州爱上租科技有限公司
        base.type_date(houseContractPage.typeMould['sign_date'], contractInfo[2])  # 签约日期:当前日期
        base.type_date(houseContractPage.typeMould['owner_sign_date'], contractInfo[2])  # 业主交房日期:当前日期
        base.type_date(houseContractPage.typeMould['fitment_start_date'], contractInfo[3])  # 装修起算日:当前日期第二天
        base.type_date(houseContractPage.typeMould['fitment_end_date'], contractInfo[5])  # 装修截止日:当前日期后一个月
        base.type_date(houseContractPage.typeMould['entrust_start_date'], contractInfo[3])  # 委托起算日:当前日期第二天
        base.type_date(houseContractPage.typeMould['entrust_end_date'], contractInfo[4])  # 委托到期日:当前日期后三年
        base.type_select(houseContractPage.typeMould['freeType'], 'OTHER')  # 免租：其他
        base.type_select(houseContractPage.typeMould['free_start_date'], contractInfo[3])  #免租开始日期:当前日期第二天
        base.type_select(houseContractPage.typeMould['free_end_date'], contractInfo[6])  #免租结束日期:当前日期后二个月
        base.type_date(houseContractPage.typeMould['first_pay_date'], contractInfo[3])  # 首次付款日:当前日期第二天
        base.type_date(houseContractPage.typeMould['second_pay_date'], contractInfo[5])  # 第二次付款日:当前日期后一个月
        base.input_text(houseContractPage.addHouseContractMould['rent_loc'], 2000)  # 租金
        base.input_text(houseContractPage.addHouseContractMould['parking_loc'], 100)  # 停车费
        base.input_text(houseContractPage.addHouseContractMould['service_fee_loc'], 100)  # 服务费
        # base.type_select(base.typeMould['payment_cycle'], '半年付')   因为租金策略的机制是点击付款周期后触发，直接赋值不会触发，所以此select不直接赋值，采用点击方式
        base.click(houseContractPage.addHouseContractMould['payment_cycle_loc_1'])  # 付款周期
        base.click(houseContractPage.addHouseContractMould['payment_cycle_loc_2'])  # 月付
        base.click(houseContractPage.addHouseContractMould['contract_strategy2.1_loc'])
        base.input_text(houseContractPage.addHouseContractMould['contract_strategy2_loc'], 2500)  # 第二年租金策略
        base.click(houseContractPage.addHouseContractMould['contract_strategy3.1_loc'])
        base.input_text(houseContractPage.addHouseContractMould['contract_strategy3_loc'], 3000)  # 第三年租金策略
        base.click(houseContractPage.addHouseContractMould['next_loc_1'])  # 下一页
        base.click(houseContractPage.addHouseContractMould['next_loc_2'])  # 下一页
        # 业主信息
        landlordName = 'AutoTest'
        base.input_text(houseContractPage.addHouseContractMould['landlord_name_loc'], landlordName)
        base.type_select(houseContractPage.typeMould['ownerCardType'], 'IDNO')  # 身份证
        base.input_text(houseContractPage.addHouseContractMould['landlord_card_loc'], '42062119910828541X')
        base.click(houseContractPage.addHouseContractMould['landlord_name_loc'])
        base.input_text(houseContractPage.addHouseContractMould['landlord_phone_loc'], '13666666666')
        base.click(houseContractPage.addHouseContractMould['landlord_name_loc'])
        base.input_text(houseContractPage.addHouseContractMould['landlord_address_loc'], u'浙江省杭州市滨江区海创基地南楼三层')
        base.click(houseContractPage.addHouseContractMould['signFlag_loc'])
        time.sleep(0.5)
        # 签约人信息
        base.input_text(houseContractPage.addHouseContractMould['email_loc'], 'ishangzu@mail.com')
        # 紧急联系人
        base.input_text(houseContractPage.addHouseContractMould['emergency_name_loc'], u'紧急联系人')
        base.input_text(houseContractPage.addHouseContractMould['emergency_phone_loc'], '13777777777')
        base.type_select(houseContractPage.typeMould['emergency_card_type'], 'IDNO')  # 身份证
        base.input_text(houseContractPage.addHouseContractMould['emergency_id_card_loc'], '411722197508214014')
        base.input_text(houseContractPage.addHouseContractMould['emergency_address_loc'], u'浙江省杭州市滨江区海创基地北楼四层')
        # 收款人信息
        base.type_select(houseContractPage.typeMould['account_name'], landlordName)  # 收款人
        # base.input_text(houseContractPage.addHouseContractMould['account_bank_loc'], u'农业银行')
        # base.input_text(houseContractPage.addHouseContractMould['account_num_loc'], '1234567890')
        #测试环境
        base.type_select(houseContractPage.typeMould['pay_object'], 'PERSONAL')  # 个人
        base.input_text(houseContractPage.addHouseContractMould['account_num_loc'], '123456789')
        base.send_keys(houseContractPage.addHouseContractMould['account_num_loc'], Keys.ENTER)
        # base.input_text(houseContractPage.addHouseContractMould['account_num_loc'], '1234567890')
        # base.send_keys(houseContractPage.addHouseContractMould['account_num_loc'], Keys.ENTER)
        #base.click(houseContractPage.addHouseContractMould['bank_loc'])  # 收款银行
        base.click(houseContractPage.addHouseContractMould['close_loc'])  # 确认无误
        base.input_text(houseContractPage.addHouseContractMould['account_bank_loc'], u'农业银行')  #收款支行
        base.click(houseContractPage.addHouseContractMould['next_loc_3'])
        base.click(houseContractPage.addHouseContractMould['submit_loc'])
        base.check_submit()
        #合同生成检查
        contractSql = "select * from house_contract where is_active='Y' and apartment_type='MANAGE' and entrust_type='ENTIRE' and contract_num='%s'" % contractNum
        base.diffAssert(lambda test: asserts(sqlbase.waitData(contractSql,1)).is_true(),1024,
                        u'%s:委托合同 %s 新增失败，执行SQL:%s' % (fileName, contractNum, contractSql))
        #房源状态检查
        houseStatusSql = "select a.rent_status from apartment a inner join house h on h.house_id = a.house_id and h.house_code = '%s'" % contractInfo[0]
        base.diffAssert(lambda test: asserts(sqlbase.serach(houseStatusSql)[0]).is_equal_to('WAITING_RENT'),1024,
                        u'%s:委托合同 %s 房源状态异常,执行SQL:%s' % (fileName, contractNum, houseStatusSql))
        #委托合同应付检查
        payableSql = "select * from house_contract_payable hcp inner join house_contract hc on hc.contract_id=hcp.contract_id and  hc.contract_num='%s' " % contractNum
        base.diffAssert(lambda test: asserts(sqlbase.get_count(payableSql)).is_equal_to(36),1024,
                        u'%s:委托合同 %s 对应委托合同应收记录生成异常，期望生成 36 条，实际生成%s条，执行SQL:%s' % (fileName, contractNum, sqlbase.get_count(payableSql), payableSql))

test_1024()