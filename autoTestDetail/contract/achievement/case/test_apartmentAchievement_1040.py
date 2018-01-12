# -*- coding:utf8 -*-

from assertpy import assert_that as asserts
from common import sqlbase
from common.base import log, consoleLog, Base
from common.interface import addHouseContractAndFitment, createCustomer, createApartmentContract, audit, auditType, \
    auditStatus

@log
def test_1040():
    """出租和委托复审后业绩生效"""

    # describe： 无前合同，出租和委托复审后业绩生效
    # data：1、出租合同无前合同；2、出租合同未复审；3、委托合同未复审；4、业绩状态为未生效；
    # result：1、未生效业绩变为生效；2、业绩中的合同复审状态变为已复审；3、未起算的业绩状态不变；

    fileName = 'apartmentAchievement_1040'

    with Base() as base:
        # 创建房源，委托合同
        dateSql = "select date(sysdate()),date_add(date(sysdate()),INTERVAL 1 day),date_add(date(sysdate()),interval 1 year),date_add(date(sysdate()),interval 3 year)," \
                  "date_add(date(sysdate()),INTERVAL 1 month) from dual"
        dateInfo = sqlbase.serach(dateSql)
        apartmentId = addHouseContractAndFitment(apartment_type='MANAGE', entrust_type='SHARE', sign_date=dateInfo[0],
                                                 owner_sign_date=dateInfo[0], entrust_start_date=dateInfo[0],
                                                 entrust_end_date=dateInfo[3], delay_date=dateInfo[3],
                                                 free_start_date=dateInfo[0], free_end_date=dateInfo[4],
                                                 first_pay_date=dateInfo[0], second_pay_date=dateInfo[4],
                                                 rent=1234, parking=123, year_service_fee=321, payment_cycle='MONTH',
                                                 fitment_start_date=dateInfo[0], fitment_end_date=dateInfo[4], rooms=3,
                                                 fitmentCost=88888)
        houseContractInfo = sqlbase.serach("select hc.contract_num,hc.contract_id from house_contract hc inner join apartment a on a.house_id = hc.house_id "
                                          "and a.apartment_id='%s' where hc.audit_status='AUDIT' " % apartmentId)
        houseContractId = houseContractInfo[1]
        # 创建租客，出租合同
        customer = createCustomer()
        apartmentContractInfo = createApartmentContract(apartement_id=apartmentId, customerInfo=customer,
                                                        rent_price=5500, sign_date=dateInfo[0],
                                                        rent_start_date=dateInfo[1], rent_end_date=dateInfo[2],
                                                        deposit=2000, payment_cycle='MONTH')
        apartmentContractNum = apartmentContractInfo['contractNum']
        apartmentContractId = apartmentContractInfo['contractID']
        # 出租合同检查
        contractAdd = "select * from apartment a,apartment_contract ac ,apartment_contract_relation acr where a.apartment_id=acr.apartment_id and acr.contract_id=ac.contract_id " \
                      "and a.apartment_id='%s'AND ac.contract_num = '%s'AND ac.audit_status='AUDIT' and ac.contract_type = 'NEWSIGN' AND ac.entrust_type='SHARE' " \
                      "AND ac.is_active='Y' " % (apartmentId, apartmentContractNum)
        base.diffAssert(lambda test: asserts(sqlbase.waitData(contractAdd,1)).is_true(), 1040,
                        u'%s:出租合同 %s 新增失败，执行SQL:%s' % (fileName, apartmentContractNum, contractAdd))
        # 业绩检查
        achievementsqla = "select aca.is_active,aca.audit_status,aca.accounting_time from apartment_contract_achievement aca inner join apartment a on a.apartment_code=aca.house_code " \
                          "and a.apartment_id='%s' where aca.contract_num='%s' and aca.deleted=0" % (apartmentId,apartmentContractNum)
        if sqlbase.waitData(achievementsqla, 1):
            achievementinfo = sqlbase.serach(achievementsqla)
            base.diffAssert(lambda test: asserts(achievementinfo[0]).is_equal_to('N'),1040,
                            u'%s:合同 %s 对应业绩生效状态异常，期望值 N 实际值 %s' % (fileName, apartmentContractNum, achievementinfo[0]))
            base.diffAssert(lambda test: asserts(achievementinfo[1]).is_equal_to('AUDIT'),1040,
                            u'%s:合同 %s 对应业绩审核状态异常, 期望值 AUDIT 实际值 %s' % (fileName, apartmentContractNum, achievementinfo[1]))
        else:
            consoleLog(u'%s:出租合同 %s 对应业绩生成异常' % (fileName, apartmentContractNum),'e')
            consoleLog(u'执行SQL：%s' % achievementsqla)
        # 委托合同复审
        audit(houseContractId, auditType.houseContract, auditStatus.chuShen, auditStatus.fuShen)
        # 出租合同复审
        audit(apartmentContractId, auditType.apartmentContract, auditStatus.chuShen, auditStatus.fuShen)
        # 业绩状态检查
        achievementsqlb = "select aca.is_active,aca.audit_status,aca.contract_audit_status from apartment_contract_achievement aca inner join apartment a on a.apartment_code=aca.house_code " \
                          "and a.apartment_id='%s' where aca.contract_num='%s' and aca.contract_audit_status='APPROVED' and aca.deleted=0" % (apartmentId, apartmentContractNum)
        if sqlbase.waitData(achievementsqlb, 1):
            achievementinfob = sqlbase.serach(achievementsqlb)
            base.diffAssert(lambda test: asserts(achievementinfob[0]).is_equal_to('Y'), 1040,
                            u'%s:合同 %s 对应业绩生效状态异常，期望值 Y 实际值 %s' % (fileName, apartmentContractNum, achievementinfob[0]))
            base.diffAssert(lambda test: asserts(achievementinfob[1]).is_equal_to('AUDIT'), 1040,
                            u'%s:合同 %s 对应业绩审核状态异常, 期望值 AUDIT 实际值 %s' % (fileName, apartmentContractNum, achievementinfob[1]))
        else:
            consoleLog(u'%s:合同 %s 对应业绩状态错误' % (fileName, apartmentContractNum), 'e')
            consoleLog(u'执行SQL:%s' % achievementsqlb)

test_1040()