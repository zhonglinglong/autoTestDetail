# -*- coding:utf8 -*-
from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.houseContract.page import houseContractEndPage


@log
def houseContractmentEnd():
    """委托合同名下无出租合同正退终止结算"""

    # describe：委托合同名下无出租合同正退终止结算
    # data：委托合同下无承租周期在当前日期之后的出租合同，委托合同到期日在当前日期之后
    # result：新增正退终止结算成功，复审通过

    #查找符合条件的委托合同
    sql = "select contract_num,entrust_end_date from house_contract where contract_id not in" \
          "(select house_contract.contract_id from apartment ,apartment_contract ,house_contract " \
          "where  house_contract.contract_id=apartment.house_contract_id and apartment.house_id=apartment_contract.house_id " \
          "and apartment_contract.real_due_date>NOW()) " \
          "and city_code = 330100 and audit_status = 'APPROVED'and contract_status = 'EFFECTIVE' and deleted = 0 and entrust_end_date>NOW() order by rand() limit 1"
    if sqlbase.get_count(sql) > 0:
        contractNum = sqlbase.serach(sql, needConvert=False)[0]  # 委托合同号
        consoleLog(u'对委托合同 %s 做新增终止结算操作' % contractNum)
        endDate = sqlbase.serach(sql)[1]  # 合同到期日
    else:
        consoleLog(u'SQL查无数据！', 'w')
        consoleLog(u'执行SQL：%s' % sql.encode('utf-8'))
        return

    with Base() as base:
        base.open(page.entrustContractPage, houseContractEndPage.addContractEndMould['tr_contract'])
        base.input_text(houseContractEndPage.searchMould['contract_num_loc'], contractNum)  # 输入合同号
        base.click(houseContractEndPage.searchMould['contract_search_button_loc'])  # 搜索
        base.staleness_of(houseContractEndPage.addContractEndMould['tr_contract'])  # 等待数据刷新
        base.context_click(houseContractEndPage.addContractEndMould['tr_contract'])  # 右击第一条数据
        base.click(houseContractEndPage.addContractEndMould['end_button_loc'], index=1)  # 终止结算
        base.wait_element(houseContractEndPage.addContractEndMould['penalty_loc'])#等待页面出现
        base.type_select(houseContractEndPage.typeMould['end_type'], 'RETREATING')  # 结算类型-正退
        base.type_date(houseContractEndPage.typeMould['end_date'], endDate)  # 终止日期
        # 结算扣款
        base.input_text(houseContractEndPage.addContractEndMould['penalty_loc'], 111)  # 违约金陪入
        base.input_text(houseContractEndPage.addContractEndMould['penalty_remark_loc'], u'违约金陪入')  # 备注
        base.input_text(houseContractEndPage.addContractEndMould['return_rent_loc'], 222)  # 返还房租
        base.input_text(houseContractEndPage.addContractEndMould['return_rent_remark_loc'], u'返还房租')  # 备注
        base.input_text(houseContractEndPage.addContractEndMould['no_charge_loc'], 333)  # 未扣款项
        base.input_text(houseContractEndPage.addContractEndMould['no_charge_remark_loc'], u'未扣款项')  # 备注
        base.input_text(houseContractEndPage.addContractEndMould['fitment_charge_loc'], 444)  # 装修扣款
        base.input_text(houseContractEndPage.addContractEndMould['fitment_charge_remark_loc'], u'装修扣款')  # 备注
        base.input_text(houseContractEndPage.addContractEndMould['other_loc'], 555)  # 其他
        base.input_text(houseContractEndPage.addContractEndMould['other_remark_loc'], u'其他信息')  # 备注
        # 代垫费用
        base.click(houseContractEndPage.addContractEndMould['tool_bar'], index=0)  # 新增代垫
        base.type_select(houseContractEndPage.typeMould['return_type_loc'], 'LIQUIDATED')  # 退款项目：违约金赔出
        base.input_text(houseContractEndPage.addContractEndMould['return_money_loc'], 666)  # 退款金额
        base.type_select(houseContractEndPage.typeMould['bear_type_loc'], 'COMPANY')  # 承担方-公司
        base.type_select(houseContractEndPage.typeMould['bear_name'], 'ISZTECH')  # 承担方姓名
        base.type_date(houseContractEndPage.typeMould['money_start_date'], '2017-07-07')  # 费用开始时间
        base.type_date(houseContractEndPage.typeMould['money_end_date'], '2017-08-08')  # 费用结束时间
        base.type_select(houseContractEndPage.typeMould['explain'], 'VACANCY')  # 情况说明-空置期  #
        base.type_select(houseContractEndPage.typeMould['dispute'], 'N')  # 是否纠纷
        base.type_date(houseContractEndPage.typeMould['receivable_date'], '2017-08-08')  # 应收日期
        # 打款信息
        base.type_select(houseContractEndPage.typeMould['pay_type'], 'OWNER')  # 打款类别-业主收款
        base.input_text(houseContractEndPage.addContractEndMould['pay_name_loc'], 'AutoTest')  # 姓名
        base.input_text(houseContractEndPage.addContractEndMould['pay_bank_loc'], u'中国银行')  # 收款银行
        base.input_text(houseContractEndPage.addContractEndMould['pay_bank_no_loc'], '12345678910')  # 银行卡号
        # base.input_text(HouseContractEndPage.addContractEndMould['company_no_loc'],u'杭州爱上租科技有限公司')
        base.click(houseContractEndPage.addContractEndMould['submit_loc'])  # 提交
        base.check_submit()  # 等待提交完成
        contractEndAdd="SELECT * FROM house_contract ,house_contract_end WHERE house_contract.contract_id = house_contract_end.contract_id AND house_contract_end.end_type='RETREATING' " \
                       "and house_contract_end.audit_status='NO_AUDIT' and house_contract.contract_num = '%s'"%contractNum.encode('utf-8')
        if sqlbase.get_count(contractEndAdd):
            consoleLog(u'委托合同 %s 终止结算新增成功' % contractNum)
        else:
            consoleLog(u'委托合同终止结算失败' ,'e')
            consoleLog(u'执行SQL：%s' % contractEndAdd.encode('utf-8'))
            return
        #审核
        base.open(page.contractEndPage, houseContractEndPage.searchMould['contract_search_button_loc'])
        base.click(houseContractEndPage.addContractEndMould['tab_info'], index=1)
        base.input_text(houseContractEndPage.searchMould['end_contract_num_loc'], contractNum)
        base.click(houseContractEndPage.searchMould['end_search_button_loc'])  # 搜索
        base.staleness_of(houseContractEndPage.searchMould['tr_contract_end'])  # 等待数据刷新
        base.dblclick(houseContractEndPage.searchMould['tr_contract_end'],
                      checkLoc=houseContractEndPage.addContractEndMould['check_loc'])
        # 初审
        base.click(houseContractEndPage.addContractEndMould['chushen_loc'])  # 初审
        base.click(houseContractEndPage.addContractEndMould['contract_audit_confirm'])  # 确定
        base.check_submit()  # 等待提交完成
        base.dblclick(houseContractEndPage.searchMould['tr_contract_end'],
                      checkLoc=houseContractEndPage.addContractEndMould['check_loc'])  # 双击第一条数据
        # 复审
        base.click(houseContractEndPage.addContractEndMould['fushen_loc'])
        base.click(houseContractEndPage.addContractEndMould['contract_audit_confirm'])
        base.check_submit()

        contractEndAud="SELECT * FROM house_contract ,house_contract_end WHERE house_contract.contract_id = house_contract_end.contract_id AND house_contract_end.end_type='RETREATING' " \
                       "and house_contract_end.audit_status='REVIEW' and house_contract.contract_num = '%s'"%contractNum.encode('utf-8')
        if sqlbase.get_count(contractEndAud):
            consoleLog(u'委托合同 %s 终止结算审核成功' % contractNum)
        else:
            consoleLog(u'委托合同终止结算审核失败' ,'e')
            consoleLog(u'执行SQL：%s' % contractEndAud.encode('utf-8'))
            return

houseContractmentEnd()