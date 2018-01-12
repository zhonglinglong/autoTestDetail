# -*- coding:utf8 -*-

import time

from common import page
from common import sqlbase
from common.base import log, consoleLog, Base, get_conf, set_conf
from contract.apartmentContract.page import apartmentContractPage


@log
def auditApartmentContract():
    """审核出租合同"""
    try:
        base=Base()
        base.open(page.apartmentContractPage, apartmentContractPage.searchContractMould['tr_contract'], havaFrame=False)
        #配置文件读取待审核合同信息
        contractNum = get_conf('apartmentContractInfo', 'contractnum')
        consoleLog(u'查询承租合同 %s 当前的审核状态' % contractNum)
        sql = "SELECT audit_status from apartment_contract where contract_num = '%s' and deleted = 0" % contractNum.encode( 'utf-8')

        if sqlbase.get_count(sql) > 0:
            if sqlbase.serach(sql)[0] == 'AUDIT':
                base.input_text(apartmentContractPage.searchContractMould['contract_num_loc'], contractNum)
            else:
                consoleLog(u'出租合同 %s 当前状态不是待审核，跳过审核用例' % contractNum, level='w')
        else:
            sql = "SELECT contract_num from apartment_contract where deleted = 0 and city_code = '330100' and contract_type = 'NEWSIGN' and audit_status = 'AUDIT' " \
                  "and contract_status = 'EFFECTIVE' and entrust_type = 'SHARE' limit 1"
            if sqlbase.get_count(sql) > 0:
                consoleLog(u'查询未审核的承租合同')
                contractNumNew = sqlbase.serach(sql)[0]
                consoleLog(u'未查询到出租合同 %s ，随机使用合同 %s 执行审核用例' % (contractNum, contractNumNew), level='w')
                contractNum = contractNumNew
                base.input_text(apartmentContractPage.searchContractMould['contract_num_loc'], contractNum)
            else:
                consoleLog(u'未查询到符合条件的承租合同，跳过审核用例', level='w')
        base.click(apartmentContractPage.searchContractMould['search_button_loc'])
        base.staleness_of(apartmentContractPage.searchContractMould['tr_contract'])
        base.dblclick(apartmentContractPage.searchContractMould['tr_contract'])
        # 打开详情页需要加载，但DOM其实已经加载完仍旧无法点击，此处加5秒等待
        for i in range(5):
            try:
                base.click(apartmentContractPage.addApartmentContractMould['tab_info_loc'], index=4)
                break
            except:
                time.sleep(1)
        # 驳回
        base.click(apartmentContractPage.addApartmentContractMould['bohui_loc'])
        base.input_text(apartmentContractPage.addApartmentContractMould['contract_audit_content'], u'自动化测试审核数据')
        base.click(apartmentContractPage.addApartmentContractMould['contract_audit_confirm'])
        base.staleness_of(apartmentContractPage.searchContractMould['tr_contract'])
        base.dblclick(apartmentContractPage.searchContractMould['tr_contract'])#双击第一条数据
        for i in range(5):
            try:
                base.click(apartmentContractPage.addApartmentContractMould['tab_info_loc'], index=4)#点租客详情
                break
            except:
                time.sleep(1)
        # 初审
        base.click(apartmentContractPage.addApartmentContractMould['chushen_loc'])
        base.click(apartmentContractPage.addApartmentContractMould['contract_audit_confirm'])
        base.staleness_of(apartmentContractPage.searchContractMould['tr_contract'])
        base.dblclick(apartmentContractPage.searchContractMould['tr_contract'])
        for i in range(5):
            try:
                base.click(apartmentContractPage.addApartmentContractMould['tab_info_loc'], index=4)
                break
            except:
                time.sleep(1)
        # 复审
        base.click(apartmentContractPage.addApartmentContractMould['fushen_loc'])
        base.click(apartmentContractPage.addApartmentContractMould['contract_audit_confirm'])
        base.check_submit()
        consoleLog(u'审核出租合同 %s 成功' % contractNum)
        #审核通过的合同编号写入配置文件
        set_conf('apartmentContractInfo', contractnum=contractNum)
    finally:
        base.driver.quit()

auditApartmentContract()
