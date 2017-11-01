def printResults(results):
   for r_i, r_val in results.items():
      print("Step #" + str(r_val['step']))
      print(r_val['request'])
      if r_val['responseStatus'] > 1 :
         print('Response:')
         print(r_val['responseStatus'])
         print(r_val['responseHeaders'])
         print(r_val['responseBody'])
         print(r_val['responseTime'])
         print(r_val['testResult'])
# todo: process results better than this and generate report

def csvHeader():
   return [["Index", "Title", "Type", "Request", "Response Status", "Response Time", "Result"]]
   
def results2Array(tcase, index, globalResult, out=[]):
   title = tcase.title
   type = tcase.type
   if globalResult:
      ok = 'OK'
   else:
      ok = 'NOK'
   line = [index, title, type, '', '', '', ok]
   out.append(line)

   for i, result in tcase.results.items():
      if result['step'] != i:
         raise NameError('nothing works as expected')
      stepIndex = str(index) + '.' + str(result['step'])
      title = tcase.steps[i]['method']
      request = str(result['request'].split('\n')[0])
      try:
         respTime = str(result['responseTime'])
      except:
         respTime = []
         pass
      respStatus = str(result['responseStatus'])
      fullTestResult = result['testResult']
      if 'NOK' in fullTestResult:
         testResult = 'NOK'
      else:
         testResult = 'OK'
      out.append([stepIndex, title,'', request, respStatus, respTime, testResult])
   return out

def logResults(tcase, index, globalResult, filename):
   # self.steps[self.stepNumber]={'method':teststep,'args':args,'expected':expected}
   # self.results[s_i] = {"step":s_i, "request": self.request.request_trace, \
         # "responseStatus": self.request.response_status, "responseHeaders": self.request.response_headers, "responseBody":self.request.response_body, "responseTime":self.request.response_time}
   #self.results[stepIndex]['testResult'] = testResultString + "status code NOK: got " + str(resp_status) + " instead of expected " + str(exp_status)
   f = open(filename, 'w')
   
   f.close()