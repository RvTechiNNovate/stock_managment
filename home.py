from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msg
import dbconnect as db
from pymysql import *
from tkinter import simpledialog as sd
from smtplib import *
from email.message import *

root=Tk()
bgclr='powder blue'
root.state('zoomed')
root.update()
root.configure(bg=bgclr)
root.resizable(width=False,height=False)
lbl_head=Label(root,bg=bgclr,text='Stock Management',font=('verdna',45,'bold'))
lbl_head.pack(side='top',anchor='c')


def reset(e1,e2,cb,e3=None,e4=None):
    u=e1.get()
    p=e2.get()
    e1.delete(0,len(u))
    e2.delete(0,len(p))
    if(cb!=None):
        cb.current(0)
    if(e3!=None and e4!=None):
        e=e3.get()
        m=e4.get()
        e3.delete(0,len(e))
        e4.delete(0,len(m))
def login(frm,e1,e2,cb):
    u=e1.get()
    p=e2.get()
    ut=cb.get()
    if(len(u)==0 or len(p)==0):
        msg.showwarning('Validation Problem','Please fill all fields')
    elif(ut=='--Select--'):
        msg.showwarning('Validation Problem','Please select user type')
    else:
        if(ut=='Admin'):
            if(u=='Admin' and p=='Admin'):
                msg.showinfo('Login','Welcome Admin')
                frm.destroy()
                welcomeAdmin()
            else:
                msg.showerror('Login Failed','Invalid username or password')
        elif(ut=='Salesman'):
            con=db.getCon()
            cur=con.cursor()
            cur.execute("select * from salesman where s_id=%s and s_pass=%s",(u,p))
            row=cur.fetchone()
            if(row==None):
                msg.showerror('Login Failed','Invalid username or password')
            else:
                msg.showinfo('Login',f'Welcome:{row[2]}')
                frm.destroy()
                welcomeUser(row)
            con.close()    
def home():
    login_frm=Frame(root,bg=bgclr)
    login_frm.place(x=0,y=100,width=root.winfo_width(),height=root.winfo_height())

    lbl_user=Label(login_frm,bg=bgclr,font=('',20,''),fg='blue',text='Username')
    lbl_user.place(x=300,y=100)

    lbl_pass=Label(login_frm,bg=bgclr,font=('',20,''),fg='blue',text='Password')
    lbl_pass.place(x=300,y=150)

    ent_user=Entry(login_frm,bd=5,font=('',15,''))
    ent_user.focus()
    ent_user.place(x=490,y=105)

    ent_pass=Entry(login_frm,show='*',bd=5,font=('',15,'bold'))
    ent_pass.place(x=490,y=155)

    lbl_usertype=Label(login_frm,bg=bgclr,font=('',20,''),fg='blue',text='User type')
    lbl_usertype.place(x=300,y=205)

    cb_usertype=ttk.Combobox(login_frm,font=('',14,''),values=['--Select--','Admin','Salesman'])
    cb_usertype.place(x=490,y=205)
    cb_usertype.current(0)

    lgn_btn=Button(login_frm,text='login',command=lambda:login(login_frm,ent_user,ent_pass,cb_usertype),bd=5,font=('',12,'bold'))
    lgn_btn.place(x=500,y=305)

    rst_btn=Button(login_frm,command=lambda:reset(ent_user,ent_pass,cb_usertype),text='reset',bd=5,font=('',12,'bold'))
    rst_btn.place(x=590,y=305)

def logout(frm):
    frm.destroy()
    home()

def back(frm):
    frm.destroy()
    welcomeAdmin()

def backUser(frm,row):
    frm.destroy()
    welcomeUser(row)

def delSal(frm):
    sid=sd.askstring("Delete Account","Enter Salesman id")
    sid=int(sid)
    con=db.getCon()
    cur=con.cursor()
    cur.execute("delete from salesman where s_id=%s",(sid,))
    con.commit()
    if(cur.rowcount==1):
       msg.showinfo('Delete Account','Account Deleted')
    else:
        msg.showwarning('Delete Account','Account not found')
    con.close()  

