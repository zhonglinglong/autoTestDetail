# -*- coding:utf8 -*-

from common import sqlbase,page
from common.base import log, consoleLog, Base
from contract.achievement.page import apartmentAchievementPage
from assertpy import assert_that as asserts

@log
def test_1137():
    """扣回业绩反审"""

    # describe：扣回业绩反审后同步到预估业绩排行榜，重新核算不可用
    # data：1、扣回业绩状态为生效；2、扣回业绩审核状态为已审核
    # result：1、业绩审核状态变为待审核；2、预估业绩排行榜中对应审核状态同步变为待审核；3、重新核算功能不可用；

    fileName = 'apartmentAchievement_1137'
    achievementSql = "select ba.contract_num,ba.apartment_code,ba.achieve_id,concat(ba.contract_end_type,'_BACK') from back_achievement ba inner join apartment a on a.apartment_code=ba.apartment_code " \
                     "and a.city_code=330100 where ba.is_active='Y' and ba.audit_status='APPROVED' AND ba.deleted=0 and ba.contract_end_type<>'RETREATING' and ba.create_time >'2017-01-01' order by rand() limit 1"
    if sqlbase.get_count(achievementSql) == 0:
        consoleLog(u'%s:SQL查无数据！'% fileName, 'w')
        consoleLog(u'执行SQL：%s' % achievementSql)
        return
    info = sqlbase.serach(achievementSql)
    contractNum = info[0]
    consoleLog(u'%s:使用合同 %s 扣回业绩做审核' % (fileName,contractNum))

    with Base() as base:
        base.open(page.backAchievementPage, apartmentAchievementPage.searchContractMould['tr_contract'])
        base.click(apartmentAchievementPage.searchContractMould['reset_button_loc'])  # 重置
        base.input_text(apartmentAchievementPage.searchContractMould['contract_num_loc'], contractNum)  # 输入合同号
        base.input_text(apartmentAchievementPage.searchContractMould['search_address_loc'], info[1])  # 房源编号
        base.click(apartmentAchievementPage.searchContractMould['search_button_loc'])  # 查找
        base.staleness_of(apartmentAchievementPage.searchContractMould['tr_contract'])  # 等待第一条数据刷新
        base.dblclick(apartmentAchievementPage.searchContractMould['tr_contract'],
                      checkLoc=apartmentAchievementPage.detailAchievementMoudle['contract_num_loc'])  # 点击第一条数据等待详情页面完全显示
        base.click(apartmentAchievementPage.detailAchievementMoudle['fanshen_button_loc'])
        base.input_text(apartmentAchievementPage.detailAchievementMoudle['contract_audit_content'], 'ok')
        base.click(apartmentAchievementPage.detailAchievementMoudle['contract_audit_confirm'])
        base.check_submit()
        achievementStatus = "select * from back_achievement where is_active='Y' and audit_status='AUDIT' AND deleted=0 and achieve_id='%s'" % info[2]
        base.diffAssert(lambda test: asserts(sqlbase.waitData(achievementStatus, 1)).is_true(), 1137,
                        u'%s:出租合同 %s 业绩反审异常'% (fileName, contractNum))
        base.dblclick(apartmentAchievementPage.searchContractMould['tr_contract'],
                      checkLoc=apartmentAchievementPage.detailAchievementMoudle['contract_num_loc'])  # 点击第一条数据等待详情页面完全显示
        try:
            base.click(apartmentAchievementPage.detailAchievementMoudle['resave_loc'])
        except:
            consoleLog(u'%s：出租合同 %s 反审后业绩无法重新核算' % (fileName, contractNum))
        # 预估排行榜业绩
        base.open(page.achievementListPrePage, apartmentAchievementPage.searchContractMould['tr_contract'])
        base.click(apartmentAchievementPage.searchContractMould['reset_button_loc'])  # 重置
        base.staleness_of(apartmentAchievementPage.searchContractMould['tr_contract'])
        base.input_text(apartmentAchievementPage.searchContractMould['contract_num_hefa_loc'],contractNum)  # 输入合同号
        base.input_text(apartmentAchievementPage.searchContractMould['search_address_loc'], info[1])  # 输入房源
        base.type_select(apartmentAchievementPage.searchContractMould['category_loc'], info[3])  # 分类
        base.click(apartmentAchievementPage.searchContractMould['search_button_loc'])  # 查找
        base.staleness_of(apartmentAchievementPage.searchContractMould['tr_contract'])  # 等待第一条数据刷新
        achievementDetailCount = sqlbase.get_count(
            "select * from contract_achievement_detail where deleted=0 and achieve_id='%s'" % info[2])
        for i in range(achievementDetailCount):
            achievement_audit_status = base.script(
                "var a = $('[datagrid-row-index=\"%s\"] > [field=\"audit_status\"] > div').text();return a" % i, True)
            audit_status = u'待审核'
            base.diffAssert(lambda test: asserts(achievement_audit_status).is_equal_to(audit_status), 1137,
                            u'%s:合同 %s 扣回业绩第 %s 条状态异常，期望值 %s 实际值 %s' % (fileName, contractNum, i+1, audit_status, achievement_audit_status))

test_1137()