# Huffman coding

# Create a dictionary of symbols and their frequencies
symbols = {'B': 8, 'F': 2, 'G': 7, 'H': 5, 'D': 2, 'A': 2, 'E': 2, 'C': 6}

# Sort the symbols by frequency
sorted_symbols = sorted(symbols.items(), key=lambda x: x[1], reverse=True)

# Create a list of symbols
symbol_list = [x[0] for x in sorted_symbols]

# Create a list of frequencies
frequency_list = [x[1] for x in sorted_symbols]

# Create a list of cumulative frequencies
cumulative_frequency_list = [sum(frequency_list[:i+1]) for i in range(len(frequency_list))]

# Create a dictionary of symbols and their codes
code_dict = {}

# Generate codes for each symbol
while len(symbol_list) > 1:
    # Find the two symbols with the lowest frequencies
    symbol1 = symbol_list[0]
    symbol2 = symbol_list[1]

    # Create a new symbol with the combined frequency of the two symbols
    new_symbol = symbol1 + symbol2
    new_frequency = frequency_list[0] + frequency_list[1]

    # Generate codes for the two symbols
    code_dict[symbol1] = '0'
    code_dict[symbol2] = '1'

    # Remove the two symbols from the list
    symbol_list.remove(symbol1)
    symbol_list.remove(symbol2)

    # Add the new symbol to the list
    symbol_list.append(new_symbol)

    # Add the new frequency to the list
    frequency_list.append(new_frequency)

    # Sort the symbols by frequency
    sorted_symbols = sorted(zip(symbol_list, frequency_list), key=lambda x: x[1], reverse=True)

    # Update the lists
    symbol_list = [x[0] for x in sorted_symbols]
    frequency_list = [x[1] for x in sorted_symbols]
    cumulative_frequency_list = [sum(frequency_list[:i+1]) for i in range(len(frequency_list))]

# Generate the code for the last symbol
code_dict[symbol_list[0]] = '0'

# Print the codes
print('Symbol\tCode')
for symbol, code in code_dict.items():
    print(f'{symbol}\t{code}')

# Encode the message
encoded_message = ''
for symbol in 'BFGFBGBGBHGBDAEDACBCBGHAFHAECBHGGFHFGHBBBCCBCBCCCBBCBCBC':
    encoded_message += code_dict[symbol]

print(f'Encoded message: {encoded_message}')