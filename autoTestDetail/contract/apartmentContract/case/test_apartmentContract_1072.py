# -*- coding:utf8 -*-

from selenium.common.exceptions import TimeoutException
from common import page
from common.base import log, consoleLog, Base
from contract.apartmentContract.page import apartmentContractPage
from assertpy import assert_that as asserts
from common import interface
from common.datetimes import today,addDays,addMonths

@log
def test_1070():
    """检测出租合同续签超过可续签日期"""
    with Base() as base:
        apartment = interface.addHouseContractAndFitment(apartment_type='MANAGE',entrust_type='ENTIRE',sign_date=today(),owner_sign_date=today(),entrust_start_date=today(),
                                             entrust_end_date=addMonths(24),delay_date=addMonths(27),free_start_date=today(),free_end_date=addMonths(1),first_pay_date=today(),
                                             second_pay_date=addMonths(1),rent=2800,parking=120,year_service_fee=180,payment_cycle='MONTH')
        customer = interface.createCustomer()
        contractInfo = interface.createApartmentContract(apartement_id=apartment,customerInfo=customer,rent_price=5500,sign_date=today(),rent_start_date=today(),rent_end_date=addMonths(12),
                                          deposit=2500,payment_cycle='MONTH')
        base.open(page.apartmentContractPage,apartmentContractPage.searchContractMould['contract_num_loc'])
        base.click(apartmentContractPage.searchContractMould['entire_tab_button'])
        base.input_text(apartmentContractPage.searchContractMould['contract_num_loc'] ,contractInfo['contractNum'], index=1)
        base.click(apartmentContractPage.searchContractMould['entire_search_button_loc'])
        base.staleness_of(apartmentContractPage.searchContractMould['entire_tr_contract'])
        interface.receipt('apartmentContract',contractInfo['contractID'])
        base.click(apartmentContractPage.searchContractMould['resign_loc'],index=1)
        base.click(apartmentContractPage.addApartmentContractMould['deposit_manage'],index=0)
        contractNum = contractInfo['contractNum']+'xu'
        base.input_text(apartmentContractPage.addApartmentContractMould['contract_num_loc'],contractNum)
        base.type_date(apartmentContractPage.typeMould['sign_date'],today())
        base.type_date(apartmentContractPage.typeMould['rent_end_date2'], addDays(1,addMonths(27)))
        try:
            base.wait_element(apartmentContractPage.alertInfo)
        except TimeoutException:
            consoleLog(u'出租合同 %s 新签成功，续签承租到期日为 %s' % (contractInfo['contractNum'],addDays(1,addMonths(27))))
            base.diffAssert(lambda t:asserts('a').ends_with('b'),1071,u'续签出租合同，承租到期日超过委托合同实际到期日时，没有弹出超过时间的提示')

test_1070()