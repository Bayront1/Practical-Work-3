import pyodbc
from os import system, name
import time
import Admin
cnxn = pyodbc.connect('Driver={SQL Server};Server=LAPTOP-U7K5FST7\MYSERVERNAME;Database=Restaurant_Python;Trusted_Connection=yes;')
cursor = cnxn.cursor()
def Supply(adminId):
    _ = system('cls')
    for row in cursor.execute(f"select * from [Admin] where [ID_Admin] = {adminId}"):
        money = row.Money_Admin

    print(f"У вас на счету {money} рублей.\n")

    for row in cursor.execute("select * from [Ingredient]"):
        idIngredient = row.ID_Ingredient
        nameIngredient = row.Name_Ingredient
        countIngredient = row.Count_Ingredient
        priceIngredient = row.Price_Ingredient
        print("Номер: ", idIngredient, ", Название: ", nameIngredient, ", Количество: ", countIngredient, ", Стоимость: ", priceIngredient, " рублей \n")
                    
    print("Нажмите любую кнопку, чтобы выйти\n")
    
    try:
        idIngredient = int(input("Выберите ингридиент для поставки: \n"))
    except ValueError:
        Admin.Admin(adminId)

    if (idIngredient > 0):
        try:
            count = int(input("Введите количество поставки: \n"))
        except ValueError:
            print("Ошибка!")
            time.sleep(2)
            Supply(adminId)

        for row in cursor.execute(f"select * from [Ingredient] where [ID_Ingredient] = {idIngredient}"):
            idNameIngredient = row.Name_Ingredient
            idCountIngredient = row.Count_Ingredient
            idPriceIngredient = row.Price_Ingredient

        endCount = idCountIngredient + count
        priceSupply = count * idPriceIngredient

        confirm = input(f"Поставка {idNameIngredient} в количестве {count} шт. - {priceSupply} Рублей\n"
                        "Нажмите '+' для подтверждения поставки\n").lower()
        
        if confirm == "+":
            money -= priceSupply
            if money >= 0:
                cursor.execute(f"update [Admin] set [Money_Admin] = {money} where [ID_Admin] = {adminId}")
                cnxn.commit()
                cursor.execute(f"update [Ingredient] set [Count_Ingredient] = {endCount} where [ID_Ingredient] = {idIngredient}")
                cnxn.commit()               
                time.sleep(2)
                print("Заказ выполнен!")
                Admin.Admin(adminId)
            else:
                print("Недостаточно средств на счету.")
                time.sleep(2)
                Admin.Admin(adminId)
        else:
            print("Отмена поставки!")
            time.sleep(2)
            Admin.Admin(adminId)
    else:
        print("Выход")
        time.sleep(2)
        Admin.Admin(adminId)