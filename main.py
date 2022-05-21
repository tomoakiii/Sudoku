# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Use a breakpoint in the code line below to debug your script.
# Press Ctrl+F8 to toggle the breakpoint.
import tkinter as tk
import numpy as np
import random
from tkinter import filedialog
import pandas as pd


class SudokuCellsNum:
    def __init__(self):
        self.cells = []
        for y in range(0, 9):
            cells = []
            for x in range(0, 9):
                if (0 <= x <= 2) & (0 <= y <= 2):
                    cell = SudokuCellNum(y + 1, x + 1, 1)
                elif (3 <= x <= 5) & (0 <= y <= 2):
                    cell = SudokuCellNum(y + 1, x + 1, 2)
                elif (6 <= x <= 8) & (0 <= y <= 2):
                    cell = SudokuCellNum(y + 1, x + 1, 3)
                elif (0 <= x <= 2) & (3 <= y <= 5):
                    cell = SudokuCellNum(y + 1, x + 1, 4)
                elif (3 <= x <= 5) & (3 <= y <= 5):
                    cell = SudokuCellNum(y + 1, x + 1, 5)
                elif (6 <= x <= 8) & (3 <= y <= 5):
                    cell = SudokuCellNum(y + 1, x + 1, 6)
                elif (0 <= x <= 2) & (6 <= y <= 8):
                    cell = SudokuCellNum(y + 1, x + 1, 7)
                elif (3 <= x <= 5) & (6 <= y <= 8):
                    cell = SudokuCellNum(y + 1, x + 1, 8)
                else:
                    cell = SudokuCellNum(y + 1, x + 1, 9)
                cells.append(cell)
            self.cells.append(cells)

    def clear(self):
        for y in range(0, 9):
            for x in range(0, 9):
                self.cells[y][x].clear()

    def getter_cell(self, yy, xx):
        return self.cells[yy][xx]

    def set_fix_value(self, yy, xx, value):
        self.cells[yy][xx].set_fix_value(int(value))

    def random_start(self):
        for y in range(0, 9):
            for x in range(0, 9):
                self.cells[y][x].set_fix_value(random.randint(0, 9))

    def import_csv(self, str_cells_):
        for y in range(0, 9):
            for x in range(0, 9):
                self.cells[y][x].set_fix_value(int(str_cells_.T[y][x]))

    def save_csv(self, fle):
        cells = np.zeros((9, 9))
        for y in range(0, 9):
            for x in range(0, 9):
                cells[y][x] = self.cells[y][x].fix_value
        np.savetxt(fle, cells.T, fmt='%d', delimiter=',')

    def try_solve(self):
        for y in range(0, 9):
            for x in range(0, 9):
                value = self.cells[y][x].fix_value
                if value > 0:
                    for n in range(0, 9):
                        if n != x:
                            self.cells[y][n].eliminate_candidate_num(value)
                        if n != y:
                            self.cells[n][x].eliminate_candidate_num(value)


