#!/usr/bin/env python

import re
import os
import sys
import shutil
import common

class Prfunc():
    def __init__(self,path):
        self.getpython(path)
        oldpath = re.sub(r'/$','',path) + '.old'
        if not os.path.exists(oldpath):
            shutil.copytree(path,oldpath)

    def sedfile(self,files):
        lines = []
        location = ''
        dire , _ = os.path.split(os.path.abspath(__file__))
        with open(files,'r') as f:
            lines = f.readlines()
        with open(dire + '/location.py','r') as f:
            location = f.read()
        index_future = 0
        index_list_future = [i for i, line in enumerate(lines) if re.search('__future__',line)]
        if index_list_future: index_future = max(index_list_future)
        with open(files, 'w') as f:
            val = False
            preval = False
            for i, line in enumerate(lines):
                if i == index_future:
                    f.write(line)
                    f.write(location)
                elif re.search('^ *def ',line):
                    f.write(line)
                    if re.search('\):',line):
                        val = True
                    else:
                        preval = True
                elif preval and re.search('\):', line):
                    val = True
                    preval = False
                    f.write(line)
                elif val:
                    m = re.match('( +)',line)
                    if m :wspace = m.group(1)
                    f.write(wspace + 'print(location())\n' + line)
                    val = False
                else:
                    f.write(line)

    def getpython(self,path):
        pythonfile_list = []
        for files in common.find_all_files(path):
            _ , ext = os.path.splitext(files)
            if ext == '.py':
                pythonfile_list.append(files)
        self.pythonfile_list = pythonfile_list
        return pythonfile_list

    def sedall(self):
        for files in self.pythonfile_list:
            self.sedfile(files)

if __name__ == '__main__':
    prfunc = Prfunc('horovod')
    prfunc.sedall()
