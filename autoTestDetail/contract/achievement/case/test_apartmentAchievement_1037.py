# -*- coding:utf8 -*-

from assertpy import assert_that as asserts
from common import sqlbase
from common.base import log, consoleLog, Base
from common.interface import createCustomer, createApartmentContract

@log
def test_1037():
    """出租合同承租周期小于一年"""

    # describe： 出租合同承租周期小于一年,生成一条业绩单
    # data：1、房源已定价2、设计工程已交房；3、有装修成本；4、房源类型为合租；5、出租合同承租周期不大于1年；
    # result：生成一条业绩单，审核状态为待审核，核发月份为空

    fileName = 'apartmentAchievement_1037'
    randomApartment = "SELECT a.apartment_code,a.apartment_id,hc.contract_num,hc.contract_id FROM apartment a INNER JOIN house_contract hc " \
                      "ON hc.contract_id = a.house_contract_id AND hc.is_active = 'Y' AND hc.deleted = 0 AND hc.audit_status='APPROVED' AND hc.contract_status = 'EFFECTIVE' " \
                      "INNER JOIN fitment_house fh on fh.house_id=hc.house_id AND fh.fitment_status='HANDOVER' WHERE a.deleted = 0 " \
                      "AND a.rent_price > 0 AND a.city_code = 330100 AND hc.entrust_type = 'SHARE' AND a.rent_status='WAITING_RENT'" \
                      "AND hc.real_due_date>date_add(date(sysdate()), interval 1 YEAR) ORDER BY RAND() LIMIT 1"
    if sqlbase.get_count(randomApartment) == 0:
        consoleLog(u'%s:SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % randomApartment)
        return
    info = sqlbase.serach(randomApartment)
    apartmentCode = info[0]
    apartmentId = info[1]
    consoleLog(u'%s:使用房源 %s 签约出租合同' % (fileName,apartmentCode))
    dateInfo = sqlbase.serach(
        "SELECT entrust_start_date,entrust_end_date,date(sysdate()),date_add(date(sysdate()), interval 1 DAY),date_add(date(sysdate()), interval 6 month) "
        "from house_contract where contract_num = '%s'" % info[2])  # 获取时间元素

    with Base() as base:
        # 创建出租合同
        customer = createCustomer()
        apartmentContractInfo = createApartmentContract(apartement_id=apartmentId, customerInfo=customer,
                                                        rent_price=5500, sign_date=dateInfo[2],
                                                        rent_start_date=dateInfo[3], rent_end_date=dateInfo[4],
                                                        deposit=2000, payment_cycle='TOW_MONTH')
        apartmentContractNum = apartmentContractInfo['contractNum']
        # 出租合同检查
        contractAdd = "select * from apartment a,apartment_contract ac ,apartment_contract_relation acr where a.apartment_id=acr.apartment_id and acr.contract_id=ac.contract_id " \
                      "and a.apartment_code='%s'AND ac.contract_num = '%s'AND ac.audit_status='AUDIT' and ac.contract_type = 'NEWSIGN' AND ac.entrust_type='SHARE' " \
                      "AND ac.is_active='Y' " % (apartmentCode, apartmentContractNum)
        base.diffAssert(lambda test: asserts(sqlbase.waitData(contractAdd,1)).is_true(),1037,
                        u'%s:出租合同 %s 新增失败，执行SQL:%s' % (fileName, apartmentContractNum, contractAdd))
        # 业绩检查
        achievementsqla = "select aca.is_active,aca.audit_status,aca.accounting_time from apartment_contract_achievement aca inner join apartment a on a.apartment_code=aca.house_code " \
                          "where contract_num='%s' and a.apartment_code='%s'and aca.deleted=0 " % (apartmentContractNum, apartmentCode)
        if sqlbase.waitData(achievementsqla, 1):
            achievementinfo = sqlbase.serach(achievementsqla)
            base.diffAssert(lambda test:asserts(achievementinfo[0]).is_equal_to('N'), 1037,
                            u'%s:合同 %s 对应业绩生效状态异常，期望值 N 实际值 %s' % (fileName, apartmentContractNum, achievementinfo[0]))
            base.diffAssert(lambda test: asserts(achievementinfo[1]).is_equal_to('AUDIT'), 1037,
                            u'%s:合同 %s 对应业绩审核状态异常, 期望值 AUDIT 实际值 %s' % (fileName, apartmentContractNum, achievementinfo[1]))
            base.diffAssert(lambda test: asserts(achievementinfo[2]).is_equal_to('None'), 1037,
                            u'%s:合同 %s 对应业绩审核发月份异常, 期望值 None 实际值 %s' % (fileName, apartmentContractNum, achievementinfo[2]))
        else:
            consoleLog( u'%s:合同 %s 对应业绩生成异常' % (fileName, apartmentContractNum),'e')
            consoleLog(u'执行SQL：%s' % achievementsqla)

test_1037()