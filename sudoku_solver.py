import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
from collections import deque

class SudokuSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.geometry("600x700")
        self.is_dark_mode = False
        self.theme_colors = {
            'light': {
                'bg': '#f0f0f0',
                'fg': '#333333',
                'cell_bg': 'white',
                'grid_bg': '#333333',
                'solver_bg': '#E8F5E9',
                'solver_fg': '#2E7D32',
                'user_bg': '#E3F2FD',
                'user_fg': '#1565C0'
            },
            'dark': {
                'bg': '#1a1a1a',
                'fg': '#ffffff',
                'cell_bg': '#2d2d2d',
                'grid_bg': '#404040',
                'solver_bg': '#1B5E20',
                'solver_fg': '#A5D6A7',
                'user_bg': '#0D47A1',
                'user_fg': '#90CAF9'
            }
        }
        
        # Initialize timer variables
        self.start_time = None
        self.timer_running = False
        self.timer_label = None
        
        # Initialize undo/redo stacks
        self.undo_stack = deque(maxlen=100)  # Store last 100 moves
        self.redo_stack = deque(maxlen=100)
        
        self.setup_ui()
    
    def setup_ui(self):
        self.root.configure(bg=self.get_theme_color('bg'))
        
        # Style configuration
        self.style = ttk.Style()
        self.style.configure('TButton', 
                           font=('Arial', 12),
                           padding=10)
        
        # Create the main frame with padding
        self.main_frame = tk.Frame(self.root, bg=self.get_theme_color('bg'))
        self.main_frame.pack(pady=20, padx=20)
        
        # Title and timer frame
        self.title_frame = tk.Frame(self.main_frame, bg=self.get_theme_color('bg'))
        self.title_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title label
        self.title_label = tk.Label(self.title_frame,
                                  text="Sudoku Solver",
                                  font=('Arial', 24, 'bold'),
                                  bg=self.get_theme_color('bg'),
                                  fg=self.get_theme_color('fg'))
        self.title_label.pack(side=tk.LEFT)
        
        # Timer label
        self.timer_label = tk.Label(self.title_frame,
                                  text="Time: 0:00",
                                  font=('Arial', 14),
                                  bg=self.get_theme_color('bg'),
                                  fg=self.get_theme_color('fg'))
        self.timer_label.pack(side=tk.RIGHT)
        
        # Create the 9x9 grid
        self.cells = {}
        self.original_values = {}
        self.create_grid()
        
        # Create buttons with modern styling
        self.button_frame = tk.Frame(self.root, bg=self.get_theme_color('bg'))
        self.button_frame.pack(pady=20)
        
        # Base button style
        button_style = {
            'font': ('Arial', 12, 'bold'),
            'borderwidth': 0,
            'padx': 20,
            'pady': 10,
            'cursor': 'hand2',
            'fg': 'white',
            'activeforeground': 'white',
            'relief': 'raised',
            'highlightthickness': 2
        }
        
        # Theme toggle button
        self.theme_button = tk.Button(self.button_frame,
                                    text="🌙 Dark Mode" if not self.is_dark_mode else "☀️ Light Mode",
                                    command=self.toggle_theme,
                                    **{**button_style,
                                       'bg': '#6A1B9A',  # Purple
                                       'activebackground': '#4A148C',
                                       'highlightbackground': '#4A148C'})
        self.theme_button.pack(side=tk.LEFT, padx=5)
        
        # Undo/Redo buttons
        self.undo_button = tk.Button(self.button_frame,
                                   text="↩️ Undo",
                                   command=self.undo_move,
                                   **{**button_style,
                                      'bg': '#FF9800',  # Orange
                                      'activebackground': '#F57C00',
                                      'highlightbackground': '#F57C00'})
        self.undo_button.pack(side=tk.LEFT, padx=5)
        
        self.redo_button = tk.Button(self.button_frame,
                                   text="↪️ Redo",
                                   command=self.redo_move,
                                   **{**button_style,
                                      'bg': '#FF9800',  # Orange
                                      'activebackground': '#F57C00',
                                      'highlightbackground': '#F57C00'})
        self.redo_button.pack(side=tk.LEFT, padx=5)
        
        # Action buttons
        self.solve_button = tk.Button(self.button_frame,
                                    text="Solve",
                                    command=self.solve_puzzle,
                                    **{**button_style,
                                       'bg': '#4CAF50',  # Green
                                       'activebackground': '#388E3C',
                                       'highlightbackground': '#388E3C'})
        self.solve_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = tk.Button(self.button_frame,
                                    text="Reset",
                                    command=self.reset_board,
                                    **{**button_style,
                                       'bg': '#F44336',  # Red
                                       'activebackground': '#D32F2F',
                                       'highlightbackground': '#D32F2F'})
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        self.generate_button = tk.Button(self.button_frame,
                                       text="Generate",
                                       command=self.generate_puzzle,
                                       **{**button_style,
                                          'bg': '#2196F3',  # Blue
                                          'activebackground': '#1976D2',
                                          'highlightbackground': '#1976D2'})
        self.generate_button.pack(side=tk.LEFT, padx=5)
        
        # Initialize the board
        self.reset_board()
    
    def get_theme_color(self, key):
        theme = 'dark' if self.is_dark_mode else 'light'
        return self.theme_colors[theme][key]
    
    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.theme_button.config(text="☀️ Light Mode" if self.is_dark_mode else "🌙 Dark Mode")
        self.apply_theme()
    
    def apply_theme(self):
        # Update root and frames
        self.root.configure(bg=self.get_theme_color('bg'))
        self.main_frame.configure(bg=self.get_theme_color('bg'))
        self.title_frame.configure(bg=self.get_theme_color('bg'))
        self.button_frame.configure(bg=self.get_theme_color('bg'))
        
        # Update title and timer
        self.title_label.configure(bg=self.get_theme_color('bg'), fg=self.get_theme_color('fg'))
        self.timer_label.configure(bg=self.get_theme_color('bg'), fg=self.get_theme_color('fg'))
        
        # Update grid
        for i in range(9):
            for j in range(9):
                cell = self.cells[(i, j)]
                if cell.get():
                    if (i, j) in self.original_values and self.original_values[(i, j)] != 0:
                        cell.config(bg=self.get_theme_color('user_bg'),
                                  fg=self.get_theme_color('user_fg'))
                    else:
                        cell.config(bg=self.get_theme_color('solver_bg'),
                                  fg=self.get_theme_color('solver_fg'))
                else:
                    cell.config(bg=self.get_theme_color('cell_bg'),
                              fg=self.get_theme_color('fg'))
    
    def create_grid(self):
        # Create a frame for the grid with a subtle shadow effect
        grid_frame = tk.Frame(self.main_frame,
                            bg=self.get_theme_color('grid_bg'),
                            padx=2,
                            pady=2)
        grid_frame.pack()
        
        for i in range(9):
            for j in range(9):
                # Create a frame for each cell with darker borders
                cell_frame = tk.Frame(grid_frame,
                                    bg=self.get_theme_color('grid_bg'),
                                    highlightbackground=self.get_theme_color('grid_bg'),
                                    highlightthickness=1)
                cell_frame.grid(row=i, column=j, padx=1, pady=1)
                
                # Create entry widget with improved styling
                entry = tk.Entry(cell_frame,
                               width=2,
                               font=('Arial', 20, 'bold'),
                               justify='center',
                               bg=self.get_theme_color('cell_bg'),
                               fg=self.get_theme_color('fg'),
                               relief='flat',
                               borderwidth=0)
                entry.pack(expand=True, fill='both')
                
                # Add validation and bindings
                entry.config(validate="key",
                           validatecommand=(entry.register(self.validate_input), '%P'))
                entry.bind('<KeyRelease>', lambda e, i=i, j=j: self.on_cell_change(i, j))
                
                # Store the entry widget
                self.cells[(i, j)] = entry
                
                # Add thicker borders for 3x3 boxes
                if i % 3 == 0 and i != 0:
                    cell_frame.config(highlightthickness=2)
                if j % 3 == 0 and j != 0:
                    cell_frame.config(highlightthickness=2)
    
    def on_cell_change(self, i, j):
        value = self.cells[(i, j)].get()
        if value:
            self.undo_stack.append((i, j, value))
            self.redo_stack.clear()  # Clear redo stack on new move
            self.cells[(i, j)].config(bg=self.get_theme_color('user_bg'),
                                    fg=self.get_theme_color('user_fg'))
    
    def undo_move(self):
        if self.undo_stack:
            i, j, value = self.undo_stack.pop()
            self.redo_stack.append((i, j, self.cells[(i, j)].get()))
            self.cells[(i, j)].delete(0, tk.END)
            self.cells[(i, j)].config(bg=self.get_theme_color('cell_bg'),
                                    fg=self.get_theme_color('fg'))
    
    def redo_move(self):
        if self.redo_stack:
            i, j, value = self.redo_stack.pop()
            self.undo_stack.append((i, j, value))
            self.cells[(i, j)].delete(0, tk.END)
            self.cells[(i, j)].insert(0, value)
            self.cells[(i, j)].config(bg=self.get_theme_color('user_bg'),
                                    fg=self.get_theme_color('user_fg'))
    
    def start_timer(self):
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()
    
    def stop_timer(self):
        self.timer_running = False
    
    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            self.timer_label.config(text=f"Time: {minutes}:{seconds:02d}")
            self.root.after(1000, self.update_timer)
    
    def validate_input(self, value):
        if value == "":
            return True
        if len(value) > 1:
            return False
        if value.isdigit() and 1 <= int(value) <= 9:
            return True
        return False
    
    def get_board(self):
        board = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                value = self.cells[(i, j)].get()
                if value:
                    board[i][j] = int(value)
        return board
    
    def set_board(self, board, highlight_changes=False):
        # Store original values if we're going to highlight changes
        if highlight_changes:
            self.original_values = {}
            for i in range(9):
                for j in range(9):
                    self.original_values[(i, j)] = board[i][j]
        
        for i in range(9):
            for j in range(9):
                value = board[i][j]
                cell = self.cells[(i, j)]
                cell.delete(0, tk.END)
                
                if value != 0:
                    cell.insert(0, str(value))
                    if highlight_changes and (i, j) in self.original_values and self.original_values[(i, j)] == 0:
                        cell.config(bg=self.get_theme_color('solver_bg'),
                                  fg=self.get_theme_color('solver_fg'))
                    else:
                        cell.config(bg=self.get_theme_color('user_bg'),
                                  fg=self.get_theme_color('user_fg'))
                else:
                    cell.config(bg=self.get_theme_color('cell_bg'),
                              fg=self.get_theme_color('fg'))
    
    def is_valid(self, board, row, col, num):
        # Check row
        for x in range(9):
            if board[row][x] == num:
                return False
        
        # Check column
        for x in range(9):
            if board[x][col] == num:
                return False
        
        # Check 3x3 box
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if board[i + start_row][j + start_col] == num:
                    return False
        
        return True
    
    def solve(self, board):
        empty = self.find_empty(board)
        if not empty:
            return True
        
        row, col = empty
        for num in range(1, 10):
            if self.is_valid(board, row, col, num):
                board[row][col] = num
                if self.solve(board):
                    return True
                board[row][col] = 0
        
        return False
    
    def find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None
    
    def solve_puzzle(self):
        board = self.get_board()
        if not self.is_valid_board(board):
            messagebox.showerror("Error", "Invalid Sudoku puzzle!")
            return
        
        if self.solve(board):
            self.set_board(board, highlight_changes=True)
            messagebox.showinfo("Success", "Puzzle solved!")
        else:
            messagebox.showerror("Error", "No solution exists!")
    
    def is_valid_board(self, board):
        # Check rows
        for row in board:
            seen = set()
            for num in row:
                if num != 0:
                    if num in seen:
                        return False
                    seen.add(num)
        
        # Check columns
        for col in range(9):
            seen = set()
            for row in range(9):
                num = board[row][col]
                if num != 0:
                    if num in seen:
                        return False
                    seen.add(num)
        
        # Check 3x3 boxes
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                seen = set()
                for i in range(3):
                    for j in range(3):
                        num = board[box_row + i][box_col + j]
                        if num != 0:
                            if num in seen:
                                return False
                            seen.add(num)
        
        return True
    
    def reset_board(self):
        self.stop_timer()
        self.timer_label.config(text="Time: 0:00")
        self.undo_stack.clear()
        self.redo_stack.clear()
        for i in range(9):
            for j in range(9):
                cell = self.cells[(i, j)]
                cell.delete(0, tk.END)
                cell.config(bg=self.get_theme_color('cell_bg'),
                          fg=self.get_theme_color('fg'))
    
    def generate_puzzle(self):
        # Create a solved board
        board = [[0 for _ in range(9)] for _ in range(9)]
        self.solve(board)
        
        # Remove numbers to create a puzzle
        cells_to_remove = random.randint(40, 50)  # Adjust difficulty here
        positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(positions)
        
        for i, j in positions[:cells_to_remove]:
            board[i][j] = 0
        
        self.set_board(board)
        self.start_timer()  # Start timer when puzzle is generated

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolver(root)
    root.mainloop() 