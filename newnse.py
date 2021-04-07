import requests
import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Language': 'en-US,en;q=0.5', 'Connection': 'keep-alive',
           'Pragma': 'no-cache', 'Cache-Control': 'no-cache',
           'Referer': 'https://www.nseindia.com/get-quotes/derivatives?symbol=NIFTY&identifier=OPTIDXNIFTY01-04-2021CE14800.00'}



#making reuest to server with url and headers at mimic firefox browser
r = requests.get(url, headers=headers, timeout=5)
# r is response code from the server
print(r)
# r is converted into p json which is equivilant to dictnory in python
p = r.json()
#print(type(p))
print('\n')


# dict p from server has 2 keys - records  and filtered. we del records and are left with only filtered
del p["records"]
# we get contents of dictionary p in new dictionary named v
v = (p.get("filtered"))
# from 'dictionary v', we extract key=data which infact is a list. So x is list here.
x = (v.get("data"))

q = (p.get("filtered").get("data"))
# This gives no of items in the list: used later to iterate no of times in for loop to get CE and PE values
#length_of_list = (len(x))
#print(length_of_list)
print('\n')



#empty list created for series in pandas
strikelist = []
pricelist =[]
OIlist =[]
pricelistPE =[]
OIlistPE =[]

# function to parse through data and append relavent "limited" data to respective lists.
def listPopulator():
    for i in range(len(x)):
        strikelist.append((x[i].get("CE").get("strikePrice")))
        pricelist.append((x[i].get("CE").get("lastPrice")))
        OIlist.append((x[i].get("CE").get("changeinOpenInterest")))
        pricelistPE.append((x[i].get("PE").get("lastPrice")))
        OIlistPE.append((x[i].get("PE").get("changeinOpenInterest")))

listPopulator()

# creating new dictionary out of the list created above to be used as pandas dataframe

newdict = {' Call Chnage OI ': OIlist, 'Call Price ': pricelist, 'Strike': strikelist, 'Put Price': pricelistPE, 'Put Chnage OI': OIlistPE}
df = pd.DataFrame(newdict)
print(df.to_string())

print("\n      -------------- Option Chain Printed -------------- \n")

'''
#plotting of data
df.plot(subplots=True)
plt.show()
'''


'''  
print("\nCall Option\n")
print((x[0].get("CE").keys()))
# iterate through the list and get values of CE. [x[i]] being the index of list , i=1, i=2
for i in range(len(x)):
    #print((x[i].get("CE").keys()))
    print((x[i].get("CE").values()))
    #print("Strike price: ", (x[i].get("CE").get("strikePrice")))

print("\nPut Option\n")
# iterate through the list and get values of PE. [x[i]] being the index of list , i=1, i=2
for i in range(len(x)):
    #print((x[i].get("CE").keys()))
    print((x[i].get("PE").values()))
'''