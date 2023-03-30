import pyodbc
from os import system, name
import time
import random
import Order
import User
cnxn = pyodbc.connect('Driver={SQL Server};Server=LAPTOP-U7K5FST7\MYSERVERNAME;Database=Restaurant_Python;Trusted_Connection=yes;')
cursor = cnxn.cursor()
endIdHachapury = []
def Orders(userId):
    _ = system('cls')
    try:
        count = int(input("Введите количество пицц:\n"
                          "Если хотите выйти, нажмите любую кнопку\n"))
    except ValueError:
        User.Users(userId)
    if (count > 0):
        if (count > 4):
            for i in range(count+1):
                print(f"Пицца №{i+1} \n")

                ingredients, idIngredient, nameIngredient, countIngredient, priceIngredient = [], [], [], [], []
                addIngridients = True

                while addIngridients ==True:
                    print("Ингридиенты: \n")

                    for row in cursor.execute("select * from [Ingredient]"):
                        idIngredient.append(row.ID_Ingredient)
                        nameIngredient.append(row.Name_Ingredient)
                        countIngredient.append(row.Count_Ingredient)
                        priceIngredient.append(row.Price_Ingredient)
                    for i in range(len(idIngredient)):
                        print("Номер: ", idIngredient[i], ", Название: ", nameIngredient[i], ", Количество: ", countIngredient[i], ", Стоимость: ", priceIngredient[i], " рублей \n")
                    print("Для пропуска нажмите любую кнопку.\n")
                    numberIngridient = int(input("Введите номер ингредиента: \n"))
                    countIngred = 0
                    for row in cursor.execute(f"select * from [Ingredient] where [ID_Ingredient] = {numberIngridient}"):
                        countIngred = row.Count_Ingredient    
                    
                    if (countIngred > 0 and numberIngridient > 0):
                        ingredients.append(numberIngridient)
                    else:
                        print("Ингридиенты не выбраны")

                    continueAdd = input("Если хотите добавить ещё один ингредиент, нажмите '+'. Для выхода нажмите любую кнопку.").lower()
                    if continueAdd == "+":
                        addIngridients = True
                    else:
                        addIngridients = False

                print("Выбранные ингредиенты:\n")
                for i in range(len(ingredients)):
                    print("Название: ",nameIngredient[ingredients[i]], ", Стоимость: ", str(priceIngredient[ingredients[i]]), " рублей \n")
                    cursor.execute(f"update [Ingredient] set [Count_Ingredient] = {countIngred-1} where [ID_Ingredient] = {numberIngridient}")
                    cnxn.commit()   
                time.sleep(2)

                for ingrid in range(len(ingredients)):
                    cursor.execute(f"insert into [Composition_Dish] ([Dish_ID], [Ingredient_ID], [User_ID]) values (?, ?, ?)", (1, ingredients[ingrid], userId))
                    cnxn.commit()
        else:
            for i in range(count+1):
                print(f"Пицца №{i+1} \n")

                ingredients, idIngredient, nameIngredient, countIngredient, priceIngredient = [], [], [], [], []
                addIngridients = True

                while addIngridients ==True:
                    print("Ингридиенты: \n")

                    for row in cursor.execute("select * from [Ingredient]"):
                        idIngredient.append(row.ID_Ingredient)
                        nameIngredient.append(row.Name_Ingredient)
                        countIngredient.append(row.Count_Ingredient)
                        priceIngredient.append(row.Price_Ingredient)
                    for i in range(len(idIngredient)):
                        print("Номер: ", idIngredient[i], ", Название: ", nameIngredient[i], ", Количество: ", countIngredient[i], ", Стоимость: ", priceIngredient[i], " рублей \n")
                    print("Для пропуска нажмите любую кнопку.\n")
                    numberIngridient = int(input("Введите номер ингредиента: \n"))
                    countIngred = 0
                    for row in cursor.execute(f"select * from [Ingredient] where [ID_Ingredient] = {numberIngridient}"):
                        countIngred = row.Count_Ingredient    
                    
                    if (countIngred > 0 and numberIngridient > 0):
                        ingredients.append(numberIngridient)
                    else:
                        print("Ингридиенты не выбраны")

                    continueAdd = input("Если хотите добавить ещё один ингредиент, нажмите '+'. Для выхода нажмите любую кнопку.").lower()
                    if continueAdd == "+":
                        addIngridients = True
                    else:
                        addIngridients = False

                print("Выбранные ингредиенты:\n")
                for i in range(len(ingredients)):
                    print("Название: ",nameIngredient[ingredients[i]], ", Стоимость: ", str(priceIngredient[ingredients[i]]), " рублей \n")
                    cursor.execute(f"update [Ingredient] set [Count_Ingredient] = {countIngred-1} where [ID_Ingredient] = {numberIngridient}")
                    cnxn.commit()   
                time.sleep(2)

                for ingrid in range(len(ingredients)):
                    cursor.execute(f"insert into [Composition_Dish] ([Dish_ID], [Ingredient_ID], [User_ID]) values (?, ?, ?)", (1, ingredients[ingrid], userId))
                    cnxn.commit()
    else:
        User.Users(userId)
    
    for row in cursor.execute("select * from [Dish]"):
        priceDish = row.Price_Dish
    priceOrder = count * priceDish
    

    ingredientId = []
    for row in cursor.execute(f"select * from [Composition_Dish] where [User_ID] = {userId}"):
        ingredientId.append(row.Ingredient_ID)
    
    for id in range(len(ingredientId)):
        for row in cursor.execute(f"select * from [Ingredient] where [ID_Ingredient] = {ingredientId[id]}"):
            priceIngridient = row.Price_Ingredient
        priceOrder += priceIngridient
    random.seed()
    if random.randint(1, 10) > 5:
        foreignObject = True
        random.seed()
        if random.randint(1, 10) > 5:
            detected = True
            discountObject = priceOrder * 0,30
            priceOrder = priceOrder - discountObject
        else:
            detected = False
    else:
        foreignObject = False
        detected = False
    for row in cursor.execute(f"select * from [User] where [ID_User] = {userId}"):
        moneyUser = row.Money_User
    for row in cursor.execute(f"select * from [Admin] where [ID_Admin] = {1}"):
        moneyAdmin = row.Money_Admin
    for row in cursor.execute(f"select * from [User] inner join [Loyalty_Card] on [Loyalty_Card_ID] = [ID_Loyalty_Card] where [ID_User] = {userId}"):
        discountLoyaltyCard = row.Discount
    discount = discountLoyaltyCard * priceOrder
    print(f"Ваша скидка : {discount}")
    priceOrder -= discount
    moneyUser -= priceOrder
    moneyAdmin += priceOrder
    if (moneyUser >= 0):
        cursor.execute(f"update [User] set [Money_User] = {moneyUser} where [ID_User] = {userId}")
        cnxn.commit()
        cursor.execute(f"update [Admin] set [Money_Admin] = {moneyAdmin} where [ID_Admin] = {1}")
        cnxn.commit()
        cursor.execute("insert into [Order] ([Count_Dish], [Price_Order], [Foreign_Object], [Detected], [Users_ID]) values (?, ?, ?, ?, ?)", 
                   (count, priceOrder,  (1 if foreignObject else 0), (1 if detected else 0), userId))
        cnxn.commit()
    else:
        print("Недостаточно денег на счету.")
        time.sleep(2)
        Order.Orders(userId)
    

    if (priceOrder > 5000):
        cursor.execute(f"update [User] set [Loyalty_Card_ID] = 2 where [ID_User] = {userId}")
        cnxn.commit()
    elif (priceOrder > 15000):
        cursor.execute(f"update [User] set [Loyalty_Card_ID] = 3 where [ID_User] = {userId}")
        cnxn.commit()
    elif (priceOrder > 25000):
        cursor.execute(f"update [User] set [Loyalty_Card_ID] = 4 where [ID_User] = {userId}")
        cnxn.commit()
           
    print("Заказ оформлен")
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
             
    time.sleep(2)
    User.Users(userId)