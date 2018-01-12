# -*- coding:utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from common.base import log,Base
from common import page
from contract.achievement.page import apartmentDefaultAchievementPage


@log
def auditDefaultAchievement():
    """审核违约业绩"""
    try:
        base=Base()
        base.open(page.apartmentAchievementPage, apartmentDefaultAchievementPage.searchContractMould['tr_contract'], havaFrame=False)
        contractnum='WB1-0067404'
        base.input_text(apartmentDefaultAchievementPage.searchContractMould['contract_num_loc'], contractnum.encode('utf-8'))#输入合同号
        base.click(apartmentDefaultAchievementPage.searchContractMould['search_button_loc'])#查找
        base.staleness_of(apartmentDefaultAchievementPage.searchContractMould['tr_contract'])#等待第一条数据刷新
        base.dblclick(apartmentDefaultAchievementPage.searchContractMould['tr_contract'],
                      apartmentDefaultAchievementPage.detailDefaultMoudle['house_code_loc'])#点击第一条数据
        #数据校验

        base.click(apartmentDefaultAchievementPage.detailDefaultMoudle['audit_button_loc'])#审核
        base.input_text(apartmentDefaultAchievementPage.detailAchievementMoudle['contract_audit_content'], u'自动化测试审核意见')#审核意见
        base.click(apartmentDefaultAchievementPage.detailAchievementMoudle['contract_audit_confirm'])#确定
        base.check_submit()#等待提交完成

    finally:
        base.driver.quit()

auditDefaultAchievement()
