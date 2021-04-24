#menambahkan file dan library yang diperlukan
from pynput.mouse import Button, Controller
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import pyautogui
import serial
import glob
import sys

#Inisialiasi Windows Aplikasi
app = tk.Tk()
app.title("TA")
app.resizable(0,0)
app.configure(bg='white')
app.iconbitmap('icon.ico')
status = tk.StringVar()
status.set("Informatics Engineering")

#Fungsi Penerima Data
def receivedata():
    data = ser.readline()
        
    x = str(data)
    y = x.split("'")
    z = y[1].split ('=')
    x1 = z[1].split(',')
    sz = len(x1[2]) - 4
    a = x1[0]
    b = x1[1]
    c = x1[2] 
    c = c[0:len(c)-2]
    d = x1[3]
    e = x1[4]
    e = e[0:len(e)-4]
      
    return data,a,b,c,d,e

#Fungsi untuk mendapatkan daftar port serial
def sPorts():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

#TKinter Functions
def callbackFunc(event):
     print(SP.get())

#Fungsi untuk menjalin komunikasi serial
def hubung():
    global ser
    ser = serial.Serial(SP.get(), 115200, timeout=1)
    try:
        if ser.isOpen():
            messagebox.showinfo("Koneksi", "Sambungan Telah Terjalin")
        elif ser.open():
            messagebox.showinfo("Koneksi", "Sambungan Berhasil")
    except SerialException:
        messagebox.showerror("Koneksi", "Sambungan Gagal")        

#Fungsi untuk memperbarui daftar port serial
def refresh():
    SP["value"]=sPorts()

#Fungsi Untuk Mengatur Titik Nol / Zero Point
def zero():
    try:
        a,b,c,d,e,f = receivedata()
        x0.set(c)
        y0.set(d)
        status.set("Zero Point Is Set.")
        labelBot["text"] = status.get()
        labelx["text"] = 'X0=' + str(x0.get()) + ' | X1=' + str(x1.get())
        labely["text"] = 'Y0=' + str(y0.get()) + ' | Y1=' + str(y1.get())
    except:
        messagebox.showerror("Koneksi", "Silahkan Restart Alat dan Program")

#Fungsi Menjalankan Program
def start():
    status.set("Start")
    labelBot["text"] = "Running ..."
    mouse.position = (x/2, y/2)

#Fungsi Menghentikan Program Untuk Sementara
def pause():
    status.set("Paused")
    labelBot["text"] = status.get()

#Fungsi Untuk Menghentikan Program
def stop():
    ser.close()
    x0.set(0)
    y0.set(0)
    x1.set(0)
    y1.set(0)
    status.set("Stopped")
    labelBot["text"] = status.get()

#Inisialisasi Variabel
ser = ""
x, y = pyautogui.size()
mouse = Controller()

prevState = tk.IntVar()
prevState.set(0)
prevStateR = tk.IntVar()
prevStateR.set(0)

#Inisialisasi variabel tkinter
x0 = tk.DoubleVar()
y0 = tk.DoubleVar()
x1 = tk.DoubleVar()
y1 = tk.DoubleVar()

#Label
labelTop = tk.Label(app, text = "Inertial Mouse", bg='white')
labelTop.grid(row=0, columnspan=2)

labelBot = tk.Label(app, text = status.get(), bg='white')
labelBot.grid(row=6, columnspan=2, pady=4)

labelx = tk.Label(app, text = "", bg='white')
labelx.grid(row=7, columnspan=2, pady=2)

labely = tk.Label(app, text = "", bg='white')
labely.grid(row=8, columnspan=2, pady=2)

#Combobox daftar serial port
SP = ttk.Combobox(app, values=sPorts(), state="readonly")
SP.grid(columnspan=2, row=1, padx=6)
SP.current(0)

#Tampilan Tombol
refresher = tk.Button(app, text="Refresh", bg="white", command=refresh, width=8)
refresher.grid(column=0, row=3, pady=2)

Conn = tk.Button(app, text="Connect", bg="white", command=hubung, width=8)
Conn.grid(column=1, row=3, pady=2)

Atur = tk.Button(app, text="Set", width=8, fg="white", bg="#004080", command=zero)
Atur.grid(column=0, row=4, pady=2)

Mulai = tk.Button(app, text="Start", width=8, fg="white", bg="#80ff00", command=start)
Mulai.grid(column=1, row=4, pady=2)

Jeda = tk.Button(app, text="Pause", width=8, fg="white", bg="#ff8040", command=pause)
Jeda.grid(column=0, row=5, pady=2)

Berhenti = tk.Button(app, text="Stop", width=8, fg="white", bg="#800000", command=stop)
Berhenti.grid(column=1, row=5, pady=2)

#Fungsi Simulasi Tetikus
def mousing():  
    try:    
        data,a,b,c,cl,cr = receivedata()
               
        h = float(x0.get()) - float(b)
        v = float(y0.get()) - float(c)
        x1.set(b)
        y1.set(c)
        
        if (status.get() == "Start"):
        
            #Pergerakan Kursor X
            if (float(h) < -20):
                mouse.move(5, 0)
            elif (float(h) > 20): 
                mouse.move(-5, 0)
                
            elif (float(h) < -16):
                mouse.move(3, 0)
            elif (float(h) > 16): 
                mouse.move(-3, 0)
                
            elif (float(h) < -12):
                mouse.move(1, 0)
            elif (float(h) > 12): 
                mouse.move(-1, 0)
            
            #Pergerakan Kursor Y
            if (float(v) < -16):
                mouse.move(0, 5)
            elif (float(v) > 16): 
                mouse.move(0, -5)
                
            elif (float(v) < -12):
                mouse.move(0, 3)
            elif (float(v) > 12): 
                mouse.move(0, -3)
                
            elif (float(v) < -8):
                mouse.move(0, 1)
            elif (float(v) > 8): 
                mouse.move(0, -1)
            
        #Click
        if (cl == '1' and prevState.get() == 0):
            mouse.click(Button.left, 1)
            prevState.set(1)                
        elif (cl == '0' and prevState.get() == 1):
            prevState.set(0)
        
        if (cr == '1' and prevStateR.get() == 0):
            mouse.click(Button.right, 1)
            prevStateR.set(1)                
        elif (cr == '0' and prevStateR.get() == 1):
            prevStateR.set(0)
    
    except:
        pass  
    app.after(1, mousing)

#Menampilkan data pada waktu yang sebenarnya
def realTimeData():
    labelx["text"] = 'X0=' + str(x0.get()) + ' | X1=' + str(x1.get())
    labely["text"] = 'Y0=' + str(y0.get()) + ' | Y1=' + str(y1.get())
    app.after(1, realTimeData)

#Menjalankan Program
realTimeData()
mousing()
app.mainloop()
