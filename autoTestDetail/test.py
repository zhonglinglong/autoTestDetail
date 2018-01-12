# -*- coding:utf8 -*-
#Author : Wu Jun
#Create on : 2017 - 09 -07

import os,subprocess,time,re
from common.base import hostSet,consoleLog,get_conf

class StartTest():
	def __init__(self):
		"""设置当前测试环境"""
		condition = get_conf('testCondition', 'test')
		hostSet(condition)

	caseFile = []
	def getCaseFile(self,filePath):
		"""获取所有测试用例文件位置"""
		list = os.listdir(filePath)
		for i in range(len(list)):
			path = os.path.abspath(os.path.join(filePath,list[i]))
			if os.path.isfile(path):
				if list[i].startswith('test_') and list[i].endswith('.py'):
					self.caseFile.append(path)
			elif os.path.isdir(path):
				self.getCaseFile(path)

	def report(self,sums):
		"""测试报告统计，追加在日志文件中"""
		with open('./test.log') as f:
			content = f.read()
			error = len(re.findall('one error at', content))
			asserts = len(re.findall('one assert at',content))
			success = sums - error
			consoleLog('=============================================')
			consoleLog('#           本次共执行 %s 个用例            #' % str(sums))
			consoleLog('#                 成功 %s 个                #' % str(success))
			consoleLog('#                 执行失败 %s 个                #' % str(error))
			consoleLog('#                 断言失败 %s 处                #' % str(asserts))
			consoleLog('=============================================')
		with open('./test.log','w') as f:
			f.truncate()

	def startTest(self,filePath,subcount,pollWait):
		"""
		轮询指定目录下的所有测试用例，按照指定的并发数执行，当某一线程的用例执行完成后，自动再继续启动剩下的用例，同时不超过指定的线程设置
		:param filePath: 需要轮询测试用例的目录
		:param subcount: 最多同时需要执行的线程数（一个用例文件启动一个子线程）
		:param pollWait: 轮询已启动的线程（用例）是否有已经完成的时间
		"""
		self.getCaseFile(filePath)
		subs = []
		if self.caseFile:
			current = 0
			for case in self.caseFile:
				sub = subprocess.Popen('python %s' % case)
				current += 1
				consoleLog(u'++++ 本次共需执行用例 %s 个，当前已启动用例 %s 个 ++++' % (str(len(self.caseFile)),current))
				subs.append(sub)
				if subcount is 1:
					sub.wait()
				def checkPoll():
					for index,s in enumerate(subs):
						if s.poll() != 0:
							if index == len(subs)-1:
								time.sleep(pollWait)
								checkPoll()
						else:
							s.kill()
							del subs[index]
							break
				if len(subs) == subcount:
					checkPoll()
				if case is self.caseFile[-1]:
					while True:
						checkPoll()
						if not subs:
							self.report(len(self.caseFile))
							break
						else:
							time.sleep(pollWait)
test = StartTest()
test.startTest('./contract/',1,1)








