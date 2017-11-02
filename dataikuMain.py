#!/usr/bin/env python
#-*- coding: utf-8 -*-
import random
import expected_result
from expected_result import *
import process_results
from process_results import *
import os


def array2csv(input, filename):
   f = open(filename,'w')
   for listline in input:
      line = ''
      for item in listline:
         line = line + str(item) + ';'
      line  = line + '\n'
      f.write(line)
   f.close

def csv2array(filename):
   out = []
   f = open(filename,'r')
   for line in f:
      splitline = line.split(';')
      splitline.pop()
      out.append(splitline)
   f.close()
   return out

def file2json(filename):
   str = ''
   f = open(filename,'r')
   for line in f:
      str+= line
   f.close()
   return json.loads(str)

logdir = './log'
try:
   os.mkdir(logdir)
except OSError:
   pass

datadir = './data'
try:
   os.mkdir(datadir)
except OSError:
   pass
   
userFilename = datadir + '/users.csv'
taskFilename = datadir + '/taskList.txt'
tagFilename = datadir + '/tagList.txt'

currentTime = time.strftime("%Y%m%d%H%M%S")
logfilename = logdir + '/logfile' + currentTime + '.txt'
reportFilename = logdir + '/testReport' + currentTime + '.csv'
      
fromFile = True

if not fromFile:
   users = []
   mainUser = "QA"
   password = "willWin"
   otherUser = "toto"
   otherPassword = "totoro"
   lightTaskList = []
   lightTagList = []
   taskList=[]
   tagDict = {}
else:
   users = csv2array(userFilename)
   if len(users) > 0:
      mainUser = users[0][0]
      password = users[0][1]
   else:
      mainUser = "QA"
      password = "willWin"
   if len(users) > 1:
      otherUser = users[1][0]
      otherPassword = users[1][1]
   else:
      otherUser = "toto"
      otherPassword = "totoro"
   taskList = file2json(taskFilename)
   tagDict = file2json(tagFilename)
   # build lightTaskList and lightTagList on this:
   lightTaskList = jsonpath.jsonpath(taskList, "$[*].title")
   lightTagList = []
   for k,v in tagDict.items():
      lightTagList.append(k)
      

userUnexists = "casper"
maxResponseTime = 1.0
sleepDelay = 1

results = csvHeader()

getTaskList = lambda tcase: json.loads(tcase.request.response_body)
# usage: taskList = getTaskList(tc)

getTagDict = lambda tcase: json.loads(tcase.request.response_body)
# usage: tagDict = getTagDict(tc)

if not fromFile:
   TestRequest().dropTheBase()
   time.sleep(sleepDelay)

testNumber = 1
tc = TestCase("listTasks - no authentication", "OK")
expected_result = expected_listTasks(taskList)
tc.addStep('listTasks',expected=expected_result)
test_result = tc.executeTest()
logResults(tc, testNumber, test_result, logfilename)
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1
if test_result:
   taskList = getTaskList(tc)

time.sleep(sleepDelay)

tc = TestCase("Authenticate - valid credentials", "OK")
tc.addStep('setCredentials',args=[mainUser,password])
# expected results for next call (authenticate):
expected_result = expected_authenticate(mainUser)
tc.addStep('authenticate',expected=expected_result)
test_result = tc.executeTest()
logResults(tc, testNumber, test_result, logfilename)
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1
if not fromFile:
   if test_result:
      users.append([mainUser,password])


tc = TestCase("Authenticate - invalid credentials", "NOK")
tc.addStep('setCredentials', args=[userUnexists,password])
expected_result = expected_authenticate(userUnexists,False)
tc.addStep('authenticate',expected=expected_result)
test_result = tc.executeTest()
logResults(tc, testNumber, test_result, logfilename)
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1

time.sleep(sleepDelay)

tc = TestCase("Create new user with existing password", "OK")
# first generate unexisting user:
randRange  = 100
randomIndex = random.randrange(0,randRange)
user = 'user' + str(randomIndex)
while user in users[:][0]:
   randomIndex = random.randrange(randRange, randRange + 100)
   user = 'user' + str(randomIndex)
   randRange+= 100
