# -*- coding:utf8 -*-

from common import sqlbase,page
from common.base import log, consoleLog, Base
from contract.achievement.page import apartmentAchievementPage
from assertpy import assert_that as asserts

@log
def test_1051():
    """业绩审核"""

    # describe：业绩审核后重新核算功能不可用
    # data：1、出单业绩状态为生效；2、出单业绩审核状态为待审核
    # result：1、业绩审核状态变为已审核；2、预估业绩排行榜中对应审核状态同步变为已审核；3、重新核算功能不可用；

    fileName = 'apartmentAchievement_1051'
    achievementSql = "select contract_num,house_code from apartment_contract_achievement where is_active='Y' and audit_status='AUDIT' AND deleted=0 and accounting_num=1 and city_code=330100 order by rand() limit 1"
    if sqlbase.get_count(achievementSql) == 0:
        consoleLog(u'%s:SQL查无数据！'% fileName, 'w')
        consoleLog(u'执行SQL：%s' % achievementSql)
        return
    info = sqlbase.serach(achievementSql)
    apartmentContractNum = info[0]
    consoleLog(u'%s:使用出租合同 %s 出单业绩做审核' % (fileName,apartmentContractNum))

    with Base() as base:
        base.open(page.apartmentAchievementPage, apartmentAchievementPage.searchContractMould['tr_contract'])
        base.click(apartmentAchievementPage.searchContractMould['reset_button_loc'])  # 重置
        base.input_text(apartmentAchievementPage.searchContractMould['contract_num_loc'], apartmentContractNum)  # 输入合同号
        base.input_text(apartmentAchievementPage.searchContractMould['search_address_loc'],info[1])  # 房源编号
        base.type_select(apartmentAchievementPage.searchContractMould['contract_type_loc'], 'NEWSIGN')  # 承租类型
        base.click(apartmentAchievementPage.searchContractMould['search_button_loc'])  # 查找
        base.staleness_of(apartmentAchievementPage.searchContractMould['tr_contract'])  # 等待第一条数据刷新
        base.dblclick(apartmentAchievementPage.searchContractMould['tr_contract'],
                      checkLoc=apartmentAchievementPage.detailAchievementMoudle['contract_num_loc'])  # 点击第一条数据等待详情页面完全显示
        base.click(apartmentAchievementPage.detailAchievementMoudle['audit_button_loc'])
        base.input_text(apartmentAchievementPage.detailAchievementMoudle['contract_audit_content'],'ok')
        base.click(apartmentAchievementPage.detailAchievementMoudle['contract_audit_confirm'])
        base.check_submit()
        achievementStatus = "select * from apartment_contract_achievement where is_active='Y' and audit_status='APPROVED' AND deleted=0 and accounting_num=1 " \
                            "and city_code=330100 and contract_num='%s'" % apartmentContractNum
        base.diffAssert(lambda test: asserts(sqlbase.waitData(achievementStatus, 1)).is_true(), 1051,
                        u'%s:出租合同 %s 业绩审核异常' % (fileName, apartmentContractNum))
        base.dblclick(apartmentAchievementPage.searchContractMould['tr_contract'],
                      checkLoc=apartmentAchievementPage.detailAchievementMoudle['contract_num_loc'])  # 点击第一条数据等待详情页面完全显示
        try:
            base.click(apartmentAchievementPage.detailAchievementMoudle['resave_loc'])
        except:
            consoleLog(u'已审核业绩无法重新核算')
        # 预发排行榜业绩
        base.open(page.achievementListPrePage, apartmentAchievementPage.searchContractMould['tr_contract'])
        base.click(apartmentAchievementPage.searchContractMould['reset_button_loc'])  # 重置
        base.staleness_of(apartmentAchievementPage.searchContractMould['tr_contract'])
        base.input_text(apartmentAchievementPage.searchContractMould['contract_num_hefa_loc'],
                        apartmentContractNum)  # 输入合同号
        base.input_text(apartmentAchievementPage.searchContractMould['search_address_loc'], info[1])  # 输入房源
        base.type_select(apartmentAchievementPage.searchContractMould['contract_type_loc'], 'NORMAL')  # 业绩类型
        base.type_select(apartmentAchievementPage.searchContractMould['rent_type_loc'], 'NEWSIGN')
        base.click(apartmentAchievementPage.searchContractMould['search_button_loc'])  # 查找
        base.staleness_of(apartmentAchievementPage.searchContractMould['tr_contract'])  # 等待第一条数据刷新
        achievementDetailCount = sqlbase.get_count(
            "select * from contract_achievement_detail acd inner join apartment_contract_achievement aca "
            "on aca.achievement_id=acd.achieve_id and aca.contract_num='%s' where acd.deleted=0" % apartmentContractNum)
        for i in range(achievementDetailCount):
            achievement_audit_status = base.script(
                "var a = $('[datagrid-row-index=\"%s\"] > [field=\"audit_status\"] > div').text();return a" % i, True)
            audit_status = u'已审核'
            base.diffAssert(lambda test: asserts(achievement_audit_status).is_equal_to(audit_status), 1051,
                            u'%s:出租合同 %s 对应预估业绩排行榜页面第 %s 条状态异常，期望值 %s 实际值 %s' % (
                            fileName, apartmentContractNum, i+1, audit_status, achievement_audit_status))

test_1051()