import TestCase
from TestCase import *


def init_expected_result():
   return {'status':0,'content':[],'responseTime':1}
   
def expected_listTasks(knownTaskList=[], newTask=None, tags=[]):
   content = []
   if newTask:
      # check if the new task is in the response
      if len(tags) > 0:
         content = [["$[*].date",'',"exists"], ["$[*].done",'',"exists"], ["$[*].id",'',"exists"], ["$[*].tags[*].name",tags,"checkInList"], ["$[*].title",newTask,"checkInList"]]
      else:
         content = [["$[*].date",'',"exists"], ["$[*].done",'',"exists"], ["$[*].id",'',"exists"], ["$[*].title",newTask,"checkInList"]]
   elif len(knownTaskList) > 0:
      # check if the response contains the exact same content than the knownTaskList in parameter
      content = [["$[*]",knownTaskList,"dictListEqual"]]
   
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
      return {'status':[400,401], 'content':[], 'responseTime': 1.0}

def expected_taskInfo(task,OK=True):
   content = []
   if OK:
      if type(task) is int:
      # not an update: just check if the right task is return
         content = [["$.date", '', "exists"], ["$.done", '', "exists"], ["$.id", task, "equal"], ["$.tags", '', "exists"], ["$.title", '', "exists"], ["$.username", '', "exists"]]
      elif type(task) is list:
      # the list task is structured this way: [taskid, {item:value, item2:123, ...}]
         content = [["$.date", '', "exists"]]
         for t_i, t_val in task[1].items():
            if t_i == "done":
               content.append(["$.done", t_val, "equal"])
            elif t_i == "title":
               content.append(["$.title", t_val, "equal"])
            else:
               print(t_i + " not supported by the test")
         
         content.append(["$.id", task[0], "equal"])
         content.append(["$.tags", '', "exists"])
         content.append(["$.username", '', "exists"])
         
      return {'status':200, 'content': content, 'responseTime': 1.0}
   else:
      return {'status':404, 'content':content, 'responseTime': 1.0}
      
def expected_taskUpdate(task,OK=True):
   content = []
   if OK:
      content = [["$.date", '', "exists"]]
      for t_i, t_val in task[1].items():
         if t_i == "done":
            content.append(["$.done", t_val, "equal"])
         elif t_i == "title":
            content.append(["$.title", t_val, "equal"])
         else:
            print(t_i + " not supported as update in Test")
      
      content.append(["$.id", task[0], "equal"])
      content.append(["$.tags", '', "exists"])
      content.append(["$.username", '', "exists"])
      
      return {'status':200, 'content': content, 'responseTime': 1.0}
   else:
      return {'status':[401,403], 'content':content, 'responseTime':1.0}