def searchPro(frm):
    p_name=sd.askstring('','Enter product name:')
    con=db.getCon()
    cur=con.cursor()
    cur.execute('select * from product where p_name=%s',(p_name,))
    row=cur.fetchone()
    if(row!=None):
        msg.showinfo('Product Found',str(row))
    else:
        msg.showwarning('','Product Not found')
    con.close()
def viewSal(frm):
    con=db.getCon()
    cur=con.cursor()
    cur.execute('select * from salesman')
    msg1=''
    for row in cur:
        for i in row:
            msg1=msg1+str(i)+'\t'
        msg1=msg1+'\n'    
    s=cur.fetchall()    
    msg.showinfo('All Salesman',msg1)
    con.close()
def welcomeAdmin():
    login_frm=Frame(root,bg=bgclr)
    login_frm.place(x=0,y=100,width=root.winfo_width(),height=root.winfo_height())

    lbl_user=Label(login_frm,bg=bgclr,font=('',15,''),fg='green',text='Welcome:Admin')
    lbl_user.place(x=10,y=100)

    logout_btn=Button(login_frm,width=15,command=lambda:logout(login_frm),font=('',12,'bold'),text='Logout',bd=5)
    logout_btn.place(relx=.85,y=100)

    addPro_btn=Button(login_frm,width=15,command=lambda:addPro(login_frm),font=('',12,'bold'),text='Add Product',bd=5)
    addPro_btn.place(x=450,y=170)

    searchPro_btn=Button(login_frm,width=15,command=lambda:searchPro(login_frm),font=('',12,'bold'),text='Search Product',bd=5)
    searchPro_btn.place(x=700,y=170)

    addSal_btn=Button(login_frm,width=15,command=lambda:addSal(login_frm),font=('',12,'bold'),text='Add Salesman',bd=5)
    addSal_btn.place(x=450,y=270)
    
    viewSal_btn=Button(login_frm,width=15,command=lambda:viewSal(login_frm),font=('',12,'bold'),text='View Salesman',bd=5)
    viewSal_btn.place(x=700,y=270)

    delSal_btn=Button(login_frm,width=15,command=lambda:delSal(login_frm),font=('',12,'bold'),text='Delete Salesman',bd=5)
    delSal_btn.place(x=550,y=370)


def changePass(sid):
    newpass=sd.askstring('Change Password','Enter new password:')
    con=db.getCon()
    cur=con.cursor()
    cur.execute('update salesman set s_pass=%s where s_id=%s',(newpass,sid))
    con.commit()
    con.close()
    msg.showinfo('Success','Password changed successfully')
def welcomeUser(row):
    login_frm=Frame(root,bg=bgclr)
    login_frm.place(x=0,y=100,width=root.winfo_width(),height=root.winfo_height())

    lbl_user=Label(login_frm,bg=bgclr,font=('',15,''),fg='green',text=f'Welcome:{row[2]}')
    lbl_user.place(x=10,y=100)

    logout_btn=Button(login_frm,width=15,command=lambda:logout(login_frm),font=('',12,'bold'),text='Logout',bd=5)
    logout_btn.place(relx=.85,y=100)

    cp_btn=Button(login_frm,width=15,command=lambda:changePass(row[0]),font=('',12,'bold'),text='Change Password',bd=5)
    cp_btn.place(x=450,y=170)

    searchPro_btn=Button(login_frm,width=15,command=lambda:searchPro(login_frm),font=('',12,'bold'),text='Search Product',bd=5)
    searchPro_btn.place(x=700,y=170)

    bill_btn=Button(login_frm,width=15,command=lambda:billing(login_frm,row),font=('',12,'bold'),text='Billing',bd=5)
    bill_btn.place(x=500,y=270)
    


