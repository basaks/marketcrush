'''

This is a tool to produce some random data sets.
This is to test the strategy.
The trend bias indicates how strongly the data should be
trending.

The result will look like this:
instrument_token,tradingsymbol,time,open,high,low,close,volume
256265,NIFTY 50,2015-04-13 09:15:00 UTC,8801.75,8801.75,8775,8775.75,0
'''
from pylab import *
from numpy import *
from datetime import datetime,timedelta

TREND_BIAS = -0.1

fid = open('sample_data/random2.csv','w')

fid.write('instrument_token,tradingsymbol,time,open,high,low,close,volume\n')
t0 = datetime(2015,4,13,9,15)

Open = 8801.75
price = []
for i in range(100000):
    this_time = t0 + timedelta(0,i*60)
    time_str = str(this_time)+' UTC'
    p = random.randn(3)+TREND_BIAS
    Low = Open + min(p)
    High = Open + max(p)
    Close = Open + sort(p)[1]
    fid.write('256265,NIFTY 50,{},{},{},{},{},0\n'.format(time_str,Open,High,Low,Close))
    Open = Close
    price.append(Open)

plot(price)
show()

