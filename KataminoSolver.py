import numpy as np
import json


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


# Main function
def main():
    # Load settings from a JSON file
    with open("settings.json", "r") as settings_file:
        settings = json.load(settings_file)

    n_rows = settings["n_rows"]
    n_cols = settings["n_cols"]
    pieces = [np.array(piece) for piece in settings["pieces"]]

    # Create an empty array of size n_rows by n_cols filled with zeros
    empty_array = np.zeros((n_rows, n_cols), dtype=int)
    puzzle_board = empty_array

    # Solve the Katamino puzzle and print the result.
    solution = solve_katamino(puzzle_board.copy(), pieces)
    if solution is not None:
        print("Solution:")
        print(solution)
    else:
        print("No solution found.")


# Run the main function if this script is executed
if __name__ == "__main__":
    main()
