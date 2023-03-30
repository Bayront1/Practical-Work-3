
set ansi_nulls on
go
set ansi_padding on
go
set quoted_identifier on 
go

create database [Restaurant_Python]
go

use [Restaurant_Python]
go

create table [dbo].[Dish]
(
	[ID_Dish] [int] not null identity(1,1) primary key,
	[Price_Dish] [decimal] (38,2) not null
)
go

insert into [Dish] ([Price_Dish]) values
(1000)

create table [dbo].[Ingredient]
(
	[ID_Ingredient] [int] not null identity(1,1) primary key,
	[Name_Ingredient] [varchar] (50) not null,
	[Count_Ingredient] [int] not null,
	[Price_Ingredient] [decimal] (38,2) not null
)
go
insert into [Ingredient] ([Name_Ingredient], [Count_Ingredient], [Price_Ingredient]) values
('Лук', 50, 20),
('Шампиньон', 50, 30),
('Помидор', 50, 15),
('Перец', 50, 12),
('Сыр', 50, 40)
go
create table [Loyalty_Card]
(
	[ID_Loyalty_Card] [int] not null identity(1,1) primary key,
	[Name_Loyalty_Card] [varchar] (50) not null unique,
	[Discount] [decimal] (38,2) not null
)
go

insert into [Loyalty_Card] ([Name_Loyalty_Card], [Discount]) values
('Обычная карта', 0),
('Бронзовая карта', 0.15),
('Серебрянная карта', 0.25),
('Золотая карта', 0.35)
go

select * from [Loyalty_Card]
go

create table [dbo].[User]
(
	[ID_User] [int] not null identity(1,1) primary key,
	[Email_User] [varchar] (50) not null unique check ([Email_User] like ('%@%.%')),
	[Password_User] [varchar] (50) not null,
	[Money_User] [decimal] (38,2) not null,
	[Loyalty_Card_ID] [int] not null references [Loyalty_Card] (ID_Loyalty_Card) on delete cascade,
)
go

insert into [User] ([Email_User], [Password_User], [Money_User], [Loyalty_Card_ID]) values
('lolka@mail.ru', 'lolka', 5000, 1)

select * from [dbo].[User]
go

create table [dbo].[Admin]
(
	[ID_Admin] [int] not null identity(1,1) primary key,
	[Email_Admin] [varchar] (50) not null unique check ([Email_Admin] like ('%@%.%')),
	[Password_Admin] [varchar] (50) not null,
	[Money_Admin] [decimal] (38,2) not null default (5000)
)
go
insert into [Admin] ([Email_Admin], [Password_Admin], [Money_Admin]) values
('aassiinnn@yandex.ru', '123', 5000)

create table [dbo].[Composition_Dish]
(
	[ID_Composition_Dish] [int] not null identity(1,1) primary key,
	[Dish_ID] [int] not null,
	[Ingredient_ID] [int] not null references [Ingredient] (ID_Ingredient) on delete cascade,
	[User_ID] [int] not null references [User] (ID_User) on delete cascade,
)
go
insert into [Composition_Dish] ([Dish_ID], [Ingredient_ID], [User_ID]) values
(1, 1, 1)
select * from Composition_Dish

create table [dbo].[Order]
(
	[ID_Order] [int] not null identity(1,1) primary key,
	[Count_Dish] [int] not null,
	[Foreign_Object] [bit] not null,
	[Detected] [bit] not null,
	[Users_ID] [int] not null references [User] (ID_User) on delete cascade,
	[Price_Order] [decimal] (38,2) not null
)
go

insert into [Order] ([Count_Dish],  [Price_Order], [Foreign_Object], [Detected], [Users_ID]) values
(1, 1, 1, 1, 1)

select * from [dbo].[Order]
create table [Supply]
(
	[ID_Supply] [int] not null identity(1,1) primary key,
	[Count_Supply] [int] not null,
	[Cost_Supply] [int] not null,
	[Sum_Supply] [int] not null,
	[Admin_ID] [int] not null references [Admin] (ID_Admin) on delete cascade,
	[Ingredient_ID] [int] not null references [Ingredient] (ID_Ingredient) on delete cascade,
)
go


