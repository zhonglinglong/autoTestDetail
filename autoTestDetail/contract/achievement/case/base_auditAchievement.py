# -*- coding:utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from common.base import log,Base
from common import page
from contract.achievement.page import apartmentAchievementPage


@log
def auditAchievement():
    """审核出房业绩"""
    try:
        base=Base()
        base.open(page.apartmentAchievementPage, apartmentAchievementPage.searchContractMould['tr_contract'], havaFrame=False)
        base.click(apartmentAchievementPage.searchContractMould['reset_button_loc'])#重置
        contractnum='WB1-0067404'
        base.input_text(apartmentAchievementPage.searchContractMould['contract_num_loc'], contractnum.encode('utf-8'))#输入合同号
        base.click(apartmentAchievementPage.searchContractMould['search_button_loc'])#查找
        base.staleness_of(apartmentAchievementPage.searchContractMould['tr_contract'])#等待第一条数据刷新
        base.dblclick(apartmentAchievementPage.searchContractMould['tr_contract'], checkLoc=apartmentAchievementPage.detailAchievementMoudle['contract_num_loc'])#点击第一条数据等待详情页面完全显示
        #数据校验

        base.click(apartmentAchievementPage.detailAchievementMoudle['audit_button_loc'])#审核
        base.input_text(apartmentAchievementPage.detailAchievementMoudle['contract_audit_content'], u'自动化测试审核意见')#审核意见
        base.click(apartmentAchievementPage.detailAchievementMoudle['contract_audit_confirm'])#确定
        base.check_submit()#等待提交完成

    finally:
        base.driver.quit()

auditAchievement()
