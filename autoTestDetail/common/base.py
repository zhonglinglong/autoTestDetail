# -*- coding:utf8 -*-
# Author : Wu Jun
# Create on : 2017 - 04 -24

from selenium import webdriver
from user import loginPage
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import  ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
import logging
import ConfigParser
import os
import requests
import re
import json
import time
import yaml
import random
import string



logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)
path = os.path.dirname(
    os.path.join(
        os.path.split(
            os.path.realpath(__file__))[0])) + '\\test.log'
fileHandler = logging.FileHandler(path)
consoleHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(process)s - %(levelname)s : %(message)s')
fileHandler.setFormatter(formatter)
consoleHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)

currentDriver = None


def log(func):
    def wrapper(*args, **kwargs):
        info = func.__doc__
        logger.info('testing at : %s' % info.decode('utf-8'))
        try:
            return func(*args, **kwargs)
        except BaseException:
            if currentDriver:
                fileName = 'D:\\errorImage\\%s-%s.png' % (
                    info.decode('utf-8'), time.strftime('%H%M%S'))
                currentDriver.driver.save_screenshot(fileName)
                currentDriver.driver.quit()
            logger.exception('Exception')
            # caseID = func.func_name.split('_')[-1]
            # caseInfo = get_yaml(int(caseID))
            # consoleLog('\n' + caseInfo) if caseInfo != '' else None
            consoleLog(func.__doc__, level='e', fromAssert=False)
        finally:
            currentDriver.driver.quit() if currentDriver else None
    return wrapper


def consoleLog(msg, level='i', fromAssert=True):
    """
    对错误的记录，写进log文件中，对于error级别的适用于断言，如存在这种用例：删除合同后，判断合同表中的deleted的字段是否为1或者再查询，是否还能查到，此时，如果不为1或者还能查到
    则调用此方法，定义为error级别
    :param msg: 需要写入的描述，如’合同删除后deleted未变成0‘
    :param level: 定义日志级别，分为i:info  w:warning  e:error
    """
    if level is 'i':
        logger.info(msg)
    elif level is 'w':
        logger.warning(msg)
    elif level is 'e':
        if fromAssert:
            logger.error('one assert at : \n%s\n' % msg)
        else:
            logger.error('======================================== one error at "%s" ========================================' % msg)

def get_fileName():
    return os.path.basename(__file__).split('.')[0]

def get_randomString():
    return ''.join(random.sample(string.ascii_letters + string.digits, 4))


def get_conf(section, option, valueType=str):
    config = ConfigParser.ConfigParser()
    path = os.path.join(os.path.split(os.path.realpath(__file__))[0]) + '\conf.ini'
    config.read(path)
    if valueType is str:
        value = config.get(section, option)
        return value
    elif valueType is int:
        value = config.getint(section, option)
        return value
    elif valueType is bool:
        value = config.getboolean(section, option)
        return value
    elif valueType is float:
        value = config.getfloat(section, option)
        return value
    else:
        value = config.get(section, option)
        return value.decode('utf-8')


def set_conf(section, **value):
    config = ConfigParser.ConfigParser()
    path = os.path.join(os.path.split(os.path.realpath(__file__))[0]) + '\conf.ini'
    config.read(path)
    for k,v in value.items():
        if type(v) is unicode:
            config.set(section,k,v.encode('utf-8'))
        else:
            config.set(section, k, v)
    config.write(open(path, 'w'))


def get_cookie(driver):
    cookies = driver.get_cookies()
    CROSS_ISZ_SESSIONID = ''
    ISZ_SESSIONID = ''
    for cookie in cookies:
        if 'name' in cookie:
            if cookie['name'] == 'ISZ_SESSIONID':
                ISZ_SESSIONID = cookie['value']
            if cookie['name'] == 'CROSS_ISZ_SESSIONID':
                CROSS_ISZ_SESSIONID = cookie['value']
    cookie = {}
    cookie['ISZ_SESSIONID'] = ISZ_SESSIONID.encode('utf-8')
    cookie['CROSS_ISZ_SESSIONID'] = CROSS_ISZ_SESSIONID.encode('utf-8')
    return cookie


