from tkinter import * 
from tkinter import filedialog

import tkinter as tk   
from tkinter import ttk
from functools import partial
import os
from .survey_format import survey_format
import csv

from pathlib import Path

ASSETS_PATH = Path(__file__).resolve().parent / "assets"



class Admin_Panel(Frame):

    def __init__(self, parent, tabControl,db):
        super().__init__(parent)
        self.db=db

        self.configure(background="#3A7FF6")



        self.admin_tab = Frame(tabControl)
        tabControl.add(self.admin_tab, text ='Admin Panel')

        
        self.admin_tab.grid_rowconfigure(0, weight=1) 
        self.admin_tab.grid_columnconfigure(0, weight=1) 


        # self.admin_tab.configure(background='black')


        self.frames = {}
        for F in (Register_Frame,Login_Frame,Admin_Frame,Settings_Frame):
            frame = F(self.admin_tab,self, db)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
            frame.grid_rowconfigure(0, weight = 1)
            frame.grid_columnconfigure(0, weight = 1)





        if(self.db.empty_admin_password()):
            self.show_frame(Register_Frame)
            # print('RegisterPage')
        else:
            self.show_frame(Login_Frame)
            # print('LoginPage') 

        # self.show_frame(Settings_Frame)   

    def show_frame(self,container):
        frame = self.frames[container]
        frame.tkraise()


class Register_Frame(Frame):

    def __init__(self, parent, controller, db):
        super().__init__(parent)

        self.db=db
        self.controller=controller

        self.admin_tab=parent
        self.configure(background="#3A7FF6")

        

  
        f1 = Frame(self)
        f1.place(anchor="c", relx=.5, rely=.5, height=500, width=500)
 
        




        f11 = Frame(f1)
        f11.place(anchor="c", relx=.5, rely=.5)
 
        

        Label(f11, text="Register", font=("Arial",30)).pack(fill=X, expand=False,padx=20, pady=20)
        
        


        #password label and password entry box
        Label(f11, font=('Lucida 15'),text="Password").pack()
        self.password = StringVar()
        Entry(f11, font=('Lucida 15'), textvariable=self.password, show='*').pack()

        Label(f11, font=('Lucida 15'),text="Retype Password").pack()
        self.retypepassword = StringVar()
        Entry(f11, font=('Lucida 15'), textvariable=self.retypepassword, show='*').pack()

        validateRegister = partial(self.validateRegister, self.password,self.retypepassword)

        #login button
        Button(f11, font=('Lucida 15'), text="Create Admin Password", command=validateRegister).pack(padx=10, pady=10)

     
        self.ValidationText = StringVar(value="")
        Label(f11, font=('Lucida 10'), textvariable=self.ValidationText).pack()

    def validateRegister(self, passwd,retypepasswd):
        password=passwd.get()
        retypepassword=retypepasswd.get()

        

        if len(password)==0:
            self.ValidationText.set("Password is Required")
            return False

        if len(password)<=4:
            self.ValidationText.set("Password must contain more than 4 Characters")
            return False
        else:
            if (retypepassword==password):
                self.db.set_admin_password(password)
                self.controller.show_frame(Admin_Frame)
                self.password.set('')
                self.retypepassword.set('')

                return True
            else:
                self.ValidationText.set("Password Do not Match")


        return False


class Login_Frame(Frame):

    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self.db=db
        self.controller=controller

        self.configure(background="#3A7FF6")

  
        f1 = Frame(self)
        f1.place(anchor="c", relx=.5, rely=.5, height=500, width=500)
 
        
        f11 = Frame(f1)
        f11.place(anchor="c", relx=.5, rely=.5)
 
        # f1.pack(fill=BOTH, expand=True)


        Label(f11, text="Login", font=("Arial",30)).pack(fill=X, expand=False,padx=20, pady=20)


        #password label and password entry box
        Label(f11, font=('Lucida 15'),text="Password").pack()
        self.password = StringVar()
        Entry(f11, font=('Lucida 15'), textvariable=self.password, show='*').pack()

        #login button
        Button(f11, font=('Lucida 15'), text="Login", command=self.validateLogin).pack(padx=10, pady=10)


     
        self.ValidationText = StringVar(value="")
        Label(f11, font=('Lucida 10'), textvariable=self.ValidationText).pack()
        self.ValidationText.set("")

    
        
    def validateLogin(self):
        password=self.password.get()

        if len(password)==0 or password=='':
            self.ValidationText.set("Please Enter your Password")
            return False

        # print("password entered :",password )


        if(self.db.check_admin_password(password)):
            # print('Login Successfull')
            self.ValidationText.set("")
            self.password.set('')
            self.controller.show_frame(Admin_Frame)
            return True

        else:
            # print('Invalid Password')
            self.ValidationText.set("Invalid Password")
            return False







