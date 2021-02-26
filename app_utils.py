from GeneSearcherProcessData import *
import tkinter as tk
from tkinter import Tk, Text, filedialog, BOTH, W, N, E, S, CENTER, NW, Y, LEFT, X, RIGHT, BOTTOM, END, DISABLED, NORMAL
from tkinter.ttk import Frame, Button, Label, Style, LabelFrame
import os

#global storage for search word + amount of clicks
word_storage = ""
click_storage = 0

def o_log(frame):

    '''
    Browsing files function. Opens the dialog to find file to upload via
    button press. Also creates the label to hold the file name, and stores
    the filepath in global data_path storage.
    PARAMS : Frame to bind label to.
    '''

    filepath = filedialog.askopenfilename(initialdir='/', title='Select File', 
            filetypes=(("spreadsheets", "*.csv"), ("all files", "*.*")))
    u_lbl = tk.Label(frame, text=os.path.basename(filepath), bg='#a8327f')
    u_lbl.place(relx=0.35, relwidth=0.3, relheight=1)

    global data_path
    data_path = filepath

def begin_search(text_frame):

    '''
    Primary backend linkage. Utilize functions from GeneSearcherProcessData.py
    to load in user data from file and data from server to compare to. Generates
    the report and sends it to display function. Bound to search_button in gui.py
    PARAMS : text frame to display report in.
    '''

    print("Beginning Search on: " + data_path)

    user_data = load_user_data(data_path)

    data_set = load_data_set_from_server()

    report = process_user_data(user_data, data_set)
    
    display_report(text_frame, report)

def display_report(text_frame, report):

    '''
    Clears current text in display and replaces with current report text.
    Format is newlines and a separating hyphen line. Also deactivates text
    editing in box. Called from begin_search() function.
    PARAMS : text box to display in and report to display.
    '''

     # ----- implement display for report -----#
    text_frame.delete(1.0, END)
    line = "-----------------------------------------------\n"

    for item in report:
        genotype = report[item][0]
        expression = report[item][1]
        weight = str(report[item][2])
        # disp_str = item + " - " + genotype + ", " + expression + ", Weight: " + weight + "\n"
        # text_frame.insert("1.0", disp_str)
        text_frame.insert("1.0", expression + "\n")
        text_frame.insert("1.0", "Genotype: %s - Weight of Evidence: %s\n" % (genotype, weight))
        text_frame.insert("1.0", "RSID: %s\n" % item)
        text_frame.insert("1.0", line)

    text_frame.config(state=DISABLED)

#def search_loop(tto_find, tto_search):
  #  countVar = tk.StringVar()
  #  pos = tto_search.search(tto_find, "1.0", stopindex="end", count=countVar)
  #  tto_search.tag_add("search", pos, "%s + %sc" (pos, countVar.get()))
  #  print(tto_find.get())

def find(entry, display):

    '''
    Function bound to search bar functionality, specifically find_button
    in gui.py. Stores word to be searched for and times the search has been
    clicked globally, as well as init a list storing indices of highlighted
    words. Word storage is used to check if a new word is entered so clicks
    can be reset, and clicks will allow us to snap to specific stored indices
    in the text display.
    PARAMS : Entry text box and the text box displaying the report.
    '''

    idx_list = []
    global word_storage
    global click_storage

    display.tag_remove("search", '1.0', END)
    e = entry.get()

    if e != word_storage:
        click_storage = 0
        word_storage = e

    if e:
        idx = '1.0'
        while 1:
            idx = display.search(e, idx, nocase=1, stopindex=END)

            if not idx: break

            lastidx = '%s+%dc' % (idx, len(e))
            idx_list.append(idx)

            display.tag_add("search", idx, lastidx)

            idx = lastidx

        if click_storage > len(idx_list) - 1:
            click_storage = 0
        if len(idx_list) != 0: display.see(idx_list[click_storage])
        click_storage = click_storage + 1