class SudokuCellNum:
    def __init__(self, yy, xx, n):
        self.candidates = np.ones(9)
        self.is_fix = 0
        self.fix_value = 0
        self.y = yy
        self.x = xx
        self.group = n

    def clear(self):
        self.candidates[:] = 1
        self.is_fix = 0
        self.fix_value = 0

    def set_fix_value(self, value):
        if 1 <= value <= 9:
            self.candidates[:] = 0
            self.candidates[value - 1] = 1
            self.is_fix = 1
            self.fix_value = value

    def eliminate_candidate_num(self, value):
        self.candidates[value - 1] = 0
        self.check_is_one_candidate()
        self.is_fix = 1
        self.fix_value = value

    def check_is_one_candidate(self):
        if np.sum(self.candidates) == 1:
            for n in range(0, 9):
                if self.candidates[n] == 1:
                    self.set_fix_value(n)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.sudoku_num = SudokuCellsNum()
        self.main_cells = []
        self.sub_cells = []
        self.make_frames()
        self.sudoku_num.random_start()
        self.sync_num_to_board()

    def sync_num_to_board(self):
        for x in range(0, 9):
            for y in range(0, 9):
                cell = self.sudoku_num.getter_cell(y, x)
                self.main_cells[y][x].delete(0, tk.END)
                self.main_cells[y][x].insert(0, str(cell.fix_value))
                for n in range(0, 9):
                    if cell.candidates[n] == 1:
                        self.sub_cells[y][x][n]['text'] = str(n + 1)
                    else:
                        self.sub_cells[y][x][n]['text'] = ""

    def copy_board_to_num(self):
        for x in range(0, 9):
            for y in range(0, 9):
                value = int(self.main_cells[y][x].get())
                self.sudoku_num.set_fix_value(y, x, value)

    def clear_sudoku(self):
        self.sudoku_num.clear()
        self.sync_num_to_board()

    def solve_sudoku(self):
        self.sudoku_num.try_solve()
        self.sync_num_to_board()

    def new_game_start(self):
        self.sudoku_num.random_start()
        self.sync_num_to_board()

    def file_load_sudoku(self):
        typ = [('', '*.txt')]
        d = 'C:\\'
        fle = filedialog.askopenfilename(filetypes=typ, initialdir=d)
        if fle:
            str_cells = np.loadtxt(fle, dtype='unicode', delimiter=',')
            self.sudoku_num.import_csv(str_cells)

    def file_save_sudoku(self):
        typ = [('', '*.txt')]
        ini_fle = "sudoku_test_1.txt"
        fle = filedialog.asksaveasfilename(filetypes=typ, initialfile=ini_fle)
        if fle:
            self.sudoku_num.save_csv(fle)

    def make_frames(self):
        button_frame = tk.Frame(self.master, relief=tk.RIDGE, bd=2)
        new_button = tk.Button(button_frame, width=10, text="New Game", command=self.new_game_start)
        new_button.pack(side=tk.LEFT)
        input_button = tk.Button(button_frame, width=10, text="Input", command=self.copy_board_to_num)
        input_button.pack(side=tk.LEFT)
        auto_button = tk.Button(button_frame, width=10, text="Auto solve", command=self.solve_sudoku)
        auto_button.pack(side=tk.LEFT)
        clear_button = tk.Button(button_frame, width=10, text="Clear", command=self.clear_sudoku)
        clear_button.pack(side=tk.LEFT)
        file_load_button = tk.Button(button_frame, width=10, text="file load", command=self.file_load_sudoku)
        file_load_button.pack(side=tk.LEFT)
        file_save_button = tk.Button(button_frame, width=10, text="file save", command=self.file_save_sudoku)
        file_save_button.pack(side=tk.LEFT)

        button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        mainframe = tk.Frame(self.master, relief=tk.RIDGE, bd=2)
        for x in range(0, 9):
            tmp_cells = []
            for y in range(0, 9):
                txt = tk.Entry(mainframe, width=6, font=("Calibri", 18))
                txt.grid(row=y, column=x)
                if ((0 <= x <= 2) | (6 <= x <= 8)) & ((0 <= y <= 2) | (6 <= y <= 8)) \
                        | ((3 <= x <= 5) & (3 <= y <= 5)):
                    txt.configure(bg="#dddddd")
                tmp_cells.append(txt)
            self.main_cells.append(tmp_cells)
        mainframe.pack(side=tk.TOP, fill=tk.X)
        subframe = tk.Frame(self.master, relief=tk.RIDGE, bd=2)

        for x in range(0, 9):
            tmp_cells = []
            for y in range(0, 9):
                sf = tk.Frame(subframe, relief=tk.RIDGE, bd=0.5)
                sf.grid(row=y, column=x)
                if ((0 <= x <= 2) | (6 <= x <= 8)) & ((0 <= y <= 2) | (6 <= y <= 8)) \
                        | ((3 <= x <= 5) & (3 <= y <= 5)):
                    tmp_bg = "#dddddd"
                else:
                    tmp_bg = "#ffffff"
                tmp_cells2 = []
                for n in range(0, 9):
                    txt = tk.Label(sf, text=str(n + 1), width=1, font=("Calibri", 6), bg=tmp_bg)
                    txt.grid(row=int(n / 3), column=int(n % 3), ipady=0, pady=0)
                    tmp_cells2.append(txt)
                tmp_cells.append(tmp_cells2)
            self.sub_cells.append(tmp_cells)
        subframe.pack(side=tk.BOTTOM, fill=tk.X)


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes("-topmost", False)
    root.title("Sudoku")
    root.geometry("800x750")
    app = Application(master=root)
    app.mainloop()
