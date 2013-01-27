#!/usr/bin/python 

import sys,getopt

def usage():
    print "Usage : --gdb-output-file=filename --in-function=<function-name>, --exclude-function=<function-name>,<function-name>"
    print "--in-function :  show only threads whose stack has functions of name <function-name> (or part thereof)"
    print "--exclude-function :  do not show threads whose stack has functions of name <function-name> (or part thereof)"
    print "---gdb-output-file : gdb output file to use"
    sys.exit(2)

try:
    opts, args = getopt.getopt(sys.argv[1:], "hg:i:e:", ["help", "gdb-output-file=","in-function=","exclude-function="])
except getopt.GetoptError, err:
    # print help information and exit:
    print str(err) # will print something like "option -a not recognized"
    usage()
    sys.exit(2)

gdb_ofile="gdb.out"
includes=""
excludes=[]

for o, a in opts:
    if o in ("-h", "--help"):
        usage()
        sys.exit()
    elif o in ("-g", "--gdb-output-file") :
        gdb_ofile=a
    elif o in ('-i', "--in-function") :
        include=a
    elif o in ('-e', "--exclude-function") :
       excludes=a.split(",")
    else :
        print "Unknown option %s" % o
        sys.exit(2)

Threads={}
f=file(gdb_ofile,"r")
skipnextLine=False
while 1: 
    if not skipnextLine :
        line=f.readline()   
    else :
        skipnextLine=False 
    if not line: break
    line=line.strip()
    if len(line) == 0 : continue
    if "to continue, or q" in line : continue
    tokens=line.split()
    if tokens[0] == "Thread" :
        thisThread=[]
        useThread=True
        hasKeyword=False
        while 1 :
            line=f.readline()
            if not line : break
            if "to continue, or q" in line : continue
            line=line.strip()
            if len(line) == 0 : break
            ttokens=line.split()
            if ttokens[0] == "Thread" :  
                skipnextLine = True
                break
            if line[0] != "#" :
                line += f.readline().strip()
            thisThread.append(line)
            for e in excludes :
                if e in line :
                    useThread=False
            if includes in line : 
                hasKeyword=True 
        if useThread and hasKeyword :
            Threads[tokens[1]]=thisThread
                       
for t in Threads :
    print "Thread %s" % t 
    for line in  Threads[t] :
       print line
    print
