# -*- coding:utf8 -*-
import time

from common import page
from common import sqlbase
from common.base import log, consoleLog, Base
from contract.houseContract.page import houseContractEndPage


@log
def houseContractmentEnd():
    """委托合同名下存在有效出租合同做终止结算"""

    # describe： 委托合同名下存在有效出租合同做终止结算
    # data：委托合同下存在有效的出租合同
    # result：新增正退终止失败

    #查找符合条件的委托合同
    sql = "select contract_num,entrust_end_date from house_contract where contract_id  in" \
          "(select house_contract.contract_id from apartment ,apartment_contract ,house_contract " \
          "where  house_contract.contract_id=apartment.house_contract_id and apartment.house_id=apartment_contract.house_id " \
          "and apartment_contract.real_due_date>NOW()) " \
          "and city_code = 330100 and audit_status = 'APPROVED'and contract_status = 'EFFECTIVE' and deleted = 0 and entrust_end_date>NOW() order by rand() limit 1"
    if sqlbase.get_count(sql) > 0:
        contractNum = sqlbase.serach(sql, needConvert=False)[0]  # 委托合同号
        consoleLog(u'取委托合同 %s 做新增终止结算操作' % contractNum)
    else:
        consoleLog(u'未找到符合条件的委托合同','w')
        consoleLog(u'执行SQL：%s' % sql.encode('utf-8'))
        return

    with Base() as base:
        base.open(page.entrustContractPage, houseContractEndPage.addContractEndMould['tr_contract'])
        base.input_text(houseContractEndPage.searchMould['contract_num_loc'], contractNum)  # 输入合同号
        base.click(houseContractEndPage.searchMould['contract_search_button_loc'])  # 搜索
        base.staleness_of(houseContractEndPage.addContractEndMould['tr_contract'])  # 等待数据刷新
        base.context_click(houseContractEndPage.addContractEndMould['tr_contract'])  # 右击第一条数据
        base.click(houseContractEndPage.addContractEndMould['end_button_loc'], index=1)  # 终止结算
        time.sleep(2)
        message=base.driver.find_element_by_css_selector('.panel-noscroll>div:nth-child(29)>div:nth-child(2)>div:nth-child(2)').text.encode('utf-8')
        if message.__contains__(u'存在有效状态的出租合同'.encode('utf-8')):
            consoleLog(message)
            pass
        else:
            consoleLog(u'该合同可以做终止结算，与预期不符！','e')
            return

houseContractmentEnd()