#-*- coding: utf-8 -*-

from ctypes import *
import optparse
from operator import itemgetter
import sys
import utils
import threading
import shutil
import time
import pickle
import hashlib
import re
import OleFileIO_PL as OLE
import os
import shutil
from random import sample, uniform, choice
from winappdbg import *
from threading import Thread


def pick():
    
    if "target" not in os.listdir("."):
        os.mkdir("target")
    if len(os.listdir("target")) == 0:
        print "input target HWP files"
        exit()
    if "temp" not in os.listdir("."):
        os.mkdir("temp")
    if "result" not in os.listdir("."):
        os.mkdir("result")
    picked_file = choice(os.listdir("target"))
    try:
        shutil.copy(os.getcwd()+"\\target\\"+picked_file, "temp")
    except:
        emptyTemp()
    finally:
        shutil.copy(os.getcwd()+"\\target\\"+picked_file, "temp")
    return picked_file


def mutations(dest_file):
    
    dest_file = os.getcwd()+"\\temp\\"+dest_file
    find_list = []
    mutate_position = []
        
    ole = OLE.OleFileIO(dest_file)
    ole_list = ole.listdir()

    for entry in ole_list:
        if "BinData" in entry and not ".OLE" in entry[1]:
            find_list.append((ole.openstream("BinData/"+entry[1]).read(16), ole.get_size("BinData/"+entry[1])))
    ole.close()
    print find_list

    fuzz_offset = []
    fuzz_byte = xrange(256)
    with open(dest_file, 'rb') as f:
        hwp = f.read()
        hwp_write = bytearray(hwp)
        hwp_length = len(hwp)
        for magic, size in find_list:
            if hwp.find(magic) != -1:
                offset = hwp.find(magic)
                mutate_position.append((offset, size))


        for offset, size in mutate_position:
            fuzz_offset += sample(xrange(offset, offset+size), int(size*uniform(0.001, 0.03)))


        for index in fuzz_offset:
            if index >= hwp_length : continue
            hwp_write[index] = choice(fuzz_byte)

        try:
            with open(dest_file, 'wb') as f:
                f.write(hwp_write)
            return True
        except IOError as error:
            print error
            return False
        

def handle(event):
    global proc
    global flag
    global crash_count
    code = event.get_event_code()
    proc = event.get_process()
    if ExceptionEvent(event.debug, event.raw).get_exception_code() in exceptions:
        flag = True
        crash = Crash(event)
        crash.fetch_extra_data( event, takeMemorySnapshot = 0 ) 

        unique = crash.signature[3]
        if unique  in unique_list:
            proc.kill()
        else:
            crash_count += 1
            unique_list.append(unique)
            report = crash.fullReport()
            key = hashlib.md5(unique).hexdigest()
            try:
                os.mkdir(r"result\%s" % key)
                with open(r"result\%s\log.txt" % key, "w") as f:f.write(report)
                shutil.copy(os.getcwd()+"\\target\\"+target_file.split('\\')[-1], "result\\%s\\seed.%s" % (key, target_file.split(".")[-1]))
                shutil.copy(os.getcwd()+"\\temp\\"+target_file.split('\\')[-1], "result\\%s\\mutate.%s" % (key, target_file.split(".")[-1]))
            except:pass
            finally:proc.kill()

def debug():
    with Debug(handle, bKillOnExit=True) as dbg:
        dbg.execl('"%s" "%s"' % (program, os.getcwd()+"\\temp\\"+target_file))
        dbg.loop()

def runloop():
    thread = Thread(target=debug)
    thread.start()
    while True:
        if flag:
            thread.join()
            break
        if time.time() > maxTime and not flag:
            try:
                proc.kill()
            except:
                os.system("taskkill /f /im %s" % program.split('\\')[-1])
            thread.join()
            break
        time.sleep(0.5)

def emptyTemp():
    while len(os.listdir("temp")) != 0 :
        for x in os.listdir("temp"):
            try:
                os.remove(r"temp\%s" % x)
            except:
                pass

timeLimit = 3
exceptions = 0x80000002, 0xC0000005, 0xC000001D, 0xC0000025,\
             0xC0000026, 0xC000008C, 0xC000008E, 0xC0000090,\
             0xC0000091, 0xC0000092, 0xC0000093, 0xC0000094,\
             0xC0000095, 0xC0000096, 0xC00000FD, 0xC0000374
unique_list = []
if "Hwp.exe" not in os.listdir("C:\\Program Files\\Hnc\\Office NEO\\HOffice96\\Bin"):
    program = raw_input("input specific Hwp.exe path : \t")
else:
    program = r"C:\Program Files\Hnc\Office NEO\HOffice96\Bin\Hwp.exe"
crash_count = 0
iter=0
while True:
    iter +=1
    flag = False
    target_file = pick()
    mutations(target_file)
    os.system('cls')
    print "Iter counts : %d / Crash : %d" % (iter, crash_count)
    maxTime = time.time() + timeLimit
    runloop()
    emptyTemp()
