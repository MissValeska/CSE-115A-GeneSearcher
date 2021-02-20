from app_utils import *
import tkinter as tk
from tkinter import Tk, Text, filedialog, BOTH, W, N, E, S, CENTER, NW, Y, LEFT, X, RIGHT, BOTTOM, END
from tkinter.ttk import Frame, Button, Label, Style, LabelFrame
import os

#Establish global storage for data_path for future parsing
data_path = ""
disp_report = {}

class App(Frame):

    def __init__(self):
        super().__init__()
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
        upload_button = tk.Button(top_frame, text='Upload Data', fg='black', command=lambda : o_log(top_frame))
        search_button = tk.Button(center, text='Begin Search!', fg='black', command=lambda : begin_search(r_display))
        find_button = tk.Button(btm_frame, text="Search Results", fg='black', command=lambda : find(search_bar, r_display))
        r_lbl = tk.Label(btm_frame, text="Results:", bg='#a8327f', font=5)
        r_display = tk.Text(btm_frame)
        
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

def main():

    root = Tk()
    root.geometry("400x500")
    app = App()
    root.mainloop()

if __name__ == '__main__':
    main()