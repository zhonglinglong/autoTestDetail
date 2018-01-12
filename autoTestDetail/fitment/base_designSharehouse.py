# -*- coding:utf8 -*-
from fitment import designSharePage
from common.base import log,consoleLog,get_conf,set_conf,Base
from common import page,sqlbase
import time

@log
def designSharehouse():
    """品牌合租公寓设计装修"""
    def common():
        #分割户型
        base.click(designSharePage.designShareMould['add_house_btn'])
        base.script("$('#rooms').numberspinner('setValue',2)")  #设置户型为2居室
        base.click(designSharePage.designShareMould['add_house_btn'])
        base.type_select(designSharePage.typeMould['fitment_style'], 'SIMPLECHINESE')
        base.script("$('[onclick=\"ShareWorkBlank.selectAll(this);\"]').click()")
        base.type_select(designSharePage.typeMould['room1_no'], 'METH')
        base.input_text(designSharePage.designShareMould['room_area'], '50', index=0)
        base.type_select(designSharePage.typeMould['room1_orientation'], 'NORTH')
        base.type_select(designSharePage.typeMould['room2_no'], 'ETH')
        base.input_text(designSharePage.designShareMould['room_area'], '20', index=1)
        base.type_select(designSharePage.typeMould['room2_orientation'], 'EAST')
        base.click(designSharePage.designShareMould['save_btn'])
        base.check_submit()
        #派单
        base.context_click(designSharePage.searchMould['tr_contract'])
        base.click(designSharePage.designShareMould['design_btn_1'], index=0)
        base.wait_element(designSharePage.designShareMould['save_btn_1'])
        user = "SELECT su.user_id FROM sys_user su, sys_position sp WHERE su.position_id = sp.position_id AND su.user_status = 'INCUMBENCY' " \
                 "AND sp.position_name LIKE '%品牌公寓专员%' LIMIT 1"
        base.type_select(designSharePage.typeMould['fitment_uid'], sqlbase.serach(user)[0])
        time.sleep(1)
        base.click(designSharePage.designShareMould['save_btn_1'])
        base.check_submit()
        #交房
        base.context_click(designSharePage.searchMould['tr_contract'])
        base.click(designSharePage.designShareMould['design_btn_2'], index=0)
        base.input_text(designSharePage.designShareMould['total_cost'], '5000.00')
        base.type_date(designSharePage.typeMould['decorate_start_date'], '2017-01-01')
        base.type_date(designSharePage.typeMould['hard_delivery_date'], '2017-01-15')
        base.type_date(designSharePage.typeMould['set_delivery_date'], '2017-01-20')
        base.click(designSharePage.designShareMould['save_btn_2'])
        base.check_submit()
        Base.succeed += 1
        sql = "SELECT hh.house_code, hh.house_id, aa.apartment_code, aa.apartment_id FROM house_contract hc INNER JOIN apartment aa ON hc.contract_id = aa.house_contract_id " \
                "INNER JOIN house hh ON hh.house_id = hc.house_id WHERE hc.contract_num = '%s' LIMIT 1" % base.contractNum.encode('utf-8')
        info = sqlbase.serach(sql)
        set_conf('houseInfo',houseCode=info[0],houseID=info[1],apartmentCode=info[2],apatmentID=info[3])
        consoleLog(u'委托合同 %s 设计装修成功' % base.contractNum)
        try:
            base.solr('apartment',get_conf('testCondition','test'))
            consoleLog(u'apartment-core增量成功')
        except:
            consoleLog(Exception.message,level='e')
            consoleLog(u'执行solr增量出现问题，请查看solr是否正常',level='e')
    try:
        base=Base()
        base.open(page.designSharePage, designSharePage.searchMould['tr_contract'], havaFrame=False)
        # 配置文件读取委托合同信息
        contractNum = get_conf('houseContractInfo', 'contractNum')
        consoleLog(u'查询委托合同 %s 是否已操作过设计工程' % contractNum)
        sql1 = "select * from house_contract where contract_num = '%s' and deleted = 0" % contractNum.encode('utf-8')
        sql2 = "select * from house_contract hc INNER JOIN fitment_house fh on hc.contract_id = fh.contract_id where hc.contract_num = '%s' and hc.deleted = 0" % contractNum.encode(
            'utf-8')

        if sqlbase.get_count(sql1) > 0 and sqlbase.get_count(sql2) is 0:
            base.input_text(designSharePage.searchMould['contract_num_loc'], contractNum)
            base.click(designSharePage.searchMould['search_btn_loc'])
            base.staleness_of(designSharePage.searchMould['tr_contract'])
            base.context_click(designSharePage.searchMould['tr_contract'])
            base.click(designSharePage.designShareMould['design_btn'], index=0)
            base.common()
        else:
            consoleLog(u'未找到委托合同 %s ，随机查询待设计的委托合同' % contractNum, level='w')
            sql = "SELECT hc.contract_num FROM house_contract hc WHERE hc.deleted = 0 AND hc.city_code = 330100 AND hc.contract_status = 'EFFECTIVE' " \
                  "AND hc.apartment_type = 'BRAND' AND hc.entrust_type = 'SHARE' AND NOT EXISTS ( SELECT 1 FROM fitment_house fh WHERE " \
                  "fh.contract_id = hc.contract_id ) ORDER BY RAND() LIMIT 1"
            if sqlbase.get_count(sql) != 0:
                base.contractNum = sqlbase.serach(sql, False)[0]
                base.input_text(designSharePage.searchMould['contract_num_loc'], contractNum)
                base.click(designSharePage.searchMould['search_btn_loc'])
                base.staleness_of(designSharePage.searchMould['tr_contract'])
                base.context_click(designSharePage.searchMould['tr_contract'])
                base.click(designSharePage.designShareMould['design_btn'], index=0)
                base.common()
            else:
                consoleLog(u'未找到待设计的品牌合租委托合同，跳过设计分割用例', level='e')
                return
    finally:
        base.driver.quit()

designSharehouse()
