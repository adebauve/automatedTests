def printResults(results):
   outstring = ''
   for r_i, r_val in results.items():
      outstring+= 'Step #' + str(r_val['step']) + '\n'
      outstring+= r_val['request'] + '\n'
      if r_val['responseStatus'] > 1 :
         outstring+= 'Response:\n'
         outstring+= str(r_val['responseStatus']) + '\n'
         outstring+= str(r_val['responseHeaders']) + '\n'
         outstring+= r_val['responseBody'] + '\n'
         outstring+= str(r_val['responseTime']) + '\n'
         outstring+= r_val['testResult'] + '\n'
   return outstring
# todo: process results better than this and generate report

def csvHeader():
   return [["Index", "Title", "Result", "Request", "Response Status", "Response Time", "Type"]]
   
def results2Array(tcase, index, globalResult, out=[]):
   title = tcase.title
   if tcase.type == "OK":
      type = "passing"
   else:
      type = "failing"
   type = tcase.type
   if globalResult:
      ok = 'OK'
   else:
      ok = 'NOK'
   line = [index, title, ok, '', '', '', type]
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
      out.append([stepIndex, title,testResult, request, respStatus, respTime, ''])
   return out

def logResults(tcase, index, globalResult, filename):
   # self.steps[self.stepNumber]={'method':teststep,'args':args,'expected':expected}
   # self.results[s_i] = {"step":s_i, "request": self.request.request_trace, \
         # "responseStatus": self.request.response_status, "responseHeaders": self.request.response_headers, "responseBody":self.request.response_body, "responseTime":self.request.response_time}
   #self.results[stepIndex]['testResult'] = testResultString + "status code NOK: got " + str(resp_status) + " instead of expected " + str(exp_status)
   f = open(filename, 'a')
   f.write(tcase.title + " START :\n================================================ \n")
   f.write(printResults(tcase.results))
   f.write(tcase.title + " END \n================================================ \n\n")
   f.close()