# -*- coding:utf8 -*-

'''
1、调试前需启动此server
2、__name__ == '__main__' 函数中需 import 待测试case文件
3、add 函数中 reload 待测试case文件
4、调用待测试case文件中的执行函数，传入 driver 参数
5、使用完成后结束服务而不是关闭打开的 chrome 窗体，以免运行多个 server 造成与 client 端口通信失败
'''

import pickle
from base import Base
from multiprocessing.connection import Listener
from threading import Thread

driver = Base(debug=True)

def rpc_server(handler, address, authkey):
   sock = Listener(address, authkey=authkey)
   while True:
       client = sock.accept()
       t = Thread(target=handler.handle_connection, args=(client,))
       t.daemon = True
       t.start()


class RPCHandler(object):
   def __init__(self):
       self._functions = {}

   def register_function(self, func):
       self._functions[func.__name__] = func

   def handle_connection(self, connection):
       try:
           while True:
               # 接收到一条消息, 使用pickle协议编码
               func_name, args, kwargs = pickle.loads(connection.recv())
               # rpc调用函数，并返回结果
               try:
                   r = self._functions[func_name](*args, **kwargs)
                   print(type(r))
                   connection.send(pickle.dumps(r))
               except Exception as e:
                   connection.send(pickle.dumps(e))
       except EOFError:
           pass


if __name__ == '__main__':
    #引用待测试case文件
   import deBugClientDemo
   from imp import reload

   # 新建一个handler类实例, 并将add方法注册到handler里面
   def add():
       #重载待测试case文件
       reload(deBugClientDemo)
       #调用待测试case文件的执行函数
       deBugClientDemo.get(driver)

   rpc_handler = RPCHandler()
   rpc_handler.register_function(add)

   # 运行server
   rpc_server(rpc_handler, ('localhost', 17001), authkey='isz')
   add()