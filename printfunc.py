#!/usr/bin/env python

import re
import os
import sys
import shutil
import common
import argparse
from pprint import pprint

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
        try:
            with open(files,'r') as f:
                lines = f.readlines()
        except:
            return
        with open(dire + '/location.py','r') as f:
            location = f.read()
        index_future = 0
        index_list_future = [i for i, line in enumerate(lines) if re.search('__future__',line)]
        if index_list_future: index_future = max(index_list_future)
        with open(files, 'w') as f:
            val = False
            preval = False
            doc_val = False
            for i, line in enumerate(lines):
                if i == index_future:
                    if i == 0:
                        f.write(location)
                        f.write(line)
                    else:
                        f.write(line)
                        f.write(location)
                elif re.search('^ *def _',line):
                    f.write(line)
                    continue
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
                elif doc_val and re.search('\"\"\"',line):
                    try:
                        firstline = min([tmpi for tmpi in range(3) if re.search('\S',lines[i+1+tmpi])])
                        #pprint(lines[i+firstline+1])
                        m = re.search('( +)',lines[i+firstline+1])
                    except:
                        firstline = 0
                        m = re.search('( +)',lines[i+firstline])
                    if m: wspace = m.group(1)
                    f.write(line +wspace + 'location()\n')
                    doc_val = False
                elif val and re.search('\S',line):
                    m = re.match('( +)',line)
                    s = re.match('( *| *r)\"\"\"',line)
                    if s:
                        if re.match('( *| *r)\"\"\".*\"\"\"',line):
                            wspace = m.group(1)
                        else:
                            f.write(line)
                            val = False
                            doc_val = True
                        continue
                    elif m:
                        wspace = m.group(1)
                    elif re.match('#',line):
                        m1 = re.match('( +)',lines[i+1])
                        wspace = m1.group(1)
                    f.write(wspace + 'location()\n' + line)
                    val = False
                #elif val and re.search('\S',line):
                #    elif re.match('\n',line):
                #        wspace = '    '
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
            if re.search('python/framework/dtypes.py',files) or \
               re.search('tensorflow/python/platform/flags.py',files):
                pass
            else:
                self.sedfile(files)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path for sed printfunc",
                        type=str)
    args = parser.parse_args()
    prfunc = Prfunc(args.path)
    prfunc.sedall()
