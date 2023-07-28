import tkinter as tk

# Initialize the board
board = [
    [' ', 'b', ' ', 'b', ' ', 'b', ' ', 'b'],
    ['b', ' ', 'b', ' ', 'b', ' ', 'b', ' '],
    [' ', 'b', ' ', 'b', ' ', 'b', ' ', 'b'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['r', ' ', 'r', ' ', 'r', ' ', 'r', ' '],
    [' ', 'r', ' ', 'r', ' ', 'r', ' ', 'r'],
    ['r', ' ', 'r', ' ', 'r', ' ', 'r', ' ']
]

# Initialize Tkinter
root = tk.Tk()
root.title("Checkers")

# Define the dimensions of the checkers board
canvas_width = 400
canvas_height = 400

# Calculate the size of each square on the board
square_size = canvas_width // 8

# Create the canvas
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

# Initialize the selected piece variable
selected_piece = None

# Function to draw the checkers board
def draw_board():
    canvas.delete("all")  # Clear the canvas
    for row in range(8):
        for col in range(8):
            x1 = col * square_size
            y1 = row * square_size
            x2 = x1 + square_size
            y2 = y1 + square_size
            color = "white" if (row + col) % 2 == 0 else "gray"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)

# Function to draw the checkers pieces
def draw_pieces():
    for row in range(8):
        for col in range(8):
            x = col * square_size + square_size // 2
            y = row * square_size + square_size // 2
            if board[row][col] == 'r':
                canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="red")
            elif board[row][col] == 'b':
                canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="black")
            elif board[row][col] == 'R':
                canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="red", outline="white", width=2)
            elif board[row][col] == 'B':
                canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="black", outline="white", width=2)

# Function to check if a move is valid
def is_valid_move(player, start_row, start_col, end_row, end_col):
    # Check if the move is within the bounds of the board
    if end_row < 0 or end_row >= 8 or end_col < 0 or end_col >= 8:
        return False

    # Check if the destination is empty
    if board[end_row][end_col] != ' ':
        return False

    # Check if the player is moving their own piece
    if player == 'r' and board[start_row][start_col] != 'r' and board[start_row][start_col] != 'R':
        return False
    elif player == 'b' and board[start_row][start_col] != 'b' and board[start_row][start_col] != 'B':
        return False

    # Check if the move is diagonal
    row_diff = end_row - start_row
    col_diff = end_col - start_col


    # Check if the move is in the correct direction for regular pieces
    if player == 'r' and row_diff > 0:
        return False
    elif player == 'b' and row_diff < 0:
        return False

    return True

# Function to make a move
def make_move(player, start_row, start_col, end_row, end_col):
    # Move the piece to the destination
    board[end_row][end_col] = board[start_row][start_col]
    board[start_row][start_col] = ' '

    # Check if a piece should be promoted to a king
    if player == 'r' and end_row == 0:
        board[end_row][end_col] = 'R'
    elif player == 'b' and end_row == 7:
        board[end_row][end_col] = 'B'

    # Check if a piece was captured
    if abs(start_row - end_row) == 2:
        captured_row = (start_row + end_row) // 2
        captured_col = (start_col + end_col) // 2
        board[captured_row][captured_col] = ' '

# Function to check if a player has won
def has_won(player):
    # Check if all of the opponent's pieces have been captured
    if player == 'r':
        opponent = 'b'
    else:
        opponent = 'r'

    for row in range(8):
        for col in range(8):
            if board[row][col] == opponent or board[row][col] == opponent.upper():
                return False

    return True

# Function to handle click events
def handle_click(event):
    # Get the row and column based on the click position
    col = event.x // square_size
    row = event.y // square_size

    # Check if a piece is selected
    global selected_piece
    if selected_piece is None:
        if board[row][col] == ' ':
            return
        selected_piece = (row, col)
    else:
        start_row, start_col = selected_piece
        # Check if the move is valid
        if is_valid_move(board[start_row][start_col], start_row, start_col, row, col):
            make_move(board[start_row][start_col], start_row, start_col, row, col)
            selected_piece = None
            # Check if the current player has won
            if has_won(board[row][col]):
                winner = "Red" if board[row][col] in ['r', 'R'] else "Black"
                print(f"{winner} player has won!")
        else:
            selected_piece = None
    # Redraw the board and pieces
    draw_board()
    draw_pieces()

# Bind the click event to the canvas
canvas.bind("<Button-1>", handle_click)

# Draw the initial board and pieces
draw_board()
draw_pieces()

# Start the Tkinter event loop
root.mainloop()
