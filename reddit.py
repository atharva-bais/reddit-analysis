import tkinter
from tkinter import *
from wordcloud import WordCloud, STOPWORDS
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import ttk
import praw
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime as dt
import numpy as np
import seaborn as sns
import nltk
from nltk.corpus import stopwords

def reddit_search():
    tb.delete('1.0',END)
    flag=0
    test=''

    reddit = praw.Reddit(client_id='DP78tG9HeZiMQg', client_secret='xF80XIHboP51Lq63viNLTzxJrmE', user_agent='RedditWebScraping')

    #getting title from input
    Sub = E1.get()

    tb.insert(INSERT,'\n-------------------------------Hottest of all------------------------------------\n')
    # get hottest posts from all subreddits
    hot_posts = reddit.subreddit('all').hot(limit=10)
    try:        
        for post in hot_posts:
            tb.insert(INSERT,post.title)
            tb.insert(INSERT,"\n")
    except TclError:
        pass

    tb.insert(INSERT,'\n------------------------------Subreddit-------------------------------------\n')
    # get 10 hot posts from the given subreddit
    hot_posts = reddit.subreddit(Sub).hot(limit=10)
    try:
        for post in hot_posts:
            tb.insert(INSERT,post.title)
            tb.insert(INSERT,"\n")
    except TclError:
        pass	
    posts = []
    this_subreddit = reddit.subreddit(Sub)
    for post in this_subreddit.hot(limit=1000):
        posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
	
    posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])

    def get_date(created):
        return dt.datetime.fromtimestamp(created)

    
    
    try:
        tb.insert(INSERT,posts)
        _timestamp = posts["created"].apply(get_date)
        posts = posts.assign(timestamp = _timestamp)
        tb.insert(INSERT,posts[['title', 'score','timestamp']])
        tb.insert(INSERT,"\n")
        #print(posts[['title', 'score','timestamp']])
        posts['interaction'] = posts['score'].divide(posts['num_comments'],fill_value=1)
        tb.insert(INSERT,posts[['title', 'score','interaction']])
        tb.insert(INSERT,"\n")
    except TclError:
        pass



    # Text numerical analysis
    prostr = ""
    for post in this_subreddit.hot(limit=1000):
            prostr += post.title
    
    data_dict = {}
    data_set_split = prostr.split()
    
    for i in data_set_split:
        data_dict.setdefault(i,0)
        data_dict[i] += 1
    rejected_words = ['a','and','I','The','can','your','get','who','Who','what','What','their','after','would','his','they','has','me','Has','A','An','i','by','at','as','do','we','-','|','all','if','from','be','are','that','was','not','so','have','about','this','my','it','with','but','you','new','the','an','of','or','is','to','for','will','over','under','above','in','on',Sub]
    for i in rejected_words:
        if i in data_dict:
            del data_dict[i]
    title_items = list(data_dict.items())
    title_items.sort(key=lambda word:word[1],reverse=True)
    print(title_items)
    finalstr="\n---------------Most Important Topics---------------------- \n"
    for i in range(10):
        finalstr+=str(title_items[i])+"\n"
        #print(title_items[i])

    tb.insert(INSERT,finalstr)



    
    tb.insert(INSERT,'\n--------------------------------Description-----------------------------------\n')

    # get given subreddit data
    given_subreddit = reddit.subreddit(Sub)

    tb.insert(INSERT,given_subreddit.description)
    

    tb.insert(INSERT,'\n--------------------------------Graphs-----------------------------------\n')

    figure1 = plt.Figure(figsize=(6,5), dpi=100)
    ax = figure1.add_subplot(111)
    line1 = FigureCanvasTkAgg(figure1, top)
    line1.get_tk_widget().grid(row=3,column=1,columnspan=3)
    posts.plot(kind="line",x='title',y='num_comments',color='red',ax=ax)
    posts.plot(kind="line",x='title',y='interaction',color='blue',ax=ax)
    ax.axes.get_xaxis().set_visible(False)
    ax.set_title('Timewise Presence Of Subreddit \''+Sub+'\'')


    figure3 = plt.Figure(figsize=(6,5), dpi=100)
    ax3 = figure3.add_subplot(111)
    ax3.scatter(posts['score'],posts['num_comments'], color = 'b')
    scatter3 = FigureCanvasTkAgg(figure3, top) 
    scatter3.get_tk_widget().grid(row=2,column=4,columnspan=1)
    ax3.legend() 
    ax3.set_xlabel('Score')
    ax3.set_ylabel('num_comments')
    ax3.set_title('Behaviour Of Subreddit \''+Sub+'\'')

    df1 = posts[['title', 'score']].groupby('title').sum()
    figure1 = plt.Figure(figsize=(6,5), dpi=100)
    ax1 = figure1.add_subplot(111)
    ax1.axes.get_xaxis().set_visible(False)
    bar1 = FigureCanvasTkAgg(figure1, top)
    bar1.get_tk_widget().grid(row=3,column=4,columnspan=1)
    df1.plot(kind='bar', legend=True, ax=ax1)
    ax1.set_title('Activity Of Subreddit \''+Sub+'\'')

    df2 = posts[['title', 'num_comments']].groupby('title').sum()
    figure1 = plt.Figure(figsize=(6,5), dpi=100)
    ax1 = figure1.add_subplot(111)
    ax1.axes.get_xaxis().set_visible(False)
    bar1 = FigureCanvasTkAgg(figure1, top)
    bar1.get_tk_widget().grid(row=3,column=5,columnspan=1)
    df2.plot(kind='bar', legend=True, ax=ax1)
    ax1.set_title('Activity Of Subreddit \''+Sub+'\' plot 2')

    
    dataset = str(posts.title.values)
    #for post in posts:
     #   dataset=dataset+post.title.str()
    #print(dataset)
    
    

    def create_word_cloud(string):
        maskArray = np.array(Image.open("cloud.png"))
        cloud = WordCloud(background_color = "white", max_words = 200, mask = maskArray, stopwords = set(STOPWORDS))
        cloud.generate(string)
        cloud.to_file("wordCloud.png")
    dataset = dataset.lower()
    create_word_cloud(dataset)

    image = Image.open("wordCloud.png")
    image=image.resize((450,400),Image.BICUBIC)
    photo = ImageTk.PhotoImage(image)

    label = Label(image=photo)
    label.image = photo 
    label.grid(row=2,column=5,columnspan=1)
    '''data_dict = {}
    data_set_split = dataset.split()
    for i in data_set_split:
        data_dict.setdefault(i,0)
        data_dict[i] += 1
    title_items = list(data_dict.items())
    title_items.sort(key=lambda word:word[1],reverse=True)
    print(title_items)'''

top = tkinter.Tk()
top.tk.call('encoding', 'system', 'utf-8')
top.wm_title("Reddit Analysis")
top.attributes("-zoomed", True)


L1 = Label(text="Subreddit Name")
L1.grid(sticky="nsew",row=1,column=1)

E1 = Entry(bd =5)
E1.grid(row=1,column=2)

#call is made here
B = tkinter.Button(text ="Search", command = reddit_search)
B.grid(row=1,column=3)

tb=Text(top)
tb.grid(row=2,column=1,columnspan=3)

top.mainloop()
