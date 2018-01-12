# -*- coding:utf8 -*-

import time

from common import sqlbase
from common.base import log, consoleLog, Base
from common.interface import addHouseContractAndFitment, createCustomer, createApartmentContract

@log
def test():
    """API创建合同"""

    # describe
    # data：
    # result：

    with Base() as base:
        #创建房源，委托合同

        houseSql = sqlbase.serach("select house_id,residential_id,building_id,house_code from house where deleted=0 and city_code=330100 order by rand() limit 1")
        houseInfo={'houseID':houseSql[0],'residentialID':houseSql[1],'buildingID':houseSql[2],'houseCode':houseSql[3]}
        dateSql = "select date(sysdate()),date_add(date(sysdate()),INTERVAL 1 day),date_add(date(sysdate()),interval 13 month),date_add(date(sysdate()),interval 16 month),date_add(date(sysdate()),INTERVAL 1 month) from dual"
        dateInfo = sqlbase.serach(dateSql)
        apartmentId = addHouseContractAndFitment(apartment_type='MANAGE', entrust_type='SHARE', sign_date=dateInfo[0],
                                                 owner_sign_date=dateInfo[0], entrust_start_date=dateInfo[0],
                                                 entrust_end_date=dateInfo[2], delay_date=dateInfo[3],
                                                 free_start_date=dateInfo[0], free_end_date=dateInfo[4],
                                                 first_pay_date=dateInfo[0], second_pay_date=dateInfo[4],
                                                 rent=1234, parking=123, year_service_fee=321, payment_cycle='MONTH',
                                                 fitment_start_date=dateInfo[0], fitment_end_date=dateInfo[4], rooms=3,
                                                 fitmentCost=88888,houseInfo=houseInfo)
        print  apartmentId
        #创建租客，出租合同
        customer = createCustomer()
        apartmentContractInfo = createApartmentContract(apartement_id=apartmentId, customerInfo=customer,
                                                        rent_price=5500, sign_date=dateInfo[0],
                                                        rent_start_date=dateInfo[1], rent_end_date=dateInfo[3],
                                                        deposit=2000, payment_cycle='MONTH')
        apartmentContractNum = apartmentContractInfo['contractNum']

        #出租合同检查
        contractAdd="SELECT DISTINCT ac.contract_num FROM apartment_contract ac, house h,apartment a WHERE ac.house_id = h.house_id " \
                    "AND ac.house_id = a.house_id AND ac.contract_num = '%s'AND ac.audit_status='AUDIT'and ac.contract_type = 'NEWSIGN' AND ac.entrust_type='SHARE' " \
                    "AND ac.is_active='Y' "% apartmentContractNum
        if sqlbase.get_count(contractAdd) == 1:#数据检查
            consoleLog(u'出租合同：%s 新增成功' % apartmentContractNum)
        else:
            consoleLog(u'合同新增失败',level = 'e')
            consoleLog(u'执行SQL:%s' % contractAdd)
            return
        #业绩检查
        achievementsqla = "select FLOOR(ABS(DATEDIFF(start_time,end_time)/30)),audit_status,is_active from apartment_contract_achievement where contract_num='%s' " % contractNum
        for i in range(5):
            if sqlbase.get_count(achievementsqla) == 1:
                achievementinfo = sqlbase.serach(achievementsqla)
                if achievementinfo[0] == 16 and achievementinfo[1] == 'AUDIT' and achievementinfo[2] == 'N':
                    consoleLog(u'合同 %s 对应生成一条业绩未生效且未审核，周期为16个月' % apartmentContractNum)
                else:
                    consoleLog(u'合同 %s 对应业绩状态异常' % apartmentContractNum,'e')
                    consoleLog(u'执行SQL:%s' % achievementsqla)
                break
            else:
                time.sleep(10)
                if i ==4:
                    consoleLog(u'合同 %s 对应业绩生成错误' % apartmentContractNum, 'e')
                    consoleLog(u'执行SQL:%s' % achievementsqla)
                else:
                    continue

test()