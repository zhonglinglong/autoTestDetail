# -*- coding:utf8 -*-
from user import userPage
from common.base import log,consoleLog,Base
from common import page

@log
def addUser(username ,userphone ,userpost ,userrole ,usermail):
    """新增用户"""
    try:
        base=Base()
        base.open(page.userPage, userPage.addUser_loc, havaFrame=False)
        base.click(userPage.addUser_loc)
        base.input_text(userPage.addUserMould['user_name_loc'], username)
        base.type_combotree(userPage.addUserMould['user_dep_loc'], '00000000000000000000000000000000')
        base.input_text(userPage.addUserMould['user_phone_loc'], userphone)
        base.type_select(userPage.addUserMould['user_post_loc'], userpost)
        base.type_select(userPage.addUserMould['user_role_loc'], userrole)
        base.input_text(userPage.addUserMould['user_mail_loc'], usermail)
        base.click(userPage.addUserMould['submit_loc'])
        base.check_submit()
        consoleLog(u'新增用户成功')
    finally:
        base.driver.quit()

#定义用户参数
username=None
userphone=None
userpost=None
userrole=None
usermail=None

addUser(username ,userphone ,userpost ,userrole ,usermail)
