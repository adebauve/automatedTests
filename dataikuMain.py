#!/usr/bin/env python
#-*- coding: utf-8 -*-
import random
import expected_result
from expected_result import *
import process_results
from process_results import *

def getCSVdata(filename):
   out = []
   f = open(filename,'r')
   for line in f:
      out.append(split(line,';'))
   f.close()
   
   return out

def array2csv(input, filename):
   f = open(filename,'w')
   for listline in input:
      line = ''
      for item in listline:
         line = line + str(item) + ';'
      line  = line + '\n'
      f.write(line)
   f.close
      
   
fromFile = False
# users = getCSVdata('./users.csv')
users = []
mainUser = "QA"
password = "willWin"
userSamePwd = "copycat"
otherUser = "toto"
otherPassword = "totoro"
maxResponseTime = 1.0

taskList=[]
tagDict = {}

results = csvHeader()

getTaskList = lambda tcase: json.loads(tcase.request.response_body)
# usage: taskList = getTaskList(tc)

getTagDict = lambda tcase: json.loads(tcase.request.response_body)
# usage: tagDict = getTagDict(tc)

if not fromFile:
   TestRequest().dropTheBase()

testNumber = 1
tc = TestCase("listTasks - empty list - no authentication", "OK")
print(tc.title + " START :\n================================================")
expected_result = expected_listTasks(taskList)
tc.addStep('listTasks',expected=expected_result)
test_result = tc.executeTest()
printResults(tc.results)
print(tc.title + " END \n================================================")
taskList = getTaskList(tc)
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1

tc = TestCase("Authenticate - valid credentials", "OK")
print(tc.title + " START :\n================================================")
tc.addStep('setCredentials',args=[mainUser,password])
# expected results for next call (authenticate):
expected_result = expected_authenticate(mainUser)
tc.addStep('authenticate',expected=expected_result)
test_result = tc.executeTest()
printResults(tc.results)
print(tc.title + " END \n================================================")
if not fromFile:
   if test_result:
      users.append([mainUser,password])
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1

tc = TestCase("Authenticate - invalid credentials", "NOK")
print(tc.title + " START :\n================================================")
tc.addStep('setCredentials', args=[otherUser,password])
expected_result = expected_authenticate(otherUser,False)
tc.addStep('authenticate',expected=expected_result)
test_result = tc.executeTest()
printResults(tc.results)
print(tc.title + " END \n================================================")
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1

tc = TestCase("Create new user with existing password", "OK")
print(tc.title + " START :\n================================================")
expected_result = init_expected_result()
expected_result['status'] = 200
expected_result['content'] = [["$.username",userSamePwd,"equal"]]
expected_result['responseTime'] = maxResponseTime
tc.addStep('createUser',args=[userSamePwd,password],expected=expected_result)
# add a login with this user to be sure:
tc.addStep('setCredentials',args=[userSamePwd,password])
expected_result = expected_authenticate(userSamePwd)
tc.addStep('authenticate',expected=expected_result)
test_result = tc.executeTest()
printResults(tc.results)
print(tc.title + " END \n================================================")
if not fromFile:
   if test_result:
      users.append([mainUser,password])
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1

tc = TestCase("Create new user with new password", "OK")
print(tc.title + " START :\n================================================")
otherUser = otherUser + 'bis'
otherPassword = otherPassword + 'bis'
expected_result = init_expected_result()
expected_result['status'] = 200
expected_result['content'] = [["$.username",otherUser,"equal"]]
expected_result['responseTime'] = maxResponseTime
tc.addStep('createUser',args=[otherUser,otherPassword],expected=expected_result)
# add a login with this user to be sure:
tc.addStep('setCredentials',args=[otherUser,otherPassword])
expected_result = expected_authenticate(otherUser)
tc.addStep('authenticate',expected=expected_result)
test_result = tc.executeTest()
printResults(tc.results)
print(tc.title + " END \n================================================")
if not fromFile:
   if test_result:
      users.append([mainUser,password])
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1

tc = TestCase("Create new task without tags while not authentified", "NOK")
taskName = 'task_' + str(random.randrange(0,100))
tags = []
print(tc.title + " START :\n================================================")
tc.request.resetCredentials()
expected_result = expected_newTask(mainUser,taskName,tags, False)
tc.addStep('createTask',args=[taskName,tags],expected=expected_result)
test_result = tc.executeTest()
printResults(tc.results)
print(tc.title + " END \n================================================")
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1


