# -*- coding:utf8 -*-
import datetime
import time

from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.houseContract.page import houseContractPage


@log
def addBrandShareHouseContract():
    """新增品牌合租公寓委托到审核通过主流程"""

    # describe：新增品牌合租公寓委托到审核通过主流程
    # data：未签约委托合同，房源状态状态为‘业主待租’
    # result：签约成功，复审通过

    sql = "SELECT hh.house_code,hh.property_name from house hh INNER JOIN house_rent hr on hh.house_id = hr.house_id " \
          "where hh.city_code = '330100' and hr.house_status = 'WAITING_RENT' and not EXISTS (" \
          "SELECT 1 from house_contract hc where hc.city_code = '330100' and hh.house_id = hc.house_id) order by rand() limit 1"
    if sqlbase.get_count(sql) ==0:
        consoleLog(u'SQL查询失败，未找到房源！',level='w')
        consoleLog(u'执行SQL：%s' % sql.encode('utf-8'))
        return

    with Base() as base:
        houseCode = sqlbase.serach(sql)[0]
        today=datetime.date.today()
        base.open(page.devHousePage, houseContractPage.addHouseContractMould['edit_loc'])
        consoleLog('使用房源 %s 签约' % sqlbase.serach(sql)[1].encode('utf-8'))
        base.input_text(houseContractPage.houseSearchMould['residential_name_loc'], houseCode)  # 输入房源编号
        base.click(houseContractPage.houseSearchMould['search_button_loc'])  # 搜索
        base.staleness_of(houseContractPage.houseSearchMould['tr_house'])  # 等待列表刷新
        contractNum = 'AutoTest' + '-' + time.strftime('%m%d%H%M') # 自定义合同编号
        base.click(houseContractPage.houseSearchMould['add_house_contract_button'], index=0)  # 新增委托
        base.input_text(houseContractPage.addHouseContractMould['inside_space_loc'], 100)  # 使用面积
        base.type_select(houseContractPage.typeMould['property_type'], 'HAVECARD')  # 有产证商品房
        base.click(houseContractPage.addHouseContractMould['pledge_loc'])  # 抵押情况：有
        base.type_select(houseContractPage.typeMould['apartment_type'], 'BRAND')  # 品牌公寓
        base.type_select(houseContractPage.typeMould['reform_way'], 'OLDRESTYLE')  # 老房全装
        base.type_select(houseContractPage.typeMould['entrust_type'], 'SHARE')  # 合租
        base.input_text(houseContractPage.addHouseContractMould['contract_num_loc'], contractNum)  # 合同编号
        base.type_select(houseContractPage.typeMould['sign_body'], 'ISZTECH')  # 杭州爱上租科技有限公司
        base.type_date(houseContractPage.typeMould['sign_date'], today)  # 签约日期
        base.type_date(houseContractPage.typeMould['owner_sign_date'], today)  # 业主交房日
        base.type_date(houseContractPage.typeMould['fitment_start_date'], today)  # 装修起算日
        base.type_date(houseContractPage.typeMould['fitment_end_date'], today + datetime.timedelta(days=7))  # 装修截止日
        base.type_date(houseContractPage.typeMould['entrust_start_date'], today)  # 委托起算日
        base.type_date(houseContractPage.typeMould['entrust_end_date'], '2020-09-12')  # 委托到期日
        base.type_select(houseContractPage.typeMould['freeType'], 'STARTMONTH')  # 免租期类型首月
        # base.type_date(houseContractPage.typeMould['free_start_date'], today)  # 免租起算日
        # base.type_date(houseContractPage.typeMould['free_end_date'], today+datetime.timedelta(days=30))  # 免租到期日
        base.type_date(houseContractPage.typeMould['first_pay_date'], today)  # 首次付款日
        base.type_date(houseContractPage.typeMould['second_pay_date'], today + datetime.timedelta(days=30))  # 第二次付款日
        base.input_text(houseContractPage.addHouseContractMould['rent_loc'], 4321)  # 房租
        base.input_text(houseContractPage.addHouseContractMould['parking_loc'], 123)  # 车位费
        base.input_text(houseContractPage.addHouseContractMould['service_fee_loc'], 234)  # 服务费
        # base.type_select(base.typeMould['payment_cycle'], '半年付')   因为租金策略的机制是点击付款周期后触发，直接赋值不会触发，所以此select不直接赋值，采用点击方式
        base.click(houseContractPage.addHouseContractMould['payment_cycle_loc_1'])  # 付款周期
        base.click(houseContractPage.addHouseContractMould['payment_cycle_loc_2'])  # 月付
        base.click(houseContractPage.addHouseContractMould['next_loc_1'])  # 下一步
        base.click(houseContractPage.addHouseContractMould['next_loc_2'])  # 下一步
        # 业主信息
        base.input_text(houseContractPage.addHouseContractMould['landlord_name_loc'], contractNum)  # 业主名字
        base.type_select(houseContractPage.typeMould['ownerCardType'], 'IDNO')  # 身份证
        base.input_text(houseContractPage.addHouseContractMould['landlord_card_loc'], '42062119910828541X')  # 身份证号
        base.click(houseContractPage.addHouseContractMould['landlord_name_loc'])
        base.input_text(houseContractPage.addHouseContractMould['landlord_phone_loc'], '13666666666')  # 联系电话
        base.click(houseContractPage.addHouseContractMould['landlord_name_loc'])
        base.input_text(houseContractPage.addHouseContractMould['landlord_address_loc'], u'浙江省杭州市滨江区海创基地南楼三层')  # 通讯地址
        base.click(houseContractPage.addHouseContractMould['signFlag_loc'])  # 勾选签约人
        time.sleep(0.5)
        # 签约人信息
        base.type_select(houseContractPage.typeMould['card_type'], 'IDNO')  # 身份证
        base.type_select(houseContractPage.typeMould['gender'], 'MALE')  # 男
        base.input_text(houseContractPage.addHouseContractMould['email_loc'], 'ishangzu@mail.com')  # email
        base.input_text(houseContractPage.addHouseContractMould['other_contact_loc'], u'浙江省杭州市滨江区海创基地北楼三层')  # 其他联系方式
        # 紧急联系人
        base.input_text(houseContractPage.addHouseContractMould['emergency_name_loc'], u'紧急联系人')  # 姓名
        base.input_text(houseContractPage.addHouseContractMould['emergency_phone_loc'], '13777777777')  # 电话
        base.type_select(houseContractPage.typeMould['emergency_card_type'], 'IDNO')  # 身份证
        base.input_text(houseContractPage.addHouseContractMould['emergency_id_card_loc'], '411722197508214014')  # 身份证号
        base.input_text(houseContractPage.addHouseContractMould['emergency_address_loc'], u'浙江省杭州市滨江区海创基地北楼四层')  # 地址
        # 收款人信息
        base.type_select(houseContractPage.typeMould['account_name'], 'AutoTest')  # 收款人，下拉框
        base.input_text(houseContractPage.addHouseContractMould['account_bank_loc'], u'农业银行')  # 收款银行
        base.input_text(houseContractPage.addHouseContractMould['account_num_loc'], '1234567890')  # 手机号
        base.click(houseContractPage.addHouseContractMould['next_loc_3'])  # 下一步
        base.click(houseContractPage.addHouseContractMould['submit_loc'])  # 提交
        base.check_submit()  # 等待提交完成
        contractAdd="SELECT * FROM house ,house_contract WHERE house.house_id = house_contract.house_id AND house_contract.is_active='Y' " \
                    "AND house_contract.apartment_type='BRAND' AND house_contract.entrust_type='SHARE' AND house_contract.audit_status='AUDIT' " \
                    "AND house.house_code='%s' AND house_contract.contract_num='%s' "%(houseCode,contractNum)
        if  sqlbase.get_count(contractAdd):#数据检查
            consoleLog(u'委托合同 %s 新增成功'% contractNum)
        else:
            consoleLog(u'委托合同新增失败','e')
            consoleLog(u'执行SQL：%s' % contractAdd.encode('utf-8'))
            return
        #合同审核
        base.open(page.entrustContractPage, houseContractPage.contractSearchMould['tr_contract'])
        base.input_text(houseContractPage.houseSearchMould['status'], '')  # 输入状态
        base.input_text(houseContractPage.contractSearchMould['contract_num_loc'], contractNum)
        base.click(houseContractPage.contractSearchMould['search_button_loc'])  # 搜索
        base.staleness_of(houseContractPage.contractSearchMould['tr_contract'])  # 等待数据刷新
        base.dblclick(houseContractPage.contractSearchMould['tr_contract'],
                      checkLoc=houseContractPage.addHouseContractMould['contract_num_loc'])  # 双击第一条数据
        # 审核租金
        base.click(houseContractPage.addHouseContractMould['tab_info_loc'], index=1)  # 租金明细
        base.click(houseContractPage.addHouseContractMould['rent_detail_selectAll'])  # 选择所有租金记录
        base.click(houseContractPage.addHouseContractMould['rent_audit_loc'])  # 租金审核
        base.click(houseContractPage.addHouseContractMould['audit_pass_loc'])  # 审核通过
        base.click(houseContractPage.addHouseContractMould['rent_audit_confirm'])  # 确认
        # 初审
        base.click(houseContractPage.addHouseContractMould['tab_info_loc'], index=3)  # 资料上传
        base.script('$("button[status=\'PASS\']")[2].click()')  # 初审
        base.click(houseContractPage.addHouseContractMould['contract_audit_confirm'])  # 确定
        base.staleness_of(houseContractPage.contractSearchMould['tr_contract'])  # 等待数据刷新
        base.dblclick(houseContractPage.contractSearchMould['tr_contract'],
                      checkLoc=houseContractPage.addHouseContractMould['contract_num_loc'])  # 双击第一条数据
        # 复审
        base.click(houseContractPage.addHouseContractMould['tab_info_loc'], index=3)  # 资料上传
        base.script('$("button[status=\'APPROVED\']")[1].click()')  # 复审
        base.click(houseContractPage.addHouseContractMould['contract_audit_confirm'])  # 确定
        base.check_submit()  # 等待上传完成
        contractAud = "SELECT * FROM house ,house_contract WHERE house.house_id = house_contract.house_id AND house_contract.is_active='Y' " \
                      "AND house_contract.apartment_type='BRAND' AND house_contract.entrust_type='SHARE' AND house_contract.audit_status='APPROVED' " \
                      "AND house.house_code='%s' AND house_contract.contract_num='%s' " % (houseCode, contractNum)
        if sqlbase.get_count(contractAud):#数据检查
            consoleLog(u'委托合同 %s 复审成功' % contractNum)
        else:
            consoleLog(u'委托合同复审失败', 'e')
            consoleLog(u'执行SQL：%s' % contractAud.encode('utf-8'))
            return

addBrandShareHouseContract()