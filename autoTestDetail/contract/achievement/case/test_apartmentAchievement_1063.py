# -*- coding:utf8 -*-

import time
from assertpy import assert_that as asserts
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.houseContract.page import houseContractEndPage


@log
def test_1063():
    """委托公司违约生成违约业绩"""

    # describe：委托合同终止结算，结算类型为公司违约，生成违约业绩
    # data：1、委托合同已复审；2、合同状态为有效；3、委托合同下无有效的出租合同；
    # result：1、合同状态变为公司违约；2、终止结算详情中核算业绩金额字段有数值；3、生成一条违约业绩，状态为未生效；4、违约业绩金额等于核算业绩金额的值；5、违约业绩分成记录插入到预估业绩排行榜；

    fileName = 'apartmentAchievement_1063'
    contractSql = "select contract_num,entrust_end_date,date(sysdate()) from house_contract where contract_id not in (select house_contract.contract_id from apartment ,apartment_contract ,house_contract " \
                    "where  house_contract.contract_id=apartment.house_contract_id and apartment.house_id=apartment_contract.house_id and apartment_contract.real_due_date>NOW()) " \
                    "and city_code = 330100 and audit_status = 'APPROVED'and contract_status = 'EFFECTIVE' and deleted = 0 and entrust_end_date>NOW() order by rand() limit 1"
    if sqlbase.get_count(contractSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % contractSql)
        return
    info = sqlbase.serach(contractSql)
    contractNum = info[0]
    consoleLog(u'%s:取随机委托合同 %s 做公司违约终止' % (fileName, contractNum))

    with Base() as base:
        base.open(page.entrustContractPage, houseContractEndPage.addContractEndMould['tr_contract'])
        base.input_text(houseContractEndPage.searchMould['contract_num_loc'], contractNum)  # 输入合同号
        base.click(houseContractEndPage.searchMould['contract_search_button_loc'])  # 搜索
        base.staleness_of(houseContractEndPage.addContractEndMould['tr_contract'])  # 等待数据刷新
        base.context_click(houseContractEndPage.addContractEndMould['tr_contract'])  # 右击第一条数据
        base.click(houseContractEndPage.addContractEndMould['end_button_loc'], index=1)  # 终止结算
        base.wait_element(houseContractEndPage.addContractEndMould['penalty_loc'])  # 等待页面出现
        base.type_select(houseContractEndPage.typeMould['end_type'], 'CORPORATE_DEFAULT')  # 结算类型-公司违约
        endNum = 'AutoHCE' + '-' + time.strftime('%m%d%H%M')
        base.input_text(houseContractEndPage.addContractEndMould['end_num_loc'],endNum)
        base.type_date(houseContractEndPage.typeMould['end_date'], contractSql[2])  # 终止日期:当天
        # 结算扣款
        base.input_text(houseContractEndPage.addContractEndMould['return_rent_loc'], 5000)  # 返还房租
        base.input_text(houseContractEndPage.addContractEndMould['return_rent_remark_loc'], u'返还房租')  # 备注
        # 代垫费用
        base.click(houseContractEndPage.addContractEndMould['tool_bar'], index=0)  # 新增代垫
        base.type_select(houseContractEndPage.typeMould['return_type_loc'], 'LIQUIDATED')  # 退款项目：违约金赔出
        base.input_text(houseContractEndPage.addContractEndMould['return_money_loc'], 2000)  # 退款金额
        base.type_select(houseContractEndPage.typeMould['bear_type_loc'], 'COMPANY')  # 承担方-公司
        base.type_select(houseContractEndPage.typeMould['bear_name'], 'ISZTECH')  # 承担方姓名
        base.type_date(houseContractEndPage.typeMould['money_start_date'], contractSql[2])  # 费用开始时间
        base.type_date(houseContractEndPage.typeMould['money_end_date'], contractSql[2])  # 费用结束时间
        base.type_select(houseContractEndPage.typeMould['explain'], 'VACANCY')  # 情况说明-空置期  #
        base.type_select(houseContractEndPage.typeMould['dispute'], 'N')  # 是否纠纷
        base.type_date(houseContractEndPage.typeMould['receivable_date'], contractSql[2])  # 应收日期
        # 打款信息
        base.type_select(houseContractEndPage.typeMould['pay_type'], 'OWNER')  # 打款类别-业主收款
        base.input_text(houseContractEndPage.addContractEndMould['pay_name_loc'], 'AutoTest')  # 姓名
        base.type_select(houseContractEndPage.typeMould['pay_object_loc'],'BUSINESS')  # 公司
        base.input_text(houseContractEndPage.addContractEndMould['pay_bank_loc'], u'中国银行')  # 收款银行
        base.input_text(houseContractEndPage.addContractEndMould['pay_bank_no_loc'], '12345678910')  # 银行卡号
        base.upload_file(houseContractEndPage.addContractEndMould['add_end_image_loc'],'C:\Users\Public\Pictures\Sample Pictures\jsp.jpg')  # 传图
        base.wait_element(houseContractEndPage.addContractEndMould['end_image_loc'])
        base.click(houseContractEndPage.addContractEndMould['submit_loc'])  # 提交
        base.check_submit()  # 等待提交完成
        # 终止结算新增检查
        contractEndAdd = "select * from house_contract hc,house_contract_end hce where hc.contract_id=hce.contract_id and hc.contract_num='%s' and hce.deleted=0 " \
                         "and hce.audit_status='NO_AUDIT' and hce.end_type='CORPORATE_DEFAULT'" % contractNum
        base.diffAssert(lambda test: asserts(sqlbase.waitData(contractEndAdd, 1)).is_true(), 1063,
                        u'%s:委托合同 %s 终止结算新增异常，执行SQL：%s' % (fileName, contractNum, contractEndAdd))
        # 合同状态检查
        contractStatus = sqlbase.serach("select contract_status from house_contract where deleted = 0 and contract_num='%s' " % contractNum)[0]
        base.diffAssert(lambda test: asserts(contractStatus).is_equal_to('CORPORATE_DEFAULT'), 1063,
                        u'%s:委托合同 %s 终止结算后状态异常，期望值 CORPORATE_DEFAULT 实际值 %s' % (fileName, contractNum, contractStatus))
        # 检查违约核算业绩金额
        base.open(page.contractEndPage, houseContractEndPage.searchMould['contract_search_button_loc'])
        base.click(houseContractEndPage.addContractEndMould['tab_info'], index=1)
        base.input_text(houseContractEndPage.searchMould['end_contract_num_loc'], contractNum)
        base.click(houseContractEndPage.searchMould['end_search_button_loc'])  # 搜索
        base.staleness_of(houseContractEndPage.searchMould['tr_contract_end'])  # 等待数据刷新
        for i in range(5):  # 核算业绩金额生成需要一定时间，这里最多等待30秒
            base.dblclick(houseContractEndPage.searchMould['tr_contract_end'],
                          checkLoc=houseContractEndPage.addContractEndMould['check_loc'])
            time.sleep(2)
            accountingMoney = base.script("var a = $('#financial_provide_money+span>input+input').val();return a", True)
            if accountingMoney == '':
                base.click(houseContractEndPage.addContractEndMould['close_detail_loc'])
                time.sleep(8)
                continue
            else:
                break
        # 违约业绩检查
        breachAchievementSql = "select is_active,accounting_money,achieve_id from breach_achievement where breach_num='%s' and deleted=0 and breach_type='CORPORATE_DEFAULT_BREACH'" % contractNum
        if sqlbase.waitData(breachAchievementSql, 1):
            breachAchievementInfo = sqlbase.serach(breachAchievementSql)
            base.diffAssert(lambda test: asserts(breachAchievementInfo[0]).is_equal_to('N'), 1063,
                            u'%s:委托合同 %s 公司违约业绩状态异常，期望值 N 实际值 %s' % (fileName, contractNum, breachAchievementInfo[0]))
            base.diffAssert(lambda test: asserts(breachAchievementInfo[1]).is_equal_to(accountingMoney), 1063,
                            u'%s:委托合同 %s 公司违约业绩金额异常，期望值 %s 实际值 %s' % (fileName, contractNum, accountingMoney, breachAchievementInfo[1]))
        else:
            consoleLog(u'%s:委托合同 %s 公司违约生成违约业绩异常，执行SQL：%s' % (fileName, contractNum, breachAchievementSql))

        # 业绩分成明细表（预估业绩排行榜数据取值表,检查违约业绩同步更新到预估业绩排行榜）
        breahAchievementDetailSql = "select * from contract_achievement ca inner join contract_achievement_detail cad on ca.achieve_id=cad.achieve_id where ca.contract_category='CORPORATE_DEFAULT_BREACH' " \
                                    "and ca.deleted=0 and ca.achieve_id='%s'" % breachAchievementInfo[2]
        achievementDetialConunt = sqlbase.get_count(breahAchievementDetailSql)
        base.diffAssert(lambda test: asserts(achievementDetialConunt).is_not_equal_to(0), 1063,
                        u'%s:委托合同 %s 公司违约违约业绩分成明细异常' % (fileName, contractNum))

test_1063()