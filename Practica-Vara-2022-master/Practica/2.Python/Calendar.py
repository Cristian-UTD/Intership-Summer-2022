#!/usr/bin/python

import tkinter as tk
from tkcalendar import Calendar, DateEntry
from datetime import date
import holidays
import smtplib
from email.message import EmailMessage
from tkinter import messagebox
from datetime import timedelta

window = tk.Tk()

window.title('Concediu')
window.geometry("350x300+10+20")
window['bg'] = "#46197F"
# window.resizable(0, 0)

textNume = tk.Label(window, text="Nume: ", fg='#00A5F1', bg='#46197F')
textNume.place(x=10, y=10)

entryNume = tk.Entry(window, width=42)
entryNume.place(x=60, y=10)

frameCalendar = tk.Frame(window, relief=tk.RAISED, borderwidth=5, bg='#46197F')
frameCalendar.place(x=60, y=50)

Calend = Calendar(master=frameCalendar, selectmode='day')
Calend.pack()

sarbatori = holidays.RO()

frameLiberSar = tk.Frame(window, bg='#46197F')
frameLiberSar.place(x=149, y=257)

textLiberSar = tk.Label(master=frameLiberSar, text="Nr.zile libere: ", fg='#00A5F1', bg='#46197F')
textLiberSar.pack(side=tk.LEFT)

ZileSar = []

textLiberZile = tk.Label(master=frameLiberSar, text="0", fg='#00A5F1', bg='#46197F')
textLiberZile.pack(side=tk.LEFT)


def range_sel(start, stop):
    global dates
    global dates2
    dates = []
    diff = (stop - start).days
    for i in range(diff + 1):
        day = start + timedelta(days=i)
        day.strftime('%Y-%m-%d')
        dates.append(day)
        if dates:
            dates2 = [x.strftime('%Y-%m-%d') for x in dates]
        else:
            print('Nimic')


def creare_event(zile):
    global z
    z = 0
    for y in zile:
        ySar = y in sarbatori
        yWeek = y.weekday()
        if (yWeek == 5 or yWeek == 6):
            pass
        else:
            if (ySar == False):
                z = z + 1
                Calend.calevent_create(y, 'Concediu', 'reminder')
            else:
                Calend.calevent_create(y, 'Concediu', 'reminder')
    textLiberZile = tk.Label(master=frameLiberSar, text=str(z), fg='#00A5F1', bg='#46197F')
    textLiberZile.pack(side=tk.LEFT)
    ZileSar.append(textLiberZile)

def selection():
    textLiberZile.destroy()
    for zile in ZileSar:
        zile.destroy()
    global data1
    Calend.calevent_remove()
    data1 = Calend.selection_get()
    dataVer = data1 in sarbatori
    dataWeek = data1.weekday()
    if (dataVer == False):
        if (dataWeek == 5 or dataWeek == 6):
            tk.messagebox.showinfo("Zi libera", "Este weekend")
            Calend.selection_clear()
            Calend.calevent_remove()
            Calend.bind("<<CalendarSelected>>", lambda x: selection())
        else:
            Calend.calevent_create(data1, 'Concediu', 'reminder')
            Calend.bind("<<CalendarSelected>>", lambda x: selection2())
            print("Ziua1 " + str(data1))
    else:
        Calend.calevent_remove()
        Calend.selection_clear()
        Calend.bind("<<CalendarSelected>>", lambda x: selection())
        tk.messagebox.showinfo("Zi libera", "Este zi de sarbatoare")
        print("Este zi de sarbatoare, pune alta data")


def selection2():
    global data2
    data2 = Calend.selection_get()
    dataVer2 = data2 in sarbatori
    dataWeek2 = data2.weekday()
    if (dataVer2 == False):
        if (dataWeek2 == 5 or dataWeek2 == 6):
            tk.messagebox.showinfo("Zi libera", "Este weekend")
            Calend.calevent_remove()
            selection()
        else:
            if (data1 < data2):
                range_sel(data1, data2)
                creare_event(dates)
                Calend.bind("<<CalendarSelected>>", lambda x: selection())
                print("Ziua2 " + str(data2))
            else:
                Calend.calevent_remove()
                selection()
    else:
        if (data1 < data2):
            range_sel(data1, data2)
            creare_event(dates)
            Calend.bind("<<CalendarSelected>>", lambda x: selection())
            print("Ziua2 " + str(data2))
        else:
            Calend.calevent_remove()
            selection()


def email():
    gmail_user = 'cinevatest2@gmail.com'
    gmail_password = 'kjgdsqeybxkxjqdn'

    msg = EmailMessage()
    if (z >= 1):
        msg.set_content(f"""Bună ziua,

   Aș dori dacă se poate să primesc pentru perioada {data1} - {data2} ({z} zile) concediu de odihnă.


   Vă mulțumesc.""")
    else:
        msg.set_content(f"""Bună ziua,

   Aș dori dacă se poate să primesc pentru ziua {data1} (1 zi) concediu de odihnă.


   Vă mulțumesc.""")

    msg['From'] = "cinevatest2@gmail.com"
    msg['To'] = "barnacristian90@gmail.com"
    msg['Subject'] = f'Concediu {Nume}'

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(gmail_user, gmail_password)
        server.send_message(msg)
        server.quit()
        tk.messagebox.showinfo("Succes", "Email-ul a fost trimis cu succes")
        print("Email sent successfully!")
    except Exception as ex:
        tk.messagebox.showerror("Eroare", "Nu se poate trimite email-ul")
        print("Something went wrong….", ex)


def send():
    print(data1, "-", data2)
    global Nume
    Nume = entryNume.get()
    if (Nume != ""):
        print("Merge")
        print(z)
        email()
    else:
        tk.messagebox.showerror("Eroare", "Numele nu a fost introdus")


def clear():
    for zile in ZileSar:
        zile.destroy()
    Calend.selection_clear()
    entryNume.delete(0, "end")
    Calend.calevent_remove()
    data1 = 0
    data2 = 0
    Nume = ""
    print(data1)
    print(data2)
    print(Nume)


Calend.bind("<<CalendarSelected>>", lambda x: selection())

butonClear = tk.Button(window, text="Clear", bg='#5D2EB9', fg='#00A5F1', command=clear)
butonClear.place(x=60, y=255)

butonSend = tk.Button(window, text="Send", bg='#5D2EB9', fg='#00A5F1', command=send)
butonSend.place(x=284, y=255)

window.mainloop()