expected_result = init_expected_result()
expected_result['status'] = 200
expected_result['content'] = [["$.username",user,"equal"]]
expected_result['responseTime'] = maxResponseTime
tc.addStep('createUser',args=[user,password],expected=expected_result)
# add a login with this user to be sure:
tc.addStep('setCredentials',args=[user,password])
expected_result = expected_authenticate(user)
tc.addStep('authenticate',expected=expected_result)
test_result = tc.executeTest()
logResults(tc, testNumber, test_result, logfilename)
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1
if not fromFile:
   if test_result:
      users.append([user,password])
      otherUser = user
      otherPassword = password

time.sleep(sleepDelay)

tc = TestCase("Create new user with new password", "OK")
# first generate unexisting user:
randRange  = 100
randomIndex = random.randrange(0,randRange)
user = 'user' + str(randomIndex)
while user in users[:][0]:
   randomIndex = random.randrange(randRange, randRange + 100)
   user = 'user' + str(randomIndex)
   randRange+= 100
pwd = 'pwd' + str(randomIndex)

expected_result = init_expected_result()
expected_result['status'] = 200
expected_result['content'] = [["$.username",user,"equal"]]
expected_result['responseTime'] = maxResponseTime
tc.addStep('createUser',args=[user,pwd],expected=expected_result)
# add a login with this user to be sure:
tc.addStep('setCredentials',args=[user,pwd])
expected_result = expected_authenticate(user)
tc.addStep('authenticate',expected=expected_result)
test_result = tc.executeTest()
logResults(tc, testNumber, test_result, logfilename)
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1
if not fromFile:
   if test_result:
      users.append([user,pwd])
      otherUser = user
      otherPassword = pwd

time.sleep(sleepDelay)

tc = TestCase("Create new user with existing username", "NOK")
user = users[random.randrange(0,len(users))][0]
pwd = "blablabla"
expected_result = init_expected_result()
expected_result['status'] = 400
expected_result['responseTime'] = maxResponseTime
tc.addStep('createUser', args=[user,pwd], expected=expected_result)
test_result = tc.executeTest()
logResults(tc, testNumber, test_result, logfilename)
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1

time.sleep(sleepDelay)

tc = TestCase("Create new task without tags while not authentified", "NOK")
taskName = 'task_' + str(random.randrange(0,100))
tags = []
tc.request.resetCredentials()
expected_result = expected_newTask(mainUser,taskName,tags, False)
tc.addStep('createTask',args=[taskName,tags],expected=expected_result)
test_result = tc.executeTest()
logResults(tc, testNumber, test_result, logfilename)
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1
if not test_result:
   lightTaskList.append(taskName)
   taskList = getTaskList(tc)

time.sleep(sleepDelay)
   
tc = TestCase("Create new task without tags while authentified", "OK")
randRange = 100
randomIndex = random.randrange(0,randRange)
taskName = 'task_' + str(randomIndex)
while taskName in lightTaskList:
   randomIndex = random.randrange(randRange,randRange + 100)
   taskName = 'task_' + str(randomIndex)
   randRange+= 100
tags = []
tc.addStep('setCredentials',args=[mainUser,password])
expected_result = expected_authenticate(mainUser)
tc.addStep('authenticate',expected=expected_result)
expected_result = expected_newTask(mainUser,taskName,tags)
tc.addStep('createTask',args=[taskName,tags],expected=expected_result)
expected_result = expected_listTasks([],taskName,tags)
# first task to be created => taskList = []
tc.addStep('listTasks', expected=expected_result)
test_result = tc.executeTest()
logResults(tc, testNumber, test_result, logfilename)
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1
if test_result:
   lightTaskList.append(taskName)
   taskList = getTaskList(tc)
else:
   # must retrieve updated taskList:
   tc = TestCase("list tasks for testing purpose","OK")
   tc.addStep('listTasks')
   tc.executeTest()
   taskList = getTaskList(tc)
   
time.sleep(sleepDelay)

# do it twice:
tc = TestCase("2nd Create new task without tags while authentified", "OK")
randRange = 100
randomIndex = random.randrange(0,randRange)
taskName = 'task_' + str(randomIndex)
while taskName in lightTaskList:
   randomIndex = random.randrange(randRange,randRange + 100)
   taskName = 'task_' + str(randomIndex)
   randRange+= 100
