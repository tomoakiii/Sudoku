# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Use a breakpoint in the code line below to debug your script.
# Press Ctrl+F8 to toggle the breakpoint.
import tkinter as tk
import numpy as np
import random
from tkinter import filedialog
from tkinter import messagebox
import copy


class SudokuCellsNum:
    def __init__(self):
        self.cells = []
        groups = [[] for _ in range(9)]
        for y in range(0, 9):
            cells = []
            for x in range(0, 9):
                if (0 <= x <= 2) & (0 <= y <= 2):
                    group = 0
                elif (3 <= x <= 5) & (0 <= y <= 2):
                    group = 1
                elif (6 <= x <= 8) & (0 <= y <= 2):
                    group = 2
                elif (0 <= x <= 2) & (3 <= y <= 5):
                    group = 3
                elif (3 <= x <= 5) & (3 <= y <= 5):
                    group = 4
                elif (6 <= x <= 8) & (3 <= y <= 5):
                    group = 5
                elif (0 <= x <= 2) & (6 <= y <= 8):
                    group = 6
                elif (3 <= x <= 5) & (6 <= y <= 8):
                    group = 7
                else:
                    group = 8
                cell = SudokuCellNum(y, x, group)
                cells.append(cell)
                groups[group].append(cell)
            self.cells.append(cells)
        self.group = []
        for n in range(0, 9):
            self.group.append(SudokuGroup(n, groups[n], type_group="group"))

        self.rows = []
        for n in range(0, 9):
            self.rows.append(SudokuGroup(n, self.cells[n][:], type_group="row"))

        self.columns = []
        for n in range(0, 9):
            self.columns.append(SudokuGroup(n, [r[n] for r in self.cells], type_group="column"))

    def clear(self):
        for y in range(0, 9):
            for x in range(0, 9):
                self.cells[y][x].clear()
        for n in range(0, 9):
            self.group[n].clear()

    def getter_cell(self, yy, xx):
        return self.cells[yy][xx]

    def set_fix_value(self, yy, xx, value):
        self.cells[yy][xx].set_fix_value(int(value))

    def random_start(self):
        for y in range(0, 9):
            for x in range(0, 9):
                self.cells[y][x].set_init_value(random.randint(0, 9))

    def import_csv(self, cells):
        for y in range(0, 9):
            for x in range(0, 9):
                self.cells[y][x].set_init_value(int(cells[y][x]))

    def save_csv(self, fle):
        cells = np.zeros((9, 9))
        for y in range(0, 9):
            for x in range(0, 9):
                cells[y][x] = int(self.cells[y][x].fix_value)
        np.savetxt(fle, cells, fmt='%d', delimiter=',')

    def try_solve(self):
        for n in range(0, 9):
            self.group[n].group_organizer()
            self.rows[n].group_organizer()
            self.columns[n].group_organizer()

    def try_solve2(self):
        for n in range(0, 9):
            for n2 in range(0, 9):
                one_group_candidate(self.group[n], self.rows[n2])
                one_group_candidate(self.group[n], self.columns[n2])
                one_group_candidate(self.rows[n], self.group[n2])
                one_group_candidate(self.rows[n], self.columns[n2])
                one_group_candidate(self.columns[n], self.group[n2])
                one_group_candidate(self.columns[n], self.rows[n2])

    def is_game_progress(self):
        for n in range(0, 9):
            if np.any(self.group[n].num_candidates == 0):
                return -1  # Failure
            if np.any(self.rows[n].num_candidates == 0):
                return -1  # Failure
            if np.any(self.columns[n].num_candidates == 0):
                return -1  # Failure

        for n in range(0, 9):
            if np.any(self.group[n].num_candidates >= 2):
                return 0  # In progress
            if np.any(self.rows[n].num_candidates >= 2):
                return 0  # In progress
            if np.any(self.columns[n].num_candidates >= 2):
                return 0  # In progress

        return 1  # clear

def one_group_candidate(group1, group2):
    for val in range(0, 9):
        is_do = True
        is_protect = np.zeros(9)
        if 2 <= group1.num_candidates[val] <= 3:
            for n in range(0, len(group1.candidates_position[val])):
                temp_cell = group1.cells[group1.candidates_position[val][n]]
                is_exist = group2.is_exist_cell(yy=temp_cell.y, xx=temp_cell.x)
                if is_exist == -1:
                    is_do = False
                    break
                else:
                    is_protect[is_exist] = 1
        else:
            is_do = False

        if is_do:
            for n in range(0, 9):
                if is_protect[n] != 1:
                    group2.cells[n].eliminate_candidate_num(value=val + 1)


