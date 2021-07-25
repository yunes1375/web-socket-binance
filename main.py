from flask import Flask,request,render_template, flash,redirect, send_file,url_for,jsonify
import time
import pymongo
import json
from datetime import datetime
def deltatime():
    nowtime=time.time()
    #calcuting time for 10 hours later or any other time
    querytime=int(nowtime)
    print(querytime)
    return querytime
def mongodata():
    data={}
    #calcuting time for Query
    deltatime1=deltatime()
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["binance"]
    mycol = mydb["trades"]
    #Query string for selection objects for last 10 hour 
    mydoc = mycol.find({"T": {"$gte": deltatime1}}).sort("value",-1)
    #selection 10 best trades or any number of best trades
    for x in range(0,10):
       dic1={}
       #select time of trade,Coin name,Price,quantity and value of best trades
       dic1['time']=str(datetime.fromtimestamp(int(mydoc[x]["E"])/1000))
       dic1['Crypto']=mydoc[x]['s']
       dic1['Price']=mydoc[x]['p']
       dic1['quantity']=mydoc[x]['q']
       dic1['value']=mydoc[x]['value']
       data[x]=dic1
    return data
app = Flask(__name__)
@app.route('/besttrades/', methods=['GET', 'POST'])
def testfn():
    # GET request
    if request.method == 'GET':
        #getting data of 10 best trade data from mongo by mongodata function as dictionary and converting to json
        return json.dumps(json.dumps(mongodata()))
    # POST request
    if request.method == 'POST':
        return 'Sucesss', 200
if __name__ == "__main__":
       app.run(host='127.0.0.1',port=80)