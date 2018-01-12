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
def test_1085():
    """委托违约业绩失效"""

    # describe：违约业绩生效审核后删除终止结算，业绩变失效
    # data：1、业绩已审核；2、终止结算未复审；
    # result：1、业绩变成已失效；2、状态同步到预估业绩排行榜；

    fileName = 'apartmentAchievement_1085'
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
        base.type_select(houseContractEndPage.typeMould['pay_object_loc'],'BUSINESS')  # 公司
        base.input_text(houseContractEndPage.addContractEndMould['pay_bank_loc'], u'中国银行')  # 收款银行
        base.input_text(houseContractEndPage.addContractEndMould['pay_bank_no_loc'], '12345678910')  # 银行卡号
        base.upload_file(houseContractEndPage.addContractEndMould['add_end_image_loc'],
                         'C:\Users\Public\Pictures\Sample Pictures\jsp.jpg')  # 传图
        base.wait_element(houseContractEndPage.addContractEndMould['end_image_loc'])
        base.click(houseContractEndPage.addContractEndMould['submit_loc'])  # 提交
        base.check_submit()  # 等待提交完成
        # 终止结算复审
        contractEndAdd = "select hce.end_id from house_contract hc,house_contract_end hce where hc.contract_id=hce.contract_id and hc.contract_num='%s' and hce.deleted=0 " \
                         "and hce.audit_status='NO_AUDIT' and hce.end_type='OWNER_DEFAULT'" % contractNum
        base.diffAssert(lambda test: asserts(sqlbase.waitData(contractEndAdd, 1)).is_true(), 1085,
                        u'%s:委托合同 %s 终止结算新增异常，执行SQL：%s' % (fileName, contractNum, contractEndAdd))
        houseContractEndId = sqlbase.serach(contractEndAdd)[0]
        audit(houseContractEndId, auditType.houseContractEnd, auditStatus.chuShen, auditStatus.fuShen)
        # 违约业绩生效
        breachAchievementSql = "select is_active,accounting_money,achieve_id from breach_achievement where breach_num='%s' and deleted=0 and breach_type='HOUSE_OWNER_DEFAULT_BREACH' " \
                                "and is_active='Y'" % contractNum
        base.diffAssert(lambda test: asserts(sqlbase.waitData(breachAchievementSql, 1)).is_true(), 1085,
                        u'%s:委托合同 %s 业主违约生效异常，执行SQL：%s' % (fileName, contractNum, breachAchievementSql))
        #业绩审核
        base.open(page.defaultAchievementPage, apartmentAchievementPage.searchContractMould['tr_contract'])
        base.click(apartmentAchievementPage.searchContractMould['reset_button_loc'])  # 重置
        time.sleep(10)
        base.input_text(apartmentAchievementPage.searchContractMould['breach_num_loc'], contractNum)  # 输入合同号
        base.click(apartmentAchievementPage.searchContractMould['search_button_loc'])  # 查找
        base.staleness_of(apartmentAchievementPage.searchContractMould['tr_contract'])  # 等待第一条数据刷新
        base.dblclick(apartmentAchievementPage.searchContractMould['tr_contract'],
                      checkLoc=apartmentAchievementPage.detailAchievementMoudle['breach_num_loc'])  # 点击第一条数据等待详情页面完全显示
        base.click(apartmentAchievementPage.detailAchievementMoudle['audit_button_loc'])
        base.input_text(apartmentAchievementPage.detailAchievementMoudle['contract_audit_content'], 'ok')
        base.click(apartmentAchievementPage.detailAchievementMoudle['contract_audit_confirm'])
        base.check_submit()
        # 终止结算反审后删除
        audit(houseContractEndId, auditType.houseContractEnd, auditStatus.fanShen)
        base.open(page.contractEndPage, houseContractEndPage.searchMould['contract_search_button_loc'])
        base.click(houseContractEndPage.addContractEndMould['tab_info'], index=1)
        base.input_text(houseContractEndPage.searchMould['end_contract_num_loc'], contractNum)
        base.click(houseContractEndPage.searchMould['end_search_button_loc'])  # 搜索
        base.staleness_of(houseContractEndPage.searchMould['tr_contract_end'])  # 等待数据刷新
        base.click(houseContractEndPage.addContractEndMould['delete_button'])
        base.click(houseContractEndPage.addContractEndMould['delete_button_confirm'])
        base.check_submit()
        # 删除委托后业绩状态
        breachAchievementNewSql = "select is_active,accounting_money,achieve_id from breach_achievement where breach_num='%s' and deleted=0 and breach_type='HOUSE_OWNER_DEFAULT_BREACH' " \
                                  "and is_active='INVALID'" % contractNum
        base.diffAssert(lambda test: asserts(sqlbase.waitData(breachAchievementNewSql,1)).is_true(), 1085,
                        u'%s:委托合同 %s 违约业绩生效审核后删除委托合同，业绩异常，执行SQL：%s' % (fileName, contractNum, breachAchievementNewSql))

        # 预估排行榜业绩
        breahAchievementDetailSql = "select ca.receivable,ca.is_active from contract_achievement ca inner join contract_achievement_detail cad on ca.achieve_id=cad.achieve_id inner " \
                                    "join breach_achievement ba on ba.achieve_id=ca.achieve_id and ba.breach_type='HOUSE_OWNER_DEFAULT_BREACH' and ba.deleted=0 and ba.breach_num='%s' " \
                                    "where ca.contract_category='HOUSE_OWNER_DEFAULT_BREACH' and ca.deleted=0" % contractNum
        breachAchievementStatus = sqlbase.serach(breahAchievementDetailSql)[1]
        base.diffAssert(lambda test: asserts(breachAchievementStatus).is_equal_to('INVALID'), 1085,
                        u'%s:委托合同 %s 违约业绩生效审核后删除委托合同,业绩分成明细业绩状态异常，期望值 INVALID 实际值 %s' % (fileName, contractNum, breachAchievementStatus))

test_1085()