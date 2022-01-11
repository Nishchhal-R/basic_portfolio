#install dependecies (alpha_vantage,matplot) using pip3


from alpha_vantage.timeseries import TimeSeries
import requests
import csv
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
load_dotenv()

stocks=[]
data_list=[]

def get_stocks():
    print('Enter all stock symbols')
    while True:
        stock_name=input()
        if stock_name=='':
            break
        else:
            stocks.append(stock_name.upper())
    
get_stocks()

quantity=[]
def stock_quantity(times):
    print('Enter quantities of shares')
    for i in range(times):
        print('Enter amount of shares of ',stocks[i],':')
        amt=input()
        quantity.append(amt)
stock_quantity(len(stocks))

stock_dates=[]
def date_stocks(times):
    print('Enter date of buying stock(YYYY-MM-DD)')
    for i in range(times):
        
        print('Enter date for',stocks[i],':')
        date=input()
        stock_dates.append(date)
date_stocks(len(stocks))

def result(a,b,c,d):
    print('\n')
    b=float(b)
    c=float(c)
    d=float(d)
    print('Last trading price of',a,'was',("%.2f"%b))
    print('Initial investment was:\u20b9',("%.2f"%c))
    print('Current investment value is:\u20B9',("%.2f"%d))
    if d>c:
        profit=((d-c)*100)/c
        print('Profit is \u20b9',("%.2f"%(d-c)),'i.e +',("%.2f"%profit),'%')
        
    else:
        loss=((c-d)*100)/c
        print('Loss is \u20b9',("%.2f"%(c-d)),'i.e -',("%.2f"%loss),'%')
           
    print('\n')
    
    

def main():
    for st,dt,qt in zip(stocks,stock_dates,quantity):
        
        url_raw='https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+st+'.BSE'+'&datatype=csv&apikey='+os.getenv('API_key')

        url = url_raw

        with requests.Session() as s:
            download = s.get(url)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            
            my_list = list(cr)
            
            y=[]
            x=[]
            for i in range(1,len(my_list)):
                x.append(i)
            
            for j in range(1,len(my_list)):
                y.append(float(my_list[j][4]))
            
            for row in my_list:
                
                if row[0]==dt:
                   buying_price=row[4]
            
            ltp=my_list[1][4]
            current=float(ltp)*int(qt)
            initial=float(buying_price)*int(qt)

            result(st,ltp,initial,current)
            
            
            question=input('Do you want to see last 100 day movement(y/n)')
            if question=='y':
                plt.plot(x,y,color='black')
                plt.title('last 100 days movement')
                plt.xlabel('Days')
                plt.ylabel('Share price')
                plt.show()
            else:
                pass

main()


