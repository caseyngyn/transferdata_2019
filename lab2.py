'''
Casey Nguyen
CIS 41b
front end GUI for transfer.py

EC ANSWER:
The severe budget cuts from CSU's therefore making them unable to accept students.
'''

import matplotlib
matplotlib.use('TkAgg')               # tell matplotlib to work with Tkinter
import tkinter as tk                    # normal import of tkinter for GUI
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Canvas widget
import matplotlib.pyplot as plt         # normal import of pyplot to plot
from transfer import Transfer
import os
from os import path
import tkinter.messagebox as tkmb
import sys

class MainWindow(tk.Tk):
    def __init__(self,*filenames):
        super().__init__()
        try:
            self.var = Transfer(*filenames)

        except IOError:
            self.withdraw()  #removes Master window
            if path.exists(filenames[0]) == False and path.exists(filenames[1]) == False and path.exists(filenames[2] == False):
                tkmb.showerror("Error",f"Can't Open: {filenames}, it was not found")
                sys.exit(0)
            elif path.exists(filenames[0]) == False:
                tkmb.showerror("Error",f"Can't Open: {filenames[0]}, it was not found")
                sys.exit(0)
            elif path.exists(filenames[1])== False:
                tkmb.showerror("Error",f"Can't Open: {filenames[1]}, it was not found")    
                sys.exit(0)
            elif path.exists(filenames[2]) == False:
                tkmb.showerror("Error",f"Can't Open: {filenames[2]}, it was not found")
                sys.exit(0)

        self.title('Transfer Rates')
        self.geometry("500x200")
        self.columnconfigure(0, weight=1)   # Set weight to row and 
        self.rowconfigure(0, weight=0)      # column where the widget is
        self.container = tk.Frame(self)
        
        # weight = 0 means their size is fixed
        # weight = 1 means it takes up as much room as it needs to
        # makes changes to the grid rows/cols
        # weights make that col/row more of a priority when expanding the window
        label = tk.Label(text = 'Community College Transfer Rate to CSU', fg = "blue",font=('Helvetica', 18))
        label.grid(row = 0, column = 0)
     
        self.make_buttons()
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

    def on_exit(self):
        '''
        This function opens a message box asking if the user wants to quit
        Then quits out of the program if the user clicks yes
        '''
        if tkmb.askyesno("Exit", "Do you want to quit the application?"):
            self.quit()

    def make_buttons(self):
        '''
        function makes buttons
        '''
        self.rowconfigure(1, weight=0)      # column where the widget is
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row = 1, column = 0,padx = 10,pady = 10)

        #button 1
        self.total_transfer_button = tk.Button(self.button_frame,text = 'Total Transfer',command = self.plot_total_transfer)
        self.total_transfer_button.grid(row=1, column=0, padx=15, pady=10)

        #button 2
        self.top_ten_button = tk.Button(self.button_frame,text = 'Top Ten',command =self.plot_top_ten )
        self.top_ten_button.grid(row=1, column=1, padx=15, pady=10)

        #button 3
        self.colleges_button = tk.Button(self.button_frame,text = 'Colleges',command = self.display_colleges)
        self.colleges_button.grid(row=1, column=2, padx=15, pady=10 )

    def plot_total_transfer(self):
        '''button 1 logic'''
        PlotWin(self.var.plotTotalTransfer)
    def plot_top_ten(self):
        '''button 2 logic'''
        PlotWin(self.var.show_top_ten)
    def display_colleges(self):
        '''button 3 logic'''
        dwin = DialogWin(self,self.var)
        self.wait_window(dwin)
        choices_idx = dwin.get_choices()
        
        if choices_idx:
            PlotWin(self.var.plotEnrollmentTrend,*choices_idx)

class PlotWin(tk.Toplevel):
    def __init__(self,fct,*args):
        super().__init__()
        self.fig = plt.figure(figsize=(5,5))
        self.focus_set()
        fct(*args)
        canvas = FigureCanvasTkAgg(self.fig, master=self)
        canvas.get_tk_widget().grid()
        canvas.draw()        

class DialogWin(tk.Toplevel):
    def __init__(self,master,data):
        super().__init__(master)
        self.cur = ()
        self.title('Choose Colleges')
        self.focus_set()     # comment this out to see the effect
        self.grab_set()      # comment this out to see the effect
        self.transient(master)    # comment this out to see the effect (on Windows system)
        option_frame = tk.Frame(self)
        S = tk.Scrollbar(option_frame,orient = "vertical")
        self.Lb = tk.Listbox(option_frame,height = 10,width = 50, selectmode = "multiple",yscrollcommand = S.set)
        S.pack(side = "right",fill = "y")
        self.Lb.pack()
        S.config(command = self.Lb.yview)
        college_name = data.college_name
       
        self.Lb.insert(tk.END,*college_name)
        self.Lb.bind("<<ListboxSelect>>",self.poll)

        option_frame.pack()
        tk.Button(self,text = "OK", command = self.destroy).pack()

        self.grab_set()
        self.focus_set()
        self.transient(master)
        self.protocol("WM_DELETE_WINDOW",self.delete)

    def poll(self,*args):
        '''get cursor selection'''
        self.cur = self.Lb.curselection()
        self.destroy()

    def delete(self):
        ''' exits the window'''
        self.cur = ()
        self.selected = None
        self.destroy()

    def get_choices(self):
        ''' returns index of college names to the Main Win'''
        return self.cur

def main():       
    filenames = ['transferCC.csv','transferYear.csv','transferData.csv']       
    app = MainWindow(*filenames)
    app.mainloop()

main()