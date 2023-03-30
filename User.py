import pyodbc
from os import system, name
import time
import Order

cnxn = pyodbc.connect('Driver={SQL Server};Server=LAPTOP-U7K5FST7\MYSERVERNAME;Database=Restaurant_Python;Trusted_Connection=yes;')
cursor = cnxn.cursor()

def Users(userId):
    _ = system('cls')
    for row in cursor.execute(f"select * from [User] where [ID_User] = '{userId}'"):
         money = row.Money_User
    for row in cursor.execute(f"select * from [User] inner join [Loyalty_Card] on [Loyalty_Card_ID] = [ID_Loyalty_Card] where [ID_User] = {userId}"):
        nameLoyaltyCard = row.Name_Loyalty_Card
        discountLoyaltyCard = row.Discount
        discount = discountLoyaltyCard * 100
    print(f"У вас на счету {money} рублей.\n")
    print(f"Ваша программа лояльности: {nameLoyaltyCard}, скидка: {discount}%\n")
   
    try:
        function = int(input("Выберите функцию\n"
        "1 - Заказать блюдо\n"
        "2 - История покупок\n"
        "3 - Выйти из аккаунта\n"))
    except ValueError:
        print("Введены неверные данные")
        time.sleep(2)
        Users(userId)

    if function > 0 and function < 4:
        match function:
            case 1:
                Order.Orders(userId)
            case 2:
                UserHistory(userId)
            case 3:
                exit()
    else:
        print("Ошибка! Выберите от 1 до 3!")
        Users(userId)

def UserHistory(userId):
    print("История заказов")
    ingredientId = []
    for row in cursor.execute(f"select * from [Order] where [Users_ID] = {userId}"):
        idOrder = row.ID_Order
        countDish = row.Count_Dish
        priceOrder = row.Price_Order
        detectedOrder = row.Detected
        if detectedOrder == 1:
            print("Номер заказа: ", idOrder, ", Пицца 'Грибная', "," Количество: ", countDish, ", Сумма заказа: ", priceOrder, "Алмаз" " \n")
        else:  
            print("Номер заказа: ", idOrder, ", Пицца 'Грибная', "," Количество: ", countDish, ", Сумма заказа: ", priceOrder, " \n")
             
    for row in cursor.execute(f"select * from [Composition_Dish] where [User_ID] = {userId}"):
        ingredientId.append(row.Ingredient_ID)
    print("Ингредиенты: ")
    for id in range(len(ingredientId)):
        for row in cursor.execute(f"select * from [Ingredient] where [ID_Ingredient] = {ingredientId[id]}"):
            nameIngredient = row.Name_Ingredient
            print(nameIngredient)
    
    input("Чтобы выйти, нажмите на любую кнопку.")
    Users(userId)