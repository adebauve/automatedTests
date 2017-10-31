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