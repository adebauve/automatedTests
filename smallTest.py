#!/usr/bin/env python
#-*- coding: utf-8 -*-
import random
import expected_result
from expected_result import *
import process_results
from process_results import *

# small test
tc = TestCase("Retrieve all the tags","OK")
print(tc.title + " START :\n================================================")
expected_result = init_expected_result()
tc.addStep("listTags", expected=expected_result)
tc.executeTest()
printResults(tc.results)