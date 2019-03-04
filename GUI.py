import tkinter as tk
import webbrowser
from selenium import webdriver
import os
from tkinter import filedialog
from tkinter.filedialog import INSERT
import tkinter.ttk as ttk
from tkinter import Tk,Frame,Button,OptionMenu,ttk,Label,Text,filedialog
from tkinter import ttk,StringVar,OptionMenu,Frame,Scrollbar,VERTICAL,Y,X,HORIZONTAL,LEFT,RIGHT,FALSE,BOTTOM,Canvas,BOTH,TRUE,NW
from Configure import getConfig,getLastDialogue,setPath,setConfig
import datetime
len_ielts=3611
PATH_TO_DRIVER ='./chromedriver'



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
        self.backend = self.dic['backend']
        self.screen_width = min(self.root.winfo_screenwidth(),width)
        self.screen_height = min(self.root.winfo_screenheight(),height)
        self.root_size = str(self.screen_width)+"x"+str(self.screen_height)
        self.root.geometry(self.root_size)
        self.root.grid_propagate(0)
        self.dic_radio_words={}
        self.dic_word_meaning={}
        self.vs=[]
        for i in range(100):
            self.root.grid_rowconfigure(i,weight=1)
        self.root.grid_columnconfigure(0,weight=1)

        self.words=[]
        self.dir_words='./words'
        self.origin_words=os.path.join(self.dir_words,"./Ielts.csv")
        self.dictionary_file=os.path.join(self.dir_words,"./Ielts.dic")
        self.readWords()
        self.readDict()
        self.url_longman='https://www.ldoceonline.com/dictionary/'
        self.url_oxford='https://dictionary.cambridge.org/zhs/词典/英语-汉语-简体/'
        self.urls = [('Longman',self.url_longman),('Oxford',self.url_oxford)]
        self.url_index = 0
        self.url = self.urls[self.url_index]
        self.menu()

        columns =6
        numEntry = 20
        self.top_roots=[]
        self.entries_list = [] #col|col|...
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

        if self.backend== 'selenium':
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--disable-infobars")
            self.browser = webdriver.Chrome(PATH_TO_DRIVER,chrome_options = chrome_options)
            self.browser.set_window_position(0,0)


        self.root.mainloop()


    def menu(self):
        self.menubar = tk.Menu(self.root,bg='dark grey')
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Choose word file",command = self.chooseWordFile)
        self.menubar.add_cascade(label=u"\u058D"+" File", menu=self.filemenu)
        self.menubar.add_command(label=u"\u25B6"+" Show next Page",command = self.getNextPage)
        self.menubar.add_command(label=u"\u047A"+" Aggregate words",command = self.aggregate)
        self.menubar.add_command(label=u"\u0CF1"+" Save Word List",command = self.SaveWordList)
        self.url=self.urls[self.url_index]
        dic_name = self.url[0]
        self.menubar.add_command(label=u"\u07F7"+" Switch dic (Current using "+dic_name+")",command = lambda:self.switchDic(self.menubar))
        self.root.config(menu=self.menubar)
    def switchDic(self,menubar):
        self.url_index = (self.url_index + 1)%(len(self.urls))
        self.url=self.urls[self.url_index]
        dic_name = self.url[0]
        menubar.entryconfigure(5, label=u"\u07F7"+" Switch dic (Current using "+dic_name+")")

        

    def SaveWordList(self):
        global len_ielts
        now = datetime.datetime.now()
        filename = now.strftime("%Y-%m-%d-%H-%M-")
        filename = str(filename)+str(len_ielts-len(self.words))+'.txt'
        filename = os.path.join(self.dir_words,filename)
        with open(filename,'w') as f:
          for line in self.words:
            f.write(line+'\n')
        


    def readWords(self):
        del(self.words[:])
        max_len = 0
        with open(self.origin_words,'r') as f:
            for line in f:
                word = line.rstrip('\r\n')
                self.words.append(word)
                max_len = max(max_len,len(line.rstrip('\r\n')))
        self.max_len = max_len 
        self.show_index=0
    def readDict(self):
        with open(self.dictionary_file,'r') as f:
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
            button.bind("<Enter>",lambda event,arg0=text:self.getMeaning(arg0))
            button.bind("<Leave>",lambda event,arg0=text:self.leaveMeaning(arg0))
            text.bind("<Enter>",lambda event,arg0=text:self.getMeaning(arg0))
            text.bind("<Leave>",lambda event,arg0=text:self.leaveMeaning(arg0))
            text.bind("<Button-1>", lambda event,arg0=text:self.clickWords(arg0))
            button.grid_remove()
        return entries

    def clickWords(self,text):
      txt = text['text']
      if len(txt) == 0:
        return
      self.root.clipboard_clear()
      self.root.clipboard_append(txt)
      url = self.url[1]+txt
      if self.backend== 'selenium':
        global PATH_TO_DRIVER
        self.browser.get(url)
      elif self.backend == 'webbrowser':
        webbrowser.open(url)





    def aggregate(self):
        words_on_page=[]
        for entries in self.entries_list:
            for pair in entries:
                text = pair[2]
                if len(text['text'])>0:
                    words_on_page.append(text['text'])
                text.config(text='')

        index = 0
        for i in self.vs:
            i.set(None)
        for entries in self.entries_list:
            for pair in entries:
                text = pair[2]
                button = self.dic_radio_words[text]
                if index >= len(words_on_page):
                    button.grid_remove()
                else:
                    button.grid()
                    text.config(text=words_on_page[index])
                index = index+1

     

        
    def getMeaning(self,text):
        self.fun_txt.delete('1.0', tk.END)
        txt = text['text']
        if len(txt)> 0:
            text.config(bg='yellow')
        else:
            return
        #print(self.dic_word_meaning[txt])
        try:
            self.fun_txt.insert(tk.END,txt)
            self.fun_txt.insert(tk.END,self.dic_word_meaning[txt])
        except Exception as e:
            print(e)
    def leaveMeaning(self,text):
        text.config(bg='dark sea green')
        

    def chooseWordFile(self):
        file_name = None 
        while file_name is None or len(file_name) == 0:
          file_name = filedialog.askopenfilename(initialdir = self.dir_words,title = "Select file",filetypes = (("word files","*.txt"),("data files","*.csv"),("all files","*.*")))
        self.origin_words = file_name
        self.readWords()

        

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
