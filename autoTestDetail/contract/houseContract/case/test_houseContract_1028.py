# -*- coding:utf8 -*-

import time
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.houseContract.page import houseContractPage
from assertpy import assert_that as asserts

@log
def test_1028():
    """正常初审,复审"""

    # describe：委托合同正常初审，复审
    # data：1、合同状态为有效或者已续；2、租金明细审核状态全部为已审3、合同审核状态为待审核；
    # result：1、无错误提示；2、合同状态变为已复审；

    fileName = 'houseContract_1028'
    contractSql = "select hc.contract_num,h.house_code from house h INNER JOIN house_contract hc on hc.house_id=h.house_id where hc.audit_status='AUDIT' and hc.deleted=0 " \
                  "and hc.is_active='Y' and hc.city_code=330100 and sign_date>'2017-01-01' and EXISTS (select * from house_contract_payable hcp where hcp.contract_id=hc.contract_id " \
                  "and hcp.end_status='NOTPAY') order by rand() limit 1"
    if sqlbase.get_count(contractSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % contractSql)
        return
    contractInfo = sqlbase.serach(contractSql)
    contractNum = contractInfo[0]
    houseCode = contractInfo[1]
    consoleLog(u'%s:取未审核委托合同 %s 做审核' % (fileName, contractNum))

    with Base() as base:
        base.open(page.entrustContractPage, houseContractPage.contractSearchMould['tr_contract'])
        base.input_text(houseContractPage.contractSearchMould['contract_num_loc'], contractNum)
        base.input_text(houseContractPage.contractSearchMould['residential_name_loc'], houseCode)
        base.click(houseContractPage.contractSearchMould['search_button_loc'])  # 搜索
        base.staleness_of(houseContractPage.contractSearchMould['tr_contract'])  # 等待列表刷新
        base.dblclick(houseContractPage.contractSearchMould['tr_contract'],
                      checkLoc=houseContractPage.addHouseContractMould['contract_num_loc'])  # 双击第一条数据
        #审核租金
        base.click(houseContractPage.addHouseContractMould['recreate_button']) # 重新生成租金明细
        base.click(houseContractPage.addHouseContractMould['tab_info_loc'], index=1)  # 租金页面
        time.sleep(3)
        base.click(houseContractPage.addHouseContractMould['rent_save_button'])  # 保存
        for i in range(3):
            try:
                base.check_submit()
                break
            except:
                message = base.script(
                    "var a=$('.panel.window.messager-window>div:nth-child(2)>div:nth-child(2)').text();return a", True)
                messagehope=u'用户数据已经被其他用户更新'
                if messagehope in message:
                    base.click(houseContractPage.addHouseContractMould['message_close_loc'])  # 关闭提示
                    base.click(houseContractPage.addHouseContractMould['rent_save_button'])  # 保存
                    base.check_submit()
        base.click(houseContractPage.addHouseContractMould['rent_detail_selectAll'])  # 全选
        base.click(houseContractPage.addHouseContractMould['rent_audit_loc'])  # 审核
        base.click(houseContractPage.addHouseContractMould['audit_pass_loc'])  # 通过
        base.click(houseContractPage.addHouseContractMould['rent_audit_confirm'])  # 确认
        # 初审
        base.click(houseContractPage.addHouseContractMould['tab_info_loc'], index=3)  # 最后一页
        time.sleep(3)
        base.script('$("button[status=\'PASS\']")[2].click()')  # 初审
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
            base.click(houseContractPage.addHouseContractMould['diffRental_button'])    #应付租金金额和租金策略中的金额不一致的提示中的确认按钮
            base.click(houseContractPage.addHouseContractMould['contract_audit_confirm'])  # 复审确认
        for i in range(3):
            try:
                base.check_submit()
                break
            except:
                message = base.script(
                    "var a=$('.panel.window.messager-window>div:nth-child(2)>div:nth-child(2)').text();return a", True)
                messagehope=u'用户数据已经被其他用户更新'
                if messagehope in message:
                    base.click(houseContractPage.addHouseContractMould['message_close_loc'])  # 关闭提示
                    base.click(houseContractPage.addHouseContractMould['contract_audit_confirm'])  # 确认
                    base.check_submit()
        # 合同状态检查
        contractSql = "select audit_status from house_contract where  contract_num='%s'" % contractNum
        auditStatus = sqlbase.serach(contractSql)[0]
        base.diffAssert(lambda test: asserts(auditStatus).is_equal_to('APPROVED'),1028,
                        u'%s:委托合同 %s 审核状态异常,期望值 APPROVED 实际值 %s，执行SQL:%s' % (fileName, contractNum, auditStatus, contractSql))

test_1028()