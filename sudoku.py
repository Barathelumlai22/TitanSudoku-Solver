import tkinter as tk
from tkinter import messagebox

# ---------- Sudoku Logic (same as yours) ----------

def is_valid(board, row, col, num):
    """
    Checks if placing 'num' at (row, col) is a valid move.
    """
    # Check row
    if num in board[row]:
        return False

    # Check column
    if num in [board[i][col] for i in range(9)]:
        return False

    # Check 3x3 box
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True


def find_empty_location(board):
    """
    Finds the next empty location (0) in the board.
    """
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None, None


def solve_sudoku(board):
    """
    Solves the Sudoku puzzle using a backtracking algorithm.
    """
    row, col = find_empty_location(board)

    # If there are no empty locations, the puzzle is solved
    if row is None:
        return True

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num

            if solve_sudoku(board):
                return True

            # Backtrack
            board[row][col] = 0

    return False


# ---------- GUI ----------

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")

        # Optional: window background color
        self.root.configure(bg="#1e1e1e")

        title_label = tk.Label(
            root,
            text="Sudoku Solver",
            font=("Helvetica", 20, "bold"),
            bg="#1e1e1e",
            fg="white"
        )
        title_label.pack(pady=10)

        # Frame that holds the whole 9x9 grid
        grid_frame = tk.Frame(root, bg="#1e1e1e")
        grid_frame.pack(padx=10, pady=10)

        self.entries = []  # 9x9 list of Entry widgets

        # Create 3x3 big blocks (with thick borders)
        self.blocks = [[None for _ in range(3)] for _ in range(3)]

        for br in range(3):  # block row
            for bc in range(3):  # block col
                block = tk.Frame(
                    grid_frame,
                    bd=3,              # thick border
                    relief="solid",
                    bg="#1e1e1e"
                )
                block.grid(row=br, column=bc, padx=4, pady=4)
                self.blocks[br][bc] = block

        # Now create the 9x9 entries inside those blocks
        for r in range(9):
            row_entries = []
            for c in range(9):
                block_row = r // 3
                block_col = c // 3
                block = self.blocks[block_row][block_col]

                e = tk.Entry(
                    block,
                    width=2,
                    font=("Helvetica", 18),
                    justify="center",
                    relief="flat"
                )
                # Position inside its 3x3 block
                local_row = r % 3
                local_col = c % 3
                e.grid(row=local_row, column=local_col, padx=2, pady=2)
                row_entries.append(e)
            self.entries.append(row_entries)

        # Bottom button frame
        button_frame = tk.Frame(root, bg="#1e1e1e")
        button_frame.pack(pady=10)

        solve_button = tk.Button(
            button_frame,
            text="Solve",
            command=self.solve,
            font=("Helvetica", 12, "bold"),
            width=10
        )
        solve_button.grid(row=0, column=0, padx=10)

        clear_button = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear,
            font=("Helvetica", 12, "bold"),
            width=10
        )
        clear_button.grid(row=0, column=1, padx=10)

    def get_board_from_gui(self):
        """
        Read numbers from the Entry widgets and build a 9x9 board.
        Empty cells or invalid inputs are treated as 0.
        """
        board = []
        for r in range(9):
            row = []
            for c in range(9):
                val = self.entries[r][c].get().strip()
                if val == "" or val == ".":
                    row.append(0)
                else:
                    try:
                        num = int(val)
                        if 0 <= num <= 9:
                            row.append(num)
                        else:
                            messagebox.showerror("Invalid Input", "Please enter numbers between 0 and 9.")
                            return None
                    except ValueError:
                        messagebox.showerror("Invalid Input", "Please enter only numbers.")
                        return None
            board.append(row)
        return board

    def fill_gui_from_board(self, board):
        """
        Put board numbers back into Entry widgets.
        """
        for r in range(9):
            for c in range(9):
                self.entries[r][c].delete(0, tk.END)
                if board[r][c] != 0:
                    self.entries[r][c].insert(0, str(board[r][c]))

    def solve(self):
        """
        Handler for Solve button.
        """
        board = self.get_board_from_gui()
        if board is None:
            return  # invalid input handled already

        if solve_sudoku(board):
            self.fill_gui_from_board(board)
            messagebox.showinfo("Success", "Sudoku solved!")
        else:
            messagebox.showinfo("No Solution", "No solution exists for this puzzle.")

    def clear(self):
        """
        Clear all entries.
        """
        for r in range(9):
            for c in range(9):
                self.entries[r][c].delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
