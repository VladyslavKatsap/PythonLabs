# Function for reading a matrix from a text file without using classes
def read_matrix_from_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        rows = len(lines)
        cols = len(lines[0].split())
        matrix = [[0 for i in range(cols)] for j in range(rows)]
        for i in range(rows):
            line = lines[i].split()
            for j in range(cols):
                matrix[i][j] = int(line[j])
        return matrix

# Function for printing a matrix without using classes
def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            print(matrix[i][j], end=' ')
        print()

# Function for multiplying a matrix by a vector without using classes
def matrix_vector_multiply(matrix, vector):
    result = [0 for i in range(len(matrix))]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            result[i] += matrix[i][j] * vector[j]
    return result

# Function for multiplying the i-th row of a matrix by a number a without using classes
def matrix_row_multiply(matrix, i, a):
    result = [0 for j in range(len(matrix[0]))]
    for j in range(len(matrix[0])):
        result[j] = matrix[i][j] * a
    return result