tags = []
tc.addStep('setCredentials',args=[mainUser,password])
expected_result = expected_authenticate(mainUser)
tc.addStep('authenticate',expected=expected_result)
expected_result = expected_newTask(mainUser,taskName,tags)
tc.addStep('createTask',args=[taskName,tags],expected=expected_result)
expected_result = expected_listTasks(taskList,taskName,tags)
# first task to be created => taskList = []
tc.addStep('listTasks', expected=expected_result)
test_result = tc.executeTest()
logResults(tc, testNumber, test_result, logfilename)
if not test_result:
   results = results2Array(tc, testNumber, test_result, results)
   # must retrieve updated taskList:
   tc = TestCase("list tasks for testing purpose","OK")
   tc.addStep('listTasks')
   tc.executeTest()
   taskList = getTaskList(tc)
testNumber+=1
if test_result:
   lightTaskList.append(taskName)
   taskList = getTaskList(tc)
   
time.sleep(sleepDelay)

tc = TestCase("Create new task with title > 20 while authentified", "NOK")
randRange = 100
randomIndex = random.randrange(0,randRange)
taskName = 'anticonstitutionnellement' + str(randomIndex)
while taskName in lightTaskList:
   randomIndex = random.randrange(randRange,randRange + 100)
   taskName = 'task_' + str(randomIndex)
   randRange+= 100
tags = []
tc.addStep('setCredentials',args=[mainUser,password])
expected_result = expected_authenticate(mainUser)
tc.addStep('authenticate',expected=expected_result)
expected_result = expected_newTask(mainUser,taskName,tags, False)
tc.addStep('createTask',args=[taskName,tags],expected=expected_result)
expected_result = expected_listTasks(taskList,taskName,tags)
# first task to be created => taskList = []
tc.addStep('listTasks', expected=expected_result)
test_result = tc.executeTest()
logResults(tc, testNumber, test_result, logfilename)
results = results2Array(tc, testNumber, test_result, results)
if test_result:
   lightTaskList.append(taskName)
   taskList = getTaskList(tc)
else:
   # must retrieve updated taskList:
   tc = TestCase("list tasks for testing purpose","OK")
   tc.addStep('listTasks')
   tc.executeTest()
   taskList = getTaskList(tc)
testNumber+=1

   
time.sleep(sleepDelay)

tc = TestCase("Create new task with unexisting tags while authentified", "OK")
# generate random taskname:
randRange = 100
randomIndex = random.randrange(0,randRange)
taskName = 'task_' + str(randomIndex)
while taskName in lightTaskList:
   randomIndex = random.randrange(randRange,randRange + 100)
   taskName = 'task_' + str(randomIndex)
   randRange+= 100
# generate between 1 and 5 random tagnames:
randNumber = random.randrange(1,5)
tags = []
for x in range(randNumber):
   tag = 'tag' + str(randomIndex)
   while tag in lightTagList:
      randomIndex = random.randrange(randRange, randRange + 100)
      tag = 'tag' + str(randomIndex)
      randRange+= 100
   tags.append(tag)
tc.addStep('setCredentials',args=[mainUser,password])
expected_result = expected_authenticate(mainUser)
tc.addStep('authenticate',expected=expected_result)
expected_result = expected_newTask(mainUser,taskName,tags)
tc.addStep('createTask',args=[taskName,tags],expected=expected_result)
expected_result = expected_listTasks(taskList,taskName,tags)
tc.addStep('listTasks',expected=expected_result)
test_result = tc.executeTest()
logResults(tc, testNumber, test_result, logfilename)
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1
if test_result:
   lightTaskList.append(taskName)
   lightTagList.extend(tags)
   taskList = getTaskList(tc)
   # clean the lightTagList from duplicates
   lightTagList = list(set(lightTagList))
else:
   # must retrieve updated taskList:
   tc = TestCase("list tasks for testing purpose","OK")
   tc.addStep('listTasks')
   tc.executeTest()
   taskList = getTaskList(tc)

time.sleep(sleepDelay)

# do it twice:
tc = TestCase("2nd Create new task with unexisting tags while authentified", "OK")
# generate random taskname:
randRange = 100
randomIndex = random.randrange(0,randRange)
taskName = 'task_' + str(randomIndex)
while taskName in lightTaskList:
   randomIndex = random.randrange(randRange,randRange + 100)
   taskName = 'task_' + str(randomIndex)
   randRange+= 100
# generate between 1 and 5 random tagnames:
randNumber = random.randrange(1,5)
tags = []
for x in range(randNumber):
   tag = 'tag' + str(randomIndex)
   while tag in lightTagList:
      randomIndex = random.randrange(randRange, randRange + 100)
      tag = 'tag' + str(randomIndex)
      randRange+= 100
   tags.append(tag)
