

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
    
    location =result.get("location")
    dict["location"]=location
    bhk =result.get("property-size").get("number")
    dict["bhk"]=bhk
    propertyType =result.get("property-type")
    dict["propertyType"]=bhk
    #if query is None:
     #   return None
    result=search(dict)
    
    #data = json.loads(req)
    res = makeWebhookResult(result)
    return res





def makeWebhookResult(data):
    
    #print("Response:")
    #print(speech)
    #print(len(data[0]))
    return "{"+buildJson(data[0],data[1],data[2],data[3],data[4])+"}"
	  

	        

def search(query):
    bhk="2"
    city="chennai"
    budgetMin="5000"
    budgetMax="10000"
    html="http://www.magicbricks.com/property-for-rent/residential-real-estate?bedroom="+bhk+"&proptype=Residential-House,Villa&cityName="+city+"&BudgetMin="+budgetMin+"&BudgetMax="+budgetMax;
    #req = urllib.request.Request(html, headers={'User-Agent': 'Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev> (KHTML, like Gecko) Chrome/<Chrome Rev> Mobile Safari/<WebKit Rev>'})
    #print(html)
    #soup = BeautifulSoup(urlopen(req).read(),"html.parser")
    content = requests.post(html,headers={'User-Agent': 'Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev> (KHTML, like Gecko) Chrome/<Chrome Rev> Mobile Safari/<WebKit Rev>'}).content
    soup = BeautifulSoup(content,"html.parser")
    projLink=[]
    projDetail=[]
    projImage=[]
    projDesc=[]
    projDescList=[]
    project=[]
    for item in soup.find_all('a',attrs={'class':'resultDetailLink'}):
            projDetail.append(item.h3.text.replace("\n",""))
            projLink.append("http://m.magicbricks.com"+item["href"])
    for item in soup.find_all('div',attrs={'class':'projImage'}):
            projImage.append(item["data-original"])
    for item in soup.find_all('div',attrs={'class' : 'propertyDesc_Less'}):
            projDesc.append(item.text)
    for item in soup.find_all('div',attrs={'class' : 'projectDescListing'}):
            projDescList.append(item.text)
    project.append(projLink)
    project.append(projDetail)
    project.append(projImage)
    project.append(projDesc)
    project.append(projDescList)
		

    return project

def buildJson(v,w,x,y,z):
    str=""
    str +="\"messages\": ["
    for i in range(10):
            str +="{ \
  \"type\": 1, \
  \"title\": \""+w[i]+"\", \
  \"subtitle\": \""+y[i]+"\",\
  \"imageUrl\": \""+x[i]+"\",\
  \"buttons\": [\
    {\
      \"text\": \"link\",\
      \"postback\": \""+v[i]+"\"\
    }\
  ]\
},"
    str =str[:-1]+"],\"speech\": \"Here you go\",\"displayText\": \"\",\"data\": \"data\",\"contextOut\": [],\
    \"source\": \"apiai-search-webhook\" "
    return str         
       


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')

