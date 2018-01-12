# -*- coding:utf8 -*-
from selenium.webdriver.common.by import By

searchUserMould = {
		'user_name_loc' : (By.ID, 'user_name_search'),
		'user_phone_loc' : (By.ID, 'user_phone_search'),
		'user_dep_loc_1' : (By.CSS_SELECTOR,'#search_panel > table > tbody > tr > td:nth-child(8) > span > span > a'),
		'user_dep_loc_2' : (By.CSS_SELECTOR,'body > div:nth-child(9) > div > ul > li > div > span:nth-child(3)'),	#部门下拉第一个
		'user_post_loc_1' : (By.CSS_SELECTOR,'#search_panel > table > tbody > tr > td:nth-child(10) > span > span > a'),
		'user_post_loc_2' : (By.CSS_SELECTOR,'body > div:nth-child(8) > div > div:nth-child(1)'),	#岗位下拉第一个
		'user_status_loc_1' : (By.CSS_SELECTOR,'#search_panel > table > tbody > tr > td:nth-child(12) > span > span > a'),
		'user_status_loc_2' : (By.CSS_SELECTOR,'body > div:nth-child(3) > div > div:nth-child(1)')	#用户状态下拉第一个
	}
addUser_loc = (By.ID,'add_btn')
addUserMould = {
		'user_name_loc' : (By.CSS_SELECTOR,'#user_name + span > input:nth-child(1)'),
		'user_dep_loc' : '.con-conditions > input#dep_id',
		'user_phone_loc' : (By.CSS_SELECTOR,'#user_phone + span > input:nth-child(1)'),
		'user_post_loc' : 'input#position_id',
		'user_role_loc' : 'input#role_id',
		'user_mail_loc' : (By.CSS_SELECTOR,'#user_email + span > input:nth-child(1)'),
		'submit_loc' : (By.ID,'submit_btn')
	}
