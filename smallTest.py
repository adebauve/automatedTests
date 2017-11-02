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

tagList = []
   
# small test
tc = TestCase("Retrieve all the tags","OK")
print(tc.title + " START :\n================================================")
expected_result = init_expected_result()
expected_result['status'] = 200
expected_result['content'] = [[".", tagList, "tagDictEqual"]]
expected_result['responseTime'] = maxResponseTime
tc.addStep("listTags", expected=expected_result)
test_result = tc.executeTest()
printResults(tc.results)

tagDict = getTagDict(tc)

print(type(tagDict))
print(tagDict)

try:
   os.remove('./smallLog.txt')
except:
   pass
logResults(tc, 1, test_result, './smallLog.txt')
array2csv(results, './test.csv')
