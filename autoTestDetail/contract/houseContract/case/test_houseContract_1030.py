# -*- coding:utf8 -*-

import time
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.houseContract.page import houseContractPage
from assertpy import assert_that as asserts

@log
def test_1030():
    """租金明细未审核无法初审"""

    # describe：租金明细未审核无法初审
    # data：1、合同状态为有效或者已续；2、合同审核状态为待审核；3、租金明细页面新增一条租金明细并保存；
    # result：1、审核失败，提示租金未审核

    fileName = 'houseContract_1030'
    contractSql = "select hc.contract_num,sysdate(),h.house_code from house h INNER JOIN house_contract hc on hc.house_id=h.house_id where hc.audit_status='AUDIT' and hc.deleted=0 " \
                  "and hc.is_active='Y' and hc.city_code=330100 and sign_date>'2017-01-01' and EXISTS (select * from house_contract_payable hcp where hcp.contract_id=hc.contract_id " \
                  "and hcp.end_status='NOTPAY') order by rand() limit 1"
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
        # 审核租金
        base.click(houseContractPage.addHouseContractMould['recreate_button'])  # 重新生成租金明细
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
        time.sleep(3)
        base.click(houseContractPage.addHouseContractMould['rent_audit_confirm'])  # 确认
        base.check_submit()
        # 新增租金明细
        base.click(houseContractPage.addHouseContractMould['add_detail_button'])  # 新增租金明细
        time.sleep(1)
        base.script("$('.erp-table>tbody>tr:last input[type=\"checkbox\"]').click()")  # 选择记录
        base.type_select(houseContractPage.addHouseContractMould['money_type_loc'], 'PARKING')  # 款项类型
        base.type_date(houseContractPage.addHouseContractMould['rent_start_date_loc'], contractInfo[1])  # 开始时间
        base.type_date(houseContractPage.addHouseContractMould['rent_end_date_loc'], contractInfo[1])  # 结束时间
        base.type_date(houseContractPage.addHouseContractMould['payable_date_loc'], contractInfo[1])  # 应付时间
        base.scrollTo(houseContractPage.addHouseContractMould['payable_amount_loc'])
        base.input_text(houseContractPage.addHouseContractMould['payable_amount_loc'], 100)  # 应付金额
        base.click(houseContractPage.addHouseContractMould['rent_save_button'])  # 保存
        base.check_submit()
        # 初审
        base.click(houseContractPage.addHouseContractMould['tab_info_loc'], index=3)  # 最后一页
        time.sleep(3)
        base.script('$("button[status=\'PASS\']")[2].click()')  # 初审
        base.click(houseContractPage.addHouseContractMould['contract_audit_confirm'])  # 确认
        base.wait_element(houseContractPage.addHouseContractMould['message_loc'])  # 等待提示出现
        message = base.script(
            "var a = $('.panel.window.messager-window>div:nth-child(2)>div:nth-child(2)').text();return a",
            True)  # 获取提示信息
        messagehope = u'租金未审核.'
        base.diffAssert(lambda test: asserts(message).contains(messagehope),1030,
                        u'%s:租金未审核合同 %s 初审异常,期望信息"%s"实际信息"%s"' % (fileName, contractNum, messagehope, message))

test_1030()