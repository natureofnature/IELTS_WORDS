import tkinter as tk
from tkinter.filedialog import INSERT
import tkinter.ttk as ttk
from tkinter import Tk,Frame,Button,OptionMenu,ttk,Label,Text,filedialog
from tkinter import ttk,StringVar,OptionMenu,Frame,Scrollbar,VERTICAL,Y,X,HORIZONTAL,LEFT,RIGHT,FALSE,BOTTOM,Canvas,BOTH,TRUE,NW
from Configure import getConfig,getLastDialogue,setPath,setConfig


class Config_gui:
    def setCanvas(self,col):
        width = int(self.dic['width'])
        height = int(self.dic['height'])
        #canvas = tk.Canvas(self.root,  height=height)
        #canvas.grid(row = 0,column = col, rowspan = 80, columnspan = 1)
        top_root = tk.Frame(self.root)
        top_root.grid(row = 0,column = col, rowspan = 80, columnspan = 1)
        #top_root.grid_propagate(0)
        #canvas.create_window((0,0), window=top_root, anchor='w')
        return top_root


    def __init__(self):
        self.root = Tk()
        self.root.title("Configure")
        self.root.style=ttk.Style()
        self.root.style.theme_use("alt")
        self.dic = getConfig()
        self.max_len = 0
        width = int(self.dic['width'])
        height = int(self.dic['height'])
        self.screen_width = min(self.root.winfo_screenwidth(),width)
        self.screen_height = min(self.root.winfo_screenheight(),height)
        self.root_size = str(self.screen_width)+"x"+str(self.screen_height)
        self.root.geometry(self.root_size)
        self.root.grid_propagate(0)
        self.dic_radio_words={}
        self.menu()
        for i in range(100):
            self.root.grid_rowconfigure(i,weight=1)

        self.words=[]
        self.origin_words="./Removed_known_words.csv"
        self.readWords()

        columns =8
        numEntry = 30
        self.top_roots=[]
        self.entries_list = []
        self.show_index = 0

        for i in range(columns):
            self.root.grid_columnconfigure(i,weight=1)

        for i in range(columns):
            top_root = self.setCanvas(i)
            entries = self.setPage(top_root,numEntry)
            self.top_roots.append(top_root)
            self.entries_list.append(entries)

        self.fun_root = tk.Frame(self.root)
        self.fun_root.grid(row = 80,column = 0, rowspan = 20, columnspan = columns)

        self.root.mainloop()


    def menu(self):
        self.menubar = tk.Menu(self.root,bg='dark grey')
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Choose testing images",command = self.changeLabel)
        self.menubar.add_cascade(label=u"\u058D"+" File", menu=self.filemenu)
        self.menubar.add_command(label="Show next Page",command = self.getNextPage)
        self.root.config(menu=self.menubar)



    def readWords(self):
        max_len = 0
        with open(self.origin_words,'r') as f:
            for line in f:
                word = line.rstrip('\r\n')
                self.words.append(word)
                max_len = max(max_len,len(line.rstrip('\r\n')))
        self.max_len = max_len 

    def getNextPage(self):
        for col in self.entries_list:
            for i in col:
                if self.show_index>=len(self.words):
                    self.show_index=0
                i[2].config(text=self.words[self.show_index])
                self.show_index = self.show_index+1


    def setPage(self,top_root,num_entry):
        for i in range(100):
            top_root.grid_rowconfigure(i,weight=1)
        top_root.grid_columnconfigure(0,weight=1)
        top_root.grid_columnconfigure(1,weight=1)
        entries = []
        for i in range(num_entry):
            v = tk.IntVar()
            label = tk.Label(top_root,text='')
            button = ttk.Radiobutton(top_root,variable = v)
            text = tk.Label(top_root,width=self.max_len+1,text='',justify=tk.LEFT,anchor=tk.W)
            #text.insert(tk.END,line.rstrip('\r\n'))
            label.grid(row = 2*i,column = 0, rowspan = 1, columnspan = 2,sticky=tk.W)
            button.grid(row = 2*i+1,column = 0, rowspan = 1, columnspan = 1,sticky=tk.E)
            text.grid(row = 2*i+1,column = 1, rowspan = 1, columnspan = 1,sticky=tk.E)
            entries.append((label,button,text))
            self.dic_radio_words[button]=text
        return entries
        
    def changeLabel(self):
        for col in self.entries_list:
            for i in col:
                i[0].config(text='change the value')



def main():
    cg = Config_gui()



if __name__ == '__main__':
    main()
