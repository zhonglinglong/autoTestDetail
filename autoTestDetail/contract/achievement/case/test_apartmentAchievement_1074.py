# -*- coding:utf8 -*-

import time
from assertpy import assert_that as asserts
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from common.interface import audit, auditType, auditStatus
from contract.achievement.page import apartmentAchievementPage
from contract.houseContract.page import houseContractEndPage


@log
def test_1074():
    """修改委托终止赔入违约金"""

    # describe：修改委托终止结算赔入违约金金额+100，违约业绩同步+100
    # data：1、委托终止结算未复审；2、委托终止类型为业主违约；3、业绩状态未审核；
    # result：1、违约业绩比之前多100；2、分成人业绩同步变化；3、预估业绩排行榜同步更新；

    fileName = 'apartmentAchievement_1074'
    contractSql = "select contract_num,entrust_end_date,date(sysdate()) from house_contract where contract_id not in (select house_contract.contract_id from apartment ,apartment_contract ,house_contract " \
                    "where  house_contract.contract_id=apartment.house_contract_id and apartment.house_id=apartment_contract.house_id and apartment_contract.real_due_date>NOW()) " \
                    "and city_code = 330100 and audit_status = 'APPROVED'and contract_status = 'EFFECTIVE' and deleted = 0 and entrust_end_date>NOW() order by rand() limit 1"
    if sqlbase.get_count(contractSql) == 0:
        consoleLog(u'%s：SQL查无数据！' % fileName, 'w')
        consoleLog(u'执行SQL：%s' % contractSql)
        return
    info = sqlbase.serach(contractSql)
    contractNum = info[0]
    consoleLog(u'%s:取随机委托合同 %s 做业主违约终止' % (fileName, contractNum))

    with Base() as base:
        base.open(page.entrustContractPage, houseContractEndPage.addContractEndMould['tr_contract'])
        base.input_text(houseContractEndPage.searchMould['contract_num_loc'], contractNum)  # 输入合同号
        base.click(houseContractEndPage.searchMould['contract_search_button_loc'])  # 搜索
        base.staleness_of(houseContractEndPage.addContractEndMould['tr_contract'])  # 等待数据刷新
        base.context_click(houseContractEndPage.addContractEndMould['tr_contract'])  # 右击第一条数据
        base.click(houseContractEndPage.addContractEndMould['end_button_loc'], index=1)  # 终止结算
        base.wait_element(houseContractEndPage.addContractEndMould['penalty_loc'])  # 等待页面出现
        base.type_select(houseContractEndPage.typeMould['end_type'], 'OWNER_DEFAULT')  # 结算类型-业主违约
        endNum = 'AutoHCE' + '-' + time.strftime('%m%d%H%M')
        base.input_text(houseContractEndPage.addContractEndMould['end_num_loc'],endNum)
        base.type_date(houseContractEndPage.typeMould['end_date'], contractSql[2])  # 终止日期:当天
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
        base.upload_file(houseContractEndPage.addContractEndMould['add_end_image_loc'],
                         'C:\Users\Public\Pictures\Sample Pictures\jsp.jpg')  # 传图
        base.wait_element(houseContractEndPage.addContractEndMould['end_image_loc'])
        base.click(houseContractEndPage.addContractEndMould['submit_loc'])  # 提交
        base.check_submit()  # 等待提交完成
        # 终止结算新增检查
        contractEndAdd = "select hce.end_id from house_contract hc,house_contract_end hce where hc.contract_id=hce.contract_id and hc.contract_num='%s' and hce.deleted=0 " \
                         "and hce.audit_status='NO_AUDIT' and hce.end_type='OWNER_DEFAULT'" % contractNum
        base.diffAssert(lambda test: asserts(sqlbase.waitData(contractEndAdd, 1)).is_true(), 1074,
                        u'%s:委托合同 %s 终止结算新增异常，执行SQL：%s' % (fileName, contractNum, contractEndAdd))
        # 违约业绩检查
        breachAchievementSql = "select is_active,accounting_money,achieve_id from breach_achievement where breach_num='%s' and deleted=0 and breach_type='HOUSE_OWNER_DEFAULT_BREACH'" % contractNum
        base.diffAssert(lambda test: asserts(sqlbase.waitData(breachAchievementSql, 1)).is_true(), 1074,
                        u'%s:委托合同 %s 业主违约生成违约业绩异常，执行SQL：%s' % (fileName, contractNum, breachAchievementSql))
        breachAchievementInfo = sqlbase.serach(breachAchievementSql)
        # 终止结算初审后修改违约核算金额
        houseContractEndId = sqlbase.serach(contractEndAdd)[0]
        audit(houseContractEndId, auditType.houseContractEnd, auditStatus.chuShen)
        base.open(page.contractEndPage, houseContractEndPage.searchMould['contract_search_button_loc'])
        base.click(houseContractEndPage.addContractEndMould['tab_info'], index=1)
        base.input_text(houseContractEndPage.searchMould['end_contract_num_loc'], contractNum)
        base.click(houseContractEndPage.searchMould['end_search_button_loc'])  # 搜索
        base.staleness_of(houseContractEndPage.searchMould['tr_contract_end'])  # 等待数据刷新
        base.dblclick(houseContractEndPage.searchMould['tr_contract_end'],
                      checkLoc=houseContractEndPage.addContractEndMould['check_loc'])
        time.sleep(2)
        financial_money_new=str(float(breachAchievementInfo[1])+100)
        # base.script("$('#financial_provide_money+span>input').val('%s')" % financial_money_new)
        base.input_text(houseContractEndPage.addContractEndMould['financial_money_loc'], financial_money_new)
        base.type_select(houseContractEndPage.typeMould['pay_object_loc'], 'BUSINESS')  # 公司
        base.input_text(houseContractEndPage.addContractEndMould['pay_bank_loc'], u'中国银行')  # 收款银行
        base.input_text(houseContractEndPage.addContractEndMould['pay_bank_no_loc'], '12345678910')  # 银行卡号
        base.click(houseContractEndPage.addContractEndMould['save_loc'])  # 保存
        base.check_submit()
        # 获取修改后业绩数据
        time.sleep(10)
        breachAchievementSql = "select is_active,accounting_money,achieve_id from breach_achievement where breach_num='%s' and deleted=0 and breach_type='HOUSE_OWNER_DEFAULT_BREACH'" % contractNum
        breachAchievementInfo = sqlbase.serach(breachAchievementSql)
        base.diffAssert(lambda test: asserts(breachAchievementInfo[1]).is_equal_to(financial_money_new), 1074,
                        u'%s:委托合同 %s 违约业绩金额异常，期望值 %s 实际值 %s' % (fileName, contractNum, financial_money_new, breachAchievementInfo[1]))
        # base.diffAssert(lambda test: asserts(personAchievementNew).is_not_equal_to(personAchievementOld), 1074,
        #                 u'%s:委托合同 %s 业主违约修改终止合同核算业绩金额后，违约业绩分成明细异常，期望值不为 %s 实际值 %s' % (fileName, contractNum, personAchievementOld, personAchievementNew))

        # 业绩分成明细表（预估业绩排行榜数据取值表,检查违约业绩同步更新到预估业绩排行榜）
        breahAchievementDetailSql = "select ca.receivable from contract_achievement ca inner join contract_achievement_detail cad on ca.achieve_id=cad.achieve_id inner join breach_achievement ba " \
                                    "on ba.achieve_id=ca.achieve_id and ba.breach_type='HOUSE_OWNER_DEFAULT_BREACH' and ba.deleted=0 and ba.breach_num='%s' " \
                                    "where ca.contract_category='HOUSE_OWNER_DEFAULT_BREACH' and ca.deleted=0 " % contractNum
        prebreachAchievement = sqlbase.serach(breahAchievementDetailSql)[0]
        base.diffAssert(lambda test: asserts(prebreachAchievement).is_equal_to(financial_money_new), 1074,
                        u'%s:委托合同 %s 业主违约修改终止合同核算业绩金额后,业绩分成明细业绩金额异常，实际值 %s 期望值 %s' % (fileName, contractNum, prebreachAchievement, financial_money_new))

test_1074()