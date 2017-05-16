"""
@author-nikhil_ponnuru

"""

import requests
import redis
import json
import threading


#connection for redis
r=redis.Redis(host='localhost',port=6379)


url_gainers="https://www.nseindia.com/live_market/dynaContent/live_analysis/gainers/niftyGainers1.json"

url_loosers="https://www.nseindia.com/live_market/dynaContent/live_analysis/losers/niftyLosers1.json"
#the above urls are json api links which give details to the nse website and hence those are being used here to parse data


#this threaded function fetches from the above mentioned urls, data in the form of json and stores them in redis as hash datatype
def fetch_and_store():
    threading.Timer(30000,fetch_and_store).start()
   # print("inside")

    gainers_str = requests.get(url_gainers).text

    loosers_str = requests.get(url_loosers).text
    print(gainers_str)



    json_gainers =  json.loads(str(gainers_str))

    json_loosers=json.loads(str(loosers_str))




    # after every successful scraping updating with the values in hash of redis--it is only O(1) in time complexity, so instead
    # of checking if a string exists and equal to new string else updating it is better to update directly all values even if they are same
    for i in range(0, 10):
        r.hset('gainers', i, json_gainers['data'][i])
        r.hset('loosers', i, json_loosers['data'][i])
#hash datatype was used because we have 2 categoies 1)loosers and ii)gainers hence to differentiate them and to store 10 values in each under their  company name



#retriving and displaying the values. here string is converted to dictionory (json) object

def retrive_and_display():

    gainers=r.hget('gainers',0)
    loosers = r.hget('loosers', 0)

    for i in range(1,10):


        gainers=gainers+","+r.hget('gainers',i)
        loosers=loosers+","+r.hget('loosers',i)
    gainers='{"data":['+gainers.replace("'",'"').replace("u",'')+"]}"
    loosers='{"data":['+ loosers.replace("'",'"').replace("u",'')+"]}"


    return json.loads(gainers),json.loads(loosers)