class SudokuGroup:
    def __init__(self, n, cells, type_group):
        self.num = n
        self.is_fix_num = np.zeros(9)
        self.cells = cells
        self.num_candidates = np.zeros(9)
        self.candidates_position = []
        self.group_num_set()
        self.type = type_group

    def is_exist_cell(self, yy, xx):
        for n in range(0, 9):
            if (self.cells[n].x == xx) & (self.cells[n].y == yy):
                return n
        return -1

    def group_organizer(self):
        self.delete_candidate()
        self.find_only_one()
        self.group_num_set()

    def clear(self):
        self.is_fix_num[:] = 0
        self.num_candidates[:] = 0

    def group_num_set(self):
        self.is_fix_num[:] = 0
        self.num_candidates[:] = 0
        self.candidates_position = [[] for _ in range(9)]

        for n in range(0, 9):
            if self.cells[n].is_fix == 1:
                self.is_fix_num[self.cells[n].fix_value - 1] = 1
            self.num_candidates[:] = self.num_candidates[:] + self.cells[n].candidates

            for val in range(0, 9):
                if self.cells[n].candidates[val] == 1:
                    self.candidates_position[val].append(n)

    def delete_candidate(self):
        for n in range(0, 9):
            if self.cells[n].is_fix == 1:
                for m in range(0, 9):
                    if n != m:
                        self.cells[m].eliminate_candidate_num(self.cells[n].fix_value)
        self.group_num_set()

    def find_only_one(self):
        for val in range(0, 9):
            if self.num_candidates[val] == 1:
                for n in range(0, 9):
                    if self.cells[n].candidates[val] == 1:
                        self.cells[n].set_fix_value(val + 1)
        self.group_num_set()


class SudokuCellNum:
    def __init__(self, yy, xx, n):
        self.candidates = np.ones(9)
        self.is_fix = 0
        self.fix_value = 0
        self.y = yy
        self.x = xx
        self.group = n
        self.initial_fix = 0

    def clear(self):
        self.candidates[:] = 1
        self.is_fix = 0
        self.fix_value = 0
        self.initial_fix = 0

    def set_fix_value(self, value):
        if 1 <= value <= 9:
            self.candidates[:] = 0
            self.candidates[value - 1] = 1
            self.is_fix = 1
            self.fix_value = value

    def set_init_value(self, value):
        if 1 <= value <= 9:
            self.candidates[:] = 0
            self.candidates[value - 1] = 1
            self.is_fix = 1
            self.fix_value = value
            self.initial_fix = 1

    def eliminate_candidate_num(self, value):
        self.candidates[value - 1] = 0
        self.check_is_one_candidate()

    def check_is_one_candidate(self):
        if (self.is_fix == 0) & (np.sum(self.candidates) == 1):
            for n in range(0, 9):
                if self.candidates[n] == 1:
                    self.set_fix_value(n + 1)


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
                if cell.is_fix == 1:
                    self.main_cells[y][x].insert(0, str(cell.fix_value))
                if cell.initial_fix == 1:
                    self.main_cells[y][x].configure(fg="#000088")
                else:
                    self.main_cells[y][x].configure(fg="#000000")

                for n in range(0, 9):
                    if cell.candidates[n] == 1:
                        if cell.is_fix == 1:
                            self.sub_cells[y][x][n]['fg'] = "#FF0000"
                        else:
                            self.sub_cells[y][x][n]['fg'] = "#000000"
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
        self.sudoku_num.try_solve2()
        self.sync_num_to_board()
        if self.sudoku_num.is_game_progress() == 1:
            messagebox.showinfo("Sudoku", "Game Clear")
        elif self.sudoku_num.is_game_progress() == -1:
            messagebox.showinfo("Sudoku", "Failure to solve")

    def new_game_start(self):
        self.sudoku_num.random_start()
        self.sync_num_to_board()

    def file_load_sudoku(self):
        typ = [('', '*.txt'), ('', '.csv')]
        d = 'C:\\'
        fle = filedialog.askopenfilename(filetypes=typ, initialdir=d)
        if fle:
            self.sudoku_num.clear()
            cells = np.genfromtxt(fle, delimiter=',', filling_values=0, encoding='utf8')
            self.sudoku_num.import_csv(cells)
            self.sync_num_to_board()

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
        for y in range(0, 9):
            tmp_cells = []
            for x in range(0, 9):
                txt = tk.Entry(mainframe, width=6, font=("Calibri", 18))
                txt.grid(row=y, column=x)
                if ((0 <= x <= 2) | (6 <= x <= 8)) & ((0 <= y <= 2) | (6 <= y <= 8)) \
                        | ((3 <= x <= 5) & (3 <= y <= 5)):
                    txt.configure(bg="#dddddd")
                tmp_cells.append(txt)
            self.main_cells.append(tmp_cells)
        mainframe.pack(side=tk.TOP, fill=tk.X)
        subframe = tk.Frame(self.master, relief=tk.RIDGE, bd=2)

        for y in range(0, 9):
            tmp_cells = []
            for x in range(0, 9):
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
    root.attributes("-topmost", True)
    root.title("Sudoku")
    root.geometry("700x780")
    app = Application(master=root)
    app.mainloop()
