import tkinter as tk
from tkinter.filedialog import INSERT
import tkinter.ttk as ttk
from tkinter import Tk,Frame,Button,OptionMenu,ttk,Label,Text,filedialog
from tkinter import ttk,StringVar,OptionMenu,Frame,Scrollbar,VERTICAL,Y,X,HORIZONTAL,LEFT,RIGHT,FALSE,BOTTOM,Canvas,BOTH,TRUE,NW
from Configure import getConfig,getLastDialogue,setPath,setConfig


class Config_gui:
    def setCanvas(self,col):
        top_root = tk.Frame(self.word_root,bg='dark sea green')
        top_root.grid(row = 0,column = col, rowspan = 1, columnspan = 1)
        return top_root

    def __init__(self):
        self.attributes = { 'Noun':'n.',
                            'Verb':'v.',
                            'Adverb':'adv.',
                            'Adjective':'adj.'
                            }



        self.root = Tk()
        self.root.title("Configure")
        self.root.style=ttk.Style()
        self.root.style.theme_use("alt")
        self.root.config(background='dark sea green')
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
        self.dic_word_meaning={}
        self.menu()
        self.vs=[]
        for i in range(100):
            self.root.grid_rowconfigure(i,weight=1)
        self.root.grid_columnconfigure(0,weight=1)

        self.words=[]
        self.origin_words="./Removed_known_words.csv"
        self.meaning_file="./full.txt"
        self.readWords()

        columns =6
        numEntry = 30
        self.top_roots=[]
        self.entries_list = []
        self.show_index = 0


        self.word_root = tk.Frame(self.root,background='dark sea green')
        self.word_root.grid(row = 0,column = 0, rowspan = 90, columnspan = 1,sticky="news")
        for i in range(columns):
            self.word_root.grid_columnconfigure(i,weight=1)
        self.word_root.grid_rowconfigure(0,weight=1)
        self.word_root.grid_propagate(0)

        self.fun_root = tk.Frame(self.root,bg='dark sea green')
        self.fun_root.grid(row = 90,column = 0, rowspan = 10, columnspan = 1,sticky="news")
        self.fun_root.grid_columnconfigure(0,weight=1)
        self.fun_root.grid_rowconfigure(0,weight=1)
        self.fun_root.grid_propagate(0)
        self.fun_txt = tk.Text(self.fun_root)
        self.fun_txt.grid(row=0,column=0,sticky='ew')

        for i in range(columns):
            top_root = self.setCanvas(i)
            entries = self.setPage(top_root,numEntry)
            self.top_roots.append(top_root)
            self.entries_list.append(entries)


        self.root.mainloop()


    def menu(self):
        self.menubar = tk.Menu(self.root,bg='dark grey')
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Choose testing images",command = self.changeLabel)
        self.menubar.add_cascade(label=u"\u058D"+" File", menu=self.filemenu)
        self.menubar.add_command(label="Show next Page",command = self.getNextPage)
        self.menubar.add_command(label="Aggregate words",command = self.getNextPage)
        self.root.config(menu=self.menubar)



    def readWords(self):
        max_len = 0
        with open(self.origin_words,'r') as f:
            for line in f:
                word = line.rstrip('\r\n')
                self.words.append(word)
                max_len = max(max_len,len(line.rstrip('\r\n')))
        self.max_len = max_len 
        with open(self.meaning_file,'r') as f:
            for line in f:
                pair = line.rstrip('\r\n')
                word = pair.split('`')[0]
                meaning = pair.split('`')[1]
                meaning = meaning.replace('\'','')
                meaning = meaning.replace('{','')
                meaning = meaning.replace('}','')
                for key,val in self.attributes.items():
                    meaning = meaning.replace(key,'\n'+val)
                self.dic_word_meaning[word]=meaning


    def getNextPage(self):
        for i in self.vs:
            i.set(None)
        for col in self.entries_list:
            for i in col:
                if self.show_index>=len(self.words):
                    self.show_index=0
                i[2].config(text=self.words[self.show_index])
                i[1].grid()
                self.show_index = self.show_index+1


    def setPage(self,top_root,num_entry):
        for i in range(100):
            top_root.grid_rowconfigure(i,weight=1)
        top_root.grid_columnconfigure(0,weight=1)
        top_root.grid_columnconfigure(1,weight=1)
        entries = []
        style = ttk.Style(top_root)
        style.configure('TCheckbutton', bordercolor='dark sea green',borderwidth=0,width=1,background='dark sea green')

        for i in range(num_entry):
            v = tk.IntVar()
            self.vs.append(v)
            label = tk.Label(top_root,text='',bg='dark sea green')
            text = tk.Label(top_root,width=self.max_len+1,text='',justify=tk.LEFT,anchor=tk.W,bg='dark sea green',fg='black')
            button = ttk.Radiobutton(top_root,variable = v,command = lambda arg0=text:self.deleteWord(arg0),style='TCheckbutton')
            #text.insert(tk.END,line.rstrip('\r\n'))
            label.grid(row = 2*i,column = 0, rowspan = 1, columnspan = 2,sticky=tk.W)
            button.grid(row = 2*i+1,column = 0, rowspan = 1, columnspan = 1,sticky=tk.E)
            text.grid(row = 2*i+1,column = 1, rowspan = 1, columnspan = 1,sticky=tk.E)
            entries.append((label,button,text))
            self.dic_radio_words[text]=button
            text.bind("<Enter>",lambda event,arg0=text:self.getMeaning(arg0))
            text.bind("<Leave>",lambda event,arg0=text:self.leaveMeaning(arg0))
            button.grid_remove()
        return entries
        
    def getMeaning(self,text):
        text.config(bg='yellow')
        self.fun_txt.delete('1.0', tk.END)
        txt = text['text']
        #print(self.dic_word_meaning[txt])
        try:
            self.fun_txt.insert(tk.END,txt)
            self.fun_txt.insert(tk.END,self.dic_word_meaning[txt])
        except Exception as e:
            print(e)
    def leaveMeaning(self,text):
        text.config(bg='dark sea green')
        

    def changeLabel(self):
        for col in self.entries_list:
            for i in col:
                i[0].config(text='change the value')

    def deleteWord(self,text):
        txt = text['text']
        self.words.remove(txt)
        text.config(text='')
        button = self.dic_radio_words[text]
        button.grid_remove()



def main():
    cg = Config_gui()



if __name__ == '__main__':
    main()
