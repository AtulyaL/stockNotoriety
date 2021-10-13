'''Author: Atulya Lohani
Python Version: Python 3.8.8
Date completed: 13 October 2021'''

import requests
from tkinter import*
from datetime import date
from datetime import timedelta
API_KEY="**********"#Enter Key for NEWSAPI
master=Tk()
master.title("Select Stock")
master.geometry('400x400')
entry=Entry(master, width=20)
entry.pack()

def getStockName():
    name=entry.get()
    master.quit()
    return name
Button(master, text="Submit", command=getStockName).pack()
master.mainloop()

def getDate():
    return (date.today() -timedelta(days=7)).strftime("%Y-%m-%d")

def rate(dict):
    """Returns a rating of the stock name given by the user. 
        This is purely based on certain keywords that might indicate a stock's
        performance between the current date and the last seven days from the current date"""
    #print(getPages().url)
    titles=[]
    descriptions=[]
    negative=['bad','bearish','bombshell','down','don\'t buy','avoid','plunge',
    'bad market','struggle','drop','fall','fail',
    'nervous','over','dive','negative','underperforms','overrated']
    positive=['rally','should buy','up', 'soar','jumps',
    'positive','leads','high','climbs','strong',
    'outperforms','overcome','beat','underrated','increases',
    'rallies','surges','surging','pay off','rise']
    rating=0
    counter=0
    for article in dict['articles']:
            titles.append(article['title'])
            descriptions.append(article['description'])
    for i in range(len(titles)):
        for j in range(len(negative)):
            if(rating>=0 and negative[j] in titles[i]):
                rating=rating-1
                counter=counter+1
        for z in range(len(positive)):
            if(positive[z] in titles[i] and rating<=counter):
                rating=rating+1
                counter=counter+1
    #rating adjusted for descriptions
    for i in range(len(descriptions)):
        for j in range(len(negative)):
            if(rating>=0 and negative[j] in descriptions[i]):
                rating=rating-1
                counter=counter+1
        for z in range(len(positive)):
            if(positive[z] in descriptions[i] and rating<=counter):
                rating=rating+1
                counter=counter+1
    return (rating,counter)

def getPagesRating():
    """
    Returns a dictionary full of json from as many pages as possible of results from the newsAPI
    """
    articles=0
    count=1
    rating=0
    date=getDate()
    name=getStockName()
    while(requests.get('https://newsapi.org/v2/everything?q='+name+
    '&page='+str(count)+'&from='+date+
    '&language=en&domains=forbes.com,finance.yahoo.com,'+
    'prnewswire.com,investopedia.com,nvestorplace.com,'+
    'seekingalpha.com,nasdaq.com,fxstreet.com,investorsobserver.com,'
    'fool.com&sortBy=publishedAt&apiKey='+API_KEY).json()["status"]=="ok"):

        req=rate(requests.get('https://newsapi.org/v2/everything?q='+name+
        '&page='+str(count)+'&from='+date+'&language=en&domains=forbes.com,'+
        'finance.yahoo.com,prnewswire.com,investopedia.com,nvestorplace.com,seekingalpha.com,'+
        'nasdaq.com,fxstreet.com,investorsobserver.com,'+
        'fool.com&sortBy=publishedAt&apiKey='+API_KEY).json())
        rating=rating+req[0]
        articles=articles+req[1]
        count=count+1
    return round((rating/articles)*100)
def output():
    """Creates a tkinter window displaying the results"""
    rating=getPagesRating()
    root=Tk()
    root.title("Results")
    root.geometry("100x200")
    text=Label(root, text=str(rating))
    if(rating<70):
        text.config(foreground="red")
    elif(rating<90 and rating>80):
        text.config(foreground="yellow")
    else:
        text.config(foreground="green")
    text.pack()
    root.mainloop()
    

output()

