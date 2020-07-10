# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 18:06:37 2018

@author: Stéphane
"""

from tkinter import Tk, StringVar, Label, Entry, Button, Listbox, Variable, Frame, DoubleVar
from function_abs import update_listbox, del_selection, update_selection, gotof2, gotof3, gotof4, sendorder, callauto
from functools import partial

_key = ''
_sign = ''
cpair = ["BTC_LSK"]
lvl = [0.789, 0.618, 0.5, 0.382, 0.236]
root = Tk()  #  Création de la fenêtre racine
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.title('ABSGUI') # Ajout d'un titre
root.geometry(str(width) + "x"+ str(height))
root.resizable(True, True) # autoriser le redimensionnement vertical.

f1 = Frame(root, bd=1, relief='solid')
f1.grid(row=0, column=0)

f2 = Frame(root, bd=1, relief='solid')

f3 = Frame(root, bd=1, relief='solid')
f4 = Frame(root, bd=1, relief='solid')

b1 = Frame(root, bd=1, relief='solid')
b1.grid(row=1, column=0)
b2 = Frame(root, bd=1, relief='solid')
b2.grid(row=1, column=1)
fsign = Frame(root, bd=1, relief='solid')
fsign = Frame(root, bd=1, relief='solid')
fsign.grid(row=0, column=5)
f2.grid_remove()
f3.grid_remove()
# f1
text1 = StringVar(f1)
text2 = StringVar(f2)
text31 = DoubleVar(f3)

textsign = StringVar(fsign)
textsign.set(_sign)
textkey = StringVar(fsign)
textkey.set(_key)

label1 = Label(f1, text='Crypto Selection')
label2 = Label(f2, text='Max from selection')
label3 = Label(f3, text='Trigger creation')
label4 = Label(f4, text ='')
label41 = Label(f4, text ='')
label42 = Label(f4, text ='Amount')
label43 = Label(f4, text ='Rate')
label44 = Label(f4, text = '')
labelb2 = Label(b2, text='Max Updated')
labelb1 = Label(b1, text='Crypto Selection')
labelsign = Label(fsign, text='Sign')
labelkey = Label(fsign, text='Key')

entry_name1 = Entry(f1, textvariable=text1)
entry_name2 = Entry(f2, textvariable=text2)
entry_name3 = Entry(f3, textvariable=text31)

entrysign = Entry(fsign, textvariable=textsign)
entrykey = Entry(fsign, textvariable=textkey)

choices1 = Variable(f1, (cpair))
choices3 = Variable(f3, (lvl))

listbox1 = Listbox(f1, listvariable=choices1, selectmode="single")
listbox2 = Listbox(f2, selectmode="single")
listbox3 = Listbox(f3, selectmode="single", listvariable=choices3)
listbox41 = Listbox(f4, selectmode="single")
listbox42 = Listbox(f4, selectmode="single")
listboxb1 = Listbox(b1, selectmode="single")
listboxb2 = Listbox(b2, selectmode="single")

# button
b_add1 = Button(f1, text='Add >> ', command=partial(update_listbox, listbox1, text1))
b_ok1 = Button(f1, text='Ok', command=partial(gotof2, listbox1, listbox2, listboxb1,listboxb2, f2))
b_del1 = Button(f1, text='Del', command=partial(del_selection, listbox1))

b_modify = Button(f2, text='Change', command=partial(update_selection, listbox2, text2))
b_ok2 = Button(f2, text='Ok', command=partial(gotof3, listbox1, f3))
b_ok3 = Button(f3, text='Ok', command=partial(gotof4, listbox1, listbox2, listbox3, listbox41, listbox42, label4, label41, label44, textsign, textkey, f4))

b_del3 = Button(f3, text='Del', command=partial(del_selection, listbox3))
b_add3 = Button(f3, text='Add >> ', command=partial(update_listbox, listbox3, text31))

b_buyorder = Button(f4, text='Put Buy Order', command=partial(sendorder,"buy", textsign, textkey, label44, listbox41, listbox42))
h = callauto(listboxb1, listboxb2, listbox3, textsign, textkey)
b_auto = Button(b2, text='Mode Auto', command=h.start)
b_stop = Button(b2, text='Stop Auto', command=h.stop)

#f1
label1.grid(column=1, row=0)
entry_name1.grid(column=1, row=1)
b_add1.grid(column=1, row=2)
b_ok1.grid(column=1, row=3)
listbox1.grid(column=2, row=2)
b_del1.grid(column=2, row=3)

#f2
label2.grid(column=1, row=0)
entry_name2.grid(column=1, row=1)
b_modify.grid(column=2, row=3)
listbox2.grid(column=2, row=2)
b_ok2.grid(column=1, row=3)

#f3
label3.grid(column=1, row=0)
listbox3.grid(column=2, row=2)
b_del3.grid(column=2, row=3)
entry_name3.grid(column=1,row=1)
b_add3.grid(column=1, row=2)
b_ok3.grid(column=1, row=3)

#f4
label4.grid(column=1, row=0)
label41.grid(column=1, row=1)
label42.grid(column=1, row=2)
label43.grid(column=2, row=2)
label44.grid(column=2, row=0)
b_buyorder.grid(column=2, row=1)
listbox41.grid(column=1, row=3)
listbox42.grid(column=2, row=3)

#b1
labelb1.grid(column=1, row=0)
listboxb1.grid(column=1, row=1)

#b2
labelb2.grid(column=1, row=0)
listboxb2.grid(column=1, row=1)
b_auto.grid(column=2, row=1)
b_stop.grid(column=2, row=2)
#fsign
labelsign.grid(column=1, row=1)
entrysign.grid(column=1, row=2)
labelkey.grid(column=1, row=3)
entrykey.grid(column=1, row=4)

root.mainloop() # Lancement de la boucle principale