class Admin_Frame(Frame):

    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self.db=db
        self.controller=controller

        self.configure(background="#3A7FF6")

        self.admin_tab=parent
        Label(self,bg='#3A7FF6',  text="Admin Panel", font=('Lucida 15')).pack()






        




        self.headings = ('ID', 'Firstname', 'Lastname', 'Age', 'Gender', 'Ethnicity', 'Disabled', 'Enjoyed', 'Curious', 'Want to know more Science',)
        


        #     print("Id: ", survey[0])
        #     print("firstname: ", survey[1])
        #     print("lastname: ", survey[2])
        #     print("age: ", survey[3])
        #     print("gender: ", survey[4])
        #     print("ethnicity: ", survey[5])
        #     print("disabled: ", survey[6])
        #     print("enjoyed: ", survey[7])
        #     print("curious: ", survey[8])
        #     print("science: ", survey[9])
 
        f3 = Frame(self,bg='#3A7FF6')


        label = tk.Label(f3,bg='#3A7FF6', text="Surveys", font=("Arial",30)).pack(fill=X, expand=False)
        # create Treeview with 3 columns
        self.listBox = ttk.Treeview(f3, columns=self.headings, show='headings')
        self.listBox.column(1, anchor=CENTER, stretch=NO, width=50)
        # set column headings
        for n, col in enumerate(self.headings):
            self.listBox.column(n, anchor=CENTER, stretch=NO, width=100)
            self.listBox.heading(col, text=col) 
        self.listBox.column(0, anchor=CENTER, stretch=NO, width=50)  
        self.listBox.column(9, anchor=CENTER, stretch=NO, width=170)   
        self.listBox.pack(fill=BOTH, expand=True, padx=10, pady=10)
        # self.listBox.grid_configure(padx=10, pady=10)


        f3.pack(fill=BOTH, expand=True)





        f1 = Frame(self,bg='#3A7FF6')


        f11 = Frame(f1,bg='#3A7FF6')



        f111 = Frame(f11,bg='#3A7FF6')
        Label(f111, text='Average Age',bg='#3A7FF6', font=('Lucida 15')).pack()
        self.AverageAgeText = StringVar(value="")
        Label(f111, textvariable=self.AverageAgeText,bg='#3A7FF6', font=('Lucida 12')).pack()
        f111.pack(fill=BOTH, expand=True,side=LEFT)



        f112 = Frame(f11,bg='#3A7FF6')
        Label(f112, text='Gender',bg='#3A7FF6', font=('Lucida 15')).pack(side=TOP)
        self.GenderText={}
        for key,value in survey_format['gender']['values'].items():
            f1121 = Frame(f112,bg='#3A7FF6')
            Label(f1121, text=value,bg='#3A7FF6').pack(side=LEFT)
            self.GenderText[key] = StringVar(value="")
            Label(f1121, textvariable=self.GenderText[key],bg='#3A7FF6').pack(side=LEFT)
            f1121.pack(side=TOP)
        f112.pack(fill=BOTH, expand=True,side=LEFT)


        f113 = Frame(f11,bg='#3A7FF6')
        Label(f113, text='Ethnicity',bg='#3A7FF6', font=('Lucida 15')).pack(side=TOP)
        self.EthnicityText={}
        for key,value in survey_format['ethnicity']['values'].items():
            f1121 = Frame(f113,bg='#3A7FF6')
            Label(f1121, text=value,bg='#3A7FF6').pack(side=LEFT)
            self.EthnicityText[key] = StringVar(value="")
            Label(f1121, textvariable=self.EthnicityText[key],bg='#3A7FF6').pack(side=LEFT)
            f1121.pack(side=TOP)
        f113.pack(fill=BOTH, expand=True,side=LEFT)

    

        f114 = Frame(f11, bg="#3A7FF6")
        Label(f114, text='Disabled', bg="#3A7FF6", font=('Lucida 15')).pack(side=TOP)
        self.DisabledText={}
        for key,value in survey_format['disabled']['values'].items():
            f1121 = Frame(f114, bg="#3A7FF6")
            Label(f1121, text=value, bg="#3A7FF6").pack(side=LEFT)
            self.DisabledText[key] = StringVar(value="")
            Label(f1121, textvariable=self.DisabledText[key], bg="#3A7FF6").pack(side=LEFT)
            f1121.pack(side=TOP)
        f114.pack(fill=BOTH, expand=True,side=LEFT)

    
        f115 = Frame(f11, bg="#3A7FF6")
        Label(f115, text='Enjoyed', bg="#3A7FF6", font=('Lucida 15')).pack(side=TOP)
        self.EnjoyedText={}
        for key,value in survey_format['enjoyed']['values'].items():
            f1121 = Frame(f115, bg="#3A7FF6")
            Label(f1121, text=value, bg="#3A7FF6").pack(side=LEFT)
            self.EnjoyedText[key] = StringVar(value="")
            Label(f1121, textvariable=self.EnjoyedText[key], bg="#3A7FF6").pack(side=LEFT)
            f1121.pack(side=TOP)
        f115.pack(fill=BOTH, expand=True,side=LEFT)



        f116 = Frame(f11, bg="#3A7FF6")
        Label(f116, text='Curious', bg="#3A7FF6", font=('Lucida 15')).pack(side=TOP)
        self.CuriousText={}
        for key,value in survey_format['curious']['values'].items():
            f1121 = Frame(f116, bg="#3A7FF6")
            Label(f1121, text=value, bg="#3A7FF6").pack(side=LEFT)
            self.CuriousText[key] = StringVar(value="")
            Label(f1121, textvariable=self.CuriousText[key], bg="#3A7FF6").pack(side=LEFT)
            f1121.pack(side=TOP)
        f116.pack(fill=BOTH, expand=True,side=LEFT)


        f117 = Frame(f11, bg="#3A7FF6")
        Label(f117, text='Want to know more Science', bg="#3A7FF6", font=('Lucida 15')).pack(side=TOP)
        self.ScienceText={}
        for key,value in survey_format['science']['values'].items():
            f1121 = Frame(f117, bg="#3A7FF6")
            Label(f1121, text=value, bg="#3A7FF6").pack(side=LEFT)
            self.ScienceText[key] = StringVar(value="")
            Label(f1121, textvariable=self.ScienceText[key], bg="#3A7FF6").pack(side=LEFT)
            f1121.pack(side=TOP)
        f117.pack(fill=BOTH, expand=True,side=LEFT)




        f11.pack(fill=BOTH, expand=True, padx=10, pady=10)



        f12 = Frame(f1, bg="#3A7FF6")
        Button(f12, font=('Lucida 10'), text="Refresh", width=15, command=self.refresh_data).pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
 
        Button(f12, font=('Lucida 10'), text="Save as CSV", width=15, command=self.ask_file_save).pack(side=LEFT,fill=BOTH, expand=True,padx=10, pady=10)
        f12.pack(fill=Y, expand=True)




        f1.pack(fill=BOTH, expand=True)
       



        # self.ValidationText = StringVar(value="")
        # self.ValidationLabel = Label(self, textvariable=self.ValidationText).pack()

        
        f2 = Frame(self, bg="pink", height=80)
        
        f21 = Frame(f2, bg="pink")
        self.settingsButton = Button(f21,width=20, font=('Lucida 20'), text="Settings", command=lambda : self.controller.show_frame(Settings_Frame)).pack(fill=BOTH, expand=True, padx=10, pady=10)
  
        f21.pack(side=LEFT, fill=Y, expand=True)

        f22 = Frame(f2, bg="pink")

        self.logoutButton = Button(f22,width=20, font=('Lucida 20'), text="Logout", command=lambda : self.controller.show_frame(Login_Frame)).pack(fill=BOTH, expand=True, padx=10, pady=10)
        f22.pack(side=LEFT, fill=Y, expand=True)

        f23 = Frame(f2, bg="pink")
        self.exitButton = Button(f23,width=20, font=('Lucida 20'), text="Exit", command= self.exit_app).pack(fill=BOTH, expand=True, padx=10, pady=10)
        f23.pack(side=LEFT, fill=Y, expand=True)

        f2.pack(anchor= S,fill=X, expand=True)
        f2.pack_propagate(0)

        self.surveys=[]

        # self.refresh_data()
  


    def refresh_data(self):

        self.surveys = self.db.get_all_surveys()



        age_list = []
        for n, survey in enumerate(self.surveys):
            asurvey=list(survey)
            
            age_list.append(survey[3])
            asurvey[4]=survey_format['gender']['values'][survey[4]]
            asurvey[5]=survey_format['ethnicity']['values'][survey[5]]
            asurvey[6]=survey_format['disabled']['values'][survey[6]]
            asurvey[7]=survey_format['enjoyed']['values'][survey[7]]
            asurvey[8]=survey_format['curious']['values'][survey[8]]
            asurvey[9]=survey_format['science']['values'][survey[9]]
            self.surveys[n]=asurvey

        try:    
            self.average_age = (sum(age_list))/len(age_list)
        except:
            self.average_age = 0
        
        self.AverageAgeText.set(self.average_age)

        for key,value in self.GenderText.items():
            self.GenderText[key].set(self.db.get_gender_count(key))

        for key,value in self.EthnicityText.items():
            self.EthnicityText[key].set(self.db.get_ethnicity_count(key))

        for key,value in self.DisabledText.items():
            self.DisabledText[key].set(self.db.get_disabled_count(key))

        for key,value in self.EnjoyedText.items():
            self.EnjoyedText[key].set(self.db.get_enjoyed_count(key))

        for key,value in self.CuriousText.items():
            self.CuriousText[key].set(self.db.get_curious_count(key))

        for key,value in self.ScienceText.items():
            self.ScienceText[key].set(self.db.get_science_count(key))



        # self.surveys.sort(key=lambda e: e[1], reverse=True)
        self.listBox.delete(*self.listBox.get_children())

        for i, args in enumerate(self.surveys, start=1):
            self.listBox.insert("", "end", values=(*args,))





    def ask_file_save(self):
        data = self.surveys
        
        file_name =tk.filedialog.asksaveasfilename(initialdir = "",title = "Save as CSV",filetypes = (("CSV file","*.csv"),),)
        # print (file_name)
        self.master.master.master.bring_to_front()
        if (file_name == None or file_name == ''):
            return

        if(not file_name.endswith(".csv")):
            file_name=file_name+'.csv'

        self.save_csv(file_name,self.headings, data)
        # print('Saved Csv')
        

    def save_csv(self,file_name,headings, data):
        with open(file_name, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headings)
            writer.writerows(data)


    def exit_app(self):
        # print('Exitted')
        self.master.master.master.destroy()
            








