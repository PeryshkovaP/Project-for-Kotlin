import random

# Баланс пользователя
balance_user = {
    'RUB': 1000000,
    'USD': 0,
    'EUR': 0,
    'USDT': 0,
    'BTC': 0
}

# Баланс терминала
balance_terminal = {
    'RUB': 10000,
    'USD': 1000,
    'EUR': 1000,
    'USDT': 1000,
    'BTC': 1.5
}

# Текущий курс
courses = {
    'RUB-USD': 90,
    'RUB-EUR': 100,
    'USD-EUR': 0.9,
    'USD-USDT': 1,
    'USD-BTC': 58000
}

# Вывод всего
def PrintMenu():
    print('Баланс пользователя: ')
    displayDict(balance_user)
    print('Баланс терминала: ')
    displayDict(balance_terminal)
    print('Текущий курс: ')
    displayDict(courses)
    
# Функция для вывода словарей
def displayDict(dict):
    for currency, amount in dict.items():
        print(f"    {currency}: {amount}")

# Ввод
def getInput():
    while True:
        try:
            command = input('Выберите действие: buy <тип обмена> <значение>, sell <тип обмена> <значение>, quit: ').strip()
            if command == 'quit':
                return None, None, None
            
            action, course, amount = command.split()
            amount = float(amount)
            return action, course.upper(), amount
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите в формате: действие курс сумма.")
            continue

# Функция обмена
def trade(course, amount, action):
    if course not in courses:
        print(f"Неверный курс {course}.")
        return False

    from_value = course.split('-')[0]
    to_value = course.split('-')[1]
    # Покупка
    if action == 'buy':
        if amount <= 0:
            print("Сумма должна быть больше 0.")
            return False
            
        value = round(amount * courses[course], 2)

        if balance_terminal[to_value] < amount:
            print("Недостаточно средств у терминала.")
            return False
        
        if balance_user[from_value] < value:
            print("Недостаточно средств у пользователя.")
            return False

        balance_terminal[to_value] -= amount
        balance_user[to_value] += amount
        balance_user[from_value] -= value
        balance_terminal[from_value] += value
        
        print(f"Куплено {amount} {to_value}.")
        return True
    # Продажа
    elif action == 'sell':
        value = round(amount / courses[course], 2)

        if balance_user[from_value] < amount:
            print("Недостаточно средств у пользователя.")
            return False

        if balance_terminal[to_value] < value:
            print("Недостаточно средств у терминала.")
            return False
        
        balance_user[from_value] -= amount
        balance_terminal[from_value] += amount
        balance_terminal[to_value] -= value
        balance_user[to_value] += value
        
        print(f"Продано {amount} {from_value}.")
        return True
    else:
        print(f"Неверная операция {action}.")
        return False

# Изменение курса
def change():
    for course, amount in courses.items():
        changed = 1 + round(random.randint(-5, 5) / 100, 2)
        courses[course] = round(amount * changed, 2)

# Функция main
def main():
    while True:
        PrintMenu()
        action, course, amount = getInput()
        if action is None:  # Если ввели quit
            print("Выход из программы.")
            break
        success = trade(course, amount, action)  
        if success:
            change()  # Изменяем курсы только при успешной сделке


if __name__ == '__main__':
    main()