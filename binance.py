import websocket,json , pymongo
#connection string formongodb
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["binance"]
mycol = mydb["trades"]
#function for inserting data in mongodb and calcuting value of trades
def on_message(ws, message):
    res = json.loads(message)
    price=float(res['data']['p'])
    quantity=float(res['data']['q'])
    value=price*quantity
    res['data']['value']=value
    mycol.insert_one(res['data'])
    
    
#function for closing connection
def on_close(ws, close_status_code, close_msg):
    print("### closed ###")
#Binance API string
socket = 'wss://stream.binance.com:9443/stream?streams=btcusdt@aggTrade/etcusdt@aggTrade/ltcusdt@aggTrade/trxusdt@aggTrade/vetusdt@aggTrade'
ws = websocket.WebSocketApp(socket,on_message=on_message,on_close=on_close)
#calling api countinuesly
ws.run_forever()