tc = TestCase("Create new task without tags while authentified", "OK")
taskName = 'task_' + str(random.randrange(0,100))
tags = []
print(tc.title + " START :\n================================================")
tc.addStep('setCredentials',args=[mainUser,password])
expected_result = expected_authenticate(mainUser)
tc.addStep('authenticate',expected=expected_result)
expected_result = expected_newTask(mainUser,taskName,tags)
tc.addStep('createTask',args=[taskName,tags],expected=expected_result)
expected_result = expected_listTasks([],taskName,tags)
# first task to be created => taskList = []
tc.addStep('listTasks', expected=expected_result)
test_result = tc.executeTest()
printResults(tc.results)
print(tc.title + " END \n================================================")
taskList = getTaskList(tc)
print(taskList)
# check unexistence by retrieving existing tasks, parsing the response to get the list of task names, etc...
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1

tc = TestCase("Create new task with unexisting tags while authentified", "OK")
taskName = 'test200'
tags = ['tag1','tag2']
print(tc.title + " START :\n================================================")
tc.addStep('setCredentials',args=[mainUser,password])
expected_result = expected_authenticate(mainUser)
tc.addStep('authenticate',expected=expected_result)
expected_result = expected_newTask(mainUser,taskName,tags)
tc.addStep('createTask',args=[taskName,tags],expected=expected_result)
expected_result = expected_listTasks(taskList,taskName,tags)
tc.addStep('listTasks',expected=expected_result)
test_result = tc.executeTest()
printResults(tc.results)
print(tc.title + " END \n================================================")
taskList = getTaskList(tc)
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1

tc = TestCase("Create new task with existing tags while authentified with another user", "OK")
taskName = 'test300'
tags = ['tag2','tag1']
print(tc.title + " START :\n================================================")
tc.addStep('setCredentials',args=[otherUser,otherPassword])
expected_result = expected_authenticate(otherUser)
tc.addStep('authenticate',expected=expected_result)
expected_result = expected_newTask(otherUser,taskName,tags)
tc.addStep('createTask',args=[taskName,tags],expected=expected_result)
expected_result = expected_listTasks(taskList,taskName,tags)
tc.addStep('listTasks',expected=expected_result)
test_result = tc.executeTest()
printResults(tc.results)
print(tc.title + " END \n================================================")
taskList = getTaskList(tc)
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1

tc = TestCase("Create new task with already existing title", "NOK")
print(tc.title + " START :\n================================================")
tc.addStep('setCredentials',args=[mainUser,password])
expected_result = expected_authenticate(mainUser)
tc.addStep('authenticate',expected=expected_result)
expected_result = expected_newTask(mainUser,taskName,tags,False)
tc.addStep('createTask',args=[taskName,tags],expected=expected_result)
expected_result = expected_listTasks()
tc.addStep('listTasks',expected=expected_result)
test_result = tc.executeTest()
printResults(tc.results)
print(tc.title + " END \n================================================")
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1

tc = TestCase("Retrieve Task information for an existing task", "OK")
print(tc.title + " START :\n================================================")
# retrieve taskid in taskList:
id_list = jsonpath.jsonpath(taskList,"$[*].id")
select_id = id_list[random.randrange(0,len(id_list))]
expected_result = expected_taskInfo(select_id)
tc.addStep('getTaskInfo', args=[select_id], expected=expected_result)
test_result = tc.executeTest()
printResults(tc.results)
print(tc.title + " END \n================================================")
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1

tc = TestCase("Update valid Task while unauthenticated", "NOK")
print(tc.title + " START :\n================================================")
# retrieve task before update:
task_before = jsonpath.jsonpath(taskList,"$[?(@.id=="+str(select_id)+")]")
updated_items = {"done":True, "tags":["upTag1"], "title": "updateNOK"}
expected_result = expected_taskUpdate([select_id, updated_items], False)
tc.addStep('updateTask', args=[select_id,updated_items['title'],updated_items['tags'],updated_items['done']], expected=expected_result)
# reminder: updateTask(self,taskid,title='',tags=[],done='')
test_result = tc.executeTest()
printResults(tc.results)
print(tc.title + " END \n================================================")
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1


