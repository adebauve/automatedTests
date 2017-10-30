#!/usr/bin/env python
#-*- coding: utf-8 -*-

import TestRequest
from TestRequest import *

class TestCase:
   title=''
   type
   #type stands for OK or NOK testcase
   steps={}
   results={}
   request=TestRequest()
   
   def __init__(self,title,type):
      self.title = title
      self.type = type
      self.results = {}
      self.steps = {}
      self.request = TestRequest()
   
   def addStep(self,stepindex,teststep,arg=''):
      self.steps[stepindex]={'method':teststep,'args':arg}
      
   def executeTest(self):
      print(self.title)
      for s_i,s_val in self.steps.items():
         print(s_val['method'])
         to_execute = getattr(self.request, s_val['method'])
         if len(s_val['args']) > 0:
            res = to_execute(*s_val['args'])
         else:
            res = to_execute()
         self.results[s_i] = {"step":s_i, "request": self.request.request_trace, \
         "responseStatus": self.request.response_status, "responseHeaders": self.request.response_headers, "responseBody":self.request.response_body, "responseTime":self.request.response_time}