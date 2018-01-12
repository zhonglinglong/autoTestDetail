# -*- coding:utf8 -*-

from common.base import log,consoleLog,Base,get_conf,set_conf
from common import page
from house.house_develop import houseAuditPage
from common import sqlbase

@log
def auditHouse():
    """审核房源"""
    try:
        base=Base()
        #需要从配置文件读取新增的房源信息才能做审核操作
        residential = get_conf('residential', 'residentialname')
        building = get_conf('residential', 'buildingname')
        unit = get_conf('residential', 'unitname')
        houseno = get_conf('residential', 'housenoname')
        address = residential + building + unit + houseno
        base.open(page.houseAuditPage, houseAuditPage.houseAuditPageloc['audit_btn'])
        base.input_text(houseAuditPage.searchMould['residentia_name_loc'], residential)
        base.input_text(houseAuditPage.searchMould['building_name_loc'], building)
        base.input_text(houseAuditPage.searchMould['unit_name_loc'], unit)
        base.input_text(houseAuditPage.searchMould['houseno_name_loc'], houseno)
        base.click(houseAuditPage.searchMould['search_button_loc'])
        base.staleness_of(houseAuditPage.searchMould['tr_house'])
        base.script('$("#audit_btn").click()')
        base.click(houseAuditPage.houseAuditPageloc['cancel_btn'])  # 审核通过
        for i in range(5):
            try:
                base.click(houseAuditPage.houseAuditPageloc['iszCommonWorkflowPageSure'])  # 确定
                break
            except:
                base.click(houseAuditPage.houseAuditPageloc['cancel_btn'])  # 审核通过
        base.check_submit()
        try:
            base.solr('house', get_conf('testCondition', 'test'))
            consoleLog(u'solr的house-core增量成功')
        except:
            consoleLog(Exception.message, level='e')
            consoleLog(u'执行house-core的增量失败，请检查solr是否正常', level='w')
            pass
        consoleLog(u'房源 %s审核成功' % address)
        house = sqlbase.serach(
            "SELECT residential_id,building_id,unit_id,house_no_id,house_id,house_code from house where property_name like '%s%%' and deleted = 0" % address.encode('utf-8'))
        set_conf('residential', residentialID=house[0], buildingID=house[1], unitID=house[2], housenoID=house[3])
        set_conf('houseInfo', houseID=house[4], houseCode=house[5])

    finally:
        base.driver.quit()

auditHouse()
