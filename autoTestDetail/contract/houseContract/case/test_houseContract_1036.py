# -*- coding:utf8 -*-
import time
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from common.interface import addHouseContractAndFitment
from contract.houseContract.page import houseContractPage
from assertpy import assert_that as asserts

@log
def test_1036():
    """到期委托合同正常删除"""

    # describe：到期委托合同可以正常删除成功
    # data：1、委托合同状态为到期；2.名下无出租合同
    # result：委托合同删除成功；

    fileName = 'houseContract_1036'
    dateSql = "select date_sub(date(sysdate()),INTERVAL 24 month),date_add(date(sysdate()),INTERVAL 1 day),date_sub(date(sysdate()),interval 5 month)," \
              "date_sub(date(sysdate()),interval 2 month),date_sub(date(sysdate()),INTERVAL 23 month) from dual"  # 时间元素
    dateInfo = sqlbase.serach(dateSql)
    houseSql = sqlbase.serach(
        "select house_id,residential_id,building_id,house_code from house where deleted=0 and city_code=330100 order by rand() limit 1")
    houseInfo = {'houseID': houseSql[0], 'residentialID': houseSql[1], 'buildingID': houseSql[2],'houseCode': houseSql[3]}  # 开发房源信息

    with Base() as base:
        #创建到期委托合同
        apartmentId = addHouseContractAndFitment(apartment_type='BRAND', entrust_type='ENTIRE', sign_date=dateInfo[0],
                                                 owner_sign_date=dateInfo[0], entrust_start_date=dateInfo[0],
                                                 entrust_end_date=dateInfo[2], delay_date=dateInfo[3],
                                                 free_start_date=dateInfo[0], free_end_date=dateInfo[4],
                                                 first_pay_date=dateInfo[0], second_pay_date=dateInfo[4],
                                                 rent=1234, parking=123, year_service_fee=321, payment_cycle='MONTH',
                                                 fitment_start_date=dateInfo[0], fitment_end_date=dateInfo[4], rooms=3,
                                                 fitmentCost=88888, houseInfo=houseInfo)
        contractSql = "select hc.contract_num,a.apartment_code from house_contract hc INNER JOIN apartment a on a.house_contract_id=hc.contract_id and a.apartment_id='%s'" % apartmentId
        contractInfo = sqlbase.serach(contractSql)
        contractNum = contractInfo[0]
        contractStatusSql = "select * from house_contract where contract_num='%s' and contract_status='EXPIRE'" % contractNum
        base.diffAssert(lambda test: asserts(sqlbase.waitData(contractStatusSql,1)).is_true(),1036,
                        u'%s:已到期合同 %s 生成异常,执行SQL：%s"' % (fileName, contractNum, contractStatusSql))
        base.open(page.entrustContractPage, houseContractPage.contractSearchMould['tr_contract'])
        base.input_text(houseContractPage.contractSearchMould['residential_name_loc'], contractInfo[1])
        base.input_text(houseContractPage.contractSearchMould['contract_num_loc'], contractNum)
        base.click(houseContractPage.contractSearchMould['search_button_loc'])
        base.staleness_of(houseContractPage.contractSearchMould['tr_contract'])
        base.click(houseContractPage.addHouseContractMould['delete_button'])
        base.click(houseContractPage.addHouseContractMould['delete_button_confirm'])
        base.check_submit()
        # 合同状态检查
        contractSqlb = "select * from house_contract where deleted=1 and contract_num='%s'" % contractNum
        base.diffAssert(lambda test: asserts(sqlbase.get_count(contractSqlb)).is_equal_to(1),1036,
                        u'%s:已到期委托合同 %s 删除异常,执行SQL：%s"' % (fileName, contractNum, contractSqlb))

test_1036()