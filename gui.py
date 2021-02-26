from app_utils import *
import tkinter as tk
from tkinter import Tk, Text, filedialog, BOTH, W, N, E, S, CENTER, NW, Y, LEFT, X, RIGHT, BOTTOM, END
from tkinter.ttk import Frame, Button, Label, Style, LabelFrame
import os

#Establish global storage for data_path for future parsing
data_path = ""

class App(Frame):
    def __init__(self, root, vc):
        super().__init__()
        self.vc = vc
        self.root = root
        self.root.geometry("400x500")
        self.initUI()
    
    def initUI(self):
        self.master.title("GeneSearcher")
        self.pack(fill=BOTH, expand=True)

        # init search variable for search bar
        #Search = tk.StringVar()

        # init background
        background_image = tk.PhotoImage(file='./GUI/Assets/background3.png')
        background_label = tk.Label(self, image=background_image)
        background_label.place(relwidth=1, relheight=1)
        background_label.image = background_image

        # create all of the main containers
        top_frame = tk.Frame(self, bg='#a8327f', bd=5)
        center = tk.Frame(self, bg='#a8327f', bd=5)
        btm_frame = tk.Frame(self, bg='#a8327f', bd=5)
        
        # place all of the main containers
        top_frame.place(relx=0.5, rely=0.1, relwidth=.75,relheight=0.1, anchor='n')
        center.place(relx=0.5, rely=0.25, relwidth=0.6, relheight=0.1, anchor='n')
        btm_frame.place(relx=0.5, rely=0.4, relwidth=0.98, relheight= 0.593, anchor='n')

        # create the widgets for each frame
        r_display = tk.Text(btm_frame)
        upload_button = tk.Button(top_frame, text='Upload Data', fg='black', command=lambda : self.o_log(top_frame))
        search_button = tk.Button(center, text='Begin Search!', fg='black', command=lambda : self.vc.generate_report(r_display))
        find_button = tk.Button(btm_frame, text="Search Results", fg='black', command=lambda : self.find(search_bar, r_display))
        r_lbl = tk.Label(btm_frame, text="Results:", bg='#a8327f', font=5)
        
        # quick break to create a trace for search bar
        #Search.trace("w", lambda name, index, mode, Search=Search: search_loop(Search, r_display))
        search_bar = tk.Entry(btm_frame)

        # layout the widgets in each frame
        upload_button.place(relheight=1, relwidth=0.3)
        search_button.place(relheight=1, relwidth=1)
        r_lbl.place(relwidth=0.2,relheight=0.1)
        search_bar.place(relx=0.5, relwidth=0.5,relheight=0.1)
        find_button.place(relx=0.4, relwidth=0.2, relheight=0.105)
        r_display.place(rely=0.15, relwidth=1, relheight=0.85)

        # add properties of widgets
        r_display.tag_configure("search", background="green")

    def o_log(self, frame):
        '''
        Browsing files function. Opens the dialog to find file to upload via
        button press. Also creates the label to hold the file name, and stores
        the filepath in global data_path storage.
        PARAMS : Frame to bind label to.
        '''

        filepath = filedialog.askopenfilename(initialdir='/', title='Select File')
        u_lbl = tk.Label(frame, text=os.path.basename(filepath), bg='#a8327f')
        u_lbl.place(relx=0.35, relwidth=0.3, relheight=1)
        self.vc.input_data_file(filepath)

    def display_report(self, text_frame, report):
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

    def find(self, entry, display):
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