class Settings_Frame(Frame):

    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self.db=db
        self.controller=controller

        self.configure(background="#3A7FF6")


        self.admin_tab=parent

        Label(self,bg="#3A7FF6", text="Admin Panel", font=('Lucida 15')).pack()


        Label(self,bg="#3A7FF6", text="Settings", font=("Arial",30)).pack(fill=X, expand=False)

        f1 = Frame(self)




        f11 = Frame(f1)

        Label(f11, font=('Lucida 15'),text="Password").pack()
        self.password = StringVar()
        Entry(f11, font=('Lucida 15'), textvariable=self.password, show='*').pack()

        self.ValidationText = StringVar(value="")
        Label(f11, font=('Lucida 20'), textvariable=self.ValidationText).pack()


        f111 = Frame(f11)
        Label(f111, font=('Lucida 15'),text="Change Password").pack()

        Label(f111, font=('Lucida 15'),text="New Password").pack()
        self.newpassword = StringVar()
        Entry(f111, font=('Lucida 15'), textvariable=self.newpassword, show='*').pack()

        Label(f111, font=('Lucida 15'),text="Retype New Password").pack()
        self.retypenewpassword = StringVar()
        Entry(f111, font=('Lucida 15'), textvariable=self.retypenewpassword, show='*').pack()

        Button(f111, font=('Lucida 15'), text="Change Password", command=self.change_password).pack()

        f111.pack(fill=BOTH, expand=True, padx=40,pady=40)

        f112 = Frame(f11)

        Label(f112, font=('Lucida 20'), fg='red',text="Danger").pack()



        Button(f112, font=('Lucida 20'), bg='red', fg='white', text="Reset Database", command=self.reset_database).pack(side=LEFT, fill=BOTH, expand=True, padx=10,pady=10)


        Button(f112, font=('Lucida 20'), bg='red', fg='white', text="Delete Surveys", command=self.delete_surveys).pack(side=LEFT, fill=BOTH, expand=True, padx=10,pady=10)

        f112.pack(fill=Y, expand=True , padx=10,pady=10)


        f11.pack(side=LEFT, fill=BOTH, expand=True, padx=10,pady=10)

        f12 = Frame(f1)

        Button(f12, font=('Lucida 20'), text="Toggle Fullscreen", command=self.toggle_fullscreen).pack(side=LEFT, padx=10,pady=10)


        f12.pack(side=LEFT,fill=BOTH, expand=True, padx=10,pady=10)

        f1.pack(fill=BOTH, expand=True, padx=10,pady=10)


        f2 = Frame(self, bg="pink", height=80)
        
        f21 = Frame(f2, bg="pink")
        Button(f21,width=20, font=('Lucida 20'), text="Admin Panel", command=lambda : self.controller.show_frame(Admin_Frame)).pack(fill=BOTH, expand=True, padx=10, pady=10)
  
        f21.pack(side=LEFT, fill=Y, expand=True)

        f22 = Frame(f2, bg="pink")

        Button(f22,width=20, font=('Lucida 20'), text="Logout", command=lambda : self.controller.show_frame(Login_Frame)).pack(fill=BOTH, expand=True, padx=10, pady=10)
        f22.pack(side=LEFT, fill=Y, expand=True)

        f23 = Frame(f2, bg="pink")
        Button(f23,width=20, font=('Lucida 20'), text="Exit", command= self.exit_app).pack(fill=BOTH, expand=True, padx=10, pady=10)
        f23.pack(side=LEFT, fill=Y, expand=True)
        
        f2.pack(anchor= S, fill=X, expand=True)
        f2.pack_propagate(0)
        

    def validatePassword(self):
        password=self.password.get()
        # print("password entered :",password )

        if not(len(password) ==0 or password == ''): 
            if(self.db.check_admin_password(password)):
                # print('Authentication Successfull')
                self.ValidationText.set("")
                self.password.set('')
                return True

            else:
                self.password.set("")
                # print('Invalid Password')
                self.ValidationText.set("Invalid Password!!!")
                return False
        else:
            # print('Required Password')
            self.ValidationText.set("Password Required!!!")


    def toggle_fullscreen(self):

        if self.db.get_settings('fullscreen') == '1':
            self.db.set_settings('fullscreen','0')
            self.master.master.master.attributes('-fullscreen',False)
            self.master.master.master.state('zoomed')

        else:
            self.db.set_settings('fullscreen','1')
            self.master.master.master.attributes('-fullscreen',True)
        

    def change_password(self):
        oldpassword=self.password.get()
        password=self.newpassword.get()
        retypepassword=self.retypenewpassword.get()
        # print("password entered :",password )
        # print("password entered :",retypepassword )
        

        if len(password)==0 or password=="":
            self.ValidationText.set("New Password is Required")
            return False

        if len(password)<=4:
            self.ValidationText.set("New Password must contain more than 4 Characters")
            return False

        else:
            if(oldpassword==password):
                self.ValidationText.set("New Password cannot be same as Old one")
            else:

                if (retypepassword==password):

                    if self.validatePassword():
                        self.db.set_admin_password(password)
                        self.ValidationText.set("Password has been Changed")
                        self.newpassword.set('')
                        self.retypenewpassword.set('')

                    
                    

                    return True
                else:
                    self.ValidationText.set("New Passwords Do not Match")


        return False

    def reset_database(self):
        if self.validatePassword():
            self.ValidationText.set("")
            self.db.remake_database()
            self.controller.show_frame(Register_Frame)

    def delete_surveys(self):
        if self.validatePassword():
            self.ValidationText.set("All Surveys has been Deleted")
            self.db.clear_survey()

    def exit_app(self):
        # print('Exitted')
        self.master.master.master.destroy()
            