tc.addStep('setCredentials',args=[mainUser,password])
expected_result = expected_authenticate(mainUser)
tc.addStep('authenticate',expected=expected_result)
expected_result = expected_newTask(mainUser,taskName,tags)
tc.addStep('createTask',args=[taskName,tags],expected=expected_result)
expected_result = expected_listTasks(taskList,taskName,tags)
tc.addStep('listTasks',expected=expected_result)
test_result = tc.executeTest()
logResults(tc, testNumber, test_result, logfilename)
if not test_result:
   results = results2Array(tc, testNumber, test_result, results)
   # must retrieve updated taskList:
   tc = TestCase("list tasks for testing purpose","OK")
   tc.addStep('listTasks')
   tc.executeTest()
   taskList = getTaskList(tc)
testNumber+=1
if test_result:
   lightTaskList.append(taskName)
   lightTagList.extend(tags)
   taskList = getTaskList(tc)
   # clean the lightTagList from duplicates
   lightTagList = list(set(lightTagList))

time.sleep(sleepDelay)

tc = TestCase("Create new task with tags > 20 char, while authentified", "NOK")
# generate random taskname:
randRange = 100
randomIndex = random.randrange(0,randRange)
taskName = 'task_' + str(randomIndex)
while taskName in lightTaskList:
   randomIndex = random.randrange(randRange,randRange + 100)
   taskName = 'task_' + str(randomIndex)
   randRange+= 100
# generate 1 tagname:
tags = []
tag = 'tagAnticonstitutionnellement' + str(randomIndex)
while tag in lightTagList:
   randomIndex = random.randrange(randRange, randRange + 100)
   tag = 'tag' + str(randomIndex)
   randRange+= 100
tags.append(tag)
tc.addStep('setCredentials',args=[mainUser,password])
expected_result = expected_authenticate(mainUser)
tc.addStep('authenticate',expected=expected_result)
expected_result = expected_newTask(mainUser,taskName,tags, False)
tc.addStep('createTask',args=[taskName,tags],expected=expected_result)
expected_result = expected_listTasks(taskList,taskName,tags)
tc.addStep('listTasks',expected=expected_result)
test_result = tc.executeTest()
logResults(tc, testNumber, test_result, logfilename)
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1
# must retrieve updated taskList:
tc = TestCase("list tasks for testing purpose","OK")
tc.addStep('listTasks')
tc.executeTest()
taskList = getTaskList(tc)
# retrieve taglist:
tc = TestCase("list tags for testing purpose","OK")
tc.addStep('listTags')
tc.executeTest()
tagDict = getTagDict(tc)
lightTagList = []
for k,v in tagDict.items():
   lightTagList.append(k)

time.sleep(sleepDelay)

tc = TestCase("Create new task with existing tag while authentified with another user", "OK")
# generate random taskname:
randRange = 100
randomIndex = random.randrange(0,randRange)
taskName = 'task_' + str(randomIndex)
while taskName in lightTaskList:
   randomIndex = random.randrange(randRange,randRange + 100)
   taskName = 'task_' + str(randomIndex)
   randRange+= 100
# tags:
randomIndex = random.randrange(len(lightTagList))
tags = []
tags.append(lightTagList[randomIndex])
tc.addStep('setCredentials',args=[otherUser,otherPassword])
expected_result = expected_authenticate(otherUser)
tc.addStep('authenticate',expected=expected_result)
expected_result = expected_newTask(otherUser,taskName,tags)
tc.addStep('createTask',args=[taskName,tags],expected=expected_result)
expected_result = expected_listTasks(taskList,taskName,tags)
tc.addStep('listTasks',expected=expected_result)
test_result = tc.executeTest()
logResults(tc, testNumber, test_result, logfilename)
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1
if test_result:
   lightTaskList.append(taskName)
   taskList = getTaskList(tc)
else:
   # must retrieve updated taskList:
   tc = TestCase("list tasks for testing purpose","OK")
   tc.addStep('listTasks')
   tc.executeTest()
   taskList = getTaskList(tc)

time.sleep(sleepDelay)

