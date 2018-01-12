# -*- coding:utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from common.base import log,consoleLog,Base,get_conf
from common import page
from contract.houseContract.page import houseContractEndPage
from common import sqlbase


@log
def deleteHouseContractEnd():
    """删除委托合同终止结算"""
    try:
        base=Base()
        base.open(page.contractEndPage, houseContractEndPage.searchMould['contract_search_button_loc'], havaFrame=False)
        base.click(houseContractEndPage.addContractEndMould['tab_info'], index=1)
        #配置文件读取待审核的委托合终止结算
        contractNum = get_conf('houseContractInfo', 'contractnum')
        consoleLog(u'查询委托合同 %s 是否存在终止结算' % contractNum)

        sql = "SELECT * from house_contract where contract_num = '%s' and deleted = 0 and audit_status = 'APPROVED' and contract_status != 'EFFECTIVE'" % contractNum.encode(
            'utf-8')
        if sqlbase.get_count(sql) > 0:
            base.input_text(houseContractEndPage.searchMould['end_contract_num_loc'], contractNum)
            base.click(houseContractEndPage.searchMould['end_search_button_loc'])
            base.staleness_of(houseContractEndPage.searchMould['tr_contract_end'])
        else:
            base.click(houseContractEndPage.searchMould['end_search_button_loc'])
            base.staleness_of(houseContractEndPage.searchMould['tr_contract_end'])
            contractNum = base.script(
                "var a = $('#ContractReceivable_table_wt > div:nth-child(1) > div:nth-child(2) > div.datagrid-view > div.datagrid-view2 > div.datagrid-body > "
                "table > tbody > tr:nth-child(1) > td[field=\"contract_num\"] > div').text();return a", True).decode(
                'utf-8')
            consoleLog(u'未找到测试合同的终止结算，随机删除委托合同 %s 的终止结算' % contractNum)
        base.click(houseContractEndPage.addContractEndMould['delete_button'])
        base.click(houseContractEndPage.addContractEndMould['delete_button_confirm'])
        base.check_submit()
        consoleLog(u'委托合同 %s 终止结算删除成功' % contractNum)
    finally:
        base.driver.quit()

deleteHouseContractEnd()
