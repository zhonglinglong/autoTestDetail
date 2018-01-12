# -*- coding:utf8 -*-

from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.apartmentContract.page import apartmentContractEndPage


@log
def apartmentContractEndDel():
    """出租合同终止结算删除，业绩删除"""

    # describe： 出租合同终止结算反审删除
    # data：1、终止结算已复审；2、对应违约业绩已生效且未审核；
    # result：违约业绩删除

    sql="SELECT ba.breach_num FROM breach_achievement ba, apartment_contract_end ace, apartment_contract ac,apartment_contract_relation acr " \
        "WHERE ac.contract_id=acr.contract_id AND ba.is_active = 'Y' AND ba.deleted = 0 AND ba.audit_status = 'AUDIT' AND ba.end_audit_status <> 'AUDITED' AND ac.city_code=330100 AND " \
        "ba.breach_num = ac.contract_num  AND ace.contract_id = ac.contract_id  and ace.audit_status='REVIEW' and ba.deleted=0  and acr.room_id in (select a.room_id " \
        "from ( SELECT a.house_id,a.apartment_code,a.room_id,COUNT(*) as count FROM apartment_contract ac, apartment a, apartment_contract_relation acr" \
        " WHERE a.house_id = ac.house_id AND a.room_id = acr.room_id AND ac.contract_id = acr.contract_id and ac.deleted=0 group by a.apartment_code  ) as a where a.count=1 ) " \
        "order by RAND() limit 1"
    if sqlbase.get_count(sql) == 1:
        contractNum = sqlbase.serach(sql)[0]
        consoleLog(u'取出租合同 %s 做出租合同终止结算交易' % contractNum)
    else:
        consoleLog(u'SQL查询无数据','w')
        return

    with Base() as base:
        #删除出租合同对应终止结算
        base.open(page.contractEndPage, apartmentContractEndPage.searchMould['tr_contract_end'])
        base.input_text(apartmentContractEndPage.searchMould['contract_num_loc'], contractNum)  # 输入合同号
        base.click(apartmentContractEndPage.searchMould['search_button_loc'])  # 搜索
        base.staleness_of(apartmentContractEndPage.searchMould['tr_contract_end'])  # 等待列表刷新
        base.dblclick(apartmentContractEndPage.searchMould['tr_contract_end'])  # 双击第一条数据
        # 反审
        base.click(apartmentContractEndPage.addContractEndMould['fanshen_loc'])  # 反审
        base.input_text(apartmentContractEndPage.addContractEndMould['contract_audit_content'], u'自动化测试审核数据')  # 审核意见
        base.click(apartmentContractEndPage.addContractEndMould['contract_audit_confirm'])  # 确定
        base.staleness_of(apartmentContractEndPage.searchMould['tr_contract_end'])  # 等待列表刷新
        base.click(apartmentContractEndPage.addContractEndMould['delete_button'])  #删除
        base.click(apartmentContractEndPage.addContractEndMould['delete_button_confirm'])  #确定
        base.staleness_of(apartmentContractEndPage.searchMould['tr_contract_end'])  # 等待列表刷新
        contractEndsql="SELECT * from apartment_contract_end ace,apartment_contract ac where ace.contract_id=ac.contract_id " \
                       "and ac.contract_num='%s' and ace.deleted=1" % contractNum.encode('utf-8')
        if  sqlbase.get_count(contractEndsql) == 1:
            consoleLog(u'出租合同 %s 终止结算删除成功' % contractNum)
        else:
            consoleLog(u'出租合同 %s 终止结算删除失败' % contractNum,'e')
            consoleLog(u'执行SQL：%s' % contractEndsql.encode('utf-8'))
            return

        breachsql="SELECT * FROM breach_achievement  where  audit_status='AUDIT' AND is_active='Y' AND breach_num='%s' and deleted=0" % contractNum.encode('utf-8')
        if sqlbase.get_count(breachsql) == 0:
            consoleLog(u'出租合同 %s 对应违约业绩删除成功' % contractNum)
        else:
            consoleLog(u'出租合同 %s 对应违约业绩未删除' % contractNum,'e')
            consoleLog(u'执行SQL：%s' % breachsql.encode('utf-8'))
            return


apartmentContractEndDel()
