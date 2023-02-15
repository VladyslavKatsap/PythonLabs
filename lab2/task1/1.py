list_of_numbers = [1, 0, 0, 1, 1, 2, -2]

length = 0
max_ratio = float('-inf')
while True:
    try:
        list_of_numbers[length]
        length += 1

    except IndexError:
        print(f" list- {length}")
        break
for i in range(length):
    for j in range(length):
        try:
            ratio = list_of_numbers[j] / list_of_numbers[i]
            if ratio > max_ratio:
                max_ratio = ratio
        except ZeroDivisionError:
            pass

print(f" max  - {max_ratio}")