# do it twice:
tc = TestCase("2nd Create new task with existing tag while authentified with another user", "OK")
# generate random taskname:
randRange = 100
randomIndex = random.randrange(0,randRange)
taskName = 'task_' + str(randomIndex)
while taskName in lightTaskList:
   randomIndex = random.randrange(randRange,randRange + 100)
   taskName = 'task_' + str(randomIndex)
   randRange+= 100
# tags:
randomIndex = random.randrange(len(lightTagList))
tags = []
tags.append(lightTagList[randomIndex])
tc.addStep('setCredentials',args=[otherUser,otherPassword])
expected_result = expected_authenticate(otherUser)
tc.addStep('authenticate',expected=expected_result)
expected_result = expected_newTask(otherUser,taskName,tags)
tc.addStep('createTask',args=[taskName,tags],expected=expected_result)
expected_result = expected_listTasks(taskList,taskName,tags)
tc.addStep('listTasks',expected=expected_result)
test_result = tc.executeTest()
logResults(tc, testNumber, test_result, logfilename)
if not test_result:
   results = results2Array(tc, testNumber, test_result, results)
   # must retrieve updated taskList:
   tc = TestCase("list tasks for testing purpose","OK")
   tc.addStep('listTasks')
   tc.executeTest()
   taskList = getTaskList(tc)
testNumber+=1
if test_result:
   lightTaskList.append(taskName)
   taskList = getTaskList(tc)

time.sleep(sleepDelay)

tc = TestCase("Create new task with already existing title", "NOK")
# taskname is the same as previous testcase
tc.addStep('setCredentials',args=[mainUser,password])
expected_result = expected_authenticate(mainUser)
tc.addStep('authenticate',expected=expected_result)
# taskName stays the same as previous test case
expected_result = expected_newTask(mainUser,taskName,tags,False)
tc.addStep('createTask',args=[taskName,tags],expected=expected_result)
expected_result = expected_listTasks()
test_result = tc.executeTest()
logResults(tc, testNumber, test_result, logfilename)
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1
if not test_result:
   # must retrieve taskList:
   tc = TestCase("list tasks for testing purpose","OK")
   tc.addStep('listTasks')
   tc.executeTest()
   taskList = getTaskList(tc)

time.sleep(sleepDelay)

tc = TestCase("Retrieve Task information for an existing task", "OK")
# retrieve taskid in taskList:
if type(taskList) is dict:
   select_id = jsonpath.jsonpath(taskList,"$.id")[0]
else:
   id_list = jsonpath.jsonpath(taskList,"$[*].id")
   if id_list:
      select_id = id_list[random.randrange(0,len(id_list))]
   else:
      raise NameError("cannot find task")
expected_result = expected_taskInfo(select_id)
tc.addStep('getTaskInfo', args=[select_id], expected=expected_result)
test_result = tc.executeTest()
logResults(tc, testNumber, test_result, logfilename)
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1

time.sleep(sleepDelay)

tc = TestCase("Update valid Task while unauthenticated", "NOK")
# retrieve task before update:
if type(taskList) is dict:
   task_before = taskList
else:
   task_before = jsonpath.jsonpath(taskList,"$[?(@.id=="+str(select_id)+")]")
updated_items = {"done":True, "tags":["upTag1"], "title": "updateNOK"}
expected_result = expected_taskUpdate([select_id, updated_items], False)
tc.addStep('updateTask', args=[select_id,updated_items['title'],updated_items['tags'],updated_items['done']], expected=expected_result)
# reminder: updateTask(self,taskid,title='',tags=[],done='')
test_result = tc.executeTest()
logResults(tc, testNumber, test_result, logfilename)
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1
if not test_result:
   # must retrieve updated taskList:
   tc = TestCase("list tasks for testing purpose","OK")
   tc.addStep('listTasks')
   tc.executeTest()
   taskList = getTaskList(tc)
   tc = TestCase("list tags for testing purpose")
   tc.addStep('listTags')
   tc.executeTest()
   tagDict = getTagDict(tc)
   lightTagList = []
   for k,v in tagDict.items():
      lightTagList.append(k)

time.sleep(sleepDelay)

tc = TestCase("Update valid Task while authenticated as the owner - change status, tags and title", "OK")
# find task where owner = mainUser
if type(taskList) is dict:
   select_task = taskList
else:
   tl = jsonpath.jsonpath(taskList, '$[?(@.username=="'+mainUser+'")]')
   if tl:
      select_task = tl[0]
   else:
      raise NameError("no task found for " + mainUser)
