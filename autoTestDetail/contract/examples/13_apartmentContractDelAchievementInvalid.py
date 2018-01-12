# -*- coding:utf8 -*-

import time

from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.achievement.page import apartmentAchievementPage
from contract.apartmentContract.page import apartmentContractPage


@log
def apartmentContractDel():
    """删除出租合同业绩失效"""

    # describe：删除出单业绩对应的出租合同，出单业绩失效
    # data：出单业绩状态为生效且已审核（取未审核数据做审核操作），未走收款流程
    # result：1.出单业绩变成已失效；
    #         2.两个业绩排行榜中也变成已失效；

    #取出单业绩生效，出租合同生效已复审，未走收款流程的数据
    sql = "select DISTINCT contract_num,audit_status from apartment_contract_achievement where is_active='Y' and audit_status<>'REJECTED' and downpayment_status='NOTGET' " \
          "AND contract_id IN (SELECT contract_id from apartment_contract where deleted = 0 and city_code = 330100 and audit_status = 'APPROVED' and contract_status = 'EFFECTIVE' )" \
          "and contract_id NOT IN (SELECT DISTINCT contract_id FROM apartment_contract_receivable  where end_status<>'NOTGET' ) order by RAND() limit 1"
    if sqlbase.get_count(sql) == 0:
        consoleLog(u'SQL查询失败', 'w')
        consoleLog(u'执行SQL：%s'%sql.encode('utf-8'))
        return
    result = sqlbase.serach(sql)

    with Base() as base:
        base.open(page.apartmentAchievementPage, apartmentAchievementPage.searchContractMould['tr_contract'])
        base.click(apartmentAchievementPage.searchContractMould['reset_button_loc'])#重置
        base.staleness_of(apartmentAchievementPage.searchContractMould['tr_contract'])  # 等待第一条数据刷新
        contractNum=result[0]
        if result[1] == 'AUDIT':#业绩未审核的做审核操作
            base.input_text(apartmentAchievementPage.searchContractMould['contract_num_loc'], contractNum)#输入合同号
            base.click(apartmentAchievementPage.searchContractMould['search_button_loc'])  # 查找
            base.staleness_of(apartmentAchievementPage.searchContractMould['tr_contract'])  # 等待第一条数据刷新
            base.dblclick(apartmentAchievementPage.searchContractMould['tr_contract'], checkLoc=
            apartmentAchievementPage.detailAchievementMoudle['contract_num_loc'])#点击第一条数据等待详情页面完全显示
            base.click(apartmentAchievementPage.detailAchievementMoudle['audit_button_loc'])#审核
            base.input_text(apartmentAchievementPage.detailAchievementMoudle['contract_audit_content'], u'自动化测试审核意见')#审核意见
            base.click(apartmentAchievementPage.detailAchievementMoudle['contract_audit_confirm'])#确定
            base.check_submit()#等待提交完成
        auditsql = "select * from apartment_contract_achievement where contract_num='%s' and audit_status='APPROVED'" % contractNum.encode('utf-8')
        if sqlbase.get_count(auditsql) == 0:
            consoleLog(u'合租合同 %s 对应业绩审核失败' % contractNum, 'e')
            consoleLog(u'执行SQL：%s' % sql.encode('utf-8'))
            return
        else:
            consoleLog(u'合租合同 %s 对应业绩审核成功' % contractNum)

        #删除出租合同
        base.open(page.apartmentContractPage, apartmentContractPage.searchContractMould['tr_contract'], havaFrame=False)
        base.input_text(apartmentContractPage.searchContractMould['contract_num_loc'], contractNum)  # 输入合同编号
        base.click(apartmentContractPage.searchContractMould['search_button_loc'])  # 搜索
        base.staleness_of(apartmentContractPage.searchContractMould['tr_contract'])  # 等待列表刷新
        base.script("$('#data_perm_btn').click()")  # 删除
        base.click(apartmentContractPage.addApartmentContractMould['delete_button_confirm'])  # 确定
        base.check_submit()  # 等待提交完成
        contractsql = "select * from apartment_contract where contract_num='%s' and deleted=1" % contractNum.encode('utf-8')
        if sqlbase.get_count(contractsql) == 1:
            consoleLog(u'出租合同 %s 删除成功' % contractNum)
        else:
            consoleLog(u'出租合同 %s 删除失败' % contractNum,'e')
            consoleLog(u'执行SQL：%s' % contractsql.encode('utf-8'))
            return

        achievementsql = "select * from apartment_contract_achievement where contract_num='%s' and audit_status='APPROVED' and is_active='INVALID'" % contractNum.encode('utf-8')
        for i in range(5):
            if sqlbase.get_count(achievementsql) == 1:
                consoleLog(u'出租合同 %s 业绩失效成功' % contractNum)
                break
            else:
                time.sleep(10)
                if i == 4:
                    consoleLog(u'出租合同 %s 业绩未失效' % contractNum, 'e')
                    consoleLog(u'执行SQL：%s' % achievementsql.encode('utf-8'))
                    return

apartmentContractDel()