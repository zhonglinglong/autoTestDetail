# -*- coding:utf8 -*-
import time

from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.apartmentContract.page import apartmentContractPage
from assertpy import assert_that as asserts
from common import interface
from common.datetimes import today,addDays,addMonths

@log
def test_1070():
    """检测出租合同正常续签"""
    with Base() as base:
        apartment = interface.addHouseContractAndFitment(apartment_type='MANAGE',entrust_type='ENTIRE',sign_date=today(),owner_sign_date=today(),entrust_start_date=today(),
                                             entrust_end_date=addMonths(24),delay_date=addMonths(27),free_start_date=today(),free_end_date=addMonths(1),first_pay_date=today(),
                                             second_pay_date=addMonths(1),rent=2800,parking=120,year_service_fee=180,payment_cycle='MONTH')
        customer = interface.createCustomer()
        contractInfo = interface.createApartmentContract(apartement_id=apartment,customerInfo=customer,rent_price=5500,sign_date=today(),rent_start_date=today(),rent_end_date=addMonths(12),
                                          deposit=2500,payment_cycle='MONTH')
        base.open(page.apartmentContractPage,apartmentContractPage.searchContractMould['contract_num_loc'])
        base.click(apartmentContractPage.searchContractMould['entire_tab_button'])
        base.input_text(apartmentContractPage.searchContractMould['contract_num_loc'],contractInfo['contractNum'],index=1)
        base.click(apartmentContractPage.searchContractMould['entire_search_button_loc'])
        base.staleness_of(apartmentContractPage.searchContractMould['entire_tr_contract'])
        interface.receipt('apartmentContract',contractInfo['contractID'])
        base.click(apartmentContractPage.searchContractMould['resign_loc'],index=1)
        base.click(apartmentContractPage.addApartmentContractMould['deposit_manage'],index=0)
        contractNum = contractInfo['contractNum']+'xu'
        base.input_text(apartmentContractPage.addApartmentContractMould['contract_num_loc'],contractNum)
        base.type_date(apartmentContractPage.typeMould['sign_date'],today())
        base.type_date(apartmentContractPage.typeMould['rent_end_date2'], addDays(-1,addMonths(24)))
        base.input_text(apartmentContractPage.addApartmentContractMould['deposit_loc'],2000)
        base.type_select(apartmentContractPage.typeMould['payment_type'],'NORMAL')
        base.type_select(apartmentContractPage.typeMould['payment_cycle'], 'TOW_MONTH')
        base.script("$('#contract_strategy_table > table > tbody > tr > td:nth-child(8) > input').click()")
        base.type_date(apartmentContractPage.addApartmentContractMould['rent_strategy1_end_loc'],addDays(-1,addMonths(24)))
        base.click(apartmentContractPage.addApartmentContractMould['next_loc_1'])
        base.click(apartmentContractPage.addApartmentContractMould['next_loc_2'])
        base.click(apartmentContractPage.addApartmentContractMould['submit_loc'])
        base.check_submit()
        consoleLog(u'已成功续签承租合同 %s' % contractNum)
        time.sleep(10)
        achievementCount = sqlbase.get_count("SELECT * from apartment_contract_achievement where contract_id = "
                                             "(SELECT contract_id from apartment_contract where contract_num = '%s' and deleted = 0)" % contractNum)
        receiptsCount = sqlbase.get_count("SELECT * from apartment_contract_receipts where contract_id = "
                                             "(SELECT contract_id from apartment_contract where contract_num = '%s' and deleted = 0)" % contractNum)
        base.diffAssert(lambda t:asserts(achievementCount).is_not_zero(), 1070, u'续签后，没有生成出单业绩')
        base.diffAssert(lambda t:asserts(receiptsCount).is_not_zero(), 1070, u'续签后，原合同押金没有转入新合同中')

test_1070()