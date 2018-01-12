# -*- coding:utf8 -*-
import datetime
import time

from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.apartmentContract.page import apartmentContractEndPage


@log
def apartmentContractEnd():
    """新增出租合同退租终止结算"""

    # describe： 新增出租合同退租终止结算，违约业绩生效
    # data：有效期内出租合同
    # result：新增终止结算通过，生成违约业绩

    sql = "SELECT contract_num,rent_end_date from apartment_contract where deleted = 0 and city_code = 330100 and audit_status = 'APPROVED' and contract_status = 'EFFECTIVE' " \
          "and contract_type = 'NEWSIGN' and entrust_type = 'SHARE' and payment_type<>'NETWORKBANK' order by rand() limit 1"
    if sqlbase.get_count(sql) > 0:  # 数据库查找可以做终止结算的合同
        info = sqlbase.serach(sql)
        contractNum = info[0]  # 出租合同编号
        consoleLog(u'使用合同 %s 做新增终止结算用例' % contractNum)
    else:
        consoleLog(u'未找到符合条件的可以做终止的出租合同','w')
        consoleLog(u'执行SQL：%s' % sql.encode('utf-8'))
        return

    with Base() as base:
        base.open(page.apartmentContractPage, apartmentContractEndPage.addContractEndMould['tr_contract'])
        base.input_text(apartmentContractEndPage.addContractEndMould['contract_num_loc'], contractNum)  # 输入合同编号
        today = datetime.date.today()
        base.click(apartmentContractEndPage.addContractEndMould['search_button_loc'])  # 搜索
        base.staleness_of(apartmentContractEndPage.addContractEndMould['tr_contract'])  # 等待列表刷新
        base.context_click(apartmentContractEndPage.addContractEndMould['tr_contract'])  # 右击第一条数据
        base.click(apartmentContractEndPage.addContractEndMould['end_button_loc'], index=1)  # 终止结算
        base.click(apartmentContractEndPage.addContractEndMould['now_end_loc'])  # 立即终止
        base.input_text(apartmentContractEndPage.addContractEndMould['receipt_num_loc'], 'AutoTest')  # 收款卡号
        base.type_date(apartmentContractEndPage.typeMould['end_date'], today)  # 终止日期：当天
        endnum = 'AutoACE' + '-' + time.strftime('%m%d%H%M')
        base.type_select(apartmentContractEndPage.typeMould['end_type'], 'OWNER_DEFAULT')  # 退租
        base.input_text(apartmentContractEndPage.addContractEndMould['end_num_loc'], endnum)  # 终止协议号
        base.input_text(apartmentContractEndPage.addContractEndMould['end_reason_loc'], u'退租')  # 终止原因
        base.type_select(apartmentContractEndPage.typeMould['receipt_type_loc'], 'PAYER')  # 承租人
        base.input_text(apartmentContractEndPage.addContractEndMould['bank_loc'], u'中国银行')  # 开户银行
        base.dblclick(apartmentContractEndPage.addContractEndMould['weiyuejin_loc'], index=12)  # 违约金
        base.input_text(apartmentContractEndPage.addContractEndMould['receivable_money_loc'], '888.88')  # 应收违约金
        base.input_text(apartmentContractEndPage.addContractEndMould['payable_money_loc'], '666.66')  # 应退违约金
        base.driver.find_element_by_id('contractFileUpload').send_keys('C:\Users\Public\Pictures\Sample Pictures\jsp.jpg')#传图
        time.sleep(2)
        base.input_text(apartmentContractEndPage.addContractEndMould['remark_loc'], 'AutoTest')  # 备注
        base.script('$("#form_submit_btn").click()')  # 提交
        base.check_submit()  # 等待提交完成
        contractEndAdd="SELECT * FROM apartment_contract ,apartment_contract_end WHERE apartment_contract.contract_id = apartment_contract_end.contract_id " \
                       "and apartment_contract_end.audit_status='NO_AUDIT' AND apartment_contract_end.end_type='OWNER_DEFAULT'" \
                       "and apartment_contract.contract_num='%s'" % contractNum.encode('utf-8')
        if sqlbase.get_count(contractEndAdd) == 1:
            consoleLog(u'出租合同 %s 终止结算新增成功' % contractNum)
        else:
            consoleLog(u'新增终止结算失败','e')
            consoleLog(u'执行SQL：%s' % contractEndAdd.encode('utf-8'))
            return

        base.open(page.contractEndPage, apartmentContractEndPage.searchMould['tr_contract_end'])
        base.input_text(apartmentContractEndPage.searchMould['contract_num_loc'], contractNum)  # 输入合同号
        base.click(apartmentContractEndPage.searchMould['search_button_loc'])  # 搜索
        base.staleness_of(apartmentContractEndPage.searchMould['tr_contract_end'])  # 等待列表刷新
        base.dblclick(apartmentContractEndPage.searchMould['tr_contract_end'])  # 双击第一条数据
        # 初审
        base.click(apartmentContractEndPage.addContractEndMould['chushen_loc'])  # 初审
        base.click(apartmentContractEndPage.addContractEndMould['contract_audit_confirm'])  # 确定
        base.staleness_of(apartmentContractEndPage.searchMould['tr_contract_end'])  # 等待列表刷新
        base.dblclick(apartmentContractEndPage.searchMould['tr_contract_end'])  # 双击第一条数据
        # 复审
        base.click(apartmentContractEndPage.addContractEndMould['fushen_loc'])  # 复审
        base.click(apartmentContractEndPage.addContractEndMould['contract_audit_confirm'])  # 确定
        base.check_submit()
        contractEndAud="SELECT * FROM apartment_contract ,apartment_contract_end WHERE apartment_contract.contract_id = apartment_contract_end.contract_id " \
                       "and apartment_contract_end.audit_status='REVIEW' AND apartment_contract_end.end_type='OWNER_DEFAULT'" \
                       "and apartment_contract.contract_num='%s'" % contractNum.encode('utf-8')
        if sqlbase.get_count(contractEndAud) == 1:
            consoleLog(u'出租合同 %s 终止结算审核通过' % contractNum)
        else:
            consoleLog(u'新增终止结算审核失败','e')
            consoleLog(u'执行SQL：%s' % contractEndAud.encode('utf-8'))
            return

        #对应违约业绩
        for i in range(5):
                breachsql="SELECT * FROM breach_achievement where  is_active='Y'  and deleted=0 and breach_type='OWNER_DEFAULT_BREACH' " \
                          "and end_audit_status='AUDITED' and breach_num='%s'" % contractNum.encode('utf-8')
                if sqlbase.get_count(breachsql) == 1:
                    consoleLog(u'合同 %s 对应违约业绩已生成并且生效' % contractNum)
                    break
                else:
                    time.sleep(10)
                    if i == 4:
                        consoleLog(u'合同 %s 对应违约业绩未生成/生效' % contractNum,'e')
                        consoleLog(u'执行SQL：%s' % breachsql.encode('utf-8'))
                        return
        #对应扣回业绩
        for i in range(5):
            backsql = "select * from back_achievement where  is_active='Y' and contract_end_type='OWNER_DEFAULT' and contract_num='%s'" % contractNum.encode('utf-8')
            if sqlbase.get_count(backsql) == 1:
                consoleLog(u'合同 %s 对应扣回业绩已生成并且生效' % contractNum)
            else:
                time.sleep(10)
                if i == 4:
                    consoleLog(u'合同 %s 对应扣回业绩未生成/生效' % contractNum, 'e')
                    consoleLog(u'执行SQL：%s' % backsql.encode('utf-8'))
                    return
        #改成直接查数据库
        # base.open(page.defaultAchievementPage, apartmentDefaultAchievementPage.searchContractMould['tr_contract'])
        # base.input_text(apartmentDefaultAchievementPage.searchContractMould['contract_num_loc'], contractNum)  # 输入合同号
        # base.click(apartmentDefaultAchievementPage.searchContractMould['search_button_loc'])  # 查找
        # base.staleness_of(apartmentDefaultAchievementPage.searchContractMould['tr_contract'])  # 等待第一条数据刷新
        # is_cative = base.script(
        #     "var a = $('[datagrid-row-index=\"0\"] > [field=\"is_active\"] > div').text();return a", True).encode(
        #     'utf-8')  # 提取搜索出的第一条数据的合同号
        # if is_cative == u'生效'.encode('utf-8'):
        #     consoleLog(u'终止结算复审通过，违约业绩已生效。')
        #     pass
        # else:
        #     consoleLog(u'违约业绩非生效状态，业务异常！')
        #     return


apartmentContractEnd()
