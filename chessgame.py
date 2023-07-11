import speech_recognition as sr
import chess
import chess.engine
import tkinter as tk

board = chess.Board()

LIGHT_COLOR = "#F0D9B5"
DARK_COLOR = "#B58863"
HIGHLIGHT_COLOR = "#7EF69C"

PIECE_UNICODE = {
    chess.PAWN: "\u2659",
    chess.KNIGHT: "\u2658",
    chess.BISHOP: "\u2657",
    chess.ROOK: "\u2656",
    chess.QUEEN: "\u2655",
    chess.KING: "\u2654"
}

previous_move_squares = set()

def draw_square(square):
    piece = board.piece_at(square)

    row = chess.square_rank(square)
    col = chess.square_file(square)
    x = col * square_size
    y = (7 - row) * square_size

    if (row + col) % 2 == 0:
        color = LIGHT_COLOR
    else:
        color = DARK_COLOR

    if square in previous_move_squares:
        color = HIGHLIGHT_COLOR

    canvas.create_rectangle(x, y, x + square_size, y + square_size, fill=color)

    if piece is not None:
        unicode_piece = PIECE_UNICODE.get(piece.piece_type, "")
        piece_color = "black" if piece.color == chess.BLACK else "white"
        canvas.create_text(x + square_size // 2, y + square_size // 2, anchor="center", text=unicode_piece,
                           font=("Arial", square_size // 2), fill=piece_color)

def draw_board():
    canvas.delete("all")

    for col in range(8):
        x = col * square_size + square_size // 2
        y = 8 * square_size + square_size // 4
        canvas.create_text(x, y, text=chr(ord('a') + col), font=("Arial", square_size // 4, "bold"), fill="black")

    for row in range(8):
        x = 8 * square_size + square_size // 4
        y = (7 - row) * square_size + square_size // 2
        canvas.create_text(x, y, text=str(row + 1), font=("Arial", square_size // 4, "bold"), fill="black")

    for square in chess.SQUARES:
        draw_square(square)

def getinput():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say your move:")
        audio = r.listen(source)

    try:
        move_text = r.recognize_google(audio)
        print("You said:", move_text)
        move_text = move_text.replace(" ", "")
        return move_text.lower()
    except sr.UnknownValueError:
        print("Unable to recognize speech! Try again.")
        return None
    except sr.RequestError as e:
        print("Speech recognition request error:", str(e))
        return None

def validate_move(move_text):
    try:
        move = chess.Move.from_uci(move_text)
        if move in board.legal_moves:
            return move
        else:
            print("Invalid move! Try again.")
            return None
    except ValueError:
        print("Invalid move format! Try again.")
        return None

def getcomputermove():
    with chess.engine.SimpleEngine.popen_uci("C:\\Users\\adhab\\Downloads\\stockfish-windows-x86-64\\stockfish\\stockfish-windows-x86-64.exe") as engine:
        result = engine.play(board, chess.engine.Limit(time=2.0))
        return result.move

def usermove():
    global previous_move_squares

    user_move = None
    while user_move is None:
        user_input = getinput()
        if user_input is not None:
            user_move = validate_move(user_input)

    previous_move_squares = {user_move.from_square, user_move.to_square}

    board.push(user_move)
    draw_board()
    root.after(1500, computermove)

def computermove():
    global previous_move_squares
    ai_move = getcomputermove()
    previous_move_squares = {ai_move.from_square, ai_move.to_square}
    board.push(ai_move)
    draw_board()
    root.after(1500,usermove)

root = tk.Tk()
root.title("Chess Game")
square_size = 50

canvas = tk.Canvas(root, width=square_size * 9, height=square_size * 9)
canvas.pack()

draw_board()

root.after(100,usermove)
root.mainloop()
