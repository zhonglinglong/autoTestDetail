# -*- coding:utf8 -*-

import time

from common import page
from common import sqlbase
from common.base import log, consoleLog, Base, get_conf, set_conf
from contract.houseContract.page import houseContractPage


@log
def addHouseContact():
    """新增委托合同"""
    #合同信息
    def addCommon():
        #base.script("$('#edit_btn + button')[0].click()")   #点击列表页第一行的新增委托
        contractNum = 'AutoTest' + '-' + time.strftime('%m%d-%H%M%S')
        base.click(houseContractPage.houseSearchMould['add_house_contract_button'], index=0)
        base.input_text(houseContractPage.addHouseContractMould['inside_space_loc'], 100)
        base.type_select(houseContractPage.typeMould['property_type'], 'HAVECARD')  # 有产证商品房
        base.click(houseContractPage.addHouseContractMould['pledge_loc'])
        base.type_select(houseContractPage.typeMould['apartment_type'], 'BRAND')  # 品牌公寓
        base.type_select(houseContractPage.typeMould['reform_way'], 'OLDRESTYLE')  # 老房全装
        base.type_select(houseContractPage.typeMould['entrust_type'], 'SHARE')  # 合租
        base.input_text(houseContractPage.addHouseContractMould['contract_num_loc'], contractNum)
        base.type_select(houseContractPage.typeMould['sign_body'], 'ISZTECH')  # 杭州爱上租科技有限公司
        base.type_date(houseContractPage.typeMould['sign_date'], '2017-02-01')
        base.type_date(houseContractPage.typeMould['owner_sign_date'], '2017-02-01')
        base.type_date(houseContractPage.typeMould['fitment_start_date'], '2017-02-01')
        base.type_date(houseContractPage.typeMould['fitment_end_date'], '2017-02-28')
        base.type_date(houseContractPage.typeMould['entrust_start_date'], '2017-02-01')
        base.type_date(houseContractPage.typeMould['entrust_end_date'], '2020-02-29')
        base.type_select(houseContractPage.typeMould['freeType'], 'STARTMONTH')  # 首月
        base.type_date(houseContractPage.typeMould['first_pay_date'], '2017-02-28')
        base.type_date(houseContractPage.typeMould['second_pay_date'], '2017-03-01')
        base.input_text(houseContractPage.addHouseContractMould['rent_loc'], 4321)
        base.input_text(houseContractPage.addHouseContractMould['parking_loc'], 123)
        base.input_text(houseContractPage.addHouseContractMould['service_fee_loc'], 234)
        # base.type_select(base.typeMould['payment_cycle'], '半年付')   因为租金策略的机制是点击付款周期后触发，直接赋值不会触发，所以此select不直接赋值，采用点击方式
        base.click(houseContractPage.addHouseContractMould['payment_cycle_loc_1'])
        base.click(houseContractPage.addHouseContractMould['payment_cycle_loc_2'])
        base.click(houseContractPage.addHouseContractMould['next_loc_1'])
        base.click(houseContractPage.addHouseContractMould['next_loc_2'])
        # 业主信息
        base.input_text(houseContractPage.addHouseContractMould['landlord_name_loc'], contractNum)
        base.type_select(houseContractPage.typeMould['ownerCardType'], 'IDNO')  # 身份证
        base.input_text(houseContractPage.addHouseContractMould['landlord_card_loc'], '42062119910828541X')
        base.click(houseContractPage.addHouseContractMould['landlord_name_loc'])
        base.input_text(houseContractPage.addHouseContractMould['landlord_phone_loc'], '13666666666')
        base.click(houseContractPage.addHouseContractMould['landlord_name_loc'])
        base.input_text(houseContractPage.addHouseContractMould['landlord_address_loc'], u'浙江省杭州市滨江区海创基地南楼三层')
        base.click(houseContractPage.addHouseContractMould['signFlag_loc'])
        time.sleep(0.5)
        # 签约人信息
        base.type_select(houseContractPage.typeMould['card_type'], 'IDNO')  # 身份证
        base.type_select(houseContractPage.typeMould['gender'], 'MALE')  # 男
        base.input_text(houseContractPage.addHouseContractMould['email_loc'], 'ishangzu@mail.com')
        base.input_text(houseContractPage.addHouseContractMould['other_contact_loc'], u'浙江省杭州市滨江区海创基地北楼三层')
        # 紧急联系人
        base.input_text(houseContractPage.addHouseContractMould['emergency_name_loc'], u'紧急联系人')
        base.input_text(houseContractPage.addHouseContractMould['emergency_phone_loc'], '13777777777')
        base.type_select(houseContractPage.typeMould['emergency_card_type'], 'IDNO')  # 身份证
        base.input_text(houseContractPage.addHouseContractMould['emergency_id_card_loc'], '411722197508214014')
        base.input_text(houseContractPage.addHouseContractMould['emergency_address_loc'], u'浙江省杭州市滨江区海创基地北楼四层')
        # 收款人信息
        base.type_select(houseContractPage.typeMould['account_name'], 'AutoTest')
        base.input_text(houseContractPage.addHouseContractMould['account_bank_loc'], u'农业银行')
        base.input_text(houseContractPage.addHouseContractMould['account_num_loc'], '1234567890')
        base.click(houseContractPage.addHouseContractMould['next_loc_3'])
        base.click(houseContractPage.addHouseContractMould['submit_loc'])
        base.check_submit()
        #将数据写入配置文件
        set_conf('houseContractInfo', contractnum=contractNum)
        sql = "SELECT contract_id from house_contract where contract_num = '%s'" % contractNum.encode('utf-8')
        set_conf('houseContractInfo', contractid=sql.serach(sql)[0])

        consoleLog(u'新增委托合同 %s 成功' % contractNum)

    try:
        base=Base()
        base.open(page.devHousePage, houseContractPage.addHouseContractMould['edit_loc'])
        #配置文件读取将要委托的房源信息
        house = get_conf('residential', 'residentialname') + get_conf('residential', 'buildingname') + get_conf(
            'residential', 'unitname') + get_conf('residential', 'housenoname')

        if sqlbase.get_count("SELECT * from house where deleted=0 AND property_name like '%s%%'" % house.encode('utf-8')) > 0:
            count = sqlbase.get_count(
                "SELECT * from house hh INNER JOIN house_contract hc on hh.house_id = hc.house_id where hc.deleted=0 AND hh.property_name like '%s%%'" % house.encode( 'utf-8'))
            if count == 0:
                base.input_text(houseContractPage.houseSearchMould['residential_name_loc'], get_conf('houseInfo', 'houseCode'))
                # 审核房源之后，solr的增量需要时间，所以在此需要多次等待，首次查询后没有发现房源，则等待一分钟后再次查询，重复五次，一旦某次查询后，发现了房源，则结束循环
                for i in range(5):
                    base.click(houseContractPage.houseSearchMould['search_button_loc'])
                    try:
                        base.find_element(houseContractPage.houseSearchMould['tr_house'])
                        if i > 1:
                            consoleLog(u'已查找到数据')
                        break
                    except:
                        consoleLog(u'未找到house-core的solr增量房源数据，尝试第%s次查找' % str(i + 1).decode('utf-8'), level='w')
                        time.sleep(5)
                base.addCommon()
            else:
                sql = "SELECT hh.house_code,hh.property_name from house hh INNER JOIN house_rent hr on hh.house_id = hr.house_id " \
                      "where hh.city_code = '330100' and hr.house_status = 'WAITING_RENT' and not EXISTS (" \
                      "SELECT 1 from house_contract hc where hc.city_code = '330100' and hh.house_id = hc.house_id) limit 1"
                houseCode = sqlbase.serach(sql)[0]
                consoleLog('测试房源不满足签约条件，随机使用房源 %s 签约' % sqlbase.serach(sql)[1])
                base.input_text(houseContractPage.houseSearchMould['residential_name_loc'], houseCode)
                base.click(houseContractPage.houseSearchMould['search_button_loc'])
                base.staleness_of(houseContractPage.houseSearchMould['tr_house'])
                base.addCommon()
        else:#配置文件无数据，在数据库随机取符合条件的数据做委托交易
            sql = "SELECT hh.house_code,hh.property_name from house hh INNER JOIN house_rent hr on hh.house_id = hr.house_id " \
                  "where hh.city_code = '330100' and hr.house_status = 'WAITING_RENT' and not EXISTS (" \
                  "SELECT 1 from house_contract hc where hc.city_code = '330100' and hh.house_id = hc.house_id) limit 1"
            houseCode = sqlbase.serach(sql)[0]
            consoleLog('未找到测试房源，随机使用房源 %s 签约' % sqlbase.serach(sql)[1])
            base.input_text(houseContractPage.houseSearchMould['residential_name_loc'], houseCode)
            base.click(houseContractPage.houseSearchMould['search_button_loc'])
            base.staleness_of(houseContractPage.houseSearchMould['tr_house'])
            base.addCommon()

    finally:
        base.driver.quit()

addHouseContact()
