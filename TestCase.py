#!/usr/bin/env python
#-*- coding: utf-8 -*-

import TestRequest
from TestRequest import *
import jsonpath
import base64

class TestCase:
   title=''
   type=''
   #type stands for OK or NOK testcase
   steps={}
   stepNumber=0
   results={}
   request=TestRequest()
   token_expiration = 600
   
   def __init__(self,title,type):
      self.title = title
      self.type = type
      self.results = {}
      self.steps = {}
      stepNumber=0
      self.request = TestRequest()
      token_expiration = 600
   
   def addStep(self,teststep,**options):
      if options.get('args'):
         args = options.get('args')
      else:
         args = ''
      
      if options.get('expected'):
         expected = options.get('expected')
      else:
         expected = []
      
      self.steps[self.stepNumber]={'method':teststep,'args':args,'expected':expected}
      self.stepNumber+=1
      
   def executeTest(self):
      result = False
      print("Execution of " + self.title)
      print("=============================================")
      for s_i,s_val in self.steps.items():
         to_execute = getattr(self.request, s_val['method'])
         if len(s_val['args']) > 0:
            res = to_execute(*s_val['args'])
         else:
            res = to_execute()
         self.results[s_i] = {"step":s_i, "request": self.request.request_trace, \
         "responseStatus": self.request.response_status, "responseHeaders": self.request.response_headers, "responseBody":self.request.response_body, "responseTime":self.request.response_time}
         result = self.checkResults(s_i)
         # exit the loop if something is wrong:
         if not result:
            print("+++NOK+++NOK+++NOK+++NOK+++NOK+++NOK+++NOK+++")
            return result
      print("===================================================================")
      return result
            
   
   def checkResults(self,stepIndex):
      expected = self.steps[stepIndex]['expected']
      if len(expected) == 0:
         # nothing to check here
         self.results[stepIndex] = {"step":stepIndex, "request": self.steps[stepIndex]['method'], "responseStatus": 0, "testResult": "OK"}
         return True
      # expected is a dictionary of elements:
      ## status = int: http status code
      ## content = list of strings: jsonpath to the value to check
      ## response time = int: response time must be inferior to the value
      # each item of the dictionnary is built as a list like this:
      #[value to check in the response, value to compare, method to use to check the value]
      testResultString = ''
      if type(expected['status']) is not list:
         if expected['status'] > 0:
            exp_status = expected['status']
            resp_status = self.request.response_status
            if exp_status == resp_status:
               testResultString = testResultString + 'HTML Status code OK\n'
            elif (exp_status >= 400 | exp_status < 500) & (resp_status == 500):
               testResultString = testResultString + 'HTML Status code NOK: ' + str(resp_status) + ' shows inappropriate error managment \n'
            else:
               self.results[stepIndex]['testResult'] = testResultString + "status code NOK: got " + str(resp_status) + " instead of expected " + str(exp_status)
               return False
      else:
         exp_status = expected['status']
         resp_status = self.request.response_status
         if resp_status in exp_status :
            testResultString = testResultString + 'HTML Status code OK\n'
         elif resp_status == 500:
            for exp in exp_status:
               if (exp >= 400) | (exp < 500):
                  testResultString = testResultString + 'HTML Status code NOK: ' + str(resp_status) + ' shows inappropriate error managment \n'
                  break
               elif exp == resp_status:
                  testResultString = testResultString + 'HTML Status code OK\n'
                  break
               else:
                  self.results[stepIndex]['testResult'] = testResultString + "status code NOK: got " + str(resp_status) + " instead of expected " + str(exp_status)
                  return False
         else:
            self.results[stepIndex]['testResult'] = testResultString + "status code NOK: got " + str(resp_status) + " instead of expected " + str(exp_status)
            return False
            
      if len(expected['content']) > 0:
         for c in expected['content']:
            path = c[0]
            expected_value = c[1]
            method = c[2]
            # todo: create special check for list of tasks
            response = json.loads(self.results[stepIndex]['responseBody'])
            if not jsonpath.jsonpath(response,path):
               if (type(expected_value) is list) & (len(expected_value) == 0):
                  pass
               else:
                  self.results[stepIndex]['testResult'] = testResultString + path + ' NOK in response: not existing\n'
                  return False
            else:
               actual_value = jsonpath.jsonpath(response,path)
               testResultString = testResultString + path + ' exists \n'

            if method == "equal":
               if actual_value[0] == expected_value:
                  testResultString = testResultString + path + ' OK \n'
               else:
                  self.results[stepIndex]['testResult'] = testResultString + path + ' NOK in response: ' + str(actual_value[0]) + '\n'
                  return False
            elif method == "listEqual":
               if len(expected_value) == 0:
                  testResultString = testResultString + path + ' OK \n'
               elif len(expected_value) != len(actual_value):
                  self.results[stepIndex]['testResult'] = testResultString + path + ' NOK in response: ' + str(actual_value) + '\n'
                  return False
               else:
                  actual_value.sort()
                  expected_value.sort()
                  if actual_value == expected_value:
                     testResultString = testResultString + path + ' OK \n'
                  else:
                     self.results[stepIndex]['testResult'] = testResultString + path + ' NOK in response: ' + str(actual_value) + '\n'
                     return False
            elif method == "taskDictListEqual":
               actual_value = sorted(actual_value, key=lambda task: task['id'])
               expected_value = sorted(expected_value, key=lambda task: task['id'])
               if len(actual_value) == len(expected_value):
                  i=0
                  same=True
                  for a in actual_value:
                     if a != expected_value[i]:
                        same=False
                        break
                     i+=1
                  if same:
                     testResultString = testResultString + path + ' OK \n'
                  else:
                     self.results[stepIndex]['testResult'] = testResultString + path + ' NOK in response: ' + str(actual_value) + '\n'
                     return False
               else:
                  self.results[stepIndex]['testResult'] = testResultString + path + ' NOK in response: ' + str(actual_value) + '\n'
                  return False
            elif method == "tagDictEqual":
               if (len(actual_value) == 0) & (len(expected_value) == 0):
                  testResultString = testResultString + 'no tags:  OK \n'
               else:
                  tmplist = []
                  # expected_value is a list of tagnames
                  # actual_value is a list of 1 dictionary, to transform into list of tagnames:
                  for k,v in actual_value[0].items():
                     tmplist.append(k)
                  tmplist.sort()
                  actual_value = tmplist
                  expected_value.sort()
                  if actual_value == expected_value:
                     testResultString = testResultString + 'tags  OK \n'
                  else:
                     self.results[stepIndex]['testResult'] = testResultString + 'tags NOK in response: ' + str(actual_value) + '\n'
                     return False
            elif method == "checkToken":
               # print("check token " + actual_value[0])
               if self.checkToken(actual_value[0]):
                  testResultString = testResultString + path + ' OK \n'
               else:
                  self.results[stepIndex]['testResult'] = testResultString + 'Token NOK: ' + actual_value[0] + '\n'
                  return False
            elif method == "equalZuluTime":
               # print('check date')
               actual_time = time.strptime(actual_value[0][:19], "%Y-%m-%dT%H:%M:%S")
               expected_time = time.gmtime(self.request.timestamp)
               if (actual_time == expected_time):
                  testResultString = testResultString + path + ' OK \n'
               else:
                  # self.results[stepIndex]['testResult'] = testResultString + path + ' NOK: ' + actual_value[0] + '\n'
                  # return False
                  testResultString = testResultString + path + ' NOK: ' + actual_value[0] + '\n'
            elif method == "exists":
               # no need to do something, it is already checked before
               pass
            elif method == "checkInList":
               # for tags: both actual and expected are list
               if type(expected_value) is list:
                  if expected_value.sort() == actual_value.sort():
                     testResultString = testResultString + path + ' OK \n'
                  else:
                     self.results[stepIndex]['testResult'] = testResultString + path + ' NOK: ' + str(actual_value) + '\n'
                     return False
               else:
               # for tasks: actual = list of tasks while expected = taskname in a string
                  if expected_value in actual_value:
                     testResultString = testResultString + path + ' OK \n'
                  else:
                     self.results[stepIndex]['testResult'] = testResultString + path + ' NOK: ' + str(actual_value) + '\n'
                     return False
            else:
               raise NameError("TEST ERROR: Verification method " + method + " is not implemented")
               
      if expected['responseTime'] > 0:
         if self.request.response_time.total_seconds() > expected['responseTime'] :
            testResultString = testResultString + 'Response time NOK: ' + str(self.request.response_time.total_seconds()) + '\n'
         else:
            testResultString = testResultString + 'Response time OK\n'
            
      self.results[stepIndex]['testResult'] = testResultString
      return True
   
   def checkToken(self,token):
      token_ok = False
      request_ts = (int)(round(self.request.timestamp))
      try:
         token_byte = base64.urlsafe_b64decode(token)
         token_str = token_byte.decode("utf-8","ignore").split('}')[0] + '}'
         token_dict = json.loads(token_str)
      except:
         print("Cannot decode token " + token)
      
      if token_dict['alg'] != 'HS256':
         raise NameError("TEST ERROR: Token management changed, update needed")
      
      iat = token_dict['iat']
      exp = token_dict['exp']
      if (token_dict['iat'] != request_ts) | (token_dict['exp'] != request_ts + self.token_expiration):
         print(token_dict['iat'])
         print(request_ts)
         print("====================")
         print(token_dict['exp'])
         print(request_ts + self.token_expiration)
         print ("TEST WARNING: the time is not right somewhere")
      if token_dict['exp'] != token_dict['iat'] + self.token_expiration :
         raise NameError("Token expiration issue")
      else:
         token_ok = True
      return token_ok

      
      







