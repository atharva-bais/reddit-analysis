import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import praw
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime as dt
import numpy as np


def reddit_search():
    tb.delete('1.0',END)
    

    reddit = praw.Reddit(client_id='DP78tG9HeZiMQg', client_secret='xF80XIHboP51Lq63viNLTzxJrmE', user_agent='RedditWebScraping')

    #getting title from input
    Sub = E1.get()

    tb.insert(INSERT,'\n-------------------------------Hottest of all------------------------------------\n')
    # get hottest posts from all subreddits
    hot_posts = reddit.subreddit('all').hot(limit=10)
    for post in hot_posts:
            tb.insert(INSERT,post.title)
            tb.insert(INSERT,"\n")

    tb.insert(INSERT,'\n------------------------------Subreddit-------------------------------------\n')
    # get 10 hot posts from the given subreddit
    hot_posts = reddit.subreddit(Sub).hot(limit=10)
    for post in hot_posts:
            tb.insert(INSERT,post.title)
            tb.insert(INSERT,"\n")
    
    posts = []
    this_subreddit = reddit.subreddit(Sub)
    for post in this_subreddit.hot(limit=1000):
        posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
    posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
    tb.insert(INSERT,posts)

    def get_date(created):
        return dt.datetime.fromtimestamp(created)

    _timestamp = posts["created"].apply(get_date)
    posts = posts.assign(timestamp = _timestamp)


    tb.insert(INSERT,posts[['title', 'score','timestamp']])
    tb.insert(INSERT,"\n")
    #print(posts[['title', 'score','timestamp']])
    posts['interaction'] = posts['score'].divide(posts['num_comments'],fill_value=1)
    tb.insert(INSERT,posts[['title', 'score','interaction']])
    tb.insert(INSERT,"\n")

    tb.insert(INSERT,'\n--------------------------------Description-----------------------------------\n')

    # get given subreddit data
    given_subreddit = reddit.subreddit(Sub)

    tb.insert(INSERT,given_subreddit.description)
    

    tb.insert(INSERT,'\n--------------------------------Graphs-----------------------------------\n')

    figure1 = plt.Figure(figsize=(6,5), dpi=100)
    ax = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, top)
    bar1.get_tk_widget().grid(row=4,column=1,columnspan=3)
    posts.plot(kind="line",x='title',y='num_comments',color='red',ax=ax)
    posts.plot(kind="line",x='title',y='interaction',color='blue',ax=ax)
    ax.axes.get_xaxis().set_visible(False)
    ax.set_title('Timewise Presence Of Subreddit')


top = tkinter.Tk()
top.wm_title("Reddit Analysis")
top.attributes("-zoomed", True)


L1 = Label(text="User Name")
L1.grid(sticky="nsew",row=1,column=1)

E1 = Entry(bd =5)
E1.grid(row=1,column=2)

#call is made here
B = tkinter.Button(text ="Search", command = reddit_search)
B.grid(row=1,column=3)

tb=Text(top)
tb.grid(row=3,column=1,columnspan=3)

can = Canvas(top,width=400,height=400)
can.grid(row=4,column=1,columnspan=3)

y = int(400 / 2)
can.create_line(0, y, 200, y, fill="#476042")


top.mainloop()
