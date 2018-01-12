# -*- coding:utf8 -*-
from common.base import log,consoleLog,Base
from common import page
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from common import sqlbase
from house.residential import residentiaPage
from selenium.webdriver.support.wait import WebDriverWait

@log
def addResidential():
    """删除楼盘"""
    try:
        mybase = Base()
        mybase.open(page.residentiaPage, residentiaPage.searchResidentialModule['search_btn'], havaFrame=False);consoleLog(u'打开JSP页面')
        # mybase.open(Page.residentiaPage, (By.ID, 'search_btn'), havaFrame=False)
        sql = 'select residential_name from residential where residential_name like "AutoTest-%" and deleted<>1'
        ResidentiaName = sqlbase.serach(sql)[0];consoleLog(u'查询结果：%s' % ResidentiaName)
        # ResidentiaName='AutoTest-0706-103107'
        mybase.input_text((By.CSS_SELECTOR, "#residential_name"), ResidentiaName,event=u'输入楼盘名称：')\
            # ;consoleLog(u'输入楼盘名称')
        mybase.click((By.ID, 'search_btn'));consoleLog(u'点击查找')
        mybase.staleness_of(residentiaPage.searchResidentialModule['tr_residential']);consoleLog(u'等待数据刷新')
        mybase.click((By.CSS_SELECTOR,
                           '#residential + div > div:nth-child(2) > div > div:nth-child(2) > div:nth-child(2) > table > tbody > tr:nth-child(1) > td:nth-child(17) > div > button:nth-child(5)'));consoleLog(u'点击删除')  # 点击删除
        mybase.click((By.CSS_SELECTOR, 'div>a>span>span'),1);consoleLog(u'确定删除')  # 点击确定
        mybase.click((By.ID, 'search_btn'));consoleLog(u'再次查找')  # 再次查找
        try:
            WebDriverWait(mybase.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                                                   '#residential + div > div:nth-child(2) > div > div:nth-child(2) > div:nth-child(2) > table > tbody > tr:nth-child(1) > td:nth-child(11) ')),
                                                 u'未找确定楼盘 %s 信息' % ResidentiaName)
            raise Exception(u'楼盘 %s 信息存在，删除失败'%ResidentiaName)
        except u'未找确定楼盘 %s 信息' % ResidentiaName:
            consoleLog(u'楼盘删除成功')
    finally:
        mybase.driver.quit()

addResidential()


