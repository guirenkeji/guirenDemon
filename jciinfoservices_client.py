# -*- coding: utf-8 -*-
import urllib2
import urllib
import json
import os
import httplib
import requests
import logging

logging.basicConfig()
# logging.error('hi')
JOB_NAME= os.environ['JOB_NAME']
STRING = os.environ['STRING']
BUILD_ID = os.environ['BUILD_ID']
content = STRING
contentlist = content.split('&')
list = []
for i in contentlist:
    p = i.split('=')
    p = p[1] 
    l = list.append(p)
(serverip,port) =tuple(list)
# curl -i -X POST -H "Content-Type: application/json" -d '{"url":"'testcat'"}' 20.26.17.145:5002/jenkins/testrelease
httpClient = httplib.HTTPConnection(serverip,port, timeout=30)
def updatestart ():
    params = {'STATUS':'0',}
    httpupdatestatuspost(params)
    print "updata start"  
def savelog (JOB_NAME,BUILD_ID,i):
    params = {'jobname':JOB_NAME,'jobbuildid':BUILD_ID,'log':i}
    httplogpost(params)
    print 'log save ok'
def savestatusinfo ():
    print 'save status ok'    
def getstatus (JOB_NAME):
    params = {'JOB_NAME':JOB_NAME}
    httpstatuspost(params)
    print 'getstatus'
#在中心获取scm相关信息    
def getscminfo ():
    params = {'JOB_NAME':JOB_NAME,'build_id':BUILD_ID}
    scmdata = httpSCMinfoPost(params)
    return scmdata   
def uploadFile():
    params = {'JOB_NAME':JOB_NAME}
    data = httpUploadFilePost(params)
    data = data.read()
    data = eval(data)
    print data['data']['icloudUrl']
    url = data['data']['icloudUrl']
    icloudip = data['data']['icloudIP']
    icloudport = data['data']['icloudport']
    print url
    path = JOB_NAME+'.war'
    files = {'file': open(path, 'rb')}
    r = requests.post(url, files=files) 
    data = r.text
    data = json.loads(data)
    scmdata = getscminfo()
    icloudinfo = {'app_id':JOB_NAME,'file_id':data['data']['id'],'build_id':BUILD_ID,'scm':scmdata} 
    httpIcloudUploadPost(icloudinfo,icloudip,icloudport)
def httplogpost (params):
    try:
        data = json.dumps(params)
#         httpClient = httplib.HTTPConnection("127.0.0.1",5013, timeout=30)
        httpClient.request("POST",'/ci/client/1.0/log',data,{"Content-Type":"application/json"})
        response = httpClient.getresponse()
        print response
    
    except Exception, e:
        print e 
def httpstatuspost (params):
    try:
        data = json.dumps(params)
        
        httpClient.request("POST",'/ci/client/1.0/status',data,{'Content-Type': 'application/json'})
        response = httpClient.getresponse()
        print response
    
    except Exception, e:
        print e  
def httpupdatestatuspost (params):
    try:
        data = json.dumps(params)
        
        httpClient.request("POST",'/ci/client/1.0/updatestatus',data,{'Content-Type': 'application/json'})
        response = httpClient.getresponse()
        print response
    
    except Exception, e:
        print e
def httpUploadFilePost (params):
   try:
       data = json.dumps(params)
  
       httpClient.request("POST",'/ci/client/1.0/uploadfile',data,{'Content-Type': 'application/json'})
       response = httpClient.getresponse()
       return response
   
   except Exception, e:
       print e  
def httpSCMinfoPost (params):
   try:
       data = json.dumps(params)
  
       httpClient.request("POST",'/ci/client/1.0/scm/data',data,{'Content-Type': 'application/json'})
       response = httpClient.getresponse()
       scm = response.read()
       scm =json.loads(scm)
       
       return scm
   
   except Exception, e:
       print e        
def httpIcloudUploadPost (params,icloudip,icloudport):
   try:
       data = json.dumps(params)
       print data,icloudip,icloudport
       httpClient = httplib.HTTPConnection(icloudip,icloudport,timeout=30)
       httpClient.request("POST",'/iCloud/v1/addAppVersion.dox?token=2Kw1Tu9SUK5eK0uM',data,{'Content-Type': 'application/json'})
       response = httpClient.getresponse()
       return response
   except Exception, e:
       print e  
                                      
if __name__ == '__main__':
#     httpSCMinfoPost({'appname':'demo','build_id':4})
    uploadFile()
#     savelog('234','23','34235')    
    