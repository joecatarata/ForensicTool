import threading
import os
import pickle
import time
import asyncio
import multiprocessing
import sys
import queue
from tkinter import *
from tkinter import ttk

class App(Tk):
    def center(self):
        self.update_idletasks()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        size = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        self.geometry("%dx%d+%d+%d" % (size + (x, y)))
        
    def __init__(self, headers, driveLetter,fileCtr,filedestination, choices, threadcount):
        Tk.__init__(self)
        self.headers = headers
        self.driveLetter = driveLetter
        self.fileCtr = fileCtr
        self.filedestination = filedestination
        self.choices = choices
        self.threadcount = threadcount
        
        manager = multiprocessing.Manager()
        self.queue = manager.Queue()
        self.listbox = Listbox(self, width=50, height=5)
        self.progressbar = ttk.Progressbar(self, orient='horizontal',
                                           length=300, mode='determinate')
        self.button = Button(self, text="Start", command=self.spawnthread)
        self.listbox.pack(padx=10, pady=10)
        self.progressbar.pack(padx=10, pady=10)
        self.button.pack(padx=10, pady=10)
        
        self.center()
        self.wm_title("Ready to Scan")

    def spawnthread(self):
        self.button.config(state="disabled")
        self.threads = []
        startnum = 0
        loopcount = self.threadcount  #100 default
        #Thread count
        #drivepath = driveLetter+":\\"
        #print(drivepath)
        #disksize = os.statvfs( drivepath )

        basecount =  10000000 / loopcount
        endnum = int(basecount)
        threads = []
        global fileCtr
        fileCtr = 0
        n=0
        for i in self.choices:
            while n < loopcount:
                if i in self.headers:
                    #SearchUsingTrailer(headers.get(i), driveLetter, i)
                    FUNC = multiprocessing.Process(target=SearchUsingTrailer, args=(self.headers.get(i), self.driveLetter, i,startnum, endnum,n+1,self.fileCtr,self.filedestination, self.queue))
                    #FUNC = AsyncSearch(headers.get(i), driveLetter, i,startnum, endnum,n+1)
                    self.threads.append(FUNC)
                    #SearchUsingTrailer(headers.get(i), driveLetter, i,startnum, endnum,n+1,)
                    print ('start number is', startnum, ' end number is', endnum)
                    startnum += int(basecount)
                    endnum += int(basecount)
                else:
                    print("Sorry file is not supported.")
                n+=1
            n = 0
            startnum = 0
            endnum = basecount

        for x in self.threads:
            x.start()
        self.wm_title("Scanning")
        self.periodiccall()

    def periodiccall(self):
        end = True
        self.checkqueue()
        if self.threads[0].is_alive():
            self.after(5, self.periodiccall)
        else:
            self.button.config(state="active")
            self.wm_title("Ready to Scan")

    def checkqueue(self):
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                self.listbox.insert('end', msg)
                self.progressbar.step(100/(self.threadcount*len(self.choices)))
            except Queue.Empty:
                pass



class ProgressGUI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self,master)
        self.pack()
        self.createWidgets()
        master.minsize(width=100, height=30)
    
    def createWidgets(self):
        self.progressbar = ttk.Progressbar(self.master, orient=HORIZONTAL, length=300, mode='determinate')
        self.progressbar.pack(side="bottom")
    
    def load(self):
        i = 0
        while i < 100:
            self.progressbar.step(1)
            time.sleep(1)
            i += 1

        
        
def loadprogress(headers, driveLetter,fileCtr,filedestination, choices, threadcount):      
    app = App(headers, driveLetter,fileCtr,filedestination, choices, threadcount)
    app.mainloop()
    
    
    

    
    
    
    
def writeToFile():
    pass


def SearchUsingTrailer(signatures,driveLetter,fileType,startnum,endnum,threadnum,fileCtr2,filedestination,mqueue):
    #drive = openDrive()
    #global fileCtr
    nfiles = 0
    time.sleep(0.5)
    headtemp = signatures[0]
    header = [headtemp[i:i+1] for i in range(len(headtemp))]
    trailtemp = signatures[1]
    trailer =  [trailtemp[i:i+1] for i in range(len(trailtemp))]
    print(header)
    print(trailer)
    nCtr = 0
    nMax = 10000000
    sector = 512
    maxSize = 10000000
    index = 0
    found = False
    pHead = '0'
    trailIndex = 0
    done = False
    with open(driveLetter, 'rb') as drive:
        #print(nCtr)
        #print("Opened Drive: " + driveLetter)
        #while nCtr < nMax:
        while startnum < endnum:
            #print(pHead, end="")
            #print(header[index])
            drive.seek(startnum * sector)
            pHead = cur = drive.read(1)
            cur = pHead
            while cur == header[index]:
                if cur == header[-1] and index == len(header)-1: #if current is equal to the last byte of the passed header
                    print("Found a potential file!")
                    print(cur, end="")
                    print(header[-1])
                    found = True
                    break
                cur = drive.read(1)
                index+=1

            if found:
                fileCtr2 += 1
                newFile = open(filedestination+"/Thread "+fileType+" "+str(threadnum)+" "+str(fileCtr2)+"."+fileType,"wb")
                curSize = 0
                trailIndex = 0
                foundTrailer = False
                done = False
                cur = pHead
                for i in header:
                    newFile.write(i)
                pHead = drive.read(1)
                done = False
                while done == False and curSize < maxSize:
                    trailIndex = 0
                    newFile.write(pHead)
                    while pHead == trailer[trailIndex]:
                        if pHead == trailer[-1] and trailIndex == len(trailer)-1:
                            print("Pumasok")
                            nfiles+=1
                            done = True
                            break
                        pHead = drive.read(1)
                        newFile.write(pHead)
                        trailIndex += 1
                        curSize += 1
                    #    print(trailIndex, end="")
                    if not done:
                        pHead = drive.read(1)
                        curSize += 1
                        trailIndex = 0

                if fileType == 'docx' or fileType == 'pptx' or fileType == 'xlsx' or fileType == 'zip':
                    i = 0
                    while i < 18:
                        pHead = drive.read(1)
                        newFile.write(pHead)
                        i += 1
                
                if fileType == 'doc' or fileType == 'ppt' or fileType == 'xls':
                    i = 0
                    while i < 500:
                        pHead = drive.read(1)
                        newFile.write(pHead)
                        i += 1
                
                newFile.close()
                if curSize >= maxSize:
                    print("False positive")
                #implement write to file
            trailIndex = 0
            index = 0
            startnum += 1
            #if endnum == 1000000:
                #print('currrent num',startnum, 'FIRST THREAD')
            #else:
                #print('currrent num',startnum)
            found = False
    print('loop no. ',threadnum,' ended')
    msg = "Thread "+str(threadnum)+" for filetype "+str(fileType)+" finished. files recovered: " + str(nfiles)
    mqueue.put(msg)
    
