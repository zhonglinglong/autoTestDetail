# -*- coding:utf8 -*-

'''
调试case文件须引入 deBugProxy 模块中的 DeBugProxy 类
调试函数需传入参数 base，使用base正常调用Base类的变量和函数
完整拷贝 if __name__ == '__main__' 方法
'''

from deBugProxy import DeBugProxy
from selenium.webdriver.common.by import By

def get(base):
    base.open('http://baidu.com', needCheck=False)
    base.input_text((By.ID, 'kw'), 'python')
    base.click((By.ID, 'su'))

# 远程连接并且调用
if __name__ == '__main__':
    from multiprocessing.connection import Client
    debugClient = Client(('localhost', 17001), authkey='isz')
    proxy = DeBugProxy(debugClient)
    handler = proxy.add()