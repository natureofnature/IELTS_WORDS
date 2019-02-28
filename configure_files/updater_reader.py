import sys
import os
from shutil import copyfile
class network_updater:
    def __init__(self):
        updater="./configure_files/updater.cfg"
        folders=[".:","./checker:","./configure_files:","./datasets:","./deployment:","./nets:","./notebooks:","./preprocessing:","./tf_extended:"]
        self.key_pair = {}
        with open(updater,'r') as f:
            current_path = None
            for line in f:
                content = line.rstrip('\r\n')
                prefix = ""
                if content in folders:
                    prefix=content.split(":")[0] 
                    current_path = prefix

                else:
                    line = line.split()
                    for file_name in line:
                        if "./" not in file_name and "pyc" not in file_name and "pycache" not in file_name:
                            path = os.path.join(current_path,file_name)
                            self.key_pair.update({file_name:path})


    def get_file_path_by_name(self,file_name):
        path = None
        try:
            path = self.key_pair[file_name]
            return path
        except:
            return 'invalid_path'


    def print_all_pair(self):
        for key,values in self.key_pair.items():
            print(key,values)


    def list_files_in_target_folder(self,target_folder):
        result = [(f,os.path.join(dp, f)) for dp, dn, filenames in os.walk(target_folder) for f in filenames]
        return result


    def updater(self,target_folder,fn):
        result = self.list_files_in_target_folder(target_folder)
        info = ""
        for item in result:
            name,path = item
            ori_path = self.get_file_path_by_name(name)
            if ori_path != "invalid_path":
                info = info+"\n"+path+" will overwrite"+ori_path
        fn(info)



