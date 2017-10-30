#!/usr/bin/env python
#-*- coding: utf-8 -*-
import TestCase
from TestCase import *

def printResults(results):
   for r_i, r_val in results.items():
      print("Step #" + str(r_val['step']))
      print(r_val['request'])
      if r_val['responseStatus'] > 1 :
         print('Response:')
         print(r_val['responseStatus'])
         print(r_val['responseHeaders'])
         print(r_val['responseBody'])
         print(r_val['responseTime'])
         print(r_val['testResult'])
# todo: process results better than this and generate report

def init_expected_result():
   return {'status':0,'content':'','responseTime':1}
   
def expected_listTasks(empty=False):
   if empty:
      content = []
   else:
   # [
       # {
           # "date": "2017-10-30T20:42:50.340241Z", 
           # "done": false, 
           # "id": 1, 
           # "tags": [], 
           # "title": "test1", 
           # "username": "QA"
       # }
   # ]
      content = [["$.date",'',"exists"], ["$.done",'',"exists"], ["$.id",'',"exists"], ["$.tags",'',"exists"], ["$.title",'',"exists"], ["$.username",'',"exists"]]
   return {'status':200, 'content':content, 'responseTime':1.0}

def expected_authenticate(user,OK=True):
   if OK:
      return {'status':200, 'content':[["$.expires",600,"equal"],["$.token","time","checkToken"],["$.username",user,"equal"]], 'responseTime':1.0}
   else:
      return {'status':401, 'content': [["$.message","Bad authentication","equal"]], 'responseTime': 1.0}

def expected_newTask(user,task,tags,OK=True):
   if OK:
      content = [["$.date", "time" , "equalZuluTime"], ["$.done", False, "equal"], ["$.tags[*].name", tags, "listEqual"], ["$.title", task, "equal"], ["$.username", user, "equal"]]
      return {'status':200, 'content': content, 'responseTime': 1.0}
   else:
      return {'status':400}

mainUser = "QA"
password = "willWin"
otherUser = "toto"
otherPwd = "totoro"
maxResponseTime = 1.0

TestRequest().dropTheBase()

tc = TestCase("listTasks - no authentication", "OK")
print(tc.title + " START :\n================================================")
expected_result = expected_listTasks(True)
tc.addStep('listTasks',expected=expected_result)
test_result = tc.executeTest()
print(tc.title + " END :\n================================================")
printResults(tc.results)

tc = TestCase("Authenticate - valid credentials", "OK")
print(tc.title + " START :\n================================================")
expected_result = init_expected_result()
tc.addStep('setCredentials',args=[mainUser,password])
# expected results for next call (authenticate):
expected_result = expected_authenticate(mainUser)
tc.addStep('authenticate',expected=expected_result)
test_result = tc.executeTest()
print(tc.title + " END :\n================================================")
printResults(tc.results)

tc = TestCase("Authenticate - invalid credentials", "NOK")
print(tc.title + " START :\n================================================")
expected_result = init_expected_result()
tc.addStep('setCredentials', args=[otherUser,otherPwd])
expected_result = expected_authenticate(otherUser,False)
tc.addStep('authenticate',expected=expected_result)
test_result = tc.executeTest()
print(tc.title + " END :\n================================================")
printResults(tc.results)

tc = TestCase("Create new user", "OK")
print(tc.title + " START :\n================================================")
expected_result = init_expected_result()
expected_result['status'] = 200
expected_result['content'] = [["$.username",otherUser,"equal"]]
expected_result['responseTime'] = maxResponseTime
tc.addStep('createUser',args=[otherUser,otherPwd],expected=expected_result)
# add a login with this user to be sure:
expected_result = init_expected_result()
tc.addStep('setCredentials',args=[otherUser,otherPwd])
expected_result = expected_authenticate(otherUser)
tc.addStep('authenticate',expected=expected_result)
test_result = tc.executeTest()
print(tc.title + " END :\n================================================")
printResults(tc.results)

