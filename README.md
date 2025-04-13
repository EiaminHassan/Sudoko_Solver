# Sudoku Solver

A modern Python application that solves Sudoku puzzles using a recursive backtracking algorithm. The application features a user-friendly GUI built with Tkinter and includes various helpful features for both solving and playing Sudoku puzzles.

## Features

### Core Functionality
- **Sudoku Solver**: Uses recursive backtracking to solve any valid Sudoku puzzle
- **Input Validation**: Ensures only valid numbers (1-9) can be entered
- **Puzzle Generation**: Creates random Sudoku puzzles with varying difficulty

### User Interface
- **Modern GUI**: Clean and intuitive interface built with Tkinter
- **Color Coding**:
  - Blue: User-input numbers
  - Green: Numbers filled by the solver
  - White/Dark: Empty cells (depending on theme)
- **Theme Support**:
  - Light Mode: Bright, easy-to-read interface
  - Dark Mode: Eye-friendly dark theme

### Additional Features
- **Timer**: Tracks solving time for generated puzzles
- **Undo/Redo**: Allows users to backtrack their moves
- **Reset Board**: Clears the entire board
- **Visual Feedback**: Highlights changes made by the solver

## Requirements

- Python 3.x
- Tkinter (usually comes with Python installation)

## Installation

1. Clone the repository or download the source code
2. Ensure Python 3.x is installed on your system
3. No additional packages are required as the application uses only built-in Python libraries

## Usage

1. Run the application:
   ```bash
   python sudoku_solver.py
   ```

2. Using the application:
   - **Generate**: Click to create a new random puzzle
   - **Solve**: Click to solve the current puzzle
   - **Reset**: Click to clear the board
   - **Undo/Redo**: Use to backtrack or redo moves
   - **Theme Toggle**: Switch between light and dark modes

3. Input numbers:
   - Click on any cell and type a number (1-9)
   - The application will validate your input
   - Invalid numbers will not be accepted

## How It Works

### Solving Algorithm
The application uses a recursive backtracking algorithm to solve Sudoku puzzles:
1. Finds the next empty cell
2. Tries numbers 1-9 in the cell
3. Checks if the number is valid (no conflicts in row, column, or 3x3 box)
4. If valid, continues to next cell
5. If no valid number is found, backtracks to previous cell

### Puzzle Generation
1. Creates a solved board using the solver
2. Randomly removes numbers to create a puzzle
3. Ensures the puzzle has a unique solution

## Contributing

Feel free to contribute to this project by:
1. Forking the repository
2. Creating a feature branch
3. Making your changes
4. Submitting a pull request

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Built with Python and Tkinter
- Inspired by classic Sudoku puzzles
- Designed for both learning and entertainment purposes 