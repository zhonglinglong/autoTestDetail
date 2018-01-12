# -*- coding:utf8 -*-

from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.apartmentContract.page import apartmentContractPage


@log
def test():
    """出租合同续签超过可续签日期"""

    # describe：检出租合同续签超过可续签日期,不可签约
    # data：1.合同应收款项全部已审;2.承租到期日>委托合同到期日+延长期
    # result：续签合同失败

    contractSql = "SELECT ac.contract_num,cp.urgent_customer_name,cp.customer_name from apartment_contract ac inner join customer_person cp on ac.person_id=cp.person_id " \
                  "where ac.deleted = 0 and ac.city_code = '330100' and ac.entrust_type='SHARE' and ac.audit_status = 'AUDIT' and ac.contract_status = 'EFFECTIVE' " \
                  "and ac.deleted=0 and payment_type='NORMAL' ORDER BY RAND() LIMIT 1"
    if sqlbase.get_count(contractSql) == 0:
        consoleLog(u'SQL查无数据！', level='w')
        consoleLog(u'执行SQL：%s' % contractSql.encode('utf-8'))
        return
    info = sqlbase.serach(contractSql)
    contractNum = info[0]
    consoleLog(u'取随机合同 %s 做续签' % contractNum)

    with Base() as base:
        base.open(page.apartmentContractPage, apartmentContractPage.searchContractMould['tr_contract'])
        base.input_text(apartmentContractPage.searchContractMould['contract_num_loc'], contractNum)
        base.click(apartmentContractPage.searchContractMould['search_button_loc'])
        base.staleness_of(apartmentContractPage.searchContractMould['tr_contract'])
        base.click((apartmentContractPage.searchContractMould['resign_loc']))  # 续签
test()