select_id = select_task["id"]
select_taskName = select_task["title"]
newTaskName = select_taskName + 'updateOK'
newTag = 'upTag' + str(randomIndex)
randRange = 100
while newTag in lightTagList:
   randomIndex = random.randrange(randRange,randRange+100)
   newTag = 'upTag' + str(randomIndex)
   randRange+= 100
tc.addStep('setCredentials',args=[mainUser,password])
expected_result = expected_authenticate(mainUser)
tc.addStep('authenticate',expected=expected_result)
# update:
updated_items = {"done":True, "tags":[newTag], "title": newTaskName}
expected_result = expected_taskUpdate([select_id, updated_items])
tc.addStep('updateTask', args=[select_id,updated_items['title'],updated_items['tags'],updated_items['done']], expected=expected_result)
# get task info to check the update:
expected_result = expected_taskInfo([select_id, updated_items])
tc.addStep('getTaskInfo', args=[select_id], expected=expected_result)
expected_result = expected_listTasks(taskList,newTaskName,[newTag])
tc.addStep('listTasks',expected=expected_result)
test_result = tc.executeTest()
logResults(tc, testNumber, test_result, logfilename)
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1
if test_result:
   taskList = getTaskList(tc)
   for t in lightTaskList:
      if t == select_taskName:
         t = newTaskName
         break
else:
   # must retrieve updated taskList:
   tc = TestCase("list tasks for testing purpose","OK")
   tc.addStep('listTasks')
   tc.executeTest()
   taskList = getTaskList(tc)
# retrieve taglist:
tc = TestCase("list tags for testing purpose", "OK")
tc.addStep('listTags')
tc.executeTest()
tagDict = getTagDict(tc)
lightTagList = []
for k,v in tagDict.items():
   lightTagList.append(k)

time.sleep(sleepDelay)

tc = TestCase("Update valid Task while authenticated as NOT the owner - change status, tags and title", "NOK")
# find task where owner = otherUser
if type(taskList) is dict:
   select_task = taskList
else:
   tl = jsonpath.jsonpath(taskList, '$[?(@.username=="'+otherUser+'")]')
   if tl:
      select_task = tl[0]
   else:
      raise NameError("no task found for " + otherUser)
select_id = select_task["id"]
# login as mainUser
tc.addStep('setCredentials',args=[mainUser,password])
expected_result = expected_authenticate(mainUser)
tc.addStep('authenticate',expected=expected_result)
# update:
updated_items = {"done":True, "tags":[newTag], "title": "updateNOK"}
expected_result = expected_taskUpdate([select_id, updated_items], False)
tc.addStep('updateTask', args=[select_id,updated_items['title'],updated_items['tags'],updated_items['done']], expected=expected_result)
# get task info to check not updated task
expected_result = expected_taskInfo([select_id, select_task])
tc.addStep('getTaskInfo', args=[select_id], expected=expected_result)
test_result = tc.executeTest()
logResults(tc, testNumber, test_result, logfilename)
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1
if not test_result:
   # must retrieve updated taskList:
   tc = TestCase("list tasks for testing purpose","OK")
   tc.addStep('listTasks')
   tc.executeTest()
   taskList = getTaskList(tc)

time.sleep(sleepDelay)

# response = tr.listTags()
tc = TestCase("Retrieve all the tags","OK")
expected_result = init_expected_result()
expected_result['status'] = 200
expected_result['content'] = [[".", lightTagList, "tagDictEqual"]]
expected_result['responseTime'] = maxResponseTime
tc.addStep("listTags", expected=expected_result)
test_result = tc.executeTest()
logResults(tc, testNumber, test_result, logfilename)
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1
if test_result:
   tagDict = getTagDict(tc)
else:
   # must retrieve clean tag list:
   tc = TestCase("list tags for testing purpose","OK")
   tc.addStep('listTags')
   tc.executeTest()
   tagDict = getTagDict(tc)
lightTagList = []
for k,v in tagDict.items():
   lightTagList.append(k)
      
time.sleep(sleepDelay)

tc = TestCase("Retrieve tag details for an existing tag", "OK")
randomIndex = random.randrange(len(lightTagList))
select_tag = lightTagList[randomIndex]
tag_info = tagDict[select_tag]
tag_list_info = tag_info.split('/')
tag_id = tag_list_info[len(tag_list_info) - 1]
expected_result = init_expected_result()
expected_result['status'] = 200
expected_result['content'] = [["$.tag", select_tag, "equal"]]
expected_result['responseTime'] = maxResponseTime
# could be nice: check cross references between tasks and tags
tc.addStep("getTagInfo", args=[tag_id], expected=expected_result)
test_result = tc.executeTest()
logResults(tc, testNumber, test_result, logfilename)
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1

