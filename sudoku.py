from sudoku_generator import *

def main():
    difficulty = input("What difficulty would you like the suduko to be? (easy, medium, or hard)")
    difficulty_dict = {'easy':30,'medium':40,'hard':50}
    user_sudoku = SudokuGenerator(difficulty_dict[difficulty])
    user_sudoku.fill_values()
    user_sudoku.remove_cells()
    user_sudoku.print_board()

if __name__ == '__main__':
    main()

