#!/usr/bin/env python

"""
Small utility to continuous trace an afs-client in a files storing x mins and keep files if something has happened
"""

import subprocess, time, getopt, sys
from multiprocessing import Process
from shutil import copyfile
import os, string

Output="afsclient.trace"
ProcessTableFilename="proctable"
numTraceFiles=2
TraceFileNames=[]
FSTRACEBIN="/usr/sbin/fstrace"
PSBIN="/bin/ps"
KILLBIN="/bin/kill"
TraceBufferSize=8192 # buffersize in k, needs to be big enough to store the data during Dumpinterval
Dumpinterval = 1 # at what interval buffer should be dumped to file
DumpProcs=[None, None]
EventCheckInterval = 1 # interval for checking for an externalEvent
RotationInterval=5 # 5 EventCheckInterval
EventFile="./fstrace_trigger"
verbose = False
debug=False
Mode="cont" 
# available Modes
# cont(inuous)
# single 

def setupFSTrace() :
    if verbose : print "Clearing log"
    try :
        subprocess.check_call([FSTRACEBIN,"clear",  "cm"])
    except subprocess.CalledProcessError:
        print "Unable to run fstrace-binary at %s." % FSTRACEBIN
        sys.exit(2)
    if verbose : print "setting eventset cm active"
    subprocess.check_call([FSTRACEBIN,"setset","cm","-active"])
    if verbose :  print "Setting buffersize of log cmfx"
    subprocess.check_call([FSTRACEBIN,"setlog","cmfx","-buffersize", "%s" % TraceBufferSize])
    return 
    
def dumpFSTrace(FileName) :
    subprocess.check_call([FSTRACEBIN,"dump","-follow","cmfx","-file",FileName, "-sleep", "%s" % Dumpinterval])
    return

def saveLogs(ProcessTable, TraceFileNo):
    NowStr=time.strftime("%H:%M:%S_%d.%m-%Y", time.localtime())
    for counter in range(numTraceFiles) :
        thisTraceFileNo=(TraceFileNo+counter) % numTraceFiles
        print "current TraceFileNo = %s" % TraceFileNo
        if verbose : print "Saving log %s-%s to %s-%s-%s" %  (Output,thisTraceFileNo,  Output,counter,  NowStr)
        copyfile("%s-%s" % (Output, thisTraceFileNo), "%s-%s-%s" % ( Output,counter,  NowStr))
    # also save ProcessTable of this interval
    if verbose : print "Saving ProcessTable to %s-%s" %  (ProcessTableFilename,NowStr)
    f=file("%s-%s" % (ProcessTableFilename,NowStr), "w+")
    _PIDs=ProcessTable.keys()
    PIDs=[]
    for pid in _PIDs :
        PIDs.append(int(pid))
    PIDs.sort()
    for pid in PIDs :
        f.write("%s %s %s\n" % (pid, ProcessTable["%s" % pid]["parentpid"],ProcessTable["%s" % pid]["cmd"]))
    f.close()
    return
    
