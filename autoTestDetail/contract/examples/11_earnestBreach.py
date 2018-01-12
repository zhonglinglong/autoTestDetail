# -*- coding:utf8 -*-

from common.base import log,consoleLog,Base
from selenium.common.exceptions import TimeoutException as TE
from common import page
from contract.earnest import earnestPage
from common import sqlbase
import datetime


@log
def earnestBreach():
    """下定违约"""

    # describe： 下定违约，违约金取下定金额
    # data：下定状态为待签
    # result：产生违约金记录

    sql="SELECT earnest.sign_status,earnest.earnest_code,earnest.earnest_money,apartment.apartment_code,earnest.confirm_status FROM earnest ,apartment " \
        "WHERE earnest.room_id = apartment.room_id and earnest.sign_status = 'WAITING_SIGN' and earnest.earnest_money>'100' and earnest.deleted=0 order by rand() limit 1"
    if sqlbase.get_count(sql) == 0:
        consoleLog(u'SQL查询失败','w')
        consoleLog(u'执行SQL：%s' % sql.encode('utf-8'))
        return
    result=sqlbase.serach(sql)

    with Base() as base:
        base.open(page.earnestPage, earnestPage.searchMouid['tr_contract'])
        base.input_text(earnestPage.searchMouid['earnest_code_loc'],result[1])#输入定金编号
        consoleLog(u'获取房源编号:%s ；定金编号：%s ；'%(result[3],result[1]))
        base.click(earnestPage.searchMouid['search_button_loc'])  # 搜索
        base.staleness_of(earnestPage.searchMouid['tr_contract'])  # 等待列表刷新
        if result[4]=='N':#未确认的需要确认
            base.click(earnestPage.searchMouid['confirm_button_loc'])#确认
            base.input_text(earnestPage.confirmMould['earnest_money_loc'], result[2])#输入金额
            base.type_select(earnestPage.confirmMould['payway'],'ALIPAY')#收款方式
            base.input_text(earnestPage.confirmMould['name_loc'],u'Autotest')#收据名字
            base.type_select(earnestPage.confirmMould['company'],'ISZTECH')#收款公司
            base.type_date(earnestPage.confirmMould['receipt_date'],datetime.date.today())#收款日期
            base.click(earnestPage.confirmMould['submit_loc'])#提交
            base.check_submit()

        base.click(earnestPage.searchMouid['breach_loc'])#点击违约
        base.input_text(earnestPage.confirmMould['breach_reason_loc'], u'autotest')#输入原因
        base.input_text(earnestPage.confirmMould['breach_money_loc'],result[2])#输入违约金额
        base.click(earnestPage.confirmMould['submit_loc'])#提交
        base.check_submit()#等待提交完成
        #页面查看违约记录  改成直接数据库查看记录
        # base.open(page.earnestBreachPage, earnestPage.searchMouid['tr_contract'])
        # base.input_text(earnestPage.searchMouid['earnest_code_loc'],result[1])#输入定金编号
        # try:
        #     base.click(earnestPage.searchMouid['search_button_loc'])#搜索
        #     base.staleness_of(earnestPage.searchMouid['tr_contract'])#等待列表刷新
        # except TE:
        #     base.click(earnestPage.searchMouid['search_button_loc'])  # 搜索
        #     base.staleness_of(earnestPage.searchMouid['tr_contract'])  # 等待列表刷新
        # base.dblclick(earnestPage.searchMouid['tr_contract'],earnestPage.confirmMould['breach_detail_loc'])
        # consoleLog(u'违约记录生成成功')
        earnestsql="select * from earnest_breach a where EXISTS (select 1 from earnest b where a.earnest_id=b.earnest_id and b.earnest_code='%s')"%result[1].encode('utf-8')
        if  sqlbase.get_count(earnestsql):
            consoleLog(u'定金编号 %s 违约记录生成成功'%result[1].encode('utf-8'))
        else:
            consoleLog(u'定金编号 %s 违约记录未生成'%result[1].encode('utf-8'),'e')
            consoleLog(u'执行SQL：%s' % earnestsql.encode('utf-8'))
            return

earnestBreach()