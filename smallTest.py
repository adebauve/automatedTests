#!/usr/bin/env python
#-*- coding: utf-8 -*-
import random
import expected_result
from expected_result import *
import process_results
from process_results import *


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

# small test
tc = TestCase("Retrieve all the tags","OK")
print(tc.title + " START :\n================================================")
expected_result = init_expected_result()
tc.addStep("listTags", expected=expected_result)
test_result = tc.executeTest()
printResults(tc.results)

tagDict = getTagDict(tc)

print(type(tagDict))
print(tagDict)

results = results2Array(tc, 1, test_result, results)
print(results)

array2csv(results, './test.csv')
