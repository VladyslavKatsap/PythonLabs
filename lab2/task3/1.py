while True:
    try:
        num1 = float(input("Введіть перший операнд: "))
        op = input("Введіть символ операції (+, -, *, /): ")
        num2 = float(input("Введіть другий операнд: "))
        if op == "+":
            result = num1 + num2
        elif op == "-":
            result = num1 - num2
        elif op == "*":
            result = num1 * num2
        elif op == "/":
            if num2 == 0:
                print("Ділення на нуль неможливе!")
                continue
            else:
                result = num1 / num2
        else:
            print("Неправильний символ операції!")
            continue
        print("Результат обчислення виразу:", result)
    except ValueError:
        print("Неправильний формат операндів!")
        continue
    break