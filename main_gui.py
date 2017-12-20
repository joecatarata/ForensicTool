from tkinter import filedialog
from tkinter import font as tkfont
from tkinter import *
from Carver import *
from tkinter import ttk 
from stat import * # ST_SIZE etc
from DriveWiper.Formatter import *
from Cipher.Cipher import *
from Steganography.steganography import *
#import win32api
import psutil
import time
import os
import base64
#import matplotlib


class Application(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.minsize(width=720, height=550)
        self.center()
        
        self.show_Main()
        #self.show_Machine_Project_2()
        
    def show_Main(self):   
        self.Main = Main_Frame(master=self)
        self.Main.FileCarverbutt["command"] = lambda: [f() for f in [self.Main.destroy, self.show_File_Carver]]
        self.Main.MACHINE_PROJECT2butt["command"] = lambda: [f() for f in [self.Main.destroy, self.show_Drive_Wiper]]
        self.Main.MACHINE_PROJECT3butt["command"] = lambda: [f() for f in [self.Main.destroy, self.show_Cipher]]
        self.Main.MACHINE_PROJECT4butt["command"] = lambda: [f() for f in [self.Main.destroy, self.show_Steganography]]
        self.Main.tkraise()
    
    def show_File_Carver(self):   
        self.File_Carver = File_Carver_Frame(master=self)
        self.File_Carver.backButt["command"] = lambda: [f() for f in [self.File_Carver.bottomLabel.destroy,self.File_Carver.destroy,self.show_Main]]
        self.File_Carver.tkraise()
    
    def show_Drive_Wiper(self):
        self.MP2 = Machine_Project_2_Frame(master=self)
        self.MP2.backButt["command"] = lambda: [f() for f in [self.MP2.destroy,self.show_Main]]
        #self.MP2.StartButt["command"] = lambda: StartWiper(self.MP2.var_drive.get()[0]) 
        self.MP2.StartButt["command"] = lambda: self.MP2.scan_drive(self.MP2.var_drive.get()) 
        self.MP2.FormatButt["command"] = self.MP2.format_drive
        self.MP2.DeleteButt["command"] = self.MP2.delete_file
        self.MP2.tkraise()
    
    def show_Cipher(self):
        self.MP3 = Machine_Project_3_Frame(master=self)
        self.MP3.StartButt["command"] = self.MP3.startcipher
        self.MP3.DecodeButt["command"] = self.MP3.startdecipher
        self.MP3.backButt["command"] = lambda: [f() for f in [self.MP3.destroy,self.show_Main]]
        self.MP3.tkraise()
    
    def show_Steganography(self):
        self.MP4 = Machine_Project_4_Frame(master=self)
        self.MP4.encodebutt["command"] = self.MP4.encode_image
        self.MP4.decodebutt["command"] = self.MP4.decode_image
        self.MP4.backButt["command"] = lambda: [f() for f in [self.MP4.destroy,self.show_Main]]
        self.MP4.tkraise()
        
    
    def center(self, sub=None):
        self.update_idletasks()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        size = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        self.geometry("%dx%d+%d+%d" % (size + (x, y)))
        
        if sub is not None:
            sub.update_idletasks()
            w = sub.winfo_screenwidth()
            h = sub.winfo_screenheight()
            size = tuple(int(_) for _ in sub.geometry().split('+')[0].split('x'))
            x = w/2 - size[0]/2
            y = h/2 - size[1]/2
            sub.geometry("%dx%d+%d+%d" % (size + (x, y)))
        
        


class Main_Frame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack(pady=15) 
        #self.createWidgets() #Creates widgets for the Frame
        #master.minsize(width=720, height=500) #sets the minimum frame size
        #self.center(master) #sets the position of the frame to the center of the screen
        master.wm_title("FORENSC Machine Project")
        self.init_ui()
    
    def init_ui(self):

        self.programFrame = LabelFrame(self, text="Programs" , font=("calibri", 12))
        self.programFrame.grid(in_=self,column=1, row=1,sticky=E+W, padx=15, ipady=5)
        
        
        self.FileCarverbutt = Button(self, font=("calibri", 12))
        self.FileCarverbutt["text"] = "File Carver"
        self.FileCarverbutt.grid(in_=self.programFrame, column=1, row=1, sticky=E+W, padx=15, pady=5, columnspan=4)
        
        #NAME IS TENTATIVE
        self.MACHINE_PROJECT2butt = Button(self, font=("calibri", 12))
        self.MACHINE_PROJECT2butt["text"] = "Drive Wiper"
        self.MACHINE_PROJECT2butt.grid(in_=self.programFrame, column=1, row=2, sticky=E+W, padx=15, pady=5, columnspan=4)
        
        #NAME IS TENTATIVE
        self.MACHINE_PROJECT3butt = Button(self, font=("calibri", 12))
        self.MACHINE_PROJECT3butt["text"] = "Cipher"
        self.MACHINE_PROJECT3butt.grid(in_=self.programFrame, column=1, row=3, sticky=E+W, padx=15, pady=5, columnspan=4)
        
        #NAME IS TENTATIVE
        self.MACHINE_PROJECT4butt = Button(self, font=("calibri", 12))
        self.MACHINE_PROJECT4butt["text"] = "Steganography"
        self.MACHINE_PROJECT4butt.grid(in_=self.programFrame, column=1, row=4, sticky=E+W, padx=15, pady=5, columnspan=4)


        
class Machine_Project_4_Frame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack(pady=15)
        
        master.wm_title("Steganography")
        self.init_ui()
        
    def browsecsv(self):
        Tk().withdraw() 
        destination = filedialog.askopenfile()
        if destination:
#            print(dir(self.destination))
            print(destination.name)
            self.currentImage = destination.name
        else:
            print("None")
    
    def lbrowsecsv(self):
        Tk().withdraw() 
        destination = filedialog.askopenfile()
        if destination:
#            print(dir(self.destination))
            print(destination.name)
            self.currentDecodeImage = destination.name
        else:
            print("None")
            
    def encode_image(self):
        print("Encoding")
        plaintext = self.plain_text_area.get("1.0",'end-1c')
        
        steganographer = Steganographer()

        if self.var_algo.get() == "Basic":
            steganographer.encodePng(self.currentImage, plaintext)
        else:
            steganographer.encodePngWithSet(self.currentImage, plaintext, self.var_algo.get())
    
    def decode_image(self):
        print("Decoding")
        steganographer = Steganographer()
        
        if self.lvar_algo.get() == "Basic":
            message = steganographer.decodePng(self.currentDecodeImage)
        else:
            message = steganographer.decodePngWithSet(self.currentDecodeImage, self.lvar_algo.get())
        
        self.decode_text_area.delete('1.0', END)
        self.decode_text_area.insert(END, message)
        

    def init_ui(self):
        self.currentImage = ""
        self.upperdiv = LabelFrame(self, text="Encode")
        self.upperdiv.pack()
        
        #ENCODE
        self.choicediv = LabelFrame(self)
        self.choicediv.grid(in_=self.upperdiv, column=1, row=1, columnspan=10)
        
        self.browsebutt = Button(self)
        self.browsebutt["text"] = "Select Image File"
        self.browsebutt["command"] = self.browsecsv
        self.browsebutt.grid(in_=self.choicediv, column=3, row=1,sticky=E+W, padx=5, columnspan=2)
        
        algos = ["Basic", "Fibonacci", "Eratosthenes", "Logarithm"]
        self.var_algo_label = StringVar() 
        self.algo_label = Label(self,textvariable=self.var_algo_label, font=("calibri", 12))
        self.var_algo_label.set("Generators:")
        self.algo_label.grid(in_=self.choicediv, column=3, row=2, padx=5)
        
        self.var_algo = StringVar(self)
        self.var_algo.set(algos[0])
        self.algo_dropdown = OptionMenu(self, self.var_algo, *algos)
        self.algo_dropdown.grid(in_=self.choicediv,column=4, row=2, padx=5)
        
        self.encodebutt = Button(self)
        self.encodebutt["text"] = "Encode"
        self.encodebutt.grid(in_=self.choicediv, column=3, row=5,sticky=E+W, padx=5, columnspan=2)
        
        self.plain_text_div = LabelFrame(self, text="Text")
        self.plain_text_div.grid(in_=self.upperdiv, column=1, row=5, columnspan=10)
        self.plain_text_area =  Text(self.plain_text_div, height=5)
        self.plain_text_area.grid(in_=self.plain_text_div,column=1, row=1,sticky=E+W, padx=5, columnspan=1, rowspan=1)
        
        
        #DECODE
        self.currentDecodeImage = ""
        self.lowerdiv = LabelFrame(self, text="Decode")
        self.lowerdiv.pack()
        
        
        self.lchoicediv = LabelFrame(self)
        self.lchoicediv.grid(in_=self.lowerdiv, column=1, row=1, columnspan=10)
        
        self.lbrowsebutt = Button(self)
        self.lbrowsebutt["text"] = "Select Image File"
        self.lbrowsebutt["command"] = self.lbrowsecsv
        self.lbrowsebutt.grid(in_=self.lchoicediv, column=3, row=1,sticky=E+W, padx=5, columnspan=2)
        
        algos = ["Basic", "Fibonacci", "Eratosthenes", "Logarithm"]
        self.lvar_algo_label = StringVar() 
        self.lalgo_label = Label(self,textvariable=self.lvar_algo_label, font=("calibri", 12))
        self.lvar_algo_label.set("Generators:")
        self.lalgo_label.grid(in_=self.lchoicediv, column=3, row=2, padx=5)
        
        self.lvar_algo = StringVar(self)
        self.lvar_algo.set(algos[0])
        self.lalgo_dropdown = OptionMenu(self, self.lvar_algo, *algos)
        self.lalgo_dropdown.grid(in_=self.lchoicediv,column=4, row=2, padx=5)
        
        self.decodebutt = Button(self)
        self.decodebutt["text"] = "Decode"
        self.decodebutt.grid(in_=self.lchoicediv, column=3, row=5,sticky=E+W, padx=5, columnspan=2)
        
        self.decode_text_div = LabelFrame(self, text="Decoded Text")
        self.decode_text_div.grid(in_=self.lowerdiv, column=1, row=5, columnspan=10)
        self.decode_text_area =  Text(self.decode_text_div, height=5)
        self.decode_text_area.grid(in_=self.decode_text_div,column=1, row=1,sticky=E+W, padx=5, columnspan=1, rowspan=1)
        
        self.backButt = Button(self, font=("calibri", 12),height = 1, width = 10)
        self.backButt["text"] = "Back"
        self.backButt.pack(in_=self, padx=10, pady=3)
    
        
        
class Machine_Project_3_Frame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack(pady=15)
        
        #Name is Tentative
        master.wm_title("Cipher")
        self.init_ui()
        
    def startcipher(self):
        print("in Start Cipher")
        self.cipher = Cipher()
        self.cipher.def_shift_num(int(self.shiftEntry.get()),True)
        self.cipher.set_dictionary(self.var_algo.get())
        plaintext = self.plain_text_area.get("1.0",'end-1c')
        
        
        if self.dynamicvar.get() == 1:
            ciphertext = self.cipher.start_dynamic_cipher(plaintext)
        else:
            ciphertext = self.cipher.start_cipher(plaintext)
        
        print(ciphertext)
        
        
        self.cipher_text_area.delete('1.0', END)
        self.cipher_text_area.insert(END, ciphertext)
        
 
    def startdecipher(self):
        print("in Start Decipher")
        
        if self.cipher:
            self.cipher.def_shift_num(int(self.shiftEntry.get()),True)
            self.cipher.set_dictionary(self.var_algo.get())
            ciphertext = self.cipher_text_area.get("1.0",'end-1c')


            if self.dynamicvar.get() == 1:
                deciphertext = self.cipher.start_dynamic_decipher(ciphertext)
            else:
                deciphertext = self.cipher.start_decipher(ciphertext)

            print(deciphertext)


            self.decipher_text_area.delete('1.0', END)
            self.decipher_text_area.insert(END, deciphertext)
        
    def init_ui(self):
    
        
        self.upperdiv = LabelFrame(self)
        self.upperdiv.pack()
        
        algos = ["Emoji", "NATO", "Super", "SHA1", "Reverse"]
        self.var_algo_label = StringVar() 
        self.algo_label = Label(self,textvariable=self.var_algo_label, font=("calibri", 12))
        self.var_algo_label.set("Algorithm:")
        self.algo_label.grid(in_=self.upperdiv, column=1, row=1,sticky=W, padx=5)
        
        self.var_algo = StringVar(self)
        self.var_algo.set(algos[0])
        self.algo_dropdown = OptionMenu(self, self.var_algo, *algos)
        self.algo_dropdown.grid(in_=self.upperdiv,column=2, row=1,sticky=E+W, padx=5) 
        
        self.var_shift_label = StringVar() 
        self.shift_label = Label(self,textvariable=self.var_shift_label, font=("calibri", 12))
        self.var_shift_label.set("Shift Number:")
        self.shift_label.grid(in_=self.upperdiv, column=1, row=2,sticky=W, padx=5)
        
        
        self.shiftEntry = Spinbox(self, from_=0, to=26)
        self.shiftEntry.grid(in_=self.upperdiv, column=2, row=2, sticky=E+W, pady=10, padx=10)
        
#        self.var_algo = StringVar(self)
#        self.var_algo.set(algos[0])
#        self.algo_dropdown = OptionMenu(self, self.var_algo, *algos)
#        self.algo_dropdown.grid(in_=self.upperdiv,column=2, row=1,sticky=E+W, padx=5) 
        
        self.dynamicvar = IntVar(self)
        self.dynamic  = Checkbutton(self, text="Dynamic",  variable=self.dynamicvar)
        self.dynamic.grid(in_=self.upperdiv, sticky=W, column=3, row=1, columnspan=1)
        
        self.StartButt = Button(self, font=("calibri", 12),height = 1, width = 10)
        self.StartButt["text"] = "Encode"
        self.StartButt.grid(in_=self.upperdiv,column=1, row=3,sticky=E+W, padx=5)
        
        self.DecodeButt = Button(self, font=("calibri", 12),height = 1, width = 10)
        self.DecodeButt["text"] = "Decode"
        self.DecodeButt.grid(in_=self.upperdiv,column=2, row=3,sticky=E+W, padx=5)
        
        #Plain Text
        self.plain_text_div = LabelFrame(self, text="Plain Text")
        self.plain_text_div.pack()
        
        self.plain_text_area =  Text(self.plain_text_div, height=5)
        self.plain_text_area.grid(in_=self.plain_text_div,column=1, row=1,sticky=E+W, padx=5, columnspan=1, rowspan=1)
        
        #Ciphered Text
        self.cipher_text_div = LabelFrame(self, text="Cipher Text")
        self.cipher_text_div.pack()
        
        self.cipher_text_area =  Text(self.cipher_text_div, height=5)
        self.cipher_text_area.grid(in_=self.cipher_text_div,column=1, row=1,sticky=E+W, padx=5, columnspan=1, rowspan=1)
        
        #DeCiphered Text
        self.decipher_text_div = LabelFrame(self, text="Decipher Text")
        self.decipher_text_div.pack()
        
        self.decipher_text_area =  Text(self.decipher_text_div, height=5)
        self.decipher_text_area.grid(in_=self.decipher_text_div,column=1, row=1,sticky=E+W, padx=5, columnspan=1, rowspan=1)
        
        self.backButt = Button(self, font=("calibri", 12),height = 1, width = 10)
        self.backButt["text"] = "Back"
        self.backButt.pack(in_=self, padx=10, pady=3)
        
        
        
    
class Machine_Project_2_Frame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack(pady=15)
        
        #Name is Tentative
        master.wm_title("Drive Wiper")
        self.init_ui()
    
    
    def format_drive(self):
        if self.wiper is not None:
            drive_format = self.var_file_system.get()
            print("Formatting Drive... into ",drive_format)
            self.wiper.formatDrive(drive_format)
        else:
            print("Please scan first.")
        
    
    def delete_file(self):
        if self.wiper is not None:
            metadata_tree_item = self.metadata_tree.item(self.metadata_tree.focus())
            filename = metadata_tree_item['values'][0]
            delete_algo = self.var_Delete_Algo.get()
            print("file_name: ", filename)
            print("delete_algo: ", delete_algo)
            self.wiper.deleteFile(filename, delete_algo)
    
    def scan_drive(self, path):
        with open(path, 'r+b') as drive:
            self.metadata_tree.delete(*self.metadata_tree.get_children())
            
            self.wiper = Wiper()
            self.wiper.setDrivePath(path)
            self.wiper.openDrive(drive)

            self.wiper.testDrive()
            print("in get FileSystem")
            #print("metadata of Drive: ")
            metadata = self.wiper.getFileSystem()
            
            print("metadata of Drive: ")
            self.fill_metadata_drive(metadata)
#            for i in range(len(metadata)):
#                print(metadata[i])
                
            print("out of get FileSystem")
            list_files = self.wiper.listFiles()
#            print(list_files)
            for num,file in enumerate(list_files):
#                print(num,file)
                file_Metadata = self.wiper.getMetaData(file)
                self.metadata_tree.insert("" , 2,    text=str(num+1), values=(file_Metadata['File Name'],file_Metadata['Inode'],file_Metadata['File Size']))
        
    def fill_metadata_drive(self, metadata):
        
        self.metadata_text_area.delete('1.0', END)
        metadata_str = ""
        for i in range(len(metadata)):
            print(str(i) +": ",metadata[i])
            if i == 0:
                metadata_str += "Device: "+metadata[i]+"\n"
            if i == 1:
                metadata_str += "Mount Point: "+metadata[i]+"\n"
            if i == 2:
                metadata_str += "File System type: "+metadata[i]+"\n"
            if i == 3:
                metadata_str += "Opts: "+metadata[i]+"\n"
            
        #metadata_str+="\n\n"+"Original output: ", str(metadata)
        self.metadata_text_area.insert(END, metadata_str)
            
        
        
#        print("3: ",metadata[4])
                
        
    def init_ui(self):
        self.upperdiv = LabelFrame(self)
        self.upperdiv.pack()
        
        #DRIVE
#        drives = win32api.GetLogicalDriveStrings()
#        the_drives = drives.split('\000')[:-1]
        drives = psutil.disk_partitions()
        the_drives = [i[0] for i in drives]
        print(the_drives)
        self.var_drive_label = StringVar() 
        self.drive_label = Label(self,textvariable=self.var_drive_label, font=("calibri", 12))
        self.var_drive_label.set("Drive:")
        self.drive_label.grid(in_=self.upperdiv, column=1, row=1,sticky=W, padx=5)
                
        self.var_drive = StringVar(self)
        self.var_drive.set(the_drives[0])
        self.drive_dropdown = OptionMenu(self, self.var_drive, *the_drives)
        self.drive_dropdown.grid(in_=self.upperdiv,column=2, row=1,sticky=E+W, padx=5) 
        
        self.StartButt = Button(self, font=("calibri", 12),height = 1, width = 10)
        self.StartButt["text"] = "Scan"
        self.StartButt.grid(in_=self.upperdiv,column=1, row=2,sticky=E+W, padx=5, columnspan=2)
        
        self.Formating_div = LabelFrame(self)
        self.Formating_div.grid(in_=self.upperdiv,column=3, row=1,sticky=E+W, padx=5, columnspan=3, rowspan=2)
        
        #FILE SYSTEM
        
        the_file_systems = ["ext4", "FAT32","exFat"]
            
        self.var_file_system_label = StringVar() 
        self.file_system_label = Label(self,textvariable=self.var_file_system_label, font=("calibri", 12))
        self.var_file_system_label.set("File System:")
        self.file_system_label.grid(in_=self.Formating_div, column=1, row=1, sticky=W, padx=5)
 
        self.var_file_system = StringVar(self)
        self.var_file_system.set(the_file_systems[0])
        self.file_system_dropdown = OptionMenu(self, self.var_file_system, *the_file_systems)
        self.file_system_dropdown.grid(in_=self.Formating_div,column=2, row=1,sticky=E+W, padx=5)
        
        self.FormatButt = Button(self, font=("calibri", 12),height = 1, width = 10)
        self.FormatButt["text"] = "Format"
        self.FormatButt.grid(in_=self.Formating_div,column=1, row=2,sticky=E+W, padx=5, columnspan=2)
        
        #METADATA OF DRIVES
        self.metadata_drive_div = LabelFrame(self, text="Drive Metadata")
        self.metadata_drive_div.grid(in_=self.upperdiv,column=1, row=3,sticky=E+W, padx=5, columnspan=3, rowspan=1)
        
#        self.metadata_text_area = Text(self)
        self.metadata_text_area =  Text(self.metadata_drive_div, width=72, height=5)
        self.metadata_text_area.grid(in_=self.metadata_drive_div,column=1, row=1,sticky=E+W, padx=5, columnspan=1, rowspan=1)
        
#        vscroll = Scrollbar(self, orient=VERTICAL, command=self.metadata_text_area.yview)
#        vscroll.place(in_=self.metadata_text_area, relx=1.0, relheight=1.0, bordermode="outside")
#        self.metadata_text_area = Text(self.master)
        
        
        #METADATA OF FILES
        self.metadata_div = LabelFrame(self, text="Files")
        self.metadata_div.grid(in_=self.upperdiv,column=1, row=4,sticky=E+W, padx=5, columnspan=4, rowspan=2)
        
        self.metadata_tree = ttk.Treeview(self)
        self.metadata_tree["columns"]=("File_Name","Inode","File_Size")
        self.metadata_tree.column("#0", width=50)
        self.metadata_tree.column("File_Name", width=150)
        self.metadata_tree.column("Inode", width=150)
        self.metadata_tree.column("File_Size", width=150)
        #self.tree.column("Status", width=100)
        self.metadata_tree.heading("File_Name", text="File Name")
        self.metadata_tree.heading("Inode", text="Inode")
        self.metadata_tree.heading("File_Size", text="File Size")
        #self.tree.heading("Status", text="Status")
        self.metadata_tree.grid(in_=self.metadata_div, column=1,row=1, padx=9, pady=5)
        
        self.delete_div = LabelFrame(self)
        self.delete_div.grid(in_=self.metadata_div,column=1, row=2, padx=5, columnspan=3, rowspan=2)
        
        self.var_delete_label = StringVar() 
        self.delete_label = Label(self,textvariable=self.var_delete_label, font=("calibri", 12))
        self.var_delete_label.set("Delete Algorithm:")
        self.delete_label.grid(in_=self.delete_div, column=1, row=1,sticky=W, padx=5)
        
        delete_algos = ["ZeroFill","OneFill","TwoFill","ThreeFill","AlterFill"]
        
        self.var_Delete_Algo = StringVar(self)
        self.var_Delete_Algo.set(delete_algos[0])
        self.delete_algo_dropdown = OptionMenu(self, self.var_Delete_Algo, *delete_algos)
        self.delete_algo_dropdown.grid(in_=self.delete_div,column=2, row=1,sticky=E+W, padx=5) 
        
        self.DeleteButt = Button(self, font=("calibri", 12),height = 1, width = 10)
        self.DeleteButt["text"] = "Delete"
        self.DeleteButt.grid(in_=self.delete_div,column=1, row=2, padx=5,sticky=E+W, columnspan=2)
        
        
        
        
        
        self.backButt = Button(self, font=("calibri", 12),height = 1, width = 10)
        self.backButt["text"] = "Back"
        self.backButt.pack(in_=self, padx=10, pady=3)
        

class File_Carver_Frame(Frame):
    def do_something(self):
        #print ("hi there, everyone!")
        start_time = time.time()
        
        tree = self.tree
        for i in tree.get_children():
            tree.delete(i)
        
        choices =[]
        
        if self.jpgvar.get() == 1:
            choices.append("jpg")
        if self.pdfvar.get() == 1:
            choices.append("pdf")
        if self.docxvar.get() == 1:
            choices.append("docx")
        if self.xlsxvar.get() == 1:
            choices.append("xlsx")
        if self.docvar.get() == 1:
            choices.append("doc")
        if self.xlsvar.get() == 1:
            choices.append("xls")
        if self.pngvar.get() == 1:
            choices.append("png")
        if self.zipvar.get() == 1:
            choices.append("zip")
        if self.pptvar.get() == 1:
            choices.append("ppt")
        if self.rarvar.get() == 1:
            choices.append("rar")
        if self.pptxvar.get() == 1:
            choices.append("pptx")
        if self.mpegvar.get() == 1:
            choices.append("mpeg")
        
        
        
        print("CHOSEN FILE TYPES",choices)
        print("NEW FILE TYPES: ",self.choices)
        
        for key in self.choices:
            print ("key: %s , value: %s" % (key, self.choices[key]))
            choices.append(key)
        
        print("ALL FILE TYPES: ",choices)
        
        
        driveLetter = self.variable.get()
        
        
        print(driveLetter)
        
        
        threadcount = int(self.threadEntry.get())
        print('threadcount: ', threadcount)
        carve(choices, driveLetter, threadcount, self, self.choices,self.destination)
        #time.sleep(3)
        self.timeelapsed.set(str(round(time.time() - start_time, 4)))
        
        files = os.listdir(self.destination)
        #print(files)
        
        
        num = 1
        for f in files:
            filepath = 'recovered/'+f
            print(os.stat(filepath))
            
            sizeString = str(os.stat(filepath)[ST_SIZE]) + " bytes"
            dateString = time.asctime(time.localtime(os.stat(filepath)[ST_MTIME]))
            self.tree.insert("" , 2,    text="#"+str(num), values=(f,sizeString,dateString))
            num += 1
        self.bottomText.set("Ready for Scan!")
        
    def finishnewBox(self):
        print('New Filetypes \[T]/')
        #hehexd = eval(input(self.headerEntry.get()))
        #print(hehexd)
        self.choices[self.extensionEntry.get()] = [base64.b16decode(bytes(self.headerEntry.get().upper(), encoding='utf-8')), base64.b16decode(bytes(self.footerEntry.get().upper(), encoding='utf-8'))]
        
        print(self.choices)
        self.newBox.destroy()
    
    def addfiletypes(self):
        self.newBox = Toplevel()
        self.newBox.wm_title("Add Filetype")
        frame = Frame(self.newBox)
        frame.pack(pady=20,padx=60)
        
        self.extensiondiv = LabelFrame(frame, text="Extension" )
        self.extensiondiv.pack()
        
        self.exin = LabelFrame(frame, text="Example input")
        self.exin.pack()
        
        self.exvar = StringVar()
        self.exLabel = Label(self.newBox,textvariable=self.exvar)
        self.exvar.set("FFD9 = b\'\\xFF\\xD9\'")
        self.exLabel.pack(in_=self.exin, padx=15, pady=10)
        
        self.extensionEntry = Entry(self.newBox, bd=2, width=10)
        self.extensionEntry.grid(in_=self.extensiondiv, column=1, row=1, sticky=E+W, pady=10, padx=10)
        self.extensionEntry.insert(0, "")
        
        self.headerdiv = LabelFrame(frame, text="Header" )
        self.headerdiv.pack(fill=BOTH, expand="yes")
        
        self.headerEntry = Entry(self.newBox, bd=2, width=30)
        self.headerEntry.grid(in_=self.headerdiv, column=1, row=1, sticky=E+W, pady=10, padx=10)
        self.headerEntry.insert(0, "")
        
        self.footerdiv = LabelFrame(frame, text="Footer" )
        self.footerdiv.pack(fill=BOTH, expand="yes")
        
        self.footerEntry = Entry(self.newBox, bd=2, width=30)
        self.footerEntry.grid(in_=self.footerdiv, column=1, row=1, sticky=E+W, pady=10, padx=10)
        self.footerEntry.insert(0, "")
        
        newBoxbutt = Button(frame)
        newBoxbutt["text"] = "Submit"
        newBoxbutt["command"] = self.finishnewBox
        newBoxbutt.pack(padx = 15, pady = 5)
        
        self.master.center(self.newBox)
    
    def browsecsv(self):
        Tk().withdraw() 
        self.destination = filedialog.askdirectory()
        print(self.destination)
        
    def createWidgets(self):
        self.choices = {}
        
        self.upperdiv = LabelFrame(self)
        self.upperdiv.pack()
        
        self.filetypes = LabelFrame(self, text="File Types" )
        self.filetypes.grid(in_=self.upperdiv,column=1, row=1,sticky=E+W, padx=15)
        
        self.jpgvar = IntVar(self)
        self.jpg  = Checkbutton(self, text="jpg",  variable=self.jpgvar)
        self.jpg.grid(in_=self.filetypes, sticky=W, column=1, row=1)
        
        self.pdfvar = IntVar(self)
        self.pdf  = Checkbutton(self, text="pdf",  variable=self.pdfvar)
        self.pdf.grid(in_=self.filetypes, sticky=W, column=1, row=2)
        
        self.docxvar = IntVar(self)
        self.docx = Checkbutton(self, text="docx", variable=self.docxvar)
        self.docx.grid(in_=self.filetypes, sticky=W, column=2, row=1)
        
        self.xlsxvar = IntVar(self)
        self.xlsx = Checkbutton(self, text="xlsx", variable=self.xlsxvar)
        self.xlsx.grid(in_=self.filetypes, sticky=W, column=2, row=2)
        
        self.docvar = IntVar(self)
        self.doc  = Checkbutton(self, text="doc",  variable=self.docvar)
        self.doc.grid(in_=self.filetypes, sticky=W, column=3, row=1)
        
        self.xlsvar = IntVar(self)
        self.xls  = Checkbutton(self, text="xls",  variable=self.xlsvar)
        self.xls.grid(in_=self.filetypes, sticky=W, column=3, row=2)
        
        self.pngvar = IntVar(self)
        self.png  = Checkbutton(self, text="png",  variable=self.pngvar)
        self.png.grid(in_=self.filetypes, sticky=W, column=4, row=1)
        
        self.pptxvar = IntVar(self)
        self.pptx = Checkbutton(self, text="pptx",  variable=self.pptxvar)
        self.pptx.grid(in_=self.filetypes, sticky=W, column=4, row=2)
        
        self.zipvar = IntVar(self)
        self.zip  = Checkbutton(self, text="zip",  variable=self.zipvar)
        self.zip.grid(in_=self.filetypes, sticky=W, column=1, row=3)
        
        self.pptvar = IntVar(self)
        self.ppt = Checkbutton(self, text="ppt",  variable=self.pptvar)
        self.ppt.grid(in_=self.filetypes, sticky=W, column=2, row=3)
        
        self.rarvar = IntVar(self)
        self.rar = Checkbutton(self, text="rar",  variable=self.rarvar)
        self.rar.grid(in_=self.filetypes, sticky=W, column=3, row=3)
        
        self.mpegvar = IntVar(self)
        self.mpeg = Checkbutton(self, text="mpeg",  variable=self.mpegvar)
        self.mpeg.grid(in_=self.filetypes, sticky=W, column=4, row=3)
        
        #self.pptxvar = IntVar(self)
        #self.pptx = Checkbutton(self, text="pptx",  variable=self.pptxvar)
        #self.pptx.grid(in_=self.filetypes, sticky=W, column=4, row=3)
        
        self.typebutt = Button(self)
        self.typebutt["text"] = "Add filetype"
        self.typebutt["command"] = self.addfiletypes
        self.typebutt.grid(in_=self.filetypes, column=1, row=4, sticky=E+W, padx=16, pady=5, columnspan=4)
        
        #modifiable file destination
        self.drives = LabelFrame(self, text="Drive")
        self.drives.grid(in_=self.upperdiv,column=2, row=1,sticky=E+W, padx=15, ipady=5, ipadx=5)
        
        #gets the current available drives
#        drives = win32api.GetLogicalDriveStrings()
#        the_drives = drives.split('\000')[:-1]
#        print(the_drives)
        drives = psutil.disk_partitions()
        the_drives = [i[0] for i in drives]
        print(the_drives)
        
        self.topdrives = LabelFrame(self)
        self.topdrives.pack(in_=self.drives)
        
        self.variable = StringVar(self)
        self.variable.set(the_drives[0])
        self.dropdown = OptionMenu(self, self.variable, *the_drives)
        self.dropdown.pack(in_=self.topdrives,side=LEFT)
        
        self.startbutt = Button(self)
        self.startbutt["text"] = "Start"
        self.startbutt["command"] = self.do_something
        self.startbutt.pack(in_=self.drives, expand="yes", ipadx=30)
        
        self.browsebutt = Button(self)
        self.browsebutt["text"] = "..."
        self.browsebutt["command"] = self.browsecsv
        self.browsebutt.pack(in_=self.topdrives,side=LEFT, padx=5)
        
        self.destination = "recovered/"
        
        self.threads = LabelFrame(self, text="Threads")
        self.threads.grid(in_=self.upperdiv,column=3, row=1,sticky=E+W, padx=15)
        #Label(self.master, text="Thread Count:").grid(in_=self.threads, column=1, row=1, sticky=E+W)
        self.threadEntry = Entry(self, bd=2, width=6)
        self.threadEntry.grid(in_=self.threads, column=2, row=1, sticky=E+W, pady=5, padx=5)
        #self.threadEntry.insert(0, "100")
        
        
        self.filesdiv = LabelFrame(self, text="Scanned Files" )
        self.filesdiv.pack(fill=BOTH, expand="yes")
        
        #Label(self, text="FILES").grid(in_=self.filesdiv, column=1,row=1, padx=220, pady=150)
        
        self.tree = ttk.Treeview(self)
        self.tree["columns"]=("Name","Size","Created Date")
        self.tree.column("#0", width=50)
        self.tree.column("Name", width=150)
        self.tree.column("Size", width=150)
        self.tree.column("Created Date", width=150)
        #self.tree.column("Status", width=100)
        self.tree.heading("Name", text="Name")
        self.tree.heading("Size", text="Size")
        self.tree.heading("Created Date", text="Created Date")
        #self.tree.heading("Status", text="Status")
        self.tree.grid(in_=self.filesdiv, column=1,row=1, padx=9, pady=5)
        
        
        
        self.progressbar = LabelFrame(self, text="Progress")
        #self.progressbar.pack(fill=X)
        
        self.loading = Label(self, text="100%")
        #self.loading.grid(in_=self.progressbar, column=1,row=1)
        
        self.timediv = LabelFrame(self, text="Time in Seconds" )
        self.timediv.pack()
        
        self.timeelapsed = StringVar()
        self.timeLabel = Label(self,textvariable=self.timeelapsed)
        self.timeelapsed.set("0:00")
        self.timeLabel.pack(in_=self.timediv)
        
        self.backButt = Button(self, font=("calibri", 12),height = 1, width = 10)
        self.backButt["text"] = "Back"
        self.backButt.pack(in_=self, padx=10, pady=3)
        
        self.bottomText = StringVar(self)
        self.bottomLabel = Label(self.master,textvariable=self.bottomText,bd=1, relief=SUNKEN, anchor=W)
        self.bottomLabel.pack(side=BOTTOM, fill=X)
        self.bottomText.set("Ready for Scan!")
        
    
    
    #master is tk
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack(pady=15) 
        self.createWidgets() #Creates widgets for the Frame
         #sets the minimum frame size
        #self.center(master) #sets the position of the frame to the center of the screen
        master.wm_title("File Recovery Software")
        
if __name__ == "__main__":
#    root = Tk()
#    app = File_Carver_Frame(master=root)
#    app.mainloop()
    app = Application()
    app.mainloop()