def addSalDb(frm,e1,e2,e3,e4):
    con=db.getCon()
    cur=con.cursor()
    cur.execute("select max(s_id) from salesman")
    sid=cur.fetchone()
    if(sid[0]!=None):
        newid=sid[0]+1
    else:
        newid=1
    cur.execute("insert into salesman values(%s,%s,%s,%s,%s)",(newid,e2.get(),e1.get(),e4.get(),e3.get()))
    con.commit()
    con.close()
    
    msg.showinfo('New Account',f'Account Created with id:{newid}')

    server=SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login('ducatproject.stock2020@gmail.com','Ducat@2020')

    msgg=EmailMessage()
    list=[e3.get()]
    msgg['TO']=list
    msgg['SUBJECT']='New Account in Stock mgt'
    msgg['FROM']='ducatproject.stock2020@gmail.com'
    msgg.set_content(f'Hello Dear,\n Your Salesman id={newid} and Password={e2.get()}')

    server.send_message(msgg)
    print('mail gaya')
    server.quit()


    frm.destroy()
    welcomeAdmin()

def addProDb(frm,e1,e2,e3):
    con=db.getCon()
    cur=con.cursor()
    cur.execute("select max(p_id) from product")
    sid=cur.fetchone()
    if(sid[0]!=None):
        newid=sid[0]+1
    else:
        newid=1
    cur.execute("insert into product values(%s,%s,%s,%s)",(newid,e1.get(),e2.get(),e3.get()))
    con.commit()
    con.close()
    msg.showinfo('New Product',f'Product Added with id:{newid}')
    frm.destroy()
    welcomeAdmin()

def addSal(frm):
    frm.destroy()
    login_frm=Frame(root,bg=bgclr)
    login_frm.place(x=0,y=100,width=root.winfo_width(),height=root.winfo_height())

    lbl_user=Label(login_frm,bg=bgclr,font=('',15,''),fg='green',text='Welcome:Admin')
    lbl_user.place(x=10,y=100)

    back_btn=Button(login_frm,width=10,command=lambda:back(login_frm),font=('',12,'bold'),text='Back',bd=5)
    back_btn.place(relx=.03,y=150)

    logout_btn=Button(login_frm,width=15,command=lambda:logout(login_frm),font=('',12,'bold'),text='Logout',bd=5)
    logout_btn.place(relx=.85,y=100)

    lbl_name=Label(login_frm,bg=bgclr,font=('',20,''),fg='blue',text='Name')
    lbl_name.place(x=300,y=200)

    lbl_pass=Label(login_frm,bg=bgclr,font=('',20,''),fg='blue',text='Password')
    lbl_pass.place(x=300,y=250)

    lbl_email=Label(login_frm,bg=bgclr,font=('',20,''),fg='blue',text='Email')
    lbl_email.place(x=300,y=300)

    lbl_mob=Label(login_frm,bg=bgclr,font=('',20,''),fg='blue',text='Mobile')
    lbl_mob.place(x=300,y=350)

    ent_name=Entry(login_frm,bd=5,font=('',15,'bold'))
    ent_name.place(x=490,y=205)

    ent_pass=Entry(login_frm,bd=5,show='*',font=('',15,'bold'))
    ent_pass.place(x=490,y=255)

    ent_email=Entry(login_frm,bd=5,font=('',15,'bold'))
    ent_email.place(x=490,y=305)

    ent_mob=Entry(login_frm,bd=5,font=('',15,'bold'))
    ent_mob.place(x=490,y=355)

    sub_btn=Button(login_frm,width=5,text='Add',command=lambda:addSalDb(login_frm,ent_name,ent_pass,ent_email,ent_mob),bd=5,font=('',12,'bold'))
    sub_btn.place(x=520,y=405)

    rst_btn=Button(login_frm,width=5,command=lambda:reset(ent_name,ent_pass,None,ent_email,ent_pass),text='reset',bd=5,font=('',12,'bold'))
    rst_btn.place(x=600,y=405)

