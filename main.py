import pandas as pd
from json_url import data_url


# Чтение файла JSON
data = pd.read_json(data_url)

'''1. Найти тариф стоимости доставки для каждого склада'''

tariffs = data.groupby('warehouse_name')['highway_cost'].sum()

# Вывод результатов Задачи 1
print('Тарифы стоимости доставки для каждого склада:')
print(tariffs)
print()

'''2. Найти суммарное количество , суммарный доход , суммарный расход и суммарную прибыль для каждого товара'''

data = pd.json_normalize(data.to_dict(orient='records'), record_path='products', meta=['order_id', 'warehouse_name', 'highway_cost'])

# Вычисление суммарного количества, дохода, расхода и прибыли для каждого товара
data['income'] = data['price'] * data['quantity']
data['expenses'] = data['highway_cost'] * data['quantity']
data['profit'] = data['income'] - data['expenses']

# Сведение данных по продуктам и расчёт суммы
product_stats = data.groupby('product').agg(
    quantity=('quantity', 'sum'),
    income=("income", "sum"),
    expenses=("expenses", "sum"),
    profit=("profit", "sum")
).reset_index()

# Вывод результатов Задачи 2
print('Статистика по товарам:')
print(product_stats)
print()

'''3. Составить табличку со столбцами 'order_id' и 'order_profit', а также вывести среднюю прибыль заказов'''

# Группировка данных по заказам и расчёт прибыли для каждого заказа
order_stats = data.groupby('order_id')['highway_cost'].sum().reset_index()
order_stats.rename(columns={'highway_cost': 'order_profit'}, inplace=True)

# Расчёт средней прибыли заказов
average_profit = order_stats['order_profit'].mean()

# Вывод результатов Задачи 3
print('Табличка со столбцами "order_id" и "order_profit":')
print(order_stats)
print('Средняя прибыль заказов:', average_profit)
print()

'''4. Составить табличку типа "warehouse_name" , "product","quantity", "profit", "percent_profit_product_of_warehouse".'''
# Расчёт прибыли для каждого заказа
data['product_profit'] = data['price'] * data['quantity'] - data['highway_cost'] * data['quantity']

# Группировка данных по складу и продукту и расчёт суммарной прибыли для каждого
warehouse_product_stats = data.groupby(['warehouse_name', 'product']).agg(
    quantity=('quantity', 'sum'),
    profit=('product_profit', 'sum'),
    total_profit=('highway_cost', 'sum')
).reset_index()

# Расчёт процента прибыли продукта
warehouse_product_stats['percent_profit_product_of_warehouse'] = (warehouse_product_stats['profit'] / warehouse_product_stats['total_profit']) * 100

# Вывод результатов Задачи 4
print('Табличка со столбцами "warehouse_name", "product", "quantity", "profit", "percent_profit_product_of_warehouse":')
print(warehouse_product_stats)
print()

'''5. Отсортировать 'percent_profit_product_of_warehouse' по убыванию и вычислить накопленный процент'''

# Сортировка таблицы по убыванию процента прибыли
sorted_warehouse_product_stats = warehouse_product_stats.sort_values(by='percent_profit_product_of_warehouse', ascending=False)

# Расчёт накопленного процент
sorted_warehouse_product_stats['accumulated_percent_profit_product_of_warehouse'] = sorted_warehouse_product_stats['percent_profit_product_of_warehouse'].cumsum()

# Вывод результатов Задачи 5
print('Задача 5 - Отсортированная табличка с накопленным процентом прибыли:')
print(sorted_warehouse_product_stats)
print()

'''6. Присвоить A,B,C - категории на основании значения накопленного процента'''

# Функция для присвоения категории A,B,C на основании накопленного процента
def assign_category(accumulated_percent):
    if accumulated_percent <= 70:
        return 'A'
    elif 70 < accumulated_percent <= 90:
        return 'B'
    else:
        return 'C'

# Получение категорий
sorted_warehouse_product_stats['category'] = sorted_warehouse_product_stats['accumulated_percent_profit_product_of_warehouse'].apply(assign_category)

# Вывод результатов Задачи 6
print(sorted_warehouse_product_stats)
print('Задача 6 - Табличка с категориями A, B, C на основании накопленного процента:')
print(sorted_warehouse_product_stats)