def carve(choices,driveLetter, threadcount, GUI, extraHeaders, filedestination):
    headers = {'jpg': [b'\xFF\xD8',b'\xFF\xD9'],
               'pdf': [b'\x25\x50\x44\x46', b'\x0A\x25\x25\x45\x4F\x46'],
               'docx': [b'\x50\x4B\x03\x04\x14\x00\x06\x00', b'\x50\x4B\x05\x06'],
               'xlsx': [b'\x50\x4B\x03\x04\x14\x00\x06\x00', b'\x50\x4B\x05\x06'],
               'png': [b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A', b'\x49\x45\x4E\x44\xAE\x42\x60\x82'],
               'doc': [b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1', b'\x38\x00\xF4\x39\xB2\x71'],
               'xls': [b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1', b'\xFE\xFF\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x57\x00\x6F\x00\x72\x00\x6B\x00\x62\x00\x6F\x00\x6F\x00\x6B\x00'],
               'zip': [b'\x50\x4B\x03\x04\x14', b'\x50\x4B\x05\x06'],
               'ppt': [b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1', b'\x50\x00\x6F\x00\x77\x00\x65\x00\x72\x00\x50\x00\x6F\x00\x69\x00\x6E\x00\x74\x00\x20\x00\x44\x00\x6F\x00\x63\x00\x75\x00\x6D\x00\x65\x00\x6E\x00\x74'],
               'rar': [b'\x52\x61\x72\x21\x1A\x07\x00', b'\x00\x40\x07\x00'],
               'pptx': [b'\x50\x4B\x03\x04\x14\x00\x06\x00', b'\x50\x4B\x05\x06'],
               'mpeg': [b'\x00\x00\x01\xB3' , b'\x00\x00\x01\xB7']
                                            
               }
    
    for key in headers:
        print ("key: %s , value: %s" % (key, headers[key]))
        
    #time.sleep(100)

    filename = 'headers'
    file = open(filename, 'wb')
    pickle.dump(headers, file)

    file = open(filename, 'rb')
    headers = pickle.load(file)
    #choices = []
    
    headers.update(extraHeaders)
    print(headers)
    """while True:
        print("Choose which file types will you want to recover")
        print("jpg")
        print("pdf")
        print("docx")
        print("xlsx")
        print("doc")
        print("xls")
        choice = (input("Enter choice(type the file type): "))

        choices.append(choice)

        AskMore = int(input("Do you want to input more files?[0/1]: "))
        if AskMore == 1:
            continue
        else:
            break
            
    driveLetter = input("Enter letter of drive to scan: ")
    driveLetter = driveLetter.upper()
    """ 
    startnum = 0
    loopcount = threadcount  #100 default
    #Thread count
    #drivepath = driveLetter+":\\"
    #print(drivepath)
    #disksize = os.statvfs( drivepath )
    
    basecount =  10000000 / loopcount
    endnum = int(basecount)
    threads = []
    global fileCtr
    fileCtr = 0
    n=0
    GUI.bottomText.set("in Carver")
    GUI.master.update()
    #drive = os.open("\\\\.\\"+driveLetter+":", 'rb')
    #test = os.open("\."+driveLetter+":",  os.O_RDONLY)
    #disksize = int(os.stat(filepath)[ST_SIZE])
    """for i in choices:
        while n < loopcount:
            if i in headers:
                #SearchUsingTrailer(headers.get(i), driveLetter, i)
                FUNC = multiprocessing.Process(target=SearchUsingTrailer, args=(headers.get(i), driveLetter, i,startnum, endnum,n+1,fileCtr,filedestination,))
                #FUNC = AsyncSearch(headers.get(i), driveLetter, i,startnum, endnum,n+1)
                threads.append(FUNC)
                #SearchUsingTrailer(headers.get(i), driveLetter, i,startnum, endnum,n+1,)
                print ('start number is', startnum, ' end number is', endnum)
                startnum += int(basecount)
                endnum += int(basecount)
            else:
                print("Sorry file is not supported.")
            n+=1
        n = 0
        startnum = 0
        endnum = basecount"""
        
        
    t = threading.Thread(target=loadprogress, args=(headers, driveLetter,fileCtr,filedestination, choices, threadcount))
    t.start()
    t.join()
        
    """   for x in threads:
        x.start()
        
    #print('Threads alive', multiprocessing.active_count())
    t.join()
    for x in threads:
        x.join()"""
    
