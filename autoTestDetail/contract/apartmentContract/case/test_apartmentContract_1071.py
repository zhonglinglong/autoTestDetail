# -*- coding:utf8 -*-

from common import page
from common import sqlbase
from common.base import log, Base
from contract.apartmentContract.page import apartmentContractPage
from assertpy import assert_that as asserts
from selenium.common.exceptions import TimeoutException

@log
def test_1071():
    """检测出租合同续签需要合同应收全部已审"""
    sql = "SELECT act.contract_num from apartment_contract act INNER JOIN apartment_contract_receivable acr on act.contract_id = acr.contract_id where act.deleted = 0 " \
                  "and acr.deleted = 0 and act.entrust_type = 'SHARE' and act.city_code = '330100' and acr.end_status = 'NOTGET' order by rand() limit 1"
    contractNum = sqlbase.serach(sql)[0]
    with Base() as base:
        base.open(page.apartmentContractPage,apartmentContractPage.searchContractMould['contract_num_loc'])
        base.input_text(apartmentContractPage.searchContractMould['contract_num_loc'],contractNum)
        base.click(apartmentContractPage.searchContractMould['search_button_loc'])
        base.staleness_of(apartmentContractPage.searchContractMould['tr_contract'])
        base.click(apartmentContractPage.searchContractMould['resign_loc'])
        try:
            base.wait_element(apartmentContractPage.alertInfo)
        except TimeoutException:
            base.diffAssert(lambda t:asserts('a').ends_with('b'), 1071, u'出租合同未全部收款审核的情况下，续签没有弹出提示')

test_1071()