tc = TestCase("Create new task without tags while authentified", "OK")
taskName = 'test1'
tags = []
print(tc.title + " START :\n================================================")
expected_result = init_expected_result()
tc.addStep('setCredentials',args=[mainUser,password])
expected_result = expected_authenticate(mainUser)
tc.addStep('authenticate',expected=expected_result)
expected_result = expected_newTask(mainUser,taskName,tags)
tc.addStep('createTask',args=[taskName,tags],expected=expected_result)
expected_result = expected_listTasks()
tc.addStep('listTasks', expected=expected_result)
# todo: generate unexisting taskname: task_randomIndex
# check unexistence by retrieving existing tasks, parsing the response to get the list of task names, etc...
# after the creation, check existence of created task in the response of the list tasks
test_result = tc.executeTest()
print(tc.title + " END :\n================================================")
printResults(tc.results)

tc = TestCase("Create new task with unexisting tags while authentified", "OK")
taskName = 'test2'
tags = ['tag1','tag2']
print(tc.title + " START :\n================================================")
expected_result = init_expected_result()
tc.addStep('setCredentials',args=[mainUser,password])
expected_result = expected_authenticate(mainUser)
tc.addStep('authenticate',expected=expected_result)
expected_result = expected_newTask(mainUser,taskName,tags)
tc.addStep('createTask',args=[taskName,tags],expected=expected_result)
expected_result = expected_listTasks()
tc.addStep('listTasks',expected=expected_result)
# todo: generate unexisting taskname: task_randomIndex
# check unexistence by retrieving existing tasks, parsing the response to get the list of task names, etc...
# after the creation, check existence of created task in the response of the list tasks
test_result = tc.executeTest()
print(tc.title + " END :\n================================================")
printResults(tc.results)

tc = TestCase("Create new task with existing tags while authentified with another user", "OK")
taskName = 'test3'
tags = ['tag2','tag1']
print(tc.title + " START :\n================================================")
expected_result = init_expected_result()
tc.addStep('setCredentials',args=[otherUser,otherPwd])
expected_result = expected_authenticate(otherUser)
tc.addStep('authenticate',expected=expected_result)
expected_result = expected_newTask(otherUser,taskName,tags)
tc.addStep('createTask',args=[taskName,tags],expected=expected_result)
expected_result = expected_listTasks()
tc.addStep('listTasks',expected=expected_result)
# todo: generate unexisting taskname: task_randomIndex
# check unexistence by retrieving existing tasks, parsing the response to get the list of task names, etc...
# after the creation, check existence of created task in the response of the list tasks
test_result = tc.executeTest()
print(tc.title + " END :\n================================================")
printResults(tc.results)

tc = TestCase("Create new task with already existing title", "NOK")
print(tc.title + " START :\n================================================")
expected_result = init_expected_result()
tc.addStep('setCredentials',args=[mainUser,password])
expected_result = expected_authenticate(mainUser)
tc.addStep('authenticate',expected=expected_result)
expected_result = expected_newTask(mainUser,taskName,tags,False)
tc.addStep('createTask',args=[taskName,tags],expected=expected_result)
expected_result = expected_listTasks()
tc.addStep('listTasks',expected=expected_result)
test_result = tc.executeTest()
print(tc.title + " END :\n================================================")
printResults(tc.results)

#response = tr.getTaskInfo(14)
#response = tr.deleteTask(14)
#response = tr.updateTask(13,'',[],'false')
#response = tr.listTags()
#response = tr.getTagInfo(2)
#response = tr.createUser("test","test")
#response = tr.dropTheBase()


# print(tr.request_trace)
# print('Response:')
# print(tr.response_status)
# print(tr.response_body)
# print(tr.response_time)

# error management:
# while True:
   # try:
      # x = int(input("Please enter a number: "))
      # break
   # except ValueError:
      # print("Oops!  That was no valid number.  Try again...")

# if x >= 10:
   # print(str(x) + ' ne peut pas être supérieur à 10')
   # raise NameError('trop grand')

# endPoint = 'http://debauve.qatest.dataiku.com:80/'
# headers = {'Content-Type':'application/json'}
# body = {'username':'QA','password':'willWin'}

# listTasksNoAuth = requests.get(endPoint, headers=headers)
# listTasksValidLogin = requests.post(endPoint + 'authenticate', headers=headers, json=body)

# print(listTasksNoAuth.request.headers)
# print('=====================================')
# print(str(listTasksNoAuth.status_code) + '\n' + listTasksNoAuth.text)
# print(str(listTasksValidLogin.status_code) + '\n' + str(listTasksValidLogin.text))





















