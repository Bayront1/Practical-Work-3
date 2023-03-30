import pyodbc
from os import system, name
import time
import Supply
cnxn = pyodbc.connect('Driver={SQL Server};Server=LAPTOP-U7K5FST7\MYSERVERNAME;Database=Restaurant_Python;Trusted_Connection=yes;')
cursor = cnxn.cursor()

def Admin(adminId):
    _ = system('cls')
    for row in cursor.execute(f"select * from [Admin] where [ID_Admin] = '{adminId}'"):
         money = row.Money_Admin
    print(f"У вас на счету {money} рублей.\n")
    try:
        function = int(input("Выберите функцию\n"
        "1 - Заказать поставку ингредиентов\n"
        "2 - Посмотреть историю заказов пользователей\n"
        "3 - Посмотреть скидочные карты пользователей\n"
        "4 - Изменить цену ингредиентам\n"
        "5 - Выйти из аккаунта\n"))
    except ValueError:
        print("Ошибка! Неверные данные")
        time.sleep(2)
        Admin(adminId)

    if function > 0 and function < 6:
        match function:
            case 1:
                Supply.Supply(adminId)
            case 2:
                AdminUsersHistory(adminId)
            case 3:
                AdminUsersLoyality(adminId)
            case 4:
                AdminUpdateIngredients(adminId)
            case 5:
                exit()
    else:
        print("Ошибка! Выберите от 1 до 4.")
        Admin(adminId)

    

def AdminUsersHistory(adminId):
    _ = system('cls')
    ingredientId = []
    for row in cursor.execute("select * from [User]"):
        userId = row.ID_User
        emailUser = row.Email_User
        moneyUser = row.Money_User
        print("Код пользователя: ", userId, ", Почта пользователя: ", emailUser, ", Баланс пользователя: ", moneyUser)

    try:
        idUser = int(input("Выберите пользователя для просмотра истории: \n"
                           "0 - Выйти на главную.\n"))
    except ValueError:
        print("Введены неверные данные")
        time.sleep(2)
        AdminUsersHistory(adminId)
    print("История заказов: ")
    for row in cursor.execute(f"select * from [Order] where [Users_ID] = {idUser}"):
        idOrder = row.ID_Order
        countDish = row.Count_Dish
        priceOrder = row.Price_Order
        detectedOrder = row.Detected
        if detectedOrder == 1:
            print("Номер заказа: ", idOrder, ", Пицца 'Грибная', "," Количество: ", countDish, ", Сумма заказа: ", priceOrder, "Алмаз" " \n")
        else:  
            print("Номер заказа: ", idOrder, ", Пицца 'Грибная', "," Количество: ", countDish, ", Сумма заказа: ", priceOrder, " \n")
             
    for row in cursor.execute(f"select * from [Composition_Dish] where [User_ID] = {idUser}"):
        ingredientId.append(row.Ingredient_ID)
    print("Ингредиенты: ")
    for id in range(len(ingredientId)):
        for row in cursor.execute(f"select * from [Ingredient] where [ID_Ingredient] = {ingredientId[id]}"):
            nameIngredient = row.Name_Ingredient
            print(nameIngredient)
    
    input("Чтобы выйти, нажмите любую кнопку")
    Admin(adminId)


def AdminUsersLoyality(adminId):
    _ = system('cls')

    print("Пользователи:\n")
    for row in cursor.execute("select * from [User]"):
        userId = row.ID_User
        emailUser = row.Email_User
        moneyUser = row.Money_User
        print("Код пользователя: ", userId, ", Почта пользователя: ", emailUser, ", Баланс пользователя: ", moneyUser)

    try:
        idUser = int(input("\nВыберите пользователя для просмотра карты лояльности: \n"
                           "Чтобы выйти, нажмите любую кнопку.\n"))
    except ValueError:
        Admin(adminId)

    if (idUser > 0):
        for row in cursor.execute(f"select * from [User] inner join [Loyalty_Card] on [Loyalty_Card_ID] = [ID_Loyalty_Card] where [ID_User] = {idUser}"):
            nameLoyality = row.Name_Loyalty_Card
            discountLoyality = row.Discount
            discount = discountLoyality * 100
        print(f"Программа лояльности: {nameLoyality}, скидка: {discount}%\n")
        input("Вернуться к функциям")
        Admin(adminId)
    elif (idUser == 0):
        Admin(adminId)
    else:
        print("Неверное действие.")
        time.sleep(2)
        AdminUsersLoyality(adminId)
def AdminUpdateIngredients(adminId):
    _ = system('cls')

    print("Пользователи:\n")
    for row in cursor.execute("select * from [Ingredient]"):
        ingredientId = row.ID_Ingredient
        nameIngredient = row.Name_Ingredient
        countIngredient = row.Count_Ingredient
        priceIngredient = row.Price_Ingredient
        print("Код ингредиента: ", ingredientId, ", Название: ", nameIngredient, ", Количество: ", countIngredient, ", Цена: ", priceIngredient)

    try:
        idIngredient = int(input("\nВыберите ингредиент: \n"
                           "Чтобы выйти, нажмите любую кнопку.\n"))
    except ValueError:
        Admin(adminId)
    try:
        IngredientPrice = int(input("\nВведите цену ингредиента \n"
                           "Чтобы выйти, нажмите любую кнопку.\n"))
    except ValueError:
        print("Ошибка!")
        AdminUpdateIngredients(adminId)
    if (idIngredient > 0):
        cursor.execute(f"update [Ingredient] set [Price_Ingredient] = {IngredientPrice} where [ID_Ingredient] = {idIngredient}")
        cnxn.commit()
        input("Вернуться к функциям")
        Admin(adminId)
    else:
        print("Ошибка! Такого ингредиента нет.")
        time.sleep(2)
        AdminUsersLoyality(adminId)