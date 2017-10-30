#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import json
import requests
from requests import Request, Session
from requests.auth import HTTPBasicAuth
# sys.path.append('path-to-ptyhon')

class TestRequest:
   session = Session()
   endpoint = 'http://debauve.qatest.dataiku.com:80/'
   url=endpoint
   cookie = {}
   request_trace=''
   response_status=0
   response_headers=''
   response_body=''
   response_time=0
   username=''
   password=''
   authentication = None
      
   # def setCookie(self,c):
      # self.cookie = c
      
   def setCredentials(self,user,pwd):
      self.username = user
      self.password = pwd
      self.authentication = HTTPBasicAuth(self.username,self.password)
   
   def resetCredentials(self):
      self.username = ''
      self.password = ''
      self.authentication = None
   
   def logRequest(self, req):
      self.request_trace = 'Request ' + req.method + ' ' + str(req.url)+'\nrequest headers:\n'+str(req.headers)+'\nrequest body:\n'+str(req.body)
      
   def saveResponse(self,resp):
      self.response_status = resp.status_code
      self.response_headers = resp.headers
      self.response_body = str(resp.text)
      self.response_time = resp.elapsed
      
   def callAndLog(self,pr):
      resp = self.session.send(pr)
         
      self.logRequest(pr)
      self.saveResponse(resp)
      # resp.raise_for_status()
      return resp

   ############ request definitions : ############
   def listTasks(self):
      self.url=self.endpoint
      req = Request('GET', self.url)
      prep_req = self.session.prepare_request(req)
      resp = self.callAndLog(prep_req)
      return resp
   
   def authenticate(self):
      self.url=self.endpoint+'authenticate'
      req = Request('POST',self.url)
      
      prep_req = self.session.prepare_request(req)
      bodydata = {'username':self.username,'password':self.password}
      
      prep_req.body = json.dumps(bodydata)
      prep_req.headers['Content-Type'] = 'application/json'
      prep_req.prepare_content_length(prep_req.body)
      resp = self.callAndLog(prep_req)
      return resp
      
   def createTask(self,title,tags):
      self.url = self.endpoint
      req = Request('PUT', self.url, auth=self.authentication)
         
      prep_req = self.session.prepare_request(req)
      bodydata = {"title":title,"tags":tags}
      
      prep_req.body = json.dumps(bodydata)
      prep_req.headers['Content-Type'] = 'application/json'
      prep_req.prepare_content_length(prep_req.body)
      resp = self.callAndLog(prep_req)
      return resp
      
   def getTaskInfo(self,taskid):
      self.url = self.endpoint + str(taskid)
      req = Request('GET', self.url, auth=self.authentication)
      
      prep_req = self.session.prepare_request(req)
      resp = self.callAndLog(prep_req)
      return resp
      
   def deleteTask(self,taskid):
      self.url = self.endpoint + str(taskid)
      req = Request('DELETE', self.url, auth=self.authentication)
      # delete task from another user works while it should be forbidden
      prep_req = self.session.prepare_request(req)
      resp = self.callAndLog(prep_req)
      
      return resp
   
   def updateTask(self,taskid,title='',tags=[],done=''):
      self.url = self.endpoint + str(taskid)
      req = Request('PATCH', self.url, auth=self.authentication)
      
      bodydata = {}
      if len(title) > 0 :
         bodydata['title'] = title
      if len(tags) > 0 :
         bodydata['tags'] = tags
      if len(done) > 0 :
         bodydata['done'] = done
      
      prep_req = self.session.prepare_request(req)
      
      prep_req.body = json.dumps(bodydata)
      prep_req.headers['Content-Type'] = 'application/json'
      prep_req.prepare_content_length(prep_req.body)
      resp = self.callAndLog(prep_req)
      return resp
      
   def listTags(self):
      self.url = self.endpoint + 'tags'
      req = Request('GET', self.url)
      prep_req = self.session.prepare_request(req)
      resp = self.callAndLog(prep_req)
      
   def getTagInfo(self,tagid):
      self.url = self.endpoint + 'tags/' + str(tagid)
      req = Request('GET', self.url)
      
      prep_req = self.session.prepare_request(req)
      resp = self.callAndLog(prep_req)
   
   def createUser(self,user,pwd):
      self.url = self.endpoint + 'users'
      req = Request('POST', self.url)
      
      bodydata = {}
      bodydata['username'] = user
      bodydata['password'] = pwd
      prep_req = self.session.prepare_request(req)
      
      prep_req.body = json.dumps(bodydata)
      prep_req.headers['Content-Type'] = 'application/json'
      prep_req.prepare_content_length(prep_req.body)
      resp = self.callAndLog(prep_req)
   
   def dropTheBase(self):
      self.url = self.endpoint + 'reset'
      req = Request('GET', self.url)
      
      prep_req = self.session.prepare_request(req)
      resp = self.callAndLog(prep_req)

########################## end of class TestRequest definition ##########################