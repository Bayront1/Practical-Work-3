import pyodbc
from os import system, name
import Admin
import User
import time
import random
import maskpass
import smtplib as smtp
cnxn = pyodbc.connect('Driver={SQL Server};Server=LAPTOP-U7K5FST7\MYSERVERNAME;Database=Restaurant_Python;Trusted_Connection=yes;')
cursor = cnxn.cursor()

def Main():
    registration = True
    role = 0
    email_user, pass_user, email_admin, pass_admin = [], [], [], []
    for row in cursor.execute("select * from [User]"):
        email_user.append(row.Email_User)
        pass_user.append(row.Password_User)
    
    for row in cursor.execute("select * from [Admin]"):
        email_admin.append(row.Email_Admin)
        pass_admin.append(row.Password_Admin)
   
    
    try:
        enter = int(input("Добро пожаловать! \n"
        "Выберите функцию: \n"
        "1 - Войти или Зарегистрироваться\n"
        "2 - Выйти\n"))
    except (KeyboardInterrupt, ValueError):
        print("Ошибка!\n")
        time.sleep(2)
        Main()
    if (enter > 0 and enter <= 2):
        match enter:
            case 1:
                email = input("Введите почту: \n")
                if (not ("@" and ".") in email):
                    print("Неверно введена почта.")
                    time.sleep(2)
                    Main()
                try:
                    password = maskpass.askpass(prompt="Введите пароль: \n", mask="*")
                except UnicodeDecodeError:
                    print("Ошибка! Вводите латиницу!")
                    time.sleep(1)
                    Main()
                for id in range(len(email_admin)):
                    if email == email_admin[id] and password == pass_admin[id]:
                        registration = False
                        for row in cursor.execute(f"select * from [Admin] where [Email_Admin] = '{email}'"):
                            id = row.ID_Admin
                            role = 1
                            EmailCheck(email, password, id, role)
                for id in range(len(email_user)):
                    if email == email_user[id] and password == pass_user[id]:
                        registration = False
                        for row in cursor.execute(f"select * from [User] where [Email_User] = '{email}'"):
                            id = row.ID_User
                            role = 2
                            EmailCheck(email, password, id, role)
                if registration == True:
                    if (email != email_admin and email != email_user):
                        EmailCheck(email, password, id, role)
                    else:
                        print("Ошибка! Неправильная почта или пароль")

                    
    else:
        print("Ошибка! Выберете от 0 до 2")
        time.sleep(2)
        Main()
def EmailCheck(email, password, id, role):
    smtpEmail = "trestaurant@mail.ru"
    code = random.randint(100,999)
    smptObj = smtp.SMTP("smtp.mail.ru", 587)
    smptObj.starttls()
    smptObj.login(smtpEmail, "a3SWegGYt7Teswg9LBGU")
    smptObj.sendmail(smtpEmail, email, f"Your code {code}")
    smptObj.quit()
    print(code)
    try:
       confirmCode = int(input("Код подтверждения выслан на почту.\n""Введите код:\n"))
    except ValueError:
        print("Введены неверные данные")
        time.sleep(2)
        Main()
    if code == confirmCode: 
        if role == 1:
            Admin.Admin(id)
        elif role == 2:
            print("Вы успешно авторизовались.")
            User.Users(id)
        else:
            random.seed()
            money = random.randint(1000, 10000)
            cursor.execute("insert into [User] ([Email_User], [Password_User], [Money_User], [Loyalty_Card_ID]) values (?, ?, ?, ?)", 
            email, password, money, '1')
            cnxn.commit()
            print("Вы успешно зарегистрировались.")
            for row in cursor.execute(f"select * from [User] where [Email_User] = '{email}'"):
                idUser = row.ID_User
            User.Users(idUser)
    else:
        print("Неверный код.")
        time.sleep(2)
        Main()
Main()