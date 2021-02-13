from GeneSearcherProcessData import *
import tkinter as tk
from tkinter import Tk, Text, filedialog, BOTH, W, N, E, S, CENTER, NW, Y, LEFT, X, RIGHT, BOTTOM, END
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

def begin_search():
    print("Beginning Search on: " + data_path)

    user_data = load_user_data(data_path)
    #print("USER_DATA: ")
    #for rsid in user_data:
       # print(rsid, " : ", user_data[rsid])

    data_set = load_data_set_from_server()
    #print(data_set)

    #report = process_user_data(user_data, data_set)
    report = dict()
    for rsid in user_data:
        if rsid in data_set:
            user_genotype = user_data[rsid][2]
            # print(rsid, " -", user_genotype)
            if user_genotype not in {"--", "DD", "II"}:
                expression = parser.match_genotype(data_set[rsid], user_genotype)
                if expression not in {"common in clinva",
                                "common in clinvar",
                                "common in complete genomic",
                                "common in complete genomics",
                                "No summary provided",
                                # "norma",
                                # "normal",
                                # "Normal",
                                "commo",
                                "averag",
                                "average",
                                "common/normal",
                                "common on affy axiom dat",
                                "common on affy axiom data",
                                None}:
                    report[rsid] = (user_genotype, expression)
    print("REPORT: ")
    for item in report:
        print(item, " - ", report[item])