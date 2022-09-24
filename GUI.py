from tkinter import *
from tkinter import ttk
import database
import datetime as dt
import time
from PIL import ImageTk, Image
import re
from tkinter import messagebox
from sqlite3 import *
import smtplib

win = Tk()
win.configure(background='lavender')
win.geometry("1900x1000+0+0")
win.title("REGISTRATION FORM")
my_image = ImageTk.PhotoImage(Image.open("wp8324853.jpg"))
my_label = Label(image=my_image)
my_label.place(x=00, y=00)

regex = '^[a-z0-9]+[._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
gender = IntVar()
agree = IntVar()


def on_press():
        check()
        agree_button_value = agree.get()

        email_id = email.get()
        first_name = fname.get()
        last_name = lname.get()
        gender_value = ""
        if gender.get() == 1:
            gender_value = 'male'
        elif gender.get() == 2:
            gender_value = 'female'
        elif gender.get() == 3:
            gender_value = 'others'
        age_value = age.get()
        contact_value = contact.get()
        event_value = my_combo.get()
        index = interests.index(event_value)
        category_value = time_combo.get()
        time1_value = time1
        time2_value = label_date.cget("text")
        if re.search(regex, email_id):
            valid = Label(win, text="")
            valid.place(x=1200, y=200)
            if agree_button_value == 1:
                label11.config(text='')
                messagebox.showinfo('Completed', 'your entry is noted')
            else:
                label11.config(text='please agree terms and condition', fg='red')

            database.insert(email_id, first_name, last_name, gender_value, age_value, event_value, category_value, time1_value, time2_value, contact_value)
            # creates SMTP session
            s = smtplib.SMTP('smtp.gmail.com', 587)
            # start TLS for security
            s.starttls()
            # Authentication
            s.login("EMAIL ID", "PASSWORD")  #### ("EMAIL ID","PASSWORD")
            # message to be sent
            message = f"Hello {first_name} {last_name}\nThanks for participating in our event.\nYour registration on" \
                      f" {time2_value} {time1_value} for {event_value} {category_value} has been confirmed. Your {event_value} {category_value} will be held on" \
                      f" {timing[index]}\n" \
                      f"Venue: {venue[index]}\nThanks,\nORION PAXX"
            # sending the mail
            s.sendmail("EMAIL ID", email_id, message)  #### EMAIL ID
            # terminating the session
            s.quit()
            valid = Label(win, text="Valid  ", fg='green')
            valid.place(x=1200, y=200)


        else:
            invalid = Label(win, text="Invalid", fg='red')
            invalid.place(x=1200, y=200)


def tick():
    global time1
    # get the current local time from the PC
    time2 = time.strftime('%H:%M:%S')
    # if time string has changed, update it
    if time2 != time1:
        time1 = time2
        label_time.config(text=time2)
    # calls itself every 200 milliseconds
    # to update the time display as needed
    # could use >200 ms, but display gets jerky
    label_time.after(200, tick)
    return time2

def data_display():
    connection = connect('base.db')  # file open
    cursor = connection.cursor()  # putting a cursor
    # insert update delete
    cursor.execute('SELECT * FROM userInfo')
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        entry_board.insert(END, row)
        entry_board.insert(END, '\n')

def check():
   for entry in fname, lname, email, contact, age, my_combo, time_combo:
       if entry.get() == '':
           return messagebox.showwarning('Warning', 'Please answer every question')

def reset():
    fname.delete(0, 'end')
    lname.delete(0, 'end')
    contact.delete(0, 'end')
    email.delete(0, 'end')
    age.delete(0, 'end')
    my_combo.delete(0, 'end')
    time_combo.delete(0, 'end')
    agree.set(0)
    gender.set(1)
    label11.config(text='')
    email.config(text='')
    entry_board.delete(1.0,'end')

label10 = Label(win, text="REGISTRATION FORM", font=('Calibre', 24), fg='red', bg='lavender')
label10.pack(pady=30)

label2 = Label(win, text="First name", fg='blue', bg='lavender')
label2.place(x=420, y=100)
fname = Entry(win, width=30)
fname.place(x=600, y=100)

