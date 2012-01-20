@echo off

REM Tuneables
REM WHERE to store the output files in the end.
SET LOGDIR=C:\Users\hanke.DIJON\Desktop\afstest
REM A Dir in AFS which is save to access to calibrate 
REM output from wirehsark and afsd.log
REM leave empty for skipping this
SET AFS_CALIB_DIR="\\AFS\openafs.org\"

REM MAGICS 
SET AFSD_LOGFILE=%WINDIR%\TEMP\afsd.log
SET HOUR=%time:~-11,2%
CALL :TRIMHOUR %HOUR%
SET NOW=%date:~-4,4%.%date:~-10,2%.%date:~-7,2%.%HOUR%_%time:~-8,2%
SET LOGFILE="%LOGDIR%"\test_%NOW%.log
SET TSHARK_LOGFILE="%LOGDIR%"\test_%NOW%.tshark.log

echo Setup environment... please wait
REM setup afs client tracing
echo %time%:Setting up fs tracing >> %LOGFILE%
echo =========================== >> %LOGFILE%
fs trace -on >> %LOGFILE% 2>&1

REM prune afsd.log
fs trace -reset >> %LOGFILE% 2>&1
fs trace -dump >> %LOGFILE% 2>&1

echo %time%:Disable crypt >> %LOGFILE%
fs setcrypt off >> %LOGFILE% 2>&1
echo =========================== >> %LOGFILE%

echo %time%:Starting wireshark... >> %LOGFILE%
REM Start tshark in new window. It will be terminated later
START "TSHARK window %NOW%" CMD /C CALL "C:\Program Files\Wireshark\tshark.exe" -f "port 7001" -i \Device\NPF_{1085281B-4782-4DF4-AB96-FBD0033E6B61} ^> %TSHARK_LOGFILE% 2^>^&1
echo =========================== >> %LOGFILE%

echo %time%:Waiting 5 secs. for tshark to startup... >> %LOGFILE%
ping -n 5 127.0.0.1 >> %LOGFILE%
echo =========================== >> %LOGFILE%

if "%AFS_CALIB_DIR%" NEQ "" ( 
    echo Calibrating timestamps by calling dir on %AFS_CALIB_DIR%
    echo %time%:Flushing CalibDir %AFS_CALIB_DIR% >> %LOGFILE%
    fs flushvolume %AFS_CALIB_DIR% >> %LOGFILE% 2>&1
    echo =========================== >> %LOGFILE%
    echo %time%:Executing "dir %AFS_CALIB_DIR%"  >> %LOGFILE%
    dir %AFS_CALIB_DIR% >> %LOGFILE%
    echo =========================== >> %LOGFILE%
)
echo %time%:Dumping AFSD Trace >> %LOGFILE%
fs trace -dump >> %LOGFILE% 2>&1
copy %AFSD_LOGFILE% %LOGDIR%\afsd_%NOW%".startup.log"
echo =========================== >> %LOGFILE%
echo "Waiting for User to terminate session" >>  %LOGFILE%

echo Do what you want to do now...
echo and then press the any-key, when issue happened to stop debugging
PAUSE

echo %time%:Dumping AFSD Trace >> %LOGFILE%
fs trace -dump >> %LOGFILE% 2>&1
copy %AFSD_LOGFILE% %LOGDIR%\afsd_%NOW%".log"
echo Finished. Terminating TSHARK window in 5 secs. 

ping -n 5 127.0.0.1 > NUL
TASKKILL /fi "WINDOWTITLE eq TSHARK window %NOW%" > NUL

echo You can find the output files now in %LOGDIR%
exit /b

REM **************
REM ****************** EOB ********************
REM **************

:ENOARG
echo filesize as arg required!
exit /b

:TRIMHOUR
Set HOUR=%*
GOTO :EOF
