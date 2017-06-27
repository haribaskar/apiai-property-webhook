

#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import requests
from flask import Flask
from flask import request
from flask import make_response
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request
import re


# Flask app should start in global layout
app = Flask(__name__)


@app.route('/chatbot', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    #print("Request:")
    #print(json.dumps(req, indent=4))

    res = processRequest(req)
    #print(res)
    #print("*********************")
    #res = json.dumps(res, indent=4)
    #print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

@app.route('/chat', methods=['GET'])
def web():
    
    return "WELCOME :)"


def processRequest(req):
    #if req.get("result").get("action") != "input.welcome":
    #    return {"action is empty"}
    dict={}
    result = req.get("result").get("parameters")
    max_currency =result.get("max_currency")
    max_budget =result.get("max_budget")
    resolvedQuery=req.get("result").get("resolvedQuery")
    location =result.get("location")
    dict["location"]=location
    try:
        bhk =result.get("property-size").get("number")
        unit =result.get("property-size").get("unit")
    except:
        bhk=1
        unit="bhk"    
    dict["bhk"]=bhk
    propertyType =result.get("property-type")
    dict["propertyType"]=bhk
    if max_currency is None:
         max_currency=""
    if max_budget is None:
         max_budget=""
    searchQuery=str(bhk)+" "+str(unit)+" "+str(propertyType)+" near "+str(location)+" "+str(max_budget)+" "+str(max_currency)+" site www.brigadegroup.com"
    print(searchQuery)
    result=search(searchQuery)
    
    #data = json.loads(req)
    res = makeWebhookResult(result)
    return res





def makeWebhookResult(data):
    print(data)
    #print("Response:")
    #print(speech)
    #print(len(data[0]))
    return "{"+buildJson(data[0],data[1])+"}"
	  

	        

def search(query):
    
    query=query.strip().split()
    query="+".join(query)
    html="https://www.google.co.in/search?q="+query
    req = urllib.request.Request(html, headers={'User-Agent': 'Mozilla/5.0 '})
    soup = BeautifulSoup(urlopen(req).read(),"html.parser")
    projLink=[]
    projDetail=[]
    projImage=[]
    projDesc=[]
    projDescList=[]
    project=[]
    h3tags = soup.find_all( 'h3', class_='r' )
    for h3 in h3tags:
          try:
              projDetail.append(h3.a.text)
              projLink.append( re.search('url\?q=(.+?)\&sa', h3.a['href']).group(1) )
          except:
              continue

    project.append(projLink)
    project.append(projDetail)
    project.append(projImage)
    project.append(projDesc)
    project.append(projDescList)
		

    return project

def buildJson(v,w):
    
    str=""
    for i in range(len(v)):
            str +=w[i]+"\n"+v[i]

    return "\"speech\": \""+str+"\",\"imageUrl\": \"https://www.google.co.in/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png\",\"displayText\": \"\",\"data\": \"data\",\"contextOut\": [],\
    \"source\": \"apiai-search-webhook\" "
           
       


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')

