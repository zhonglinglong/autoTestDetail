# -*- coding:utf8 -*-

from assertpy import assert_that as asserts

from common import sqlbase
from common.base import log, consoleLog, Base
from common.interface import createCustomer, createApartmentContract, audit, auditType, auditStatus


@log
def test_1041():
    """前合同终止结算复审、出租和委托复审后业绩生效"""

    # describe： 无前合同，出租和委托复审后业绩生效
    # data：1、出租合同有前合同；2、前合同终止结算已复审3、出租合同未复审；4、委托合同已复审；5、业绩状态为未生效；
    # result：1、未生效业绩变为生效；2、业绩中的合同复审状态变为已复审；3、未起算的业绩状态不变；

    fileName = 'apartmentAchievement_1041'
    randomApartment = "select a.apartment_id,a.apartment_code from apartment a inner join apartment_contract_relation acr on a.apartment_id=acr.apartment_id " \
                      "INNER JOIN apartment_contract ac on acr.contract_id=ac.contract_id where a.rent_status='WAITING_RENT' and a.is_active='Y'and ac.contract_id in " \
                      "(select ace.contract_id from apartment_contract_end ace  INNER JOIN house_contract hc on hc.contract_num=ace.house_contract_num and hc.audit_status='APPROVED' " \
                      "AND hc.entrust_type = 'SHARE' AND hc.contract_status = 'EFFECTIVE' and hc.real_due_date>date_add(date(sysdate()), interval 1 YEAR) where ace.audit_status='REVIEW' ) ORDER BY RAND() LIMIT 1"
    if sqlbase.get_count(randomApartment) == 0:
        consoleLog(u'SQL查无数据！', 'w')
        consoleLog(u'执行SQL：%s' % randomApartment)
        return
    info = sqlbase.serach(randomApartment)
    apartmentCode = info[1]
    apartmentId = info[0]
    consoleLog(u'使用有前出租合同弄的房源 %s 签约承租合同' % apartmentCode)
    dateInfo = sqlbase.serach("select date(sysdate()),date_add(date(sysdate()),INTERVAL 1 day),date_add(date(sysdate()),interval 1 year),date_add(date(sysdate()),interval 3 year),date_add(date(sysdate()),INTERVAL 1 month) from dual")

    with Base() as base:
        # 创建租客，出租合同
        customer = createCustomer()
        apartmentContractInfo = createApartmentContract(apartement_id=apartmentId, customerInfo=customer,
                                                        rent_price=5500, sign_date=dateInfo[0],
                                                        rent_start_date=dateInfo[1], rent_end_date=dateInfo[2],
                                                        deposit=2000, payment_cycle='MONTH')
        apartmentContractNum = apartmentContractInfo['contractNum']
        apartmentContractId = apartmentContractInfo['contractID']
        # 业绩检查
        achievementsqla = "select aca.is_active,aca.audit_status,aca.accounting_time from apartment_contract_achievement aca inner join apartment a on a.apartment_code=aca.house_code " \
                          "where contract_num='%s' and a.apartment_code='%s' and aca.deleted=0" % (apartmentContractNum, apartmentCode)
        if  sqlbase.waitData(achievementsqla,1):
            achievementinfo = sqlbase.serach(achievementsqla)
            base.diffAssert(lambda test:asserts(achievementinfo[0]).is_equal_to('N'),1041,
                            u'%s:合同 %s 对应业绩生效状态异常，期望值 N 实际值 %s' % (fileName, apartmentContractNum, achievementinfo[0]))
            base.diffAssert(lambda test: asserts(achievementinfo[1]).is_equal_to('AUDIT'),1041,
                            u'%s:合同 %s 对应业绩审核状态异常, 期望值 AUDIT 实际值 %s' % (fileName, apartmentContractNum, achievementinfo[1]))
        else:
            consoleLog(u'%s:合同 %s 对应业绩生成失败' % (fileName, apartmentContractNum), 'e')
            consoleLog(u'执行SQL:%s' % achievementsqla)
            raise
        # 出租合同复审
        audit(apartmentContractId, auditType.apartmentContract, auditStatus.chuShen, auditStatus.fuShen)
        contractAudit = "select * from apartment_contract ac where ac.contract_num = '%s'AND ac.audit_status='APPROVED'and ac.contract_type = 'NEWSIGN' " \
                    "AND ac.entrust_type='SHARE' AND ac.is_active='Y'" % apartmentContractNum
        base.diffAssert(lambda test:asserts(sqlbase.get_count(contractAudit)).is_equal_to(1), 1041,
                        u'%s:合同 %s 审核失败,执行SQL: %s' % (fileName, apartmentContractNum, contractAudit))
        # 业绩检查
        achievementsqlb = "select aca.is_active,aca.audit_status,aca.contract_audit_status from apartment_contract_achievement aca inner join apartment a on a.apartment_code=aca.house_code " \
                          "where contract_num='%s' and a.apartment_code='%s' and aca.deleted=0 and aca.contract_audit_status='APPROVED'" % (apartmentContractNum, apartmentCode)
        if sqlbase.waitData(achievementsqlb,1):
            achievementinfob = sqlbase.serach(achievementsqlb)
            base.diffAssert(lambda test: asserts(achievementinfob[0]).is_equal_to('Y'),1041,
                            u'%s:合同 %s 对应业绩生效状态异常，期望值 Y 实际值 %s' % (fileName, apartmentContractNum, achievementinfob[0]))
            base.diffAssert(lambda test: asserts(achievementinfob[1]).is_equal_to('AUDIT'),1041,
                            u'%s:合同 %s 对应业绩审核状态异常, 期望值 AUDIT 实际值 %s' % (fileName, apartmentContractNum, achievementinfob[1]))
            base.diffAssert(lambda test: asserts(achievementinfob[2]).is_equal_to('APPROVED'),1041,
                            u'%s:合同 %s 对应业绩合同复审状态异常, 期望值 APPROVED 实际值 %s' % (fileName, apartmentContractNum, achievementinfob[2]))
        else:
            consoleLog(u'%s:合同 %s 对应业绩状态错误' % (fileName, apartmentContractNum), 'e')
            consoleLog(u'执行SQL:%s' % achievementsqla)

test_1041()