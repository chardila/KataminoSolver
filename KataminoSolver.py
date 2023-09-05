import json
import numpy as np


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


def load_puzzle_settings(filename):
    try:
        with open(filename, 'r') as file:
            settings = json.load(file)
            return settings
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def print_solution(solution):
    print(solution)


# Main function
def create_puzzle_board(n_rows, n_cols):
    """
    Create an empty array of size n_rows by n_cols filled with zeros.

    Args:
        n_rows (int): The number of rows in the puzzle board.
        n_cols (int): The number of columns in the puzzle board.

    Returns:
        numpy.ndarray: The puzzle board array.
    """
    return np.zeros((n_rows, n_cols), dtype=int)


def solve_katamino_puzzle(puzzle_board, pieces):
    """
    Solve the Katamino puzzle.

    Args:
        puzzle_board (numpy.ndarray): The puzzle board array.
        pieces (list): The list of puzzle pieces.

    Returns:
        numpy.ndarray or None: The solution if found, None otherwise.
    """
    return solve_katamino(puzzle_board.copy(), pieces)


def main():
    """
    Main function to load puzzle settings, create the puzzle board, solve the Katamino puzzle, and print the result.
    """
    # Load settings from a JSON file
    settings_filename = "settings.json"
    puzzle_settings = load_puzzle_settings(settings_filename)

    if puzzle_settings is None:
        print(f"Unable to load puzzle settings from '{settings_filename}'.")
        return

    n_rows = puzzle_settings.get("n_rows")
    n_cols = puzzle_settings.get("n_cols")

    if n_rows is None or n_cols is None:
        print("The 'n_rows' or 'n_cols' key is missing in the puzzle settings.")
        return

    if "pieces" not in puzzle_settings:
        print("The 'pieces' key is missing in the puzzle settings.")
        return

    pieces = [np.array(piece) for piece in puzzle_settings["pieces"]]

    # Create the puzzle board
    puzzle_board = create_puzzle_board(n_rows, n_cols)

    # Solve the Katamino puzzle and print the result.
    solution = solve_katamino_puzzle(puzzle_board, pieces)
    if solution is not None:
        print("Solution:")
        print_solution(solution)
    else:
        print("No solution found.")


# Run the main function if this script is executed
if __name__ == "__main__":
    main()