label3 = Label(win, text="Last name", fg='blue', bg='lavender')
label3.place(x=900, y=100)
lname = Entry(win, width=30,)
lname.place(x=1000, y=100)

label = Label(win, text="Email id", fg='blue', bg='lavender')
label.place(x=900, y=200)
email = Entry(win, width=30)
email.place(x=1000, y=200)

label9 = Label(win, text="Contact No", fg='blue', bg='lavender')
label9.place(x=420, y=200)
contact = Entry(win, width=30)
contact.place(x=600, y=200)


label4 = Label(win, text="Age", fg='blue', bg='lavender')
label4.place(x=420, y=150)
age = Entry(win, width=30)
age.place(x=600, y=150)


label6 = Label(win, text='Gender', fg='blue', bg='lavender')
label6.place(x=900, y=150)
male_gender = Radiobutton(win, text='Male', variable=gender, value=1, fg='blue', bg='lavender')
male_gender.place(x=1000, y=150)
female_gender = Radiobutton(win, text='Female', variable=gender, value=2, fg='blue', bg='lavender')
female_gender.place(x=1070, y=150)
other_gender = Radiobutton(win, text='Other', variable=gender, value=3, fg='blue', bg='lavender')
other_gender.place(x=1145, y=150)

#creating a list of games
interests = [
    'valorant',
    'minecraft',
    'rocket league'
]

#creating a list of category
valorant_lobby = [
    'spikerush',
    'unrated',
    'compititive'
]

minecraft_lobby = [
    'pvp',
    'speedrun',
    'challengers'
]

rocketleague_lobby = [
    'rated',
    'casual',
    'compititive'

]

timing = [
    '2-03-2021, 2:00pm to 4:00pm',
    '4-03-2021, 2:00pm to 4:00pm',
    '6-03-2021, 2:00pm to 4:00pm'
]

venue = [
    '10th floor DMCE',
    '11th floor DMCE',
    '5th floor DMCE'
]

label7 = Label(win, text='You are interested in :', fg='blue', bg='lavender')
label7.place(x=420, y=250)

def pick_category(e):
   if my_combo.get() == 'valorant':
    time_combo.config(value=valorant_lobby)
    time_combo.current(0)

   if my_combo.get() == 'minecraft':
       time_combo.config(value=minecraft_lobby)
       time_combo.current(0)

   if my_combo.get() == 'rocket league':
       time_combo.config(value=rocketleague_lobby )
       time_combo.current(0)

my_combo = ttk.Combobox(win,  width=30, value=interests)
#my_combo.current(0)
my_combo.place(x=600,y=250)
#bind
my_combo.bind("<<ComboboxSelected>>", pick_category)

label8 = Label(win, text='Category:',fg='blue', bg='lavender')
label8.place(x=900, y=250)
time_combo = ttk.Combobox(win, width=30, value=[""])
time_combo.place(x=1000,y=250)

agree_button = Checkbutton(win, text='I agree with terms and conditions', variable=agree, onvalue=1, offvalue=0, bg='lavender')
agree_button.place(x=700, y=305)
label11=Label(win, text='', fg='white')
label11.place(x=1000, y=305)

login_button = Button(win, text='Sign Up', width=30, pady=5, fg='black', bg='white',  font=("Calibre", 10, 'bold'), command=on_press)
login_button.place(x=670, y=350)

data_button=Button(win, text='view all entries', width=30, pady=5, fg='black', bg='white', command=data_display, font=("Calibre", 10, 'bold'))
data_button.place(x=670, y=400)
entry_board=Text(win, width=1, height=1)
entry_board.place(x=0, y=500, width=1000, height=600)

clr_button=Button(win, text='clear all', width=30, pady=5, fg='black', bg='white', command=reset, font=("Calibre", 10, 'bold'))
clr_button.place(x=670, y=440)

label_date = Label(win, text=f"{dt.date.today():%d %B %Y}", fg="blue", font=("Calibre", 14), bg='lavender')
label_date.place(x=20, y=400)
time1 = ''
label_time = Label(win, font=('Calibre', 14), fg='blue', bg='lavender')
label_time.place(x=185, y=400)
time2 = tick()

gender.set(1)
win.mainloop()