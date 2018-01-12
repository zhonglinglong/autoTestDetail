# -*- coding:utf8 -*-

import time
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.houseContract.page import houseContractPage
from assertpy import assert_that as asserts

@log
def test_1033():
    """已初审的合同新添加租金明细且未审时无法复审"""

    # describe：反审后已初审的合同新添加租金明细且未审时无法复审
    # data：1、合同状态为有效或者已续；2、合同审核状态为已审核；3、初审后在租金明细页面新增一条租金明细并保存；
    # result：1、审核失败，提示租金未审核

    fileName = 'houseContract_1033'
    contractSql = "select hc.contract_num,sysdate(),h.house_code from house h INNER JOIN house_contract hc on hc.house_id=h.house_id where hc.audit_status='APPROVED' and hc.deleted=0 " \
                  "and hc.is_active='Y' and hc.city_code=330100 and sign_date>'2017-01-01' order by rand() limit 1"
    if sqlbase.get_count(contractSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % contractSql)
        return
    contractInfo = sqlbase.serach(contractSql)
    contractNum = contractInfo[0]
    houseCode = contractInfo[2]
    consoleLog(u'%s:取未审核委托合同 %s 做审核' % (fileName, contractNum))

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
        time.sleep(2)
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
        # 新增租金明细
        base.click(houseContractPage.addHouseContractMould['tab_info_loc'], index=1)  # 租金明细
        base.click(houseContractPage.addHouseContractMould['add_detail_button'])  #新增租金明细
        time.sleep(1)
        base.script("$('.erp-table>tbody>tr:last input[type=\"checkbox\"]').click()")  # 选择记录
        base.type_select(houseContractPage.addHouseContractMould['money_type_loc'], 'PARKING')  # 款项类型
        base.type_date(houseContractPage.addHouseContractMould['rent_start_date_loc'], contractInfo[1])  # 开始时间
        base.type_date(houseContractPage.addHouseContractMould['rent_end_date_loc'], contractInfo[1])  # 结束时间
        base.type_date(houseContractPage.addHouseContractMould['payable_date_loc'], contractInfo[1])  # 应付时间
        base.scrollTo(houseContractPage.addHouseContractMould['payable_amount_loc'])
        base.input_text(houseContractPage.addHouseContractMould['payable_amount_loc'], 100)  # 应付金额
        base.click(houseContractPage.addHouseContractMould['rent_save_button'])  # 保存
        #复审
        base.click(houseContractPage.addHouseContractMould['tab_info_loc'], index=3)  # 最后一页
        time.sleep(3)
        base.script('$("button[status=\'APPROVED\']")[2].click()')  # 复审
        try:
            base.click(houseContractPage.addHouseContractMould['contract_audit_confirm'])  # 确认
        except:
            base.click(houseContractPage.addHouseContractMould['zujincofirm_loc'])  # 租金策略不符提示
            base.click(houseContractPage.addHouseContractMould['contract_audit_confirm'])  # 确认
        base.wait_element(houseContractPage.addHouseContractMould['message_loc'])  # 等待提示出现
        time.sleep(1)
        message = base.script(
            "var a = $('.panel.window.messager-window>div:nth-child(2)>div:nth-child(2)').text();return a",
            True)  # 获取提示信息
        messagehope = u'租金未审核.'
        base.diffAssert(lambda test: asserts(message).is_equal_to(messagehope),1033,
                        u'%s:租金未审核合同 %s 复审异常,期望信息"%s"实际信息"%s"' % (fileName, contractNum, messagehope, message))

test_1033()