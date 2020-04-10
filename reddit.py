import tkinter
from tkinter import *
from tkinter import messagebox


def reddit_search():
   tb.delete('1.0',END)
   tb.insert(INSERT,E1.get())

top = tkinter.Tk()
top.attributes("-zoomed", True)


L1 = Label(text="User Name")
L1.grid(sticky="nsew",row=1,column=1)

E1 = Entry(bd =5)
E1.grid(row=1,column=2)

B = tkinter.Button(text ="Search", command = reddit_search)
B.grid(row=2,column=1,columnspan=2)

tb=Text(top)
tb.grid(row=3,column=2,columnspan=2)



top.mainloop()
