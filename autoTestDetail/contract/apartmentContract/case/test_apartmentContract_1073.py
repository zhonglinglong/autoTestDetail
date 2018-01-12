# -*- coding:utf8 -*-

from common import page
from common import sqlbase
from common.base import log, Base
from assertpy import assert_that as asserts
from selenium.common.exceptions import TimeoutException
from contract.apartmentContract.page import apartmentContractPage
from selenium.webdriver.common.by import By

@log
def test_1073():
    """出租合同3个页面的保存调用同一个接口，但是参数不一致，检测接口是否正常"""
    with Base() as base:
        contractNum = sqlbase.serach("select contract_num from query_apartment_contract where audit_status = 'AUDIT' and city_code = '330100' and contract_status = 'EFFECTIVE' "
                                     "and entrust_type = 'SHARE' order by rand() limit 1")
        base.open(page.apartmentContractPage, apartmentContractPage.searchContractMould['contract_num_loc'])
        base.input_text(apartmentContractPage.searchContractMould['contract_num_loc'],contractNum)
        base.click(apartmentContractPage.searchContractMould['search_button_loc'])
        base.staleness_of(apartmentContractPage.searchContractMould['tr_contract'])
        base.dblclick(apartmentContractPage.searchContractMould['tr_contract'],checkLoc=apartmentContractPage.saveBtn)
        for i in range(3):
            base.click(apartmentContractPage.editTab, index=i+2)
            # base.click(apartmentContractPage.saveBtn,index=i)
            base.wait_element(apartmentContractPage.saveBtn)
            base.driver.find_elements(By.CSS_SELECTOR, '.search-button-wrapper #form_save')[i].click()
            try:
                base.check_submit()
            except TimeoutException:
                base.diffAssert(lambda t:asserts('1').contains('2'), 1073, u'合同详情第 %s 个tab页无法保存' % str(i+1))

test_1073()