def updateProcessTable():
    ProcessTable={}
    call=subprocess.Popen([PSBIN, "-eaf"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    line=call.stdout.readline() # ignore headerline
    while 1:
        line=call.stdout.readline()
        if not line :break
        tokens=line.split()
        if len(tokens) < 8 : continue
        pid=tokens[1]
	parentpid=tokens[2]
        cmd=string.join(tokens[7:], " ")
        # we do make the assumption that a pid is not reused within a rotationinterval.
        ProcessTable[pid] ={"cmd" : cmd}
	ProcessTable[pid]["parentpid"] = parentpid
    return ProcessTable

def getChildPid(pid,ProcessTable) :
    kids=[]
    for _pid in ProcessTable :
	if ProcessTable[_pid]["parentpid"] == "%s" % pid :
	    kids.append(_pid)
    pids=ProcessTable.keys()
    pids.sort()
    if 0 :
        for p in pids :
	    print "%s : %s" % (p,ProcessTable[p])
    return kids

def killPid(pid,signal="TERM") :
    rc=subprocess.call([KILLBIN, "-%s" % signal,pid])
    return rc

def main():
    setupFSTrace()
    TraceFileNo=0
    FileName=TraceFileNames[TraceFileNo]
    DumpProcNum=0
    if debug : print "Spawning dump-process to %s" % FileName
    DumpProcs[DumpProcNum] = Process(target=dumpFSTrace, args=(FileName,))
    DumpProcs[DumpProcNum].start()
    if Mode == "single" : # single-shot mode
        while 1 :
            if debug : print "Waiting for %s until next check for external Event." % EventCheckInterval
            ProcessTable=updateProcessTable()
            if externalEvent(EventFile) : 
                DumpProcs[DumpProcNum].terminate()
                ProcessTable=updateProcessTable()
                if debug : 
                      print "Killing childpids of %s : %s " % (DumpProcs[DumpProcNum].pid,getChildPid("%s" % DumpProcs[DumpProcNum].pid,ProcessTable))
		for kid in getChildPid("%s" % DumpProcs[DumpProcNum].pid,ProcessTable) :
		    killPid(kid)
                saveLogs(ProcessTable)
                break
            time.sleep(EventCheckInterval)
        sys.exit(0)
    # continuous run
    while 1 :
        Waited=0
        while Waited < RotationInterval :
            if debug : print "Waiting for %s until next check for external Event." % EventCheckInterval
            time.sleep(EventCheckInterval)
            Waited += 1
            ProcessTable=updateProcessTable()
            if debug : 
                print "Waitcount = %s" % Waited
                print "RotationInterval %s" % RotationInterval 
                print "ProcessTable :"
                print len(ProcessTable)
            if externalEvent(EventFile) :
                saveLogs(ProcessTable, TraceFileNo)
        if debug : print "Rotating Logs"
        TraceFileNo = (TraceFileNo+1) % (numTraceFiles)
        FileName=TraceFileNames[TraceFileNo]
        newDumpProcNum= (DumpProcNum +1) % 2
        if debug : print "Spawning next dump-process no %s to %s" % (newDumpProcNum, FileName)
        DumpProcs[newDumpProcNum] = Process(target=dumpFSTrace, args=(FileName,))
	DumpProcs[newDumpProcNum].start()
        ProcessTable=updateProcessTable()
        if debug : print "Terminating last dump-process %s" % DumpProcNum
        DumpProcs[DumpProcNum].terminate()
        if debug : 
            print "Killing childpids of %s : %s " % (DumpProcs[DumpProcNum].pid,getChildPid("%s" % DumpProcs[DumpProcNum].pid,ProcessTable))
	for kid in getChildPid("%s" % DumpProcs[DumpProcNum].pid,ProcessTable) :
	    if debug : print ProcessTable[kid]
	    killPid(kid)
	if debug: print DumpProcs
        DumpProcNum=newDumpProcNum
    return
    
#
# This function has to be replaced for new debugging cases
#

def externalEvent(EventFile):
    if os.path.isfile(EventFile) :
        os.unlink(EventFile)
        if verbose : print "external event happened!"
        return True
    if debug : print "no external event"
    return False

def usage():
    print "ClientTracing.py --dumpinterval=# --rotationinterval=# --buffersize=# --numfiles # --mode=[cont|single] --savemode=[lastonly|all] --verbose --debug"
    print "--dumpinterval=# / secs : interval of fstrace in secs to dump information"
    print "--eventcheckinterval=# / secs : How many secondes to wait between checking for an event" 
    print "--Eventfile=<name> : file to check if an external event happened" 
    print "--rotationinterval=# /units EventCheckInterval" 
    print "--buffersize=# buffer of fstrace log in memory"
    print "--numfiles # how many logfiles to write" 
    print "--mode=[cont|single]" 
    print 
    print "An event is triggered by the existance of the file %s\n" % EventFile
    print "You may also overwrite the function externalEvent()"


if __name__ == "__main__" :
    try:
        opts, args = getopt.getopt(sys.argv[1:], "he:E:d:r:m:b:vdn:s:", ["help", "eventcheckinterval=","Eventfile=","dumpinterval=", "rotationinterval=", "mode=", "buffersize=","verbose", "debug","numfiles=", "savemode="])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-v", "--verbose"):
            verbose = True
        elif o in ("-d", "--debug") :
            debug = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-e", "--eventcheckinterval") :
            EventCheckInterval = int(a)
        elif o in ("-E", "--Eventfile") :
            EventFile = int(a)
        elif o in ("-d", "--dumpinterval") :
            Dumpinterval = int(a)
        elif o in ('-r', "--rotationinterval") :
            RotationInterval = int(a)
        elif o in ("-b", "--buffersize") :
            TraceBufferSize=int(a)
        elif o in ("-m", "--mode") :
            Mode=a
            if not Mode in ['cont','single']  :
                print "mode takes only >cont< or >single< "
                sys.exit(2)
        elif o in ("-o", "--output") :
            Output=a
        elif o in ("-n", "--numfiles") :
            numTraceFiles=int(a)
        else :
            print "Unknown option %s" % o
            sys.exit(2)
    for i in range(int(numTraceFiles)) :
        TraceFileNames.append("%s-%s"% (Output, i))
    
    if verbose :
        print "Buffersize: %s" % TraceBufferSize
        print "Dumpinterval: %s" % Dumpinterval
        print "number of Tracfiles : %s" % numTraceFiles
        print "TraceFilenames: %s-#" % Output
        print "Rotationinterval: %s" % RotationInterval
        print "ProcessTableFilename=%s" % ProcessTableFilename
        print "Mode: %s" % Mode
    main()
