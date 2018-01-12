# -*- coding:utf8 -*-
from common.base import log,consoleLog,Base,set_conf
from common import page
from common import sqlbase
import time
from house.residential import  residentiaPage


@log
def addResidential():
    """新增楼盘"""
    try:
        mybase = Base()
        mybase.open(page.residentiaPage, residentiaPage.searchResidentialModule['search_btn'], havaFrame=False)#
        # url = 'http://isz.ishangzu.com/isz_house/ResidentialController/searchResidentialList.action'
        # data = {"city_code":"330100","residential_name":"AutoTest","pageNumber":1,"pageSize":30,"sort":"t.create_time","order":"desc"}
        # if request(url,data=data) >= 1:
        # 	consoleLog('已有测试楼盘 AutoTest，跳过新增',level='w')
        # 楼盘地址
        residentialName = 'AutoTest' + '-' + time.strftime('%m%d-%H%M%S')#定义楼盘名称
        mybase.click(residentiaPage.addResidentialMould['add_btn'])#新增
        mybase.input_text(residentiaPage.addResidentialMould['residential_name'], residentialName)#楼盘名称
        mybase.click(residentiaPage.addResidentialMould['residential_jianpin'])#简拼
        mybase.click(residentiaPage.addResidentialMould['byname_btn'])#楼盘别买添加
        mybase.input_text(residentiaPage.addResidentialMould['byname'], 'auto')#楼盘别名
        mybase.click(residentiaPage.addResidentialMould['save_button_btn'])#别名保存
        mybase.type_select(residentiaPage.typeMould['area_code'], "330102") # 城区：上城区
        mybase.type_select(residentiaPage.typeMould['business_circle_name'], "35") #商圈：四季青
        mybase.input_text(residentiaPage.addResidentialMould['address'], u'自动化测试街道地址')#街道
        mybase.click(residentiaPage.addResidentialMould['get_location_btn'])#获取经纬
        mybase.input_text(residentiaPage.addResidentialMould['search_address'], u'海创基地')#地址关键字
        mybase.click(residentiaPage.addResidentialMould['search_map_btn'])#查询
        mybase.click(residentiaPage.addResidentialMould['search_address'])#点击输入框
        mybase.click(residentiaPage.addResidentialMould['map_point'])#
        mybase.click(residentiaPage.addResidentialMould['save_location_btn'])#保存
        # 基础信息
        mybase.type_select(residentiaPage.typeMould['property_type'], 'ordinary')#
        sql = "SELECT sd.parent_id from sys_department sd INNER JOIN sys_user sur on sur.dep_id = sd.dep_id INNER JOIN sys_position spt on spt.position_id = sur.position_id " \
              "where sd.dep_district = '330100' and sd.dep_id <> '00000000000000000000000000000000' and (spt.position_name like '资产管家%' or spt.position_name like '综合管家%') ORDER BY RAND() LIMIT 1"
        mybase.type_combotree(residentiaPage.typeMould['department_loc'], sqlbase.serach(sql)[0])#
        mybase.input_text(residentiaPage.addResidentialMould['build_date'], 1988)#
        mybase.input_text(residentiaPage.addResidentialMould['totle_buildings'], 10)#
        mybase.input_text(residentiaPage.addResidentialMould['total_unit_count'], 30)#
        mybase.input_text(residentiaPage.addResidentialMould['total_house_count'], 20)#
        mybase.input_text(residentiaPage.addResidentialMould['build_area'], 400)#
        mybase.input_text(residentiaPage.addResidentialMould['property_company'], u'杭州爱上租物业有限公司')#
        mybase.input_text(residentiaPage.addResidentialMould['property_fee'], 2)#
        mybase.input_text(residentiaPage.addResidentialMould['plot_ratio'], 80)#
        mybase.input_text(residentiaPage.addResidentialMould['green_rate'], 20)#
        mybase.input_text(residentiaPage.addResidentialMould['parking_amount'], 200)#
        mybase.input_text(residentiaPage.addResidentialMould['other_info'], u'临近公交地铁，附近有超市，环境优美')#
        # 周边配套，图片
        mybase.input_text(residentiaPage.addResidentialMould['bus_stations'], u'六合桥')#
        mybase.input_text(residentiaPage.addResidentialMould['metro_stations'], u'滨江站')#
        # 提交新增楼盘字典
        mybase.click(residentiaPage.addResidentialMould['submit_btn'])#
        mybase.check_submit()
        consoleLog(u'楼盘 %s 新增成功' % residentialName)#
        # 栋座
        mybase.input_text(residentiaPage.searchResidentialModule['residential_name'], residentialName)#
        mybase.click(residentiaPage.searchResidentialModule['search_btn'])#
        mybase.staleness_of(residentiaPage.searchResidentialModule['tr_residential'])#
        mybase.click(residentiaPage.addResidentialMould['building_info_btn'])#
        mybase.click(residentiaPage.addResidentialMould['add_building_btn'])#
        mybase.input_text(residentiaPage.addResidentialMould['building_name'], 'Building')#
        mybase.click(residentiaPage.addResidentialMould['lng_lat_btn'])#
        mybase.input_text(residentiaPage.addResidentialMould['input_searchMap'], u'逸天广场')#
        mybase.click(residentiaPage.addResidentialMould['input_searchMap'])#
        mybase.click(residentiaPage.addResidentialMould['searchMap_btn'])#
        mybase.click(residentiaPage.addResidentialMould['save_lng_lat_btn'])#
        mybase.type_select(residentiaPage.typeMould['property_use'], 'ordinary')#
        mybase.type_select(residentiaPage.addResidentialMould['ground_floors'], 10)#
        mybase.type_select(residentiaPage.addResidentialMould['underground_floors'], 2)#
        mybase.type_select(residentiaPage.addResidentialMould['ladder_count'], 30)#
        mybase.type_select(residentiaPage.addResidentialMould['house_count'], 100)#
        mybase.click(residentiaPage.addResidentialMould['save_unitname_btn'])#
        # 单元
        mybase.click(residentiaPage.addResidentialMould['unit_info_btn'])#
        mybase.click(residentiaPage.addResidentialMould['add_unit_btn '])#
        mybase.input_text(residentiaPage.addResidentialMould['unit_name'], 'Unit')#
        mybase.click(residentiaPage.addResidentialMould['save_unitname_btn'])#
        # 楼层
        mybase.click(residentiaPage.addResidentialMould['floor_info_btn'])#
        mybase.click(residentiaPage.addResidentialMould['add_floor_btn'])#
        mybase.input_text(residentiaPage.addResidentialMould['floor_name'], 'Floor')#
        mybase.click(residentiaPage.addResidentialMould['save_unitname_btn'])#
        # 房号
        mybase.click(residentiaPage.addResidentialMould['house_info_btn'])#
        mybase.click(residentiaPage.addResidentialMould['add_house_btn'])#
        mybase.input_text(residentiaPage.addResidentialMould['house_no'], 'Houseno')
        mybase.click(residentiaPage.addResidentialMould['save_unitname_btn'])#
        consoleLog(u'栋座相关新增成功')
    finally:
        mybase.driver.quit()

addResidential()


