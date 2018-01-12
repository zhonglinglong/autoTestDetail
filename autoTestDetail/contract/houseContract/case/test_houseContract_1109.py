# -*- coding:utf8 -*-

import time
from assertpy import assert_that as asserts
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.houseContract.page import houseContractEndPage

@log
def test_1109():
    """委托终止结算审核流程"""

    # describe：委托终止结算审核流程
    # data：1、委托终止结算待审核
    # result：1、驳回，初审，复审，反审成功

    fileName = 'apartmentContract_1109'
    contractSql = "select contract_num,entrust_end_date,date(sysdate()) from house_contract where contract_id not in (select house_contract.contract_id from apartment ,apartment_contract ,house_contract " \
                  "where  house_contract.contract_id=apartment.house_contract_id and apartment.house_id=apartment_contract.house_id and apartment_contract.real_due_date>NOW()) " \
                  "and city_code = 330100 and audit_status = 'APPROVED'and contract_status = 'EFFECTIVE' and deleted = 0 and entrust_end_date>NOW() order by rand() limit 1"
    if sqlbase.get_count(contractSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % contractSql)
        return
    info = sqlbase.serach(contractSql)
    contractNum = info[0]
    consoleLog(u'%s:取合同 %s 终止结算做审核' % (fileName, contractNum))

    with Base() as base:
        base.open(page.entrustContractPage, houseContractEndPage.addContractEndMould['tr_contract'])
        base.input_text(houseContractEndPage.searchMould['contract_num_loc'], contractNum)  # 输入合同号
        base.click(houseContractEndPage.searchMould['contract_search_button_loc'])  # 搜索
        base.staleness_of(houseContractEndPage.addContractEndMould['tr_contract'])  # 等待数据刷新
        base.context_click(houseContractEndPage.addContractEndMould['tr_contract'])  # 右击第一条数据
        base.click(houseContractEndPage.addContractEndMould['end_button_loc'], index=1)  # 终止结算
        base.wait_element(houseContractEndPage.addContractEndMould['penalty_loc'])  # 等待页面出现
        base.type_select(houseContractEndPage.typeMould['end_type'], 'OWNER_DEFAULT')  # 结算类型-业主违约
        base.type_date(houseContractEndPage.typeMould['end_date'], contractSql[1])  # 终止日期:当天
        endNum = 'AutoHCE' + '-' + time.strftime('%m%d%H%M')
        base.input_text(houseContractEndPage.addContractEndMould['end_num_loc'],endNum)
        # 结算扣款
        base.input_text(houseContractEndPage.addContractEndMould['penalty_loc'], 2000)  # 违约金陪入
        base.input_text(houseContractEndPage.addContractEndMould['penalty_remark_loc'], u'违约金陪入')  # 备注
        base.input_text(houseContractEndPage.addContractEndMould['return_rent_loc'], 5000)  # 返还房租
        base.input_text(houseContractEndPage.addContractEndMould['return_rent_remark_loc'], u'返还房租')  # 备注
        base.type_date(houseContractEndPage.typeMould['receivable_date'], contractSql[2])  # 应收日期
        # 打款信息
        base.type_select(houseContractEndPage.typeMould['pay_type'], 'OWNER')  # 打款类别-业主收款
        base.input_text(houseContractEndPage.addContractEndMould['pay_name_loc'], 'AutoTest')  # 姓名
        base.type_select(houseContractEndPage.typeMould['pay_object_loc'], 'BUSINESS')  # 公司
        base.input_text(houseContractEndPage.addContractEndMould['pay_bank_loc'], u'中国银行')  # 收款银行
        base.input_text(houseContractEndPage.addContractEndMould['pay_bank_no_loc'], '12345678910')  # 银行卡号
        base.upload_file(houseContractEndPage.addContractEndMould['add_end_image_loc'],'d:\jsp.png')  # 传图
        base.wait_element(houseContractEndPage.addContractEndMould['end_image_loc'])
        base.click(houseContractEndPage.addContractEndMould['submit_loc'])  # 提交
        base.check_submit()  # 等待提交完成
        # 终止结算新增检查
        contractEndAdd = "select hce.end_id from house_contract hc,house_contract_end hce where hc.contract_id=hce.contract_id and hc.contract_num='%s' and hce.deleted=0 " \
                         "and hce.audit_status='NO_AUDIT' and hce.end_type='OWNER_DEFAULT'" % contractNum
        base.diffAssert(lambda test: asserts(sqlbase.waitData(contractEndAdd, 1)).is_true(), 1109,
                        u'%s:委托合同 %s 正退终止结算新增异常，执行SQL：%s' % (fileName, contractNum, contractEndAdd))
        base.open(page.contractEndPage, houseContractEndPage.searchMould['contract_search_button_loc'])
        base.click(houseContractEndPage.addContractEndMould['tab_info'], index=1)
        base.input_text(houseContractEndPage.searchMould['end_contract_num_loc'], contractNum)
        base.click(houseContractEndPage.searchMould['end_search_button_loc'])
        base.staleness_of(houseContractEndPage.searchMould['tr_contract_end'])
        for i in range(5):#核算业绩金额生成需要一定时间，这里最多等待50秒
            base.dblclick(houseContractEndPage.searchMould['tr_contract_end'],
                          checkLoc=houseContractEndPage.addContractEndMould['check_loc'])
            time.sleep(2)
            accountingMoney = base.script("var a = $('#financial_provide_money+span>input+input').val();return a",True)
            if accountingMoney == '':
                base.click(houseContractEndPage.addContractEndMould['close_detail_loc'])
                time.sleep(8)
                continue
            else:
                break
        # 驳回
        # base.dblclick(houseContractEndPage.searchMould['tr_contract_end'],
        #               checkLoc=houseContractEndPage.addContractEndMould['check_loc'])
        base.input_text(houseContractEndPage.addContractEndMould['remark_loc'],u'驳回')
        base.type_select(houseContractEndPage.typeMould['pay_object_loc'], 'BUSINESS')  # 公司
        base.input_text(houseContractEndPage.addContractEndMould['pay_bank_loc'], u'中国银行')  # 收款银行
        base.input_text(houseContractEndPage.addContractEndMould['pay_bank_no_loc'], '12345678910')  # 银行卡号
        base.click(houseContractEndPage.addContractEndMould['bohui_loc'])
        base.input_text(houseContractEndPage.addContractEndMould['contract_audit_content'], u'自动化测试审核数据')
        base.click(houseContractEndPage.addContractEndMould['contract_audit_confirm'])
        base.check_submit()
        base.dblclick(houseContractEndPage.searchMould['tr_contract_end'],
                      checkLoc=houseContractEndPage.addContractEndMould['check_loc'])
        # 初审
        base.click(houseContractEndPage.addContractEndMould['chushen_loc'])
        base.click(houseContractEndPage.addContractEndMould['contract_audit_confirm'])
        base.check_submit()
        base.dblclick(houseContractEndPage.searchMould['tr_contract_end'],
                      checkLoc=houseContractEndPage.addContractEndMould['check_loc'])
        # 复审
        base.click(houseContractEndPage.addContractEndMould['fushen_loc'])
        base.click(houseContractEndPage.addContractEndMould['contract_audit_confirm'])
        base.check_submit()
        base.dblclick(houseContractEndPage.searchMould['tr_contract_end'],
                      checkLoc=houseContractEndPage.addContractEndMould['check_loc'])
        # 反审
        base.click(houseContractEndPage.addContractEndMould['fanshen_loc'])
        base.input_text(houseContractEndPage.addContractEndMould['contract_audit_content'], u'自动化测试审核数据')
        base.click(houseContractEndPage.addContractEndMould['contract_audit_confirm'])
        base.check_submit()
        # 删除终止结算
        base.click(houseContractEndPage.addContractEndMould['delete_button'])
        base.click(houseContractEndPage.addContractEndMould['delete_button_confirm'])
        base.check_submit()
        houseContractEndDelSql = "select * from house_contract_end where end_contract_num='%s' and deleted=0" % endNum
        base.diffAssert(lambda test: asserts(sqlbase.get_count(houseContractEndDelSql)).is_not_equal_to(1), 1109,
                        u'%s:委托合同 %s 终止结算删除异常，执行SQL：%s' % (fileName, contractNum, houseContractEndDelSql))
test_1109()