time.sleep(sleepDelay)

tc = TestCase("Retrieve tag details for an unexisting tag", "NOK")
randRange = 100
randomIndex = random.randrange(randRange)
for k, v in tagDict.items():
   tag_list_info = v.split('/')
   tag_id = tag_list_info[len(tag_list_info) - 1]
   if randomIndex == tag_id:
      randomIndex = random.randRange(randRange,randRange+100)
      randRange+= 100
   else:
      break
expected_result = init_expected_result()
expected_result['status'] = 404
expected_result['content'] = []
expected_result['responseTime'] = maxResponseTime
# could be nice: check cross references between tasks and tags
tc.addStep("getTagInfo", args=[randomIndex], expected=expected_result)
test_result = tc.executeTest()
logResults(tc, testNumber, test_result, logfilename)
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1

time.sleep(sleepDelay)

tc = TestCase("Delete task while authentified as NOT the owner", "NOK")
if type(taskList) is dict:
   select_task = taskList
else:
   tl = jsonpath.jsonpath(taskList, '$[?(@.username=="'+otherUser+'")]')
   if tl:
      select_task = tl[0]
   else:
      raise NameError("no task found for " + otherUser)
select_id = select_task["id"]
expected_result = init_expected_result()
expected_result['status'] = 401
expected_result['content'] = []
expected_result['responseTime'] = 1.0
tc.addStep('setCredentials',args=[mainUser,password])
tc.addStep('deleteTask',args=[select_id], expected=expected_result)
test_result = tc.executeTest()
logResults(tc, testNumber, test_result, logfilename)
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1
if not test_result:
   # must retrieve updated taskList:
   tc = TestCase("list tasks for testing purpose","OK")
   tc.addStep('listTasks')
   tc.executeTest()
   taskList = getTaskList(tc)

time.sleep(sleepDelay)


tc = TestCase("Delete task while authentified as the owner", "OK")
if type(taskList) is dict:
   select_task = taskList
else:
   tl = jsonpath.jsonpath(taskList, '$[?(@.username=="'+mainUser+'")]')
   if tl:
      select_task = tl[0]
   else:
      raise NameError("no task found for " + mainUser)
select_id = select_task["id"]
expected_result = init_expected_result()
expected_result['status'] = 200
expected_result['content'] = []
expected_result['responseTime'] = 1.0
tc.addStep('setCredentials',args=[mainUser,password])
tc.addStep('deleteTask',args=[select_id], expected=expected_result)
tc.addStep('listTasks')
test_result = tc.executeTest()
logResults(tc, testNumber, test_result, logfilename)
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1
if test_result:
   taskList = getTaskList(tc)

time.sleep(sleepDelay)

tc = TestCase("Retrieve Task information for unexisting task", "NOK")
# generate taskid not existing
randRange = 100
select_id = random.randrange(0,randRange)
while select_id in id_list:
   select_id = random.randrange(randRange,randRange + 100)
   randRange+= 100
expected_result = expected_taskInfo(select_id, False)
tc.addStep('getTaskInfo', args=[select_id], expected=expected_result)
test_result = tc.executeTest()
logResults(tc, testNumber, test_result, logfilename)
results = results2Array(tc, testNumber, test_result, results)
testNumber+=1

# for testing purpose: retrieve taglist:
tc = TestCase("Retrieve tag list for testing purpose", "OK")
expected_result = init_expected_result()
tc.addStep("listTags")
test_result = tc.executeTest()
logResults(tc, testNumber, test_result, logfilename)
if not test_result:
   results = results2Array(tc, testNumber, test_result, results)
testNumber+=1
if test_result:
   tagDict = getTagDict(tc)

array2csv(results, reportFilename)
# userFilename = './users.csv'
# taskFilename = './taskList.txt'
# tagFilename = './tagDict.txt'
array2csv(users,userFilename)

f = open(taskFilename,'w')
f.write(json.dumps(taskList))
f.close()

f = open(tagFilename, 'w')
f.write(json.dumps(tagDict))
f.close()


























