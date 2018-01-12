# -*- coding:utf8 -*-

from common.base import log,consoleLog,Base,get_conf,set_conf
from common import page
from house.house_develop import houseAddPage
from common import sqlbase

@log
def addHouse():
    """新增房源"""
    def common(testData):
            """详细信息"""
            user = sqlbase.serach(
                "select user_id,dep_id from sys_user WHERE user_phone = '15168368432' and user_status = 'INCUMBENCY' limit 1")#拓房人信息
            base.type_combotree(houseAddPage.typeMould['did'], user[1])
            base.type_select(houseAddPage.typeMould['uid'], user[0])
            # 出租信息
            base.type_click(houseAddPage.typeMould['house_status'])
            base.type_select(houseAddPage.typeMould['source'], 'INTRODUCE')
            base.input_text(houseAddPage.houseAddMould['rental_price'], 3000)
            #详细信息
            base.type_select(houseAddPage.typeMould['rooms'], '1')
            base.type_select(houseAddPage.typeMould['livings'], '1')
            base.type_select(houseAddPage.typeMould['kitchens'], '1')
            base.type_select(houseAddPage.typeMould['bathrooms'], '1')
            base.type_select(houseAddPage.typeMould['balconys'], '1')
            base.input_text(houseAddPage.houseAddMould['build_area'], '60.00')  # 面积
            base.type_select(houseAddPage.typeMould['orientation'], 'NORTH')
            base.type_select(houseAddPage.typeMould['property_type'], 'MULTI_LIFE')
            base.type_select(houseAddPage.typeMould['property_use'], 'HOUSE')
            base.type_select(houseAddPage.typeMould['fitment_type'], 'FITMENT_ROUGH')
            base.type_select(houseAddPage.typeMould['remark'], u'Atuo备注信息')
            base.type_select(houseAddPage.typeMould['look_type'], 'DIRECTION')
            base.type_select(houseAddPage.typeMould['look_date'], u'2017-09-06')
            base.click(houseAddPage.houseAddMould['form_btn'])  # 保存
            if testData:
                consoleLog(u'测试数据房源新增成功')
            else:
                consoleLog(u'随机数据房源新增成功，物业地址为：%s%s%s%s' % (base.house[0], base.house[1], base.house[2], base.house[3]),
                           level='w')
                set_conf('residential', residentialName=base.house[0], buildingName=base.house[1], unitName=base.house[2],
                         housenoname=base.house[3],
                         residentialid=base.house[4], buildingid=base.house[5], unitid=base.house[6], housenoid=base.house[7])
    try:
        base = Base()
        base.open(page.houseAddPage, houseAddPage.houseAddMould['test'], havaFrame=False)
        sqltHouse = "SELECT * from residential where residential_name = '%s' and deleted = 0" % get_conf('residential','residentialname').encode('utf-8')#获取配置文件中的房源
        if sqlbase.get_count(sqltHouse) != 0:
            # 基本信息
            base.input_text(houseAddPage.houseAddMould['property_name'], get_conf('residential', 'residentialname')[:-1])
            base.click(houseAddPage.houseAddMould['property_name_click'])
            base.input_text(houseAddPage.houseAddMould['contact_people'], 'AutoTest')
            base.input_text(houseAddPage.houseAddMould['building_name_search'], get_conf('residential', 'buildingname')[:-1])
            base.click(houseAddPage.houseAddMould['buidlding_click'])
            if get_conf('testCondition', 'test') == 'test':
                base.click(houseAddPage.houseAddMould['add_contact_btn'])
                base.input_text(houseAddPage.houseAddMould['contact_tel2'], '18279881085')
                base.click(houseAddPage.houseAddMould['save_contact_btn'])
            elif get_conf('testCondition', 'test') == 'mock':
                base.input_text(houseAddPage.houseAddMould['contact_tel1'], '18279881085')
            base.input_text(houseAddPage.houseAddMould['unit_search'], get_conf('residential', 'unitname')[:-1])
            base.script("$('[style=\"display: block;\"]')[1].click()")
            base.input_text(houseAddPage.houseAddMould['contact_people'], 'AutoTest')
            base.input_text(houseAddPage.houseAddMould['house_no_search'], get_conf('residential', 'housenoname'))
            base.script("$('[style=\"display: block;\"]')[2].click()")
            base.input_text(houseAddPage.houseAddMould['contact_people'], 'AutoTest')
            common(True)
        else:#如果配置文件中没有房源就从数据库提取符合条件的房源数据
            sql_house_info = "SELECT rr.residential_name, rb.building_name, rbu.unit_name, rbhn.house_no, rr.residential_id, rb.building_id, rbu.unit_id, rbhn.house_no_id " \
                             "FROM residential rr INNER JOIN residential_building rb ON rr.residential_id = rb.residential_id INNER JOIN residential_building_unit rbu ON rb.building_id" \
                             " = rbu.building_id INNER JOIN residential_building_house_no rbhn ON rbhn.building_id = rbu.building_id WHERE rr.deleted = 0 AND rr.city_code = '330100' " \
                             "AND NOT EXISTS ( SELECT 1 FROM house_develop hdd WHERE hdd.city_code = '330100' AND hdd.house_no_id = rbhn.house_no_id ) LIMIT 1"
            house_info = sqlbase.serach(sql_house_info, False)
            base.house = house_info
            base.input_text(houseAddPage.houseAddMould['property_name'], house_info[0][:-1])
            base.click(houseAddPage.houseAddMould['property_name_click'])
            base.input_text(houseAddPage.houseAddMould['contact_people'], 'AutoTest')
            base.input_text(houseAddPage.houseAddMould['building_name_search'], house_info[1][:-1])
            base.click(houseAddPage.houseAddMould['buidlding_click'])
            if get_conf('testCondition', 'test') == 'test':
                base.click(houseAddPage.houseAddMould['add_contact_btn'])
                base.input_text(houseAddPage.houseAddMould['contact_tel2'], '18279881085')
                base.click(houseAddPage.houseAddMould['save_contact_btn'])
            elif get_conf('testCondition', 'test') == 'mock':
                base.input_text(houseAddPage.houseAddMould['contact_tel1'], '18279881085')
            base.input_text(houseAddPage.houseAddMould['unit_search'], house_info[2][:-1])
            base.script("$('[style=\"display: block;\"]')[1].click()")
            base.input_text(houseAddPage.houseAddMould['contact_people'], 'AutoTest')
            base.input_text(houseAddPage.houseAddMould['house_no_search'], house_info[3])
            base.script("$('[style=\"display: block;\"]')[2].click()")
            base.input_text(houseAddPage.houseAddMould['contact_people'], 'AutoTest')
            common(False)
    finally:
        base.driver.quit()

addHouse()
