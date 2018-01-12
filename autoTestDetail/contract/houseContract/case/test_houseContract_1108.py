# -*- coding:utf8 -*-

from assertpy import assert_that as asserts
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from common.interface import auditType, audit, auditStatus
from contract.houseContract.page import houseContractEndPage


@log
def test_1108():
    """终止结算修改"""

    # describe：未复审的终止结算可以修改内容，复审后不可修改
    # data：1.有效未审核委托合同2.名下无有效出租合同
    # result：1.初审后修改成功2.复审后修改失败

    fileName = 'apartmentContract_1108'
    contractSql = "select contract_num,entrust_end_date,date(sysdate()) from house_contract where contract_id not in (select house_contract.contract_id from apartment ,apartment_contract ,house_contract " \
                  "where  house_contract.contract_id=apartment.house_contract_id and apartment.house_id=apartment_contract.house_id and apartment_contract.real_due_date>NOW()) " \
                  "and city_code = 330100 and audit_status = 'APPROVED'and contract_status = 'EFFECTIVE' and deleted = 0 and entrust_end_date>NOW() order by rand() limit 1"
    if sqlbase.get_count(contractSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % contractSql)
        return
    info = sqlbase.serach(contractSql)
    contractNum = info[0]
    consoleLog(u'%s:取随机委托合同 %s 做终止结算' % (fileName, contractNum))

    with Base() as base:
        base.open(page.entrustContractPage, houseContractEndPage.addContractEndMould['tr_contract'])
        base.input_text(houseContractEndPage.searchMould['contract_num_loc'], contractNum)  # 输入合同号
        base.click(houseContractEndPage.searchMould['contract_search_button_loc'])  # 搜索
        base.staleness_of(houseContractEndPage.addContractEndMould['tr_contract'])  # 等待数据刷新
        base.context_click(houseContractEndPage.addContractEndMould['tr_contract'])  # 右击第一条数据
        base.click(houseContractEndPage.addContractEndMould['end_button_loc'], index=1)  # 终止结算
        base.wait_element(houseContractEndPage.addContractEndMould['penalty_loc'])  # 等待页面出现
        base.type_select(houseContractEndPage.typeMould['end_type'], 'RETREATING')  # 结算类型-正退
        base.type_date(houseContractEndPage.typeMould['end_date'], contractSql[1])  # 终止日期:当天
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
        base.click(houseContractEndPage.addContractEndMould['submit_loc'])  # 提交
        base.check_submit()  # 等待提交完成
        # 终止结算新增检查
        contractEndAdd = "select hce.end_id from house_contract hc,house_contract_end hce where hc.contract_id=hce.contract_id and hc.contract_num='%s' and hce.deleted=0 " \
                         "and hce.audit_status='NO_AUDIT' and hce.end_type='RETREATING'" % contractNum
        base.diffAssert(lambda test: asserts(sqlbase.waitData(contractEndAdd, 1)).is_true(), 1108,
                        u'%s:委托合同 %s 正退终止结算新增异常，执行SQL：%s' % (fileName, contractNum, contractEndAdd))
        end_id=sqlbase.serach(contractEndAdd)[0]
        audit(end_id, auditType.houseContractEnd, auditStatus.chuShen)  # 初审
        #修改违约金陪入
        base.open(page.contractEndPage, houseContractEndPage.searchMould['contract_search_button_loc'])
        base.click(houseContractEndPage.addContractEndMould['tab_info'], index=1)
        base.input_text(houseContractEndPage.searchMould['end_contract_num_loc'], contractNum)
        base.click(houseContractEndPage.searchMould['end_search_button_loc'])  # 搜索
        base.staleness_of(houseContractEndPage.searchMould['tr_contract_end'])  # 等待数据刷新
        base.dblclick(houseContractEndPage.searchMould['tr_contract_end'],
                      checkLoc=houseContractEndPage.addContractEndMould['check_loc'])
        base.input_text(houseContractEndPage.addContractEndMould['penalty_loc'], 3000)  # 违约金陪入
        base.type_select(houseContractEndPage.typeMould['pay_object_loc'], 'BUSINESS')  # 公司
        base.input_text(houseContractEndPage.addContractEndMould['pay_bank_loc'], u'中国银行')  # 收款银行
        base.input_text(houseContractEndPage.addContractEndMould['pay_bank_no_loc'], '12345678910')  # 银行卡号
        base.click(houseContractEndPage.addContractEndMould['save_loc'])  # 保存
        base.check_submit()
        audit(end_id, auditType.houseContractEnd, auditStatus.fuShen)  # 复审
        base.open(page.contractEndPage, houseContractEndPage.searchMould['contract_search_button_loc'])
        base.click(houseContractEndPage.addContractEndMould['tab_info'], index=1)
        base.input_text(houseContractEndPage.searchMould['end_contract_num_loc'], contractNum)
        base.click(houseContractEndPage.searchMould['end_search_button_loc'])  # 搜索
        base.staleness_of(houseContractEndPage.searchMould['tr_contract_end'])  # 等待数据刷新
        base.dblclick(houseContractEndPage.searchMould['tr_contract_end'],
                      checkLoc=houseContractEndPage.addContractEndMould['check_loc'])
        try:
            base.input_text(houseContractEndPage.addContractEndMould['penalty_loc'], 4000)  # 违约金陪入
            base.click(houseContractEndPage.addContractEndMould['save_loc'])  # 保存
            base.check_submit()
        except:
            consoleLog(u'已复审的终止结算不能修改！')

test_1108()