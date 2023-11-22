import sqlite3
import tkinter
from tkinter import messagebox


def login():
    global islogin, cuser, cnt, count
    user = txt_user.get()
    pas = txt_pass.get()
    sql = '''SELECT * FROM students WHERE user=? AND pass=? '''
    result = cnt.execute(sql, (user, pas))
    row = result.fetchall()
    if len(row) > 0:
        lbl_msg.configure(text="welcome to your account.", fg="green")
        islogin = True
        cuser = user
        win.destroy()
        show_courses()
    else:
        lbl_msg.configure(text="wrong username or password", fg="red")
        count -= 1
        if count == 0:
            btn_login.configure(state="disabled")


def validation(user, pas):
    global cnt
    sql = '''SELECT * FROM students WHERE pass=? '''
    result = cnt.execute(sql, (pas,))
    row = result.fetchall()
    if user == "" or pas == "":
        lbl_msg.configure(text="Please fill the textbox!", fg="red")
        return False
    if len(row) == 1:
        lbl_msg.configure(text="username already existed!", fg="red")
        return False
    if len(pas) < 8:
        lbl_msg.configure(text="The length of the password must be 8", fg="red")
        return False
    return True


def submit():
    global cnt
    user = txt_user.get()
    pas = txt_pass.get()
    result = validation(user, pas)
    if result is False:
        return
    sql = '''INSERT INTO students (user,pass)
        VALUES(?,?)'''
    cnt.execute(sql, (user, pas))
    cnt.commit()
    lbl_msg.configure(text="submit done", fg="green")


# ---------login WINDOW----------
islogin = False
count = 3
cuser = ""
cnt = sqlite3.connect("students.db")
win = tkinter.Tk()
win.title("login")
win.geometry("300x200")
# -------------------------
lbl_user = tkinter.Label(win, text="username:")
lbl_user.pack()
txt_user = tkinter.Entry(win)
txt_user.pack()

lbl_pass = tkinter.Label(win, text="password:")
lbl_pass.pack()
txt_pass = tkinter.Entry(win)
txt_pass.pack()

btn_login = tkinter.Button(win, text="login", command=login)
btn_login.pack()

btn_submit = tkinter.Button(win, text="submit", command=submit)
btn_submit.pack()

lbl_msg = tkinter.Label(win, text="")
lbl_msg.pack()

# -------------------unit selection window--------------
def add_new_item(txt_unit,lbl_msg2,unit,cuser):
    sql = '''SELECT dars FROM students WHERE user=? '''
    result = cnt.execute(sql,(cuser,))
    rows = result.fetchone()
    if rows[0] is None:
        sql = '''UPDATE students SET dars=? WHERE user=?'''
        cnt.execute(sql, (unit+",", cuser))
        cnt.commit()
        lbl_msg2.configure(text="Your unit has been successfully selected.", fg="green")
        txt_unit.delete(0, "end")
    else:
        sql = '''UPDATE students SET dars=dars ||? WHERE user=?'''
        cnt.execute(sql, (unit+",", cuser))
        cnt.commit()
        lbl_msg2.configure(text="Your unit has been successfully selected.", fg="green")
        txt_unit.delete(0, "end")
        

def choose_unit(txt_unit, lbl_msg2):
    global cnt, cuser
    unit = txt_unit.get()
    sql = '''SELECT * FROM units WHERE unitname=? '''
    result = cnt.execute(sql, (unit,))
    rows = result.fetchall()
    sql = '''SELECT * FROM students WHERE user=? AND dars LIKE ? '''
    result2 = cnt.execute(sql,(cuser,'%'+unit+'%'))
    rows2 = result2.fetchall()
    if unit == "":
        lbl_msg2.configure(text="Please fill the textbox!", fg="red")
        return
    if len(rows2) > 0:
        lbl_msg2.configure(text="You selected this unit before!", fg="red")
        return
    if len(rows) == 0:
        lbl_msg2.configure(text="unit name is wrong!", fg="red")
        return
    else:
        add_new_item(txt_unit,lbl_msg2,unit,cuser)
        
       
def show_units(lbl_msg2, btn_unit):
    sql = '''SELECT dars FROM students WHERE user=? '''
    result = cnt.execute(sql, (cuser,))
    rows = result.fetchone()
    if rows[0] is None:
        lbl_msg2.configure(text="You have no units!", fg="red")
    else:
        for item in rows:
            items = (f"your units: {item}")
        confirm = messagebox.askyesno(message="this is "+str(items)+"\ndo you want to add more?")
        if confirm:
            choose_unit()
        elif not confirm:
            lbl_msg2.configure(text="Unit selection is done", fg="green")
            btn_unit.configure(state="disabled")


def show_courses():
    global cnt, cuser, new_win
    new_win = tkinter.Tk()
    new_win.title("select units")
    new_win.geometry("400x300")

    lbl_unit = tkinter.Label(new_win, text="Write the name of the unit:")
    lbl_unit.pack()
    txt_unit = tkinter.Entry(new_win)
    txt_unit.pack()

    btn_unit = tkinter.Button(new_win, text="select unit:", command=lambda:choose_unit(txt_unit,lbl_msg2))
    btn_unit.pack()

    btn_units = tkinter.Button(new_win, text="show selected units:", command=lambda:show_units(lbl_msg2,btn_unit))
    btn_units.pack()

    lbl_msg2 = tkinter.Label(new_win, text="")
    lbl_msg2.pack()

    lbl_msg = tkinter.Label(new_win, text="1.Math1(3)\n""2.Math2(3)\n""3.English(2)\n""4.Physics(2)\n""5.Programming(2)\n""6.Datastructure(2)\n")
    lbl_msg.pack()

    new_win.mainloop()

win.mainloop()