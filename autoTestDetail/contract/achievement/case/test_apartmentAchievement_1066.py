# -*- coding:utf8 -*-
import time

from assertpy import assert_that as asserts
from selenium.webdriver.common.keys import Keys
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from common.interface import audit, auditType, auditStatus
from contract.achievement.page import apartmentAchievementPage
from contract.apartmentContract.page import apartmentContractEndPage
from contract.apartmentContract.page import apartmentContractPage
from contract.houseContract.page import houseContractEndPage


@log
def test_1066():
    """委托违约业绩由未生效变成生效"""

    # describe：委托合同终止结算，结算类型为业主违约，生成违约业绩
    # data：1、业绩违约类别为业主违约或者公司违约；2、业绩状态为未生效且未审核；3、委托合同已复审；4、委托终止结算未复审；
    # result：1、业绩状态变为生效；2、业绩产生核发月份；3、业绩状态和核发月份同步更新到预估业绩排行榜；4、生效业绩加入核发业绩排行榜；

    fileName = 'apartmentAchievement_1066'
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
        # 添加终止结算
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
        # 终止结算新增检查
        contractEndAdd = "select hce.end_id from house_contract hc,house_contract_end hce where hc.contract_id=hce.contract_id and hc.contract_num='%s' and hce.deleted=0 " \
                         "and hce.audit_status='NO_AUDIT' and hce.end_type='OWNER_DEFAULT'" % contractNum
        base.diffAssert(lambda test: asserts(sqlbase.waitData(contractEndAdd, 1)).is_true(), 1066,
                        u'%s:委托合同 %s 终止结算新增异常，执行SQL：%s' % (fileName, contractNum, contractEndAdd))
        breachAchievementSql = "select is_active,accounting_money,achieve_id from breach_achievement where breach_num='%s' and deleted=0 and breach_type='HOUSE_OWNER_DEFAULT_BREACH'" \
                               "and is_active='N'" % contractNum
        base.diffAssert(lambda test: asserts(sqlbase.waitData(breachAchievementSql,1)).is_true(), 1066,
                        u'%s:委托合同 %s 业主违约业绩生成异常' % (fileName, contractNum))
        # 复审终止结算
        houseContractEndId = sqlbase.serach(contractEndAdd)[0]
        audit(houseContractEndId, auditType.houseContractEnd, auditStatus.chuShen, auditStatus.fuShen)
        # 违约业绩生效检查
        breachAchievementActiveSql = "select accounting_time,achieve_id from breach_achievement where breach_num='%s' and deleted=0 and breach_type='HOUSE_OWNER_DEFAULT_BREACH' " \
                                     "and is_active='Y'" % contractNum
        if sqlbase.waitData(breachAchievementActiveSql,1):
            breachAchievementInfo = sqlbase.serach(breachAchievementActiveSql)
            base.diffAssert(lambda test: asserts(breachAchievementInfo[0]).is_not_empty(), 1066,
                            u'%s:委托合同 %s 业主违约违约业绩生效核发月份生成异常' % (fileName, contractNum))  #  核发业绩排行榜取值处
        else:
            consoleLog(u'%s:委托合同 %s 业主违约违约业绩生效异常' % (fileName, contractNum),'e')

        # 业绩分成明细表（预估业绩排行榜数据取值表,检查违约业绩核发月份同步更新到预估业绩排行榜）
        breahAchievementDetailSql = "select * from contract_achievement ca inner join contract_achievement_detail cad on ca.achieve_id=cad.achieve_id where ca.contract_category='HOUSE_OWNER_DEFAULT_BREACH' " \
                                    "and ca.deleted=0 and ca.achieve_id='%s'and ca.achievement_month='%s'" % (breachAchievementInfo[1], breachAchievementInfo[0])
        achievementDetialConunt = sqlbase.get_count(breahAchievementDetailSql)
        base.diffAssert(lambda test: asserts(achievementDetialConunt).is_not_equal_to(0), 1066,
                        u'%s:委托合同 %s 业主违约违约业绩分成明细异常' % (fileName, contractNum))
        # 核发业绩排行榜检查
        base.open(page.achievementListPage, apartmentAchievementPage.searchContractMould['tr_contract'])
        base.click(apartmentAchievementPage.searchContractMould['reset_button_loc'])  # 重置
        base.staleness_of(apartmentAchievementPage.searchContractMould['tr_contract'])
        base.input_text(apartmentAchievementPage.searchContractMould['contract_num_hefa_loc'], contractNum)  # 输入合同号
        base.type_select(apartmentAchievementPage.searchContractMould['category_loc'], 'HOUSE_OWNER_DEFAULT_BREACH')  # 分类：业主违约
        base.click(apartmentAchievementPage.searchContractMould['search_button_loc'])  # 查找
        base.staleness_of(apartmentAchievementPage.searchContractMould['tr_contract'])  # 等待第一条数据刷新
        for i in range(achievementDetialConunt):
            achievement_month = base.script(
                "var a = $('[datagrid-row-index=\"%s\"] > [field=\"achievement_month\"] > div').text();return a" % i,True)
            base.diffAssert(lambda test: asserts(achievement_month).is_equal_to(breachAchievementInfo[0]), 1042,
                            u'%s:委托合同 %s 对应业主违约业绩有核发月份的同步到核发业绩排行榜异常' % (fileName, contractNum))

test_1066()