def addPro(frm):
    frm.destroy()
    login_frm=Frame(root,bg=bgclr)
    login_frm.place(x=0,y=100,width=root.winfo_width(),height=root.winfo_height())

    lbl_user=Label(login_frm,bg=bgclr,font=('',15,''),fg='green',text='Welcome:Admin')
    lbl_user.place(x=10,y=100)

    back_btn=Button(login_frm,width=10,command=lambda:back(login_frm),font=('',12,'bold'),text='Back',bd=5)
    back_btn.place(relx=.03,y=150)

    logout_btn=Button(login_frm,width=15,command=lambda:logout(login_frm),font=('',12,'bold'),text='Logout',bd=5)
    logout_btn.place(relx=.85,y=100)

    lbl_name=Label(login_frm,bg=bgclr,font=('',20,''),fg='blue',text='Name')
    lbl_name.place(x=300,y=200)

    lbl_qty=Label(login_frm,bg=bgclr,font=('',20,''),fg='blue',text='Qty')
    lbl_qty.place(x=300,y=250)

    lbl_price=Label(login_frm,bg=bgclr,font=('',20,''),fg='blue',text='Price')
    lbl_price.place(x=300,y=300)

    ent_name=Entry(login_frm,bd=5,font=('',15,'bold'))
    ent_name.place(x=490,y=205)

    ent_qty=Entry(login_frm,bd=5,font=('',15,'bold'))
    ent_qty.place(x=490,y=255)

    ent_price=Entry(login_frm,bd=5,font=('',15,'bold'))
    ent_price.place(x=490,y=305)

    sub_btn=Button(login_frm,width=5,text='Add',command=lambda:addProDb(login_frm,ent_name,ent_qty,ent_price),bd=5,font=('',12,'bold'))
    sub_btn.place(x=520,y=405)

    rst_btn=Button(login_frm,width=5,command=lambda:reset(ent_name,ent_pass,None,ent_email,ent_pass),text='reset',bd=5,font=('',12,'bold'))
    rst_btn.place(x=600,y=405)

def billDb(frm,cb,e):
    p_n=cb.get()
    u_qty=int(e.get())
    con=db.getCon()
    cur=con.cursor()
    cur.execute('select p_qty from product where p_name=%s',(p_n,))
    db_qty=cur.fetchone()[0]
    if(db_qty>=u_qty):
        cur.execute('update product set p_qty=p_qty-%s where p_name=%s',(u_qty,p_n))
        con.commit()
        msg.showinfo('','Billing done')
    else:
        msg.showwarning('','Insufficient quantity')
        
def billing(frm,row):
    frm.destroy()
    login_frm=Frame(root,bg=bgclr)
    login_frm.place(x=0,y=100,width=root.winfo_width(),height=root.winfo_height())

    lbl_user=Label(login_frm,bg=bgclr,font=('',15,''),fg='green',text=f'Welcome:{row[2]}')
    lbl_user.place(x=10,y=100)

    back_btn=Button(login_frm,width=10,command=lambda:backUser(login_frm,row),font=('',12,'bold'),text='Back',bd=5)
    back_btn.place(relx=.03,y=150)

    logout_btn=Button(login_frm,width=15,command=lambda:logout(login_frm),font=('',12,'bold'),text='Logout',bd=5)
    logout_btn.place(relx=.85,y=100)

    lbl_name=Label(login_frm,bg=bgclr,font=('',15,''),fg='blue',text='Select Product')
    lbl_name.place(x=300,y=200)

    lbl_qty=Label(login_frm,bg=bgclr,font=('',15,''),fg='blue',text='Qty')
    lbl_qty.place(x=300,y=250)

    con=db.getCon()
    cur=con.cursor()
    cur.execute('select * from product')
    product=[]
    for rowp in cur:
        product.append(rowp[1])
    con.close()

    cb=ttk.Combobox(login_frm,values=product)
    cb.current(0)
    cb.place(x=490,y=205)

    ent_qty=Entry(login_frm,bd=5,font=('',15,'bold'))
    ent_qty.place(x=490,y=255)

    sub_btn=Button(login_frm,width=5,text='Bill',command=lambda:billDb(login_frm,cb,ent_qty),bd=5,font=('',12,'bold'))
    sub_btn.place(x=520,y=405)

    rst_btn=Button(login_frm,width=5,command=lambda:reset(ent_name,ent_pass,None,ent_email,ent_pass),text='reset',bd=5,font=('',12,'bold'))
    rst_btn.place(x=600,y=405)




home()
root.mainloop()
