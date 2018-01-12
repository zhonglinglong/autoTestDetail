# -*- coding:utf8 -*-
import time

from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.houseContract.page import houseContractPage
from assertpy import assert_that as asserts

@log
def test_1029():
    """已审核的合同反审后初审,复审"""

    # describe：已审核的合同反审后初审,复审
    # data：1、合同状态为有效或者已续；2、合同审核状态为已审核；
    # result：1、无错误提示；2、合同状态变为已复审；

    fileName = 'houseContract_1029'
    contractSql = "select hc.contract_num,h.house_code from house h INNER JOIN house_contract hc on hc.house_id=h.house_id where hc.audit_status='APPROVED' and hc.deleted=0 " \
                  "and hc.is_active='Y' and hc.city_code=330100 and EXISTS (select * from house_contract_payable hcp where hcp.contract_id=hc.contract_id and hcp.end_status='NOTPAY') " \
                  "order by rand() limit 1"
    if sqlbase.get_count(contractSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName,'w')
        consoleLog(u'执行SQL：%s' % contractSql)
        return
    contractInfo = sqlbase.serach(contractSql)
    contractNum = contractInfo[0]
    houseCode = contractInfo[1]
    consoleLog(u'%s:取已审核委托合同 %s 做反审后审核' % (fileName, contractNum))

    with Base() as base:
        base.open(page.entrustContractPage, houseContractPage.contractSearchMould['tr_contract'])
        base.input_text(houseContractPage.contractSearchMould['contract_num_loc'], contractNum)
        base.input_text(houseContractPage.contractSearchMould['residential_name_loc'], houseCode)
        base.click(houseContractPage.contractSearchMould['search_button_loc'])  # 搜索
        base.staleness_of(houseContractPage.contractSearchMould['tr_contract'])  # 等待列表刷新
        base.dblclick(houseContractPage.contractSearchMould['tr_contract'],
                      checkLoc=houseContractPage.addHouseContractMould['contract_num_loc'])  # 双击第一条数据
        #反审
        base.click(houseContractPage.addHouseContractMould['tab_info_loc'], index=3)  # 最后一页
        base.script('$("button[status=\'REAUDIT\']")[1].click()')  # 反审
        base.input_text(houseContractPage.addHouseContractMould['contract_audit_content'], u'自动化反审')  # 反审意见
        base.click(houseContractPage.addHouseContractMould['contract_audit_confirm'])  # 确定
        base.staleness_of(houseContractPage.contractSearchMould['tr_contract'])  # 等待数据刷新
        base.dblclick(houseContractPage.contractSearchMould['tr_contract'],
                      checkLoc=houseContractPage.addHouseContractMould['contract_num_loc'])  # 双击第一条数据
        # 初审
        base.click(houseContractPage.addHouseContractMould['tab_info_loc'], index=3)  # 最后一页
        time.sleep(3)
        base.script('$("button[status=\'PASS\']")[1].click()')  # 初审
        base.click(houseContractPage.addHouseContractMould['contract_audit_confirm'])  # 确认
        base.staleness_of(houseContractPage.contractSearchMould['tr_contract'])  # 等待数据刷新
        base.dblclick(houseContractPage.contractSearchMould['tr_contract'],
                      checkLoc=houseContractPage.addHouseContractMould['contract_num_loc'])  # 双击第一条数据
        # 复审
        base.click(houseContractPage.addHouseContractMould['tab_info_loc'], index=3)  # 最后一页
        time.sleep(3)
        base.script('$("button[status=\'APPROVED\']")[1].click()')  # 复审
        try:
            base.click(houseContractPage.addHouseContractMould['contract_audit_confirm'])  # 确认
        except:
            message = base.script("var a=$('.messager-body.panel-body.panel-body-noborder.window-body span').text();return a",True)
            messagehope1 = u'应付租金大于租金策略'
            messagehope2 = u'租金策略大于应付租金'
            if messagehope1 in message or messagehope2 in message:
                base.click(houseContractPage.addHouseContractMould['rentdif_cofirm_loc'])  # 租金策略不同提示确定
            base.click(houseContractPage.addHouseContractMould['contract_audit_confirm'])  # 确认
        base.check_submit()  # 等待提交完成
        # 合同状态检查
        contractSql = "select audit_status from house_contract where  deleted=0 and contract_num='%s'" % contractNum
        auditStatus = sqlbase.serach(contractSql)[0]
        base.diffAssert(lambda test: asserts(auditStatus).is_equal_to('APPROVED'),1029,
                        u'%s:委托合同 %s 反审后复审异常,期望值 APPROVED 实际值 %s，执行SQL:%s' % (fileName, contractNum, auditStatus, contractSql))

test_1029()