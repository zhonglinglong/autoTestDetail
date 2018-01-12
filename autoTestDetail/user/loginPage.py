# -*- coding:utf8 -*-

from selenium.webdriver.common.by import By


#登录页面
userNameInput = (By.NAME, 'user_phone')
passWordInput = (By.NAME, 'user_pwd')
loginButton = (By.ID, 'login_btn')

#退出登录
yes = (By.CSS_SELECTOR,'.l-btn-text')
quit = (By.CSS_SELECTOR,'#logout > span')

#修改密码
oldpwd = (By.ID,'old_pwd')
newpwd = (By.ID,'user_pwd')
confirmpwd = (By.ID,'user_pwd_confirm')
submit = (By.ID,'submit_btn')




