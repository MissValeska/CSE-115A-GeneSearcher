import tkinter as tk
from tkinter import Tk, Text, filedialog, BOTH, W, N, E, S, CENTER, NW, Y, LEFT, X, RIGHT, BOTTOM, END
from tkinter.ttk import Frame, Button, Label, Style, LabelFrame
import os

#Establish global storage for data_path for future parsing
data_path = ""

#open file dialog and create label to hold name, as well as store path.
def o_log(frame):
    filepath = filedialog.askopenfilename(initialdir='/', title='Select File', 
            filetypes=(("spreadsheets", "*.csv"), ("all files", "*.*")))
    u_lbl = tk.Label(frame, text=os.path.basename(filepath))
    u_lbl.grid(row=1, column=2)

    global data_path
    data_path = filepath

def parse():
    print("Beginning parse on: " + data_path)

class App(Frame):

    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.master.title("GeneSearcher")
        self.pack(fill=BOTH, expand=True)

        # create all of the main containers
        top_frame = tk.Frame(self, width=450, height=50, padx=3, pady=3)
        center = tk.Frame(self, width=450, height=50, padx=3, pady=3)
        center2 = tk.LabelFrame(self, width=450, height=20, padx=1, pady=3)
        btm_frame = tk.LabelFrame(self, bg='lavender', width=450, height=375, padx=3, pady=3)

        # layout of the main containers
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        center.grid_columnconfigure(0, weight=1)
        center.grid_rowconfigure(1, weight=1)

        center2.grid_columnconfigure(0, weight=1)
        center2.grid_columnconfigure(1, weight=1)
        center2.grid_rowconfigure(1, weight=1)

        btm_frame.grid_rowconfigure(1, weight=1)
        btm_frame.grid_columnconfigure(0, weight=1)

        top_frame.grid(row=0, sticky="ew")
        center.grid(row=1, sticky="ew")
        center2.grid(row=3, sticky="ew")
        btm_frame.grid(row=4, sticky="ew")

        # create the widgets for each frame
        filler_label = tk.Label(top_frame, text='')
        upload_button = tk.Button(top_frame, text='Upload Data', command=lambda : o_log(top_frame))
        search_button = tk.Button(center, text='Begin Search!', command=lambda : parse())
        r_lbl = tk.Label(center2, text="Results:")
        search_bar = tk.Entry(center2, width=40)
        search_bar.insert(END, 'search for keywords...')
        r_disp = tk.Text(btm_frame)
        r_disp.insert(END, "Will display results in table format")

        # layout the widgets in each frame
        filler_label.grid(row=0, columnspan=3)
        upload_button.grid(row=1, column=0)
        search_button.grid(row=1, column=0)
        r_lbl.grid(row=1,column=0)
        search_bar.grid(row=1, column=1)
        #r_disp.pack(fill=BOTH, expand=True)

def main():

    root = Tk()
    root.geometry("500x500")
    app = App()
    root.mainloop()

if __name__ == '__main__':
    main()