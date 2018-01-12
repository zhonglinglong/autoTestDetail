# -*- coding:utf8 -*-

from common import page
from common import sqlbase
from common.base import log, consoleLog, Base, get_conf
from contract.houseContract.page import houseContractEndPage


@log
def addContractEnd():
    """新增委托合同终止结算"""
    try:
        base=Base()
        base.open(page.entrustContractPage, houseContractEndPage.addContractEndMould['tr_contract'], havaFrame=False)
        #配置文件读取将要终止的委托合同
        contractNum = get_conf('houseContractInfo', 'contractnum')
        sql = "SELECT entrust_end_date from house_contract hc where hc.contract_num = '%s' and deleted = 0 and audit_status = 'APPROVED' and contract_status = 'EFFECTIVE'" % contractNum.encode('utf-8')

        if sqlbase.get_count(sql) > 0:
            base.input_text(houseContractEndPage.searchMould['contract_num_loc'], contractNum)
            endDate = sqlbase.serach(sql)[0]
        else:
            consoleLog(u'未找到或不满足新增终止条件的合同 %s，开始随机查找符合条件的委托合同' % contractNum, level='w')
            sql = "select house_contract.contract_num,house_contract.entrust_end_date from house_contract where house_contract.contract_id not in " \
                  "(select house_contract.contract_id from apartment ,apartment_contract ,house_contract where  house_contract.contract_id=apartment.house_contract_id " \
                  "and apartment.house_id=apartment_contract.house_id and house_contract.deleted = 0 and house_contract.audit_status = 'APPROVED' and house_contract.contract_status = 'EFFECTIVE' " \
                  "and house_contract.city_code = 330100 and apartment_contract.real_due_date>NOW()) and contract_num<>'' limit 1"
            if sqlbase.get_count(sql) > 0:
                contractNum = sqlbase.serach(sql, needConvert=False)[0]
                consoleLog(u'随机对委托合同 %s 做新增终止结算操作' % contractNum, level='w')
                base.input_text(houseContractEndPage.searchMould['contract_num_loc'], contractNum)
                endDate = sqlbase.serach(sql)[1]
            else:
                consoleLog(u'未找到符合条件的委托合同，跳过终止结算用例')
                return
        base.click(houseContractEndPage.searchMould['contract_search_button_loc'])
        base.staleness_of(houseContractEndPage.addContractEndMould['tr_contract'])
        base.context_click(houseContractEndPage.addContractEndMould['tr_contract'])#右击第一条数据
        base.click(houseContractEndPage.addContractEndMould['end_button_loc'], index=1)
        base.input_text(houseContractEndPage.addContractEndMould['penalty_loc'], 111)
        base.type_select(houseContractEndPage.typeMould['end_type'], 'RETREATING')  # 结算类型-正退
        base.type_date(houseContractEndPage.typeMould['end_date'], endDate)
        # 结算扣款
        base.input_text(houseContractEndPage.addContractEndMould['penalty_remark_loc'], u'违约金陪入')
        base.input_text(houseContractEndPage.addContractEndMould['return_rent_loc'], 222)
        base.input_text(houseContractEndPage.addContractEndMould['return_rent_remark_loc'], u'返还房租')
        base.input_text(houseContractEndPage.addContractEndMould['no_charge_loc'], 333)
        base.input_text(houseContractEndPage.addContractEndMould['no_charge_remark_loc'], u'未扣款项')
        base.input_text(houseContractEndPage.addContractEndMould['fitment_charge_loc'], 444)
        base.input_text(houseContractEndPage.addContractEndMould['fitment_charge_remark_loc'], u'装修扣款')
        base.input_text(houseContractEndPage.addContractEndMould['other_loc'], 555)
        base.input_text(houseContractEndPage.addContractEndMould['other_remark_loc'], u'其他信息')
        # 代垫费用
        base.click(houseContractEndPage.addContractEndMould['tool_bar'], index=0)
        base.type_select(houseContractEndPage.typeMould['return_type_loc'], 'LIQUIDATED')  # 违约金赔出
        base.input_text(houseContractEndPage.addContractEndMould['return_money_loc'], 666)
        base.type_select(houseContractEndPage.typeMould['bear_type_loc'], 'COMPANY')  # 承担方-公司
        base.type_select(houseContractEndPage.typeMould['bear_name'], 'ISZTECH')
        base.type_date(houseContractEndPage.typeMould['money_start_date'], '2017-07-07')
        base.type_date(houseContractEndPage.typeMould['money_end_date'], '2017-08-08')
        base.type_select(houseContractEndPage.typeMould['explain'], 'VACANCY')  # 情况说明-空置期
        base.type_select(houseContractEndPage.typeMould['dispute'], 'N')
        base.type_date(houseContractEndPage.typeMould['receivable_date'], '2017-08-08')
        # 打款信息
        base.type_select(houseContractEndPage.typeMould['pay_type'], 'OWNER')  # 打款类别-业主收款
        base.input_text(houseContractEndPage.addContractEndMould['pay_name_loc'], 'AutoTest')
        base.input_text(houseContractEndPage.addContractEndMould['pay_bank_loc'], u'中国银行')
        base.input_text(houseContractEndPage.addContractEndMould['pay_bank_no_loc'], '12345678910')
        # base.input_text(HouseContractEndPage.addContractEndMould['company_no_loc'],u'杭州爱上租科技有限公司')
        base.click(houseContractEndPage.addContractEndMould['submit_loc'])
        base.check_submit()
        consoleLog(u'委托合同 %s 终止结算新增成功' % contractNum)
    finally:
        base.driver.quit()

addContractEnd()
