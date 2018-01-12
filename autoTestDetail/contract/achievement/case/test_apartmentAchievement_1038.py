# -*- coding:utf8 -*-

from common import sqlbase
from common.base import log, consoleLog, Base
from common.interface import addHouseContractAndFitment, createCustomer, createApartmentContract
from assertpy import assert_that as asserts

@log
def test_1038():
    """承租周期大于一年且小于18个月生成一条业绩"""

    # describe： 出租合同承租周期小于一年,生成一条业绩单
    # data：1、房源类型为服务整租；2、出租合同承租周期为16个月；3、承租到期日等于委托延长期到期日；
    # result：生成一条业绩单，审核状态为待审核，核发月份为空

    fileName = 'apartmentAchievement_1038'

    with Base() as base:
        # 创建房源，委托合同
        dateSql = "select date(sysdate()),date_add(date(sysdate()),INTERVAL 1 day),date_add(date(sysdate()),interval 13 month),date_add(date(sysdate()),interval 16 month)," \
                  "date_add(date(sysdate()),INTERVAL 1 month) from dual"
        dateInfo = sqlbase.serach(dateSql)
        apartmentId = addHouseContractAndFitment(apartment_type='MANAGE', entrust_type='ENTIRE', sign_date=dateInfo[0],
                                                 owner_sign_date=dateInfo[0], entrust_start_date=dateInfo[0],
                                                 entrust_end_date=dateInfo[2], delay_date=dateInfo[3],
                                                 free_start_date=dateInfo[0], free_end_date=dateInfo[4],
                                                 first_pay_date=dateInfo[0], second_pay_date=dateInfo[4],
                                                 rent=1234, parking=123, year_service_fee=321, payment_cycle='MONTH',
                                                 fitment_start_date=dateInfo[0], fitment_end_date=dateInfo[4], rooms=3,
                                                 fitmentCost=88888)
        # 创建租客，出租合同
        customer = createCustomer()
        apartmentContractInfo = createApartmentContract(apartement_id=apartmentId, customerInfo=customer,
                                                        rent_price=5500, sign_date=dateInfo[0],
                                                        rent_start_date=dateInfo[1], rent_end_date=dateInfo[3],
                                                        deposit=2000, payment_cycle='MONTH')
        apartmentContractNum = apartmentContractInfo['contractNum']
        # 出租合同检查
        contractAdd = "select * from apartment a,apartment_contract ac ,apartment_contract_relation acr where a.apartment_id=acr.apartment_id and acr.contract_id=ac.contract_id " \
                      "and a.apartment_id='%s'AND ac.contract_num = '%s'AND ac.audit_status='AUDIT' and ac.contract_type = 'NEWSIGN' AND ac.entrust_type='ENTIRE' " \
                      "AND ac.is_active='Y' " % (apartmentId, apartmentContractNum)
        base.diffAssert(lambda test: asserts(sqlbase.waitData(contractAdd, 1)).is_true(), 1038,
                        u'%s:出租合同 %s 新增失败，执行SQL:%s' % (fileName, apartmentContractNum, contractAdd))
        # 业绩检查
        achievementsqla = "select FLOOR(ABS(DATEDIFF(aca.start_time,aca.end_time)/30)),aca.audit_status,aca.is_active from apartment_contract_achievement aca inner join apartment a " \
                          "on a.apartment_code=aca.house_code and a.apartment_id='%s' where aca.contract_num='%s' and aca.deleted=0" % (apartmentId, apartmentContractNum)
        if sqlbase.waitData(achievementsqla, 1):
            achievementinfo = sqlbase.serach(achievementsqla)
            base.diffAssert(lambda test: asserts(achievementinfo[0]).is_equal_to(16), 1038,
                            u'%s:合同 %s 对应业绩周期异常，期望值 16 实际值 %s' % (fileName, apartmentContractNum, achievementinfo[0]))
            base.diffAssert(lambda test: asserts(achievementinfo[1]).is_equal_to('AUDIT'), 1038,
                            u'%s:合同 %s 对应业绩审核状态异常, 期望值 AUDIT 实际值 %s' % (fileName, apartmentContractNum, achievementinfo[1]))
            base.diffAssert(lambda test: asserts(achievementinfo[2]).is_equal_to('N'), 1038,
                            u'%s:合同 %s 对应业绩生效状态异常, 期望值 N 实际值 %s' % (fileName, apartmentContractNum, achievementinfo[2]))
        else:
            consoleLog(u'%s:合同 %s 对应业绩生成异常' % (fileName, apartmentContractNum),'e')
            consoleLog(u'执行SQL：%s'% achievementsqla)

test_1038()