def get_yaml(id):
    """
    断言失败的情况下，将case信息打印至log
    :param id: 对应的case序号
    :return: case信息
    """
    path = os.path.join(os.path.split(os.path.realpath(__file__))[0]) + '\\testCase.yaml'
    yy = yaml.load(open(path).read())
    caseInfo = ''
    for module in yy:
        if not isinstance(yy[module], str):
            for caseName in yy[module]:
                if type(yy[module][caseName]) is not str:
                    for caseExplain in yy[module][caseName]:
                        if type(yy[module][caseName][caseExplain]) is not str:
                            if yy[module][caseName][caseExplain]['序号'.decode('utf-8')] == id:
                                for key,info in yy[module][caseName][caseExplain].items():
                                    if type(info) is int:
                                        caseInfo += u'案例描述：' + caseExplain + '\n' + key + u'：' + str(id) + '\n'
                                    else:
                                        for i in info:
                                            caseInfo += key + u'：' + i + '\n'
    return caseInfo

def request(url,needCookie=True,data=None,contentType='application/json',method='post',**params):
    headers = {
        'content-type': contentType,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
    }
    if needCookie:
        cookie = eval(get_conf('cookieInfo', 'cookies'))
        if method == 'get':
            if params:
                text = requests.get(url, params).text
                pass
            else:
                pass
        if method == 'post':
            r = requests.post(url,data=json.dumps(data),headers=headers,cookies = cookie)
            text = r.text.encode('utf-8')
            if r.status_code == 200:
                count = int(re.findall('"total":(.*?)}',text)[0])
                return count
            else:
                info = 'url : %s \n data : %s \n cookie : %s \n value : %s' % (url,data,cookie,text)
                consoleLog(u'当前接口异常：' + info,level='e')
    else:
        if method == 'get':
            pass
        if method == 'post':
            pass


def clearConf():
    config = ConfigParser.ConfigParser()
    config.read('conf.ini')
    sections = config.sections()
    sections.remove('db')
    sections.remove('testCondition')
    sections.remove('host')
    for x in sections:
        for y in config.options(x):
            config.set(x, y)
    config.write(open('conf.ini', 'w'))

def hostSet(condition):
    set_conf('testCondition', test=condition)
    filepath = r'C:\Windows\System32\drivers\etc\hosts'
    hosts = None
    f = open(filepath, 'w')
    if condition == 'test':
        set_conf('db', host='192.168.0.208', user='wujun', password='wujun', db='isz_erp_npd', charset='utf8')
        hosts = get_conf('host','test')
    elif condition == 'mock':
        set_conf('db', host='192.168.0.208', user='wujun', password='wujun', db='isz_erp', charset='utf8')
        hosts = get_conf('host','mock')
    f.write(hosts)
    f.close()


def solr(core, condition):
    """
    房源的solr增量
    :param core: 目前为house或者apartment
    :param condition: test或者mock
    :return: 无返回
    """
    url = {
        'house': {
            'test': 'http://192.168.0.216:8080/solr/house_core/dataimport',
            'mock': 'http://192.168.0.216:8080/solr/apartment_core/dataimport'
        },
        'apartment': {
            'test': 'http://192.168.0.203:8080/solr/house_core/dataimport',
            'mock': 'http://192.168.0.203:8080/solr/apartment_core/dataimport'
        }
    }
    data = 'command=delta-import&commit=true&wt=json&indent=true&verbose=false&clean=false&optimize=false&debug=false'
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
    }
    re = requests.post(url[core][condition], data, headers=headers)
    if re.status_code is 200:
        consoleLog(u'%s-core 执行成功' % core)
    else:
        consoleLog(u'%s-core 执行异常！' % core, 'w')

class Base(object):
    """
    Base封装所有页面都公用的方法，例如各种定位、等待、点击、输入等
    """
    _instance = None
    instanceCount = 0

    def __new__(self, *args, **kw):
        """
        使用单例模式：控制同一线程只启动一个实例
        """
        if not self._instance:
            self._instance = super(Base, self).__new__(self, *args, **kw)
            Base.instanceCount += 1
        return self._instance

    def __init__(self, **kw):
        """
        实例化WebDriver对象并登录
        """
        if kw['debug']:
            self.driver = webdriver.Chrome()
        else:
            if self.instanceCount == 1:
                self.instanceCount += 1
                self.driver = webdriver.Chrome()
                self.driver.implicitly_wait(10)
                self.open('http://isz.ishangzu.com/isz_base/', loginPage.userNameInput)
                self.input_text(loginPage.userNameInput, get_conf('loginUser', 'user'))
                self.input_text(loginPage.passWordInput, get_conf('loginUser', 'pwd'))
                self.click(loginPage.loginButton)
                set_conf('cookieInfo', cookies=get_cookie(self.driver))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # if exc_type is not None:
        #     global currentDriver
        #     currentDriver = self
        global currentDriver
        currentDriver = self
        return False

    def diffAssert(self, func, id, msg):
        """
        断言方法，与实际与预期结果做对比
        :param func: 匿名函数：直接使用Base类的实例化对象asserts，如diffAssert(lambda test:asserts('实际值).is_equal_to('预期值'),'实际值与预期值不一致')
        :param id: case对应的序号
        :param msg:不一样的情况下的说明
        :return:无返回结果
        """
        try:
            func('test')
        except:
            caseInfo = get_yaml(int(id))
            consoleLog('\n' + caseInfo + '\n' + u'实际结果：' + msg, level='e', fromAssert=True)

    def open(self, url, loc=None, havaFrame=False, needCheck=True):
        """
        重写打开地址函数
        :param url: 目标地址
        :param loc: 接收一个By对象的元组，用以确认页面加载完成
        :param havaFrame:是否需要切进frame
        """
        self.driver.get(url)
        if havaFrame:
            self.switch_frame(0)
        if needCheck:
            WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(loc))
        self.driver.maximize_window()

    def whetherPresence(self, loc):
        """判断传入对象是否存在"""
        try:
            self.driver.find_element(*loc)
            return True
        except:
            return False

    def staleness_of(self, loc, index=None):
        """
        此方法主要适用情况如合同初审后，需要再次双击列表页打开进行复审的操作。
        初审后dialog会关闭，此时列表页会重新刷新，此时若去双击会报StaleElementReferenceException，所以在此显示等待
        """
        if type(index) == int:
            # eles = self.find_elements(index, *loc)
            try:
                WebDriverWait(self.driver, 15).until(EC.staleness_of(self.find_elements(index, *loc)))
            except TimeoutException:
                pass
        else:
            # ele = self.find_element(*loc)
            try:
                WebDriverWait(self.driver, 15).until(EC.staleness_of(self.find_element(*loc)))
            except TimeoutException:
                pass

    def wait_element(self, loc):
        """
        等待目标元素出现
        :param loc: 接收一个By对象的元组，用以确认页面加载完成
        """
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(loc), message=u'等待元素未出现，请查看截图')

    def find_element(self,*loc):
        """
        返回单个元素定位
        """
        try:
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(loc), u'未找到指定元素')
        except BaseException:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(loc))
        return self.driver.find_element(*loc)

    def find_elements(self, index, *loc):
        """
        返回多个元素定位
        :param index: 定位目标为数组时，需指定所需元素在数组中的位置
        """
        try:
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(loc))
        except BaseException:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(loc))
        if index != None:
            return self.driver.find_elements(*loc)[index]
        else:
            return self.driver.find_elements(*loc)

    def send_keys(self,loc,keys):
        self.find_element(*loc).send_keys(keys)

    def upload_file(self, loc, path):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(loc), message=u'上传元素未出现')
        self.driver.find_element(*loc).send_keys(path)

    def check_submit(self):
        """
        等待提交完成的提示出现，如新增或修改数据后的保存成功等提示，以确认数据正常插入或更新。目前所有界面的提示存在时长为3s，所以等待3s
        PS：一开始加这么长时间的硬性等待，我是拒绝的，但后面发现很多界面的操作必须要等待这个提示完全消失才可以，我尝试了各种办法也做不到完全避免，所以妥协了，硬等待就硬等待吧
        :param loc: 提示的元素定位
        """
        loc = (
            By.CSS_SELECTOR,
            '.bootstrap-growl.alert.alert-info.alert-dismissible')
        WebDriverWait(
            self.driver,
            20).until(
            EC.presence_of_element_located(loc),
            u'没有找到提交成功记录')
        time.sleep(3)

    def input_text(self, loc, text,index = None):
        """
        重写send_keys方法
        :param loc:目标元素
        :param text:输入值
        :param first:默认为输入框无内容，为False时则先清空再输入
        :param index:定位目标为数组时，需指定所需元素在数组中的位置
        """
        if type(index) == int:
            eles = self.find_elements(index,*loc)
            for i in range(10):
                try:
                    eles.click()
                    break
                except WebDriverException:
                    time.sleep(1)
            eles.clear()
            eles.send_keys(text)
        else:
            ele = self.find_element(*loc)
            for i in range(10):
                try:
                    ele.click()
                    break
                except WebDriverException:
                    time.sleep(1)
            ele.clear()
            ele.send_keys(text)

    def click(self, loc,index = None):
        """
        重写click方法
        :param index: 默认为定位单个元素点击，如定位返回数组，则调用多个元素定位方法
        """
        #WebDriverWait(self.driver,10).until(EC.element_to_be_clickable(loc),u'元素不可点击')
        if type(index) == int:
            eles = self.find_elements(index,*loc)
            for i in range(10):
                try:
                    eles.click()
                    break
                except WebDriverException:
                    time.sleep(1)
        else:
            ele = self.find_element(*loc)
            for i in range(10):
                try:
                    ele.click()
                    break
                except WebDriverException:
                    time.sleep(1)

    def dblclick(self,loc,index = None,checkLoc = None):
        """
        重写双击方法
        :param loc: 可执行双击的元素  （注：需核实元素是否有双击事件，如定位到tr中的某一个td时，双击是无效的，对tr的双击才有效。
        是否有效，可在chrome的console中验证，如$('#test'）.dblclick()
        :param index:默认为定位单个元素点击，如定位返回数组，则调用多个元素定位方法
        :param checkLoc:传递一个打开后的界面中的元素，用以确认双击成功打开详情页
        """
        if type(index) == int:
            for i in range(10):
                eles = self.find_elements(index, *loc)
                try:
                    ActionChains(self.driver).double_click(eles).perform()
                    if checkLoc != None:
                        for i in range(10):
                            try:
                                self.driver.find_element(*checkLoc)
                                break
                            except NoSuchElementException:
                                ActionChains(self.driver).double_click(eles).perform()
                    break
                except StaleElementReferenceException:
                    time.sleep(1)
        else:
            for i in range(5):
                ele = self.find_element(*loc)
                try:
                    ActionChains(self.driver).double_click(ele).perform()
                    if checkLoc != None:
                        for i in range(10):
                            try:
                                self.driver.find_element(*checkLoc)
                                break
                            except NoSuchElementException:
                                e = self.find_element(*loc)
                                ActionChains(self.driver).double_click(e).perform()
                    break
                except StaleElementReferenceException:
                    time.sleep(1)

    def context_click(self,loc,index = None):
        """
        重写右击方法
        :param loc: 可执行右击的元素
        :param index: 默认为定位单个元素点击，如定位返回数组，则调用多个元素定位方法
        """
        if type(index) == int:
            eles = self.find_elements(index,*loc)
            ActionChains(self.driver).context_click(eles).perform()
        else:
            ele = self.find_element(*loc)
            ActionChains(self.driver).context_click(ele).perform()

    def switch_frame(self, loc):
        self.driver.switch_to_frame(loc)

    def script(self, js,returnValue=False):
        """
        尽量少用js，因为执行速度远远高于网络和系统反应速度，很容易报错。
        迫不得已用到js的情况下无外乎点击、传值等，如果太快页面没刷新过来会导致报WebDriverException（目前已知会报出WebDriverException），此处捕获后，等待1秒再次执行js，最多十次，若执行成功则跳出循环
        :param js:
        :return:
        """
        for i in range(10):
            try:
                if returnValue:
                    value = self.driver.execute_script(js)
                    return value
                else:
                    self.driver.execute_script(js)
                break
            except WebDriverException,e:
                # consoleLog(e)
                # consoleLog(u'js执行失败，正进行第%s次尝试' % str(i+1).decode('utf-8'))
                time.sleep(1)

    def type_date(self, loc, dateValue):
        """
        定义type_date方法，用于处理日期控件的传参
        :param loc: 接收jquery的选择器的值，如 #id  .class  css选择器，不是page页面中定义的元素元组
        :param dateValue: 具体时间值，格式如2017-01-02
        """
        #js = "$(\"%s\").removeAttr('readonly');$(\"%s\").attr('value','%s')" % (loc,loc,date)
        #上面的是调用js原生方法，由于前段框架的问题，原生方法传参无效，需利用jquery调用easyui中的方法
        js = "$('%s').datebox('setValue','%s')" % (loc ,dateValue)
        self.script(js)
        time.sleep(0.2)

    def type_select(self, loc, selectedValue):
        """
        定义type_select方法，用于处理下拉控件的传参
        :param loc: 接收jquery的选择器的值，如 #id  .class  css选择器，不是page页面中定义的元素元组
        :param selectedValue: 由于页面在单击选择后，会传给后台key，而不是value，所以此处的传参为数据字典中的Key，而非value！！！
        """
        js = "$('%s').combobox('setValue','%s')" % (loc, selectedValue)
        self.script(js)
        time.sleep(0.2)

    def type_combotree(self, loc, selectedValue):
        """
        定义type_combotree方法，用于处理系统中下拉为tree的控件，如部门的选择
        :param loc: 接收jquery的选择器的值，如 #id  .class  css选择器，不是page页面中定义的元素元组
        :param selectedValue: 由于页面在单击选择后，会传给后台key，而不是value，所以此处的传参为数据字典中的Key，而非value！！！
        """
        js = r"$('%s').combotree('setValue','%s')" % (loc, selectedValue)
        self.script(js)
        time.sleep(0.2)

    def type_checkbox(self, loc, ischecked):
        """
        定义type_checkbox方法，用于处理复选框控件的传参
        :param loc: 接收jquery的选择器的值，如 #id  .class  css选择器，不是page页面中定义的元素元组
        :param ischecked: 为boolean值
        """
        js = r"$('%s').attr('checked','%s')" % (loc, ischecked)
        self.script(js)
        time.sleep(0.2)

    def scrollTo(self,loc,index = None):
        if type(index) == int:
            ele = self.find_elements(index, *loc)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", ele)
        else:
            ele = self.find_element(*loc)
            self.driver.execute_script("arguments[0].scrollIntoView(true);",ele)

    def search_wait(self, click_loc, wait_loc, index = None):
        """
        点击搜索或者重置之后，所等待的页面元素没有捕捉到，重新点击刷新页面
        :param click_loc: 点击的元素
        :param index:默认为定位单个元素点击，如定位返回数组，则调用多个元素定位方法
        :param wait_loc: 点击操作后页面刷新，用以确认页面元素是否出现
        """
        if type(index) == int:
            for i in range(5):
                eles = self.find_elements(index, *click_loc)
                try:
                    eles.click()
                    if wait_loc is not None:
                        for i in range(3):
                            try:
                                self.staleness_of(wait_loc)
                                break
                            except TimeoutException:
                                eles.click()
                    break
                except WebDriverException:
                    time.sleep(1)
        else:
            for i in range(5):
                ele = self.find_element(*click_loc)
                try:
                    ele.click()
                    if wait_loc is not None:
                        for i in range(3):
                            try:
                                self.staleness_of(wait_loc)
                                break
                            except TimeoutException:
                                ele.click()
                    break
                except WebDriverException:
                    time.sleep(1)

if __name__ == '__main__':
    pass