tc = TestCase("Update valid Task while authenticated as the owner - change status, tags and title", "OK")
print(tc.title + " START :\n================================================")
# find task where owner = mainUser
select_task = jsonpath.jsonpath(taskList, '$[?(@.username=="'+mainUser+'")]')[0]
select_id = select_task["id"]
tc.addStep('setCredentials',args=[mainUser,password])
expected_result = expected_authenticate(mainUser)
tc.addStep('authenticate',expected=expected_result)
# update:
updated_items = {"done":True, "tags":["upTag1"], "title": "updateOK"}
expected_result = expected_taskUpdate([select_id, updated_items])
tc.addStep('updateTask', args=[select_id,updated_items['title'],updated_items['tags'],updated_items['done']], expected=expected_result)
# get task info to check the update:
expected_result = expected_taskInfo([select_id, updated_items])
tc.addStep('getTaskInfo', args=[select_id], expected=expected_result)
test_result = tc.executeTest()
printResults(tc.results)
print(tc.title + " END \n================================================")
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1


tc = TestCase("Update valid Task while authenticated as the NOT the owner - change status, tags and title", "NOK")
print(tc.title + " START :\n================================================")
# find task where owner = otherUser
select_task = jsonpath.jsonpath(taskList, '$[?(@.username=="'+otherUser+'")]')[0]
select_id = select_task["id"]
# login as mainUser
tc.addStep('setCredentials',args=[mainUser,password])
expected_result = expected_authenticate(mainUser)
tc.addStep('authenticate',expected=expected_result)
# update:
updated_items = {"done":True, "tags":["upTag2"], "title": "updateNOK"}
expected_result = expected_taskUpdate([select_id, updated_items], False)
tc.addStep('updateTask', args=[select_id,updated_items['title'],updated_items['tags'],updated_items['done']], expected=expected_result)
# get task info to check not updated task
expected_result = expected_taskInfo([select_id, select_task])
tc.addStep('getTaskInfo', args=[select_id], expected=expected_result)
test_result = tc.executeTest()
printResults(tc.results)
print(tc.title + " END \n================================================")
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1

# TODO
#response = tr.listTags()
#response = tr.getTagInfo(2)
# tc = TestCase("Retrieve all the tags","OK")
# print(tc.title + " START :\n================================================")
# expected_result = init_expected_result()
# tc.addStep("listTags", expected=expected_result)


tc = TestCase("Delete task while authentified as NOT the owner", "NOK")
print(tc.title + " START :\n================================================")
# use same task as previous test case
expected_result = init_expected_result()
expected_result['status'] = 401
expected_result['content'] = []
expected_result['responseTime'] = 1.0
tc.addStep('setCredentials',args=[mainUser,password])
tc.addStep('deleteTask',args=[select_id], expected=expected_result)
test_result = tc.executeTest()
printResults(tc.results)
print(tc.title + " END \n================================================")
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1


tc = TestCase("Delete task while authentified as the owner", "OK")
print(tc.title + " START :\n================================================")
select_task = jsonpath.jsonpath(taskList, '$[?(@.username=="'+mainUser+'")]')[0]
select_id = select_task["id"]
expected_result = init_expected_result()
expected_result['status'] = 200
expected_result['content'] = []
expected_result['responseTime'] = 1.0
tc.addStep('setCredentials',args=[mainUser,password])
tc.addStep('deleteTask',args=[select_id], expected=expected_result)
test_result = tc.executeTest()
printResults(tc.results)
print(tc.title + " END \n================================================")
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1

tc = TestCase("Retrieve Task information for unexisting task", "NOK")
print(tc.title + " START :\n================================================")
# generate taskid not existing
range = 100
select_id = random.randrange(0,range)
while select_id in id_list:
   select_id = random.randrange(range,2*range)
   range*=2
expected_result = expected_taskInfo(select_id, False)
tc.addStep('getTaskInfo', args=[select_id], expected=expected_result)
test_result = tc.executeTest()
printResults(tc.results)
print(tc.title + " END \n================================================")
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1

array2csv(results, './test.csv')

























