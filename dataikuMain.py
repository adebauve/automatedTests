#!/usr/bin/env python
#-*- coding: utf-8 -*-
import TestCase
from TestCase import *

def printResults(results):
   for r_i, r_val in results.items():
      print(r_val['step'])
      print(r_val['request'])
      print('Response:')
      print(r_val['responseStatus'])
      print(r_val['responseHeaders'])
      print(r_val['responseBody'])
      print(r_val['responseTime'])
# todo: process results better than this and generate report

TestRequest().dropTheBase()

tc = TestCase("listTasks - no authentication", "OK")
tc.addStep(0,'listTasks')
tc.executeTest()
printResults(tc.results)

tc = TestCase("Authenticate - valid credentials", "OK")
tc.addStep(0,'setCredentials',['QA','willWin'])
tc.addStep(1,'authenticate')
tc.executeTest()
printResults(tc.results)

tc = TestCase("Authenticate - invalid credentials", "NOK")
tc.addStep(0,'setCredentials',['kaput','boom'])
tc.addStep(1,'authenticate')
tc.executeTest()
printResults(tc.results)

tc = TestCase("Create new user", "OK")
tc.addStep(0,'createUser',['toto','toto'])
# todo: save username and password for some following test cases
tc.executeTest()
printResults(tc.results)

tc = TestCase("Create new task without tags while authentified", "OK")
tc.addStep(0,'setCredentials',['QA','willWin'])
tc.addStep(1,'authenticate')
tc.addStep(2,'createTask',['test1',[]])
tc.addStep(3,'listTasks')
# todo: generate unexisting taskname: task_randomIndex
# check unexistence by retrieving existing tasks, parsing the response to get the list of task names, etc...
# after the creation, check existence of created task in the response of the list tasks
tc.executeTest()
printResults(tc.results)

tc = TestCase("Create new task with unexisting tags while authentified", "OK")
tc.addStep(0,'setCredentials',['QA','willWin'])
tc.addStep(1,'authenticate')
tc.addStep(2,'createTask',['test2',['tag1','tag2']])
tc.addStep(3,'listTasks')
# todo: generate unexisting taskname: task_randomIndex
# check unexistence by retrieving existing tasks, parsing the response to get the list of task names, etc...
# after the creation, check existence of created task in the response of the list tasks
tc.executeTest()
printResults(tc.results)

tc = TestCase("Create new task with existing tags while authentified with another user", "OK")
tc.addStep(0,'setCredentials',['toto','toto'])
tc.addStep(1,'authenticate')
tc.addStep(2,'createTask',['test4',['tag1','tag3']])
tc.addStep(3,'listTasks')
# todo: generate unexisting taskname: task_randomIndex
# check unexistence by retrieving existing tasks, parsing the response to get the list of task names, etc...
# after the creation, check existence of created task in the response of the list tasks
tc.executeTest()
printResults(tc.results)

#response = tr.listTasks()
#tr.setCredentials("QA","willWin")
#tr.setCredentials("test","test")

#tr.resetCredentials()
#response = tr.authenticate()
#response = tr.createTask("again",[])
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





















