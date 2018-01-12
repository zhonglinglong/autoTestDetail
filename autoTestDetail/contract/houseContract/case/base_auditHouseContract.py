# -*- coding:utf8 -*-

from common import page
from common import sqlbase
from common.base import log, consoleLog, Base, get_conf
from contract.houseContract.page import houseContractPage


@log
def addHouseContact():
    """审核委托合同"""
    try:
        base=Base()
        base.open(page.entrustContractPage, houseContractPage.contractSearchMould['tr_contract'], havaFrame=False)
        #配置文件读取委托合同信息
        contractNum = get_conf('houseContractInfo', 'contractNum');if contractNum!=None:consoleLog(u'配置文件中获得委托合同编号：%s'%contractNum)
        sql = "SELECT audit_status from house_contract where contract_num = '%s' and deleted = 0" % contractNum.encode('utf-8')
        if sqlbase.get_count(sql) > 0:
            if sqlbase.serach(sql)[0] == 'AUDIT':
                pass
            else:
                base.input_text(houseContractPage.houseSearchMould['status'], 'AUDIT')#待审核
                base.click(houseContractPage.contractSearchMould['search_button_loc'])
                base.staleness_of(houseContractPage.contractSearchMould['tr_contract'])
                contractNum = base.script(
                    "var a = $('[datagrid-row-index=\"0\"] > [field=\"contract_num\"] > div').text();return a",
                    True).decode('utf-8')
                consoleLog(u'使用随机委托合同：%s 做审核操作' % contractNum, level='w')
        else:
            base.input_text(houseContractPage.houseSearchMould['status'], 'AUDIT')
            base.click(houseContractPage.contractSearchMould['search_button_loc'])
            base.staleness_of(houseContractPage.contractSearchMould['tr_contract'])
            contractNum = base.script(
                "var a = $('[datagrid-row-index=\"0\"] > [field=\"contract_num\"] > div').text();return a", True).decode(
                'utf-8')
            consoleLog(u'使用随机委托合同：%s 做审核操作' % contractNum, level='w')
        base.input_text(houseContractPage.houseSearchMould['status'], '')
        base.input_text(houseContractPage.contractSearchMould['contract_num_loc'], contractNum);consoleLog(u'实际审核委托合同编号：%s' % contractNum)
        base.click(houseContractPage.contractSearchMould['search_button_loc'])
        base.staleness_of(houseContractPage.contractSearchMould['tr_contract'])
        base.dblclick(houseContractPage.contractSearchMould['tr_contract'], checkLoc=houseContractPage.addHouseContractMould['contract_num_loc'])
        # 驳回
        base.click(houseContractPage.addHouseContractMould['tab_info_loc'], index=3)
        base.script('$("button[status=\'REJECTED\']")[1].click()')
        base.input_text(houseContractPage.addHouseContractMould['contract_audit_content'], u'自动化测试审核数据')
        base.click(houseContractPage.addHouseContractMould['contract_audit_confirm'])
        base.staleness_of(houseContractPage.contractSearchMould['tr_contract'])
        base.dblclick(houseContractPage.contractSearchMould['tr_contract'], checkLoc=houseContractPage.addHouseContractMould['contract_num_loc'])
        # 审核租金
        base.click(houseContractPage.addHouseContractMould['tab_info_loc'], index=1)
        base.click(houseContractPage.addHouseContractMould['rent_detail_selectAll'])
        base.click(houseContractPage.addHouseContractMould['rent_audit_loc'])
        base.click(houseContractPage.addHouseContractMould['audit_pass_loc'])
        base.click(houseContractPage.addHouseContractMould['rent_audit_confirm'])
        # 初审
        base.click(houseContractPage.addHouseContractMould['tab_info_loc'], index=3)
        base.script('$("button[status=\'PASS\']")[2].click()')
        base.click(houseContractPage.addHouseContractMould['contract_audit_confirm'])
        base.staleness_of(houseContractPage.contractSearchMould['tr_contract'])
        base.dblclick(houseContractPage.contractSearchMould['tr_contract'], checkLoc=houseContractPage.addHouseContractMould['contract_num_loc'])
        # 复审
        base.click(houseContractPage.addHouseContractMould['tab_info_loc'], index=3)
        base.script('$("button[status=\'APPROVED\']")[1].click()')
        base.click(houseContractPage.addHouseContractMould['contract_audit_confirm'])
        base.check_submit()
        consoleLog(u'委托合同：%s 审核成功' % contractNum)

    finally:
        base.driver.quit()

addHouseContact()
