from GeneSearcherProcessData import *
import tkinter as tk
from tkinter import Tk, Text, filedialog, BOTH, W, N, E, S, CENTER, NW, Y, LEFT, X, RIGHT, BOTTOM, END, DISABLED, NORMAL
from tkinter.ttk import Frame, Button, Label, Style, LabelFrame
import os

#open file dialog and create label to hold name, as well as store path.
def o_log(frame):
    filepath = filedialog.askopenfilename(initialdir='/', title='Select File', 
            filetypes=(("spreadsheets", "*.csv"), ("all files", "*.*")))
    u_lbl = tk.Label(frame, text=os.path.basename(filepath), bg='#a8327f')
    u_lbl.place(relx=0.35, relwidth=0.3, relheight=1)

    global data_path
    data_path = filepath

def begin_search(text_frame):
    print("Beginning Search on: " + data_path)

    user_data = load_user_data(data_path)

    data_set = load_data_set_from_server()

    report = process_user_data(user_data, data_set)
    
    display_report(text_frame, report)

def display_report(text_frame, report):
     # ----- implement display for report -----#
    text_frame.delete(1.0, END)
    line = "-----------------------------------------------"

    for item in report:
        disp_str = item + " - " + report[item][0] + ", " + report[item][1] + "\n"
        text_frame.insert("1.0", disp_str)
        text_frame.insert("1.0", line)

    text_frame.config(state=DISABLED)

#def search_loop(tto_find, tto_search):
  #  countVar = tk.StringVar()
  #  pos = tto_search.search(tto_find, "1.0", stopindex="end", count=countVar)
  #  tto_search.tag_add("search", pos, "%s + %sc" (pos, countVar.get()))
  #  print(tto_find.get())

def find(entry, display):
    
    display.tag_remove("search", '1.0', END)
    e = entry.get()

    if e:
        idx = '1.0'
        while 1:
            idx = display.search(e, idx, nocase=1, stopindex=END)

            if not idx: break

            lastidx = '%s+%dc' % (idx, len(e))

            display.tag_add("search", idx, lastidx)
            idx = lastidx