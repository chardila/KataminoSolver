import numpy as np

# Define the Katamino puzzle board as a binary matrix.
# Use 0 for empty cells and 1 for filled cells.
# Replace this with the actual puzzle configuration.
# Example: Puzzle 'Super Slam 11A'

n = 5  # Number of rows
m = 5  # Number of columns

# Create an empty array of size n by m filled with zeros
empty_array = np.zeros((n, m))

puzzle_board = empty_array

# Define the Katamino puzzle pieces as a list of binary matrices.
# Replace this with the actual pieces for your puzzle.
# Example: Puzzle 'Super Slam 11A'
pieces = [
    np.array([
        [1, 1],
        [1, 1]
    ]),
    np.array([
        [1, 1],
        [1, 1]
    ]),
    np.array([
        [1, 1, 1],
        [1, 1, 1]
    ]),
    np.array([
        [1, 1, 1],
        [1, 1, 1]
    ]),
    np.array([
        [1, 1, 1, 1, 1],
    ]),
    # Add more pieces...
]


# Define a function to rotate a piece 90 degrees.
def rotate_piece(piece):
    return np.rot90(piece)


# Define a function to mirror a piece.
def mirror_piece(piece):
    return np.fliplr(piece)


# Function to check if a piece can be placed on the board at a given position.
def can_place(board, piece, x, y):
    height, width = piece.shape
    return all(
        0 <= x + i < board.shape[1] and 0 <= y + j < board.shape[0]
        and (piece[j, i] == 0 or board[y + j, x + i] == 0)
        for i in range(width)
        for j in range(height)
    )


# Function to place a piece on the board at a given position.
def place_piece(board, piece, x, y):
    board[y:y + piece.shape[0], x:x + piece.shape[1]] += piece


# Function to remove a piece from the board at a given position.
def remove_piece(board, piece, x, y):
    board[y:y + piece.shape[0], x:x + piece.shape[1]] -= piece


# Function to find the next empty cell on the board.
def find_empty_cell(board):
    for y in range(board.shape[0]):
        for x in range(board.shape[1]):
            if board[y, x] == 0:
                return x, y
    return None


# Function to solve the Katamino puzzle using Algorithm X.
def solve_katamino(board, pieces_parameter):
    if np.count_nonzero(board) == board.size:
        return board  # Puzzle is already solved

    cell = find_empty_cell(board)
    if cell is None:
        return None  # No empty cells left but not solved

    x, y = cell
    for piece in pieces_parameter:
        for _ in range(4):  # Rotate the piece 4 times
            if can_place(board, piece, x, y):
                place_piece(board, piece, x, y)
                solution_parameter = solve_katamino(board, pieces_parameter)
                if solution_parameter is not None:
                    return solution_parameter
                remove_piece(board, piece, x, y)
            piece = rotate_piece(piece)
        mirror_piece(piece)

    return None  # No solution found


# Solve the Katamino puzzle and print the result.
solution = solve_katamino(puzzle_board.copy(), pieces)
if solution is not None:
    print("Solution:")
    print(solution)
else:
    print("No solution found.")
