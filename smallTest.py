#!/usr/bin/env python
#-*- coding: utf-8 -*-
import random
import expected_result
from expected_result import *
import process_results
from process_results import *
import os

getTagDict = lambda tcase: json.loads(tcase.request.response_body)

results = csvHeader()

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

print(csv2array(userFilename))
taskList = file2json(taskFilename)
print(taskList)
tagList = file2json(tagFilename)
print(tagList)