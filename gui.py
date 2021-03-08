# from app_utils import *
import tkinter as tk
from tkinter import Tk, Text, filedialog, BOTH, CENTER, N, NW, Y, LEFT, X, END, DISABLED, Toplevel
from tkinter.ttk import Frame, Button, Label
import os

class App(Frame):
    def __init__(self, root, vc):
        super().__init__()
        self.vc = vc
        self.root = root
        self.root.geometry("400x500")
        self.initUI()

        self.word_storage = ""
        self.click_storage = 0
    
    def initUI(self):
        self.master.title("GeneSearcher")
        self.pack(fill=BOTH, expand=True)

        # init background
        background_image = tk.PhotoImage(file='./GUI/Assets/background3.png')
        background_label = tk.Label(self, image=background_image)
        background_label.place(relx=.5, rely=.5, anchor='center')
        background_label.image = background_image

        # create all of the main containers
        self.report_frame = ReportFrame(self.master, self.vc.export_report)
        self.input_frame = InputFrame(self.master, self.o_log)
        self.run_frame = RunFrame(self.master, self.vc.generate_report)

        # place all of the main containers
        self.input_frame.place(relx=0.5, rely=0.1, relwidth=.9, anchor='n')
        self.run_frame.place(relx=0.5, rely=0.17, relwidth=0.9, anchor='n')
        self.report_frame.place(relx=0.5, rely=0.4, relwidth=0.98, relheight= 0.593, anchor='n')

    def o_log(self, frame):
        '''
        Browsing files function. Opens the dialog to find file to upload via
        button press. Also creates the label to hold the file name, and stores
        the filepath in global data_path storage.
        PARAMS : Frame to bind label to.
        '''

        filepath = filedialog.askopenfilename(initialdir='/', title='Select File')
        u_lbl = tk.Label(frame, text=os.path.basename(filepath), bg='#a8327f')
        # u_lbl.place(relx=1, rely=.5, relwidth=0.7, relheight=1, anchor='e')
        u_lbl.pack(side=LEFT)
        self.vc.input_data_file(filepath)

    def display_report(self, report):
        self.report_frame.update_report(report)


class InputFrame(tk.Frame):
    def __init__(self, master=None, fn=None):
        super().__init__(master=master, bg='#a8327f', bd=5)
        self.upload_button = tk.Button(self, text='Upload Data', fg='black', command=lambda : fn(self))
        # upload_button.place(relheight=1, relwidth=0.3)
        self.upload_button.pack(side=LEFT)
        self.upload_button.config(highlightthickness=0)
        self.upload_button.config(highlightbackground='#a8327f')

class RunFrame(tk.Frame):
    def __init__(self, master=None, fn=None):
        super().__init__(master=master, bg='#a8327f', bd=5)
        self.search_button = tk.Button(self, text='Begin Search!', fg='black', command=lambda : fn())
        # self.search_button.place(relheight=1, relwidth=1)
        self.search_button.pack(fill=X, expand=True)
        self.search_button.config(highlightthickness=0)
        self.search_button.config(highlightbackground='#a8327f')

class ReportFrame(tk.Frame):
    def __init__(self, master=None, export_fn = None):
        super().__init__(master=master, bg='#a8327f', bd=5)
        
        self.click_storage = 0
        self.word_storage = ""
        
        # create the widgets for each report frame
        top_bar = tk.Frame(self, bg='#a8327f')
        self.search_bar = tk.Entry(top_bar)
        self.search_bar.config(highlightthickness=0)
        self.search_bar.config(highlightbackground='#a8327f')
        self.search_bar.bind("<Return>", lambda value : self.find(self.search_bar, self.r_display))

        self.find_button = tk.Button(top_bar, text="Find", fg='black', command=lambda : self.find(self.search_bar, self.r_display))
        self.find_button.config(highlightthickness=0)
        self.find_button.config(highlightbackground='#a8327f')

        self.export_button = tk.Button(top_bar, text="Export", fg='black', command= lambda : export_fn())
        self.export_button.config(highlightthickness=0)
        self.export_button.config(highlightbackground='#a8327f')
        
        self.r_lbl = tk.Label(top_bar, text="Results:", bg='#a8327f', font=5)

        self.r_lbl.pack(side=LEFT)
        self.export_button.pack(side=LEFT)
        self.find_button.pack(side=LEFT)
        self.search_bar.pack(side=LEFT, fill=X, expand=True)

        top_bar.place(anchor='nw', relwidth=1, relheight=.15)

        self.r_display = tk.Text(self)
        self.r_display.place(rely=0.15, relwidth=1, relheight=0.85)
        # add properties of widgets
        self.r_display.tag_configure("search", background="yellow")
        
        # quick break to create a trace for search bar
        # Search.trace("w", lambda name, index, mode, Search=Search: search_loop(Search, r_display))
        

    def update_report(self, report):
        '''
        Clears current text in display and replaces with current report text.
        Format is newlines and a separating hyphen line. Also deactivates text
        editing in box. Called from begin_search() function.
        PARAMS : text box to display in and report to display.
        '''
        text_frame = self.r_display
        
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
        # global word_storage
        # global click_storage

        display.tag_remove("search", '1.0', END)
        e = entry.get()

        if e != self.word_storage:
            self.click_storage = 0
            self.word_storage = e

        if e:
            idx = '1.0'
            while 1:
                idx = display.search(e, idx, nocase=1, stopindex=END)

                if not idx: break

                lastidx = '%s+%dc' % (idx, len(e))
                idx_list.append(idx)

                display.tag_add("search", idx, lastidx)

                idx = lastidx

            if self.click_storage > len(idx_list) - 1:
                self.click_storage = 0
            if len(idx_list) != 0: display.see(idx_list[self.click_storage])
            self.click_storage = self.click_storage + 1


class TextWindow(Toplevel):

    def __init__(self, title="title", master=None):

        super().__init__(master=master)
        self.title(title)
        self.geometry("400x500")
        label = Label(self, text="This is a new window")
        label.pack()
