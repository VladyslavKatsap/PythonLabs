import mymodule as m

matrix1 = m.read_matrix_from_file("matr.txt")

m.print_matrix(matrix1)

# vector = []
# for i in range(5):
#    value = int(input("Enter value for element " + str(i) + ": "))
#    vector.append(value)

# print(m.matrix_vector_multiply(matrix1, vector))

a = int(input("Enter value for А = "))
row = int(input("Enter row = "))
print(m.matrix_row_multiply(matrix1, row, a))
m.print_matrix(matrix1)
