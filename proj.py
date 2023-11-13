from tkinter import *
import tkinter as tk
import tkinter.messagebox as mbox
from PIL import ImageTk, Image
import time
import psutil
import socket
import sqlite3
import os  # Import the os module

conn = sqlite3.connect('network_usage.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS network_usage
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   usage REAL)''')
conn.commit()

window1 = tk.Tk()
window1.title("Network Usage Tracker")
window1.geometry('1000x700')

start1 = tk.Label(text="NETWORK USAGE\nTRACKER", font=("Arial", 55,"underline"), fg="magenta")
start1.place(x=150, y=10)

def start_fun():
    window1.destroy()

startb = Button(window1, text="START", command=start_fun, font=("Arial", 25), bg="orange", fg="blue", borderwidth=3, relief="raised")
startb.place(x=130, y=590)

# For the path to the image, use os.path.join to construct the full path
image_folder = r'C:\Users\vijay\c++\Python\Images'
image_filename = 'front.png'
image_path = os.path.join(image_folder, image_filename)

# Load the image using PIL
img1 = ImageTk.PhotoImage(Image.open(image_path))
panel = tk.Label(window1, image=img1)
panel.place(x=320, y=200)

def exit_win():
    if mbox.askokcancel("Exit", "Do you want to exit?"):
        window1.destroy()

exitb = Button(window1, text="EXIT", command=exit_win, font=("Arial", 25), bg="red", fg="blue", borderwidth=3, relief="raised")
exitb.place(x=730, y=590)
window1.protocol("WM_DELETE_WINDOW", exit_win)
window1.mainloop()

window = Tk()
window.title("Network Usage Tracker")
window.geometry("1000x700")

top1 = Label(window, text="NETWORK USAGE\nTRACKER", font=("Arial", 50, 'underline'), fg="magenta")
top1.place(x=190, y=10)

top1 = Label(window, text="MAX LIMIT  :  1 MB/sec", font=("Arial", 50), fg="green")
top1.place(x=130, y=180)

path_text = Text(window, height=1, width=24, font=("Arial", 50), bg="white", fg="blue", borderwidth=2, relief="solid")
path_text.place(x=50, y=300)

top1 = Label(window, text="Connection Status :", font=("Arial", 50), fg="green")
top1.place(x=200, y=450)

l2 = Label(window, fg='blue', font=("Arial", 30))
l2.place(x=200, y=530)

def convert_to_gbit(value):
    return value/1024./1024./1024.*8

old_value = 0
update_running = True  # Flag to control updating

def stop_update():
    global update_running
    update_running = False

def start_update():
    global update_running
    update_running = True
    update_label()

stop_button = Button(window, text="STOP", command=stop_update, font=("Arial", 20), bg="red", fg="blue", borderwidth=3, relief="raised")
stop_button.place(x=300, y=625)  # Adjusted the x-coordinate and spacing

start_button = Button(window, text="START", command=start_update, font=("Arial", 20), bg="green", fg="blue", borderwidth=3, relief="raised")
start_button.place(x=500, y=625)  # Adjusted the x-coordinate and spacing

def update_label():
    global old_value, update_running
    if update_running:
        new_value = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
        usage = new_value - old_value

        cursor.execute("INSERT INTO network_usage (usage) VALUES (?)", (usage,))
        conn.commit()

        cursor.execute("SELECT * FROM network_usage")
        rows = cursor.fetchall()

        display_records = "\n".join([f"Record {row[0]}: Usage {row[1]} bytes" for row in rows[-5:]])
        print("Usage Records:")
        print(display_records)

        IPaddress = socket.gethostbyname(socket.gethostname())
        if IPaddress == "127.0.0.1":
            l2.configure(text="No internet, your localhost is\n" + IPaddress)
        else:
            l2.configure(text="Connected, with the IP address\n" + IPaddress)

        if(new_value - old_value > 1000000):
            mbox.showinfo("Exceed Status", "Max Limit Usage Exceeded.")

        old_value = new_value

        path_text.delete("1.0", "end")
        path_text.insert(END, "Usage : " + str(usage) + " bytes/sec")

    window.after(1000, update_label)  # Schedule the next update after 1 second

update_label()

def exit_win():
    if mbox.askokcancel("Exit", "Do you want to exit?"):
        window.destroy()

window.protocol("WM_DELETE_WINDOW", exit_win)
window.mainloop()