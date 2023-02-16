
# Shannon-Fano coding

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
for i in range(len(symbol_list)):
    code = ''
    for j in range(i):
        if cumulative_frequency_list[j] < cumulative_frequency_list[i]:
            code += '1'
        else:
            code += '0'
    code_dict[symbol_list[i]] = code

# Print the codes
print('Symbol\tCode')
for symbol, code in code_dict.items():
    print(f'{symbol}\t{code}')

# Encode the message
encoded_message = ''
for symbol in 'BFGFBGBGBHGBDAEDACBCBGHAFHAECBHGGFHFGHBBBCCBCBCCCBBCBCBC':
    encoded_message += code_dict[symbol]

print(f'Encoded message: {encoded_message}')
