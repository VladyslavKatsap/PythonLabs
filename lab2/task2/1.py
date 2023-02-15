# Initialize counters
runtime_error_count = 0
type_error_count = 0
value_error_count = 0

# Get input from the user
while True:
    user_input = input("Enter a number (or 'done' to finish): ")
    if user_input == "done":
        break
    else:
        try:
            number = int(user_input)
            if number > 9:
                raise RuntimeError
            elif number < 0:
                raise TypeError
            elif number >= 0 and number <= 9:
                raise ValueError
        except RuntimeError:
            runtime_error_count += 1
        except TypeError:
            type_error_count += 1
        except ValueError:
            value_error_count += 1

# Print the counts
print("RuntimeError count:", runtime_error_count)
print("TypeError count:", type_error_count)
print("ValueError count:", value_error_count)