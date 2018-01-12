# -*- coding:utf8 -*-

from selenium.webdriver.common.by import By



searchResidentialModule = {
	'residential_name' : (By.ID,'residential_name'),
	'search_btn' : (By.ID,'search_btn'),
	'reset_btn' : (By,'reset_btn'),
	'tr_residential' : (By.CSS_SELECTOR,'tr[datagrid-row-index="0"]'),
	'all_tr_count' : (By.CSS_SELECTOR,'.datagrid-btable > tbody > tr')
}
addResidentialMould = {
	# 楼盘地址
	'add_btn' : (By.ID, 'add_btn'),  # 新增楼盘
	'residential_name': (By.CSS_SELECTOR,'#residential_name + span > input'),  #楼盘名称
	'residential_jianpin': (By.CSS_SELECTOR,'#residential_jianpin + span > input '), #楼盘简拼
	'byname_btn': (By.ID, 'other_contact_btn'), #楼盘别名添加按钮
	'byname': (By.CSS_SELECTOR, '#byname + span > input'), #楼盘别名
	'save_button_btn': (By.ID, 'contact_form_btn'), # 保存
	'address': (By.CSS_SELECTOR, '#address + span > input:nth-child(1)'),#街道地址
	'get_location_btn': (By.ID, 'get_btn'), #获取经纬度
	'search_address': (By.ID, 'tipinput'), #输入关键字
	'map_point' : (By.CLASS_NAME,'amap_lib_placeSearch_poi'),
	'search_map_btn': (By.ID, 'searchMap'), # 点击查询
	'save_location_btn': (By.ID, 'add_geo_btn'),#保存经纬度
	# 基础信息
	'department'  : 'body > div:nth-child(23) > div > ul > li > ul > li:nth-child(2) > ul > li:nth-child(1) > ul > li:nth-child(1) > ul > li:nth-child(1) > div > span:nth-child(7)',#责任部门
	'build_date': (By.CSS_SELECTOR, '#build_date + span > input'),  # 建筑年代
	'totle_buildings' : (By.CSS_SELECTOR,'#totle_buildings + span > input'),#总栋数
	'total_unit_count': (By.CSS_SELECTOR, '#total_unit_count + span > input'),  #总单元数
	'total_house_count': (By.CSS_SELECTOR, '#total_house_count + span > input'),  #总户数
	'build_area': (By.CSS_SELECTOR, '#build_area + span > input'),  #占地面积
	'property_company': (By.ID, 'property_company'),  #物业公司
	'property_fee': (By.ID, 'property_fee'),  #物业费
	'plot_ratio': (By.CSS_SELECTOR, '#plot_ratio + span > input'),  # 容积率
	'green_rate': (By.CSS_SELECTOR, '#green_rate + span > input'),  # 绿化率
	'parking_amount': (By.CSS_SELECTOR, '#parking_amount + span > input'),  # 车位数
	'other_info': (By.ID, 'other_info'),  # 楼盘亮点
	# 周边配套，图片，保存
	'bus_stations': (By.ID, 'bus_stations'),#公交站
	'metro_stations': (By.ID, 'metro_stations'), #地铁站
	'roomsFileUpload_btn': (By.CSS_SELECTOR,'#base_img > table > tbody > tr > td > a'),#图片上传
	'submit_btn': (By.ID, 'form_btn'),#保存
	#栋座信息
	'building_info_btn' : (By.CSS_SELECTOR,'#residential + div > div:nth-child(2) > div > div:nth-child(2) > div:nth-child(2) > table > tbody > tr:nth-child(1) > td:nth-child(17) > div > button:nth-child(2)'), #栋座信息按钮
	'add_building_btn': (By.CSS_SELECTOR, '#ResidentialBuilding_table > div > a'),  # 新增楼座
	'building_name': (By.CSS_SELECTOR, '#residential_building_info > table > tbody > tr:nth-child(2) > td:nth-child(2) > input'),# 栋座名称
	'lng_lat_btn': (By.ID, 'get_btn'),  # 经纬度
	'input_searchMap': (By.CSS_SELECTOR, '#myPageTop > table > tbody > tr:nth-child(2) > td:nth-child(1) > input'),# 关键字输入框
	'searchMap_btn': (By.ID, 'searchMap'),  # 查询
	'save_lng_lat_btn': (By.ID, 'add_geo_btn'),  # 保存
	'ground_floors': '#ground_floors',  # 地面层数
	'underground_floors': '#underground_floors',  # 地下层数
	'ladder_count': '#ladder_count',  # 梯数
	'house_count': '#house_count',  # 户数
	#单元信息
	'unit_info_btn': (By.CSS_SELECTOR, '#buliding + div > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > table > tbody > tr:nth-child(1) > td:nth-child(11) > div > button:nth-child(1)'),  # 单元信息
	'add_unit_btn ': (By.CSS_SELECTOR, '#ResidentialBuildingUnit_table > div > a'),  # 新增
	'unit_name': (By.ID, 'unit_name'),  # 单元名称
	'save_unitname_btn': (By.ID, 'form_btn'),  # 保存
	#楼层信息
	'floor_info_btn': (By.CSS_SELECTOR, '#buliding_unit + div > div:nth-child(2) > div > div:nth-child(2) > div:nth-child(2) > table > tbody > tr > td:nth-child(4) > div > button:nth-child(1)'),# 楼层信息
	'add_floor_btn': (By.CSS_SELECTOR, '#ResidentialBuildingFloor_table > div > a'),  # 新增
	'floor_name': (By.ID, 'floor_name'),  # 楼层名称
	#房号信息
	'house_info_btn': (By.CSS_SELECTOR, '#buliding_floor + div > div > div > div> div > table > tbody > tr > td:nth-child(4) > div > button:nth-child(1)'),# 房号信息
	'add_house_btn': (By.CSS_SELECTOR, '#ResidentialBuildingHouseNo_table > div >a '),  # 新增
	'house_no': (By.ID, 'house_no')  # 房号名称
}

typeMould = {
	'area_code': '#area_code ',  # 城区-
	'business_circle_name': '#taBusinessCircleString '  ,# 商圈
	'property_type': '#property_type ',  # 物业类型
	'property_use': '#housing_type',  # 物业用途
	'department_loc' : '#taDepartString'	#责任部门
	}



