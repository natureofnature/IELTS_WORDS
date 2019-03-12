import sys
import os
import sys
if getattr(sys, 'frozen', False):
    working_dir= os.path.dirname(sys.executable)
elif __file__:
    working_dir = os.path.dirname(__file__)
path_file = os.path.join(working_dir,"./configure_files/history_path.info")
path_dics = {}

def getConfig():
    global working_dir
    config = os.path.join(working_dir,"./configure_files/config.cfg")
    width = 0 
    height = 0 
    dic = {}
    with open(config) as f:
        for line in f:
            tmp = (line.rstrip('\r\n').split(":->"))
            if len(tmp) <2:
                tmp.append("Undefined")
            dic.update({tmp[0]:tmp[1]})
    return dic
def setConfig(dic,key,value):
    global working_dir
    config = os.path.join(working_dir,"./configure_files/config.cfg")
    dic[key] = value
    with open(config,'w') as f:
        for k,v in dic.items():
            f.write(k+":->"+v+"\n")
            


def getLastDialogue():
    global path_file
    global path_dics
    with open(path_file,'r') as f:
        for line in f:
            tmp = (line.rstrip('\r\n').split(":->"))
            path_dics.update({tmp[0]:tmp[1]})
    return path_dics 


def setPath(keyword,value):
    global path_file
    global path_dics
    path_dics.update({keyword:value})
    with open(path_file,'w') as f:
        for k,p in path_dics.items():
            f.write(k+":->"+p+"\n")

def getParameters():
    config = "./parameters/parameters.dat"
    dic = {}
    with open(config) as f:
        for line in f:
            try:
                tmp = (line.rstrip('\r\n').split(":->"))
                dic.update({tmp[0]:tmp[1]})
            except:
                pass
    return dic
