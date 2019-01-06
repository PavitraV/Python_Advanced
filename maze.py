import sys
from itertools import chain
import numpy as np

class MazeError(Exception):
    def __init__(self, message):
        self.message = message

class Maze:
    i = 0
    print_flag = True
    def __init__(self, maze_name):
        self.possible_cul = []
        self.count_uniq = []
        self.walls = []
        self.gates = []
        open_file = open(maze_name)
        data = open_file.readlines()
        matrix = []
        for i in data:
            lists = []
            for j in i:
                if (j in '0123'):
                    lists.append(int(j))
                elif j in ' \n\t':
                    pass
                else:
                    raise MazeError('Incorrect input.')
            if (lists != []):
                matrix.append(lists)
        row = len(matrix)-1
        for col in range(len(matrix[0])):
            if matrix[row][col] == 2 or matrix[row][col] == 3:
                raise MazeError('Input does not represent a maze.')
        col = len(matrix[0])-1
        for row in range(len(matrix)):
            if matrix[row][col] == 1 or matrix[row][col] == 3:
                raise MazeError('Input does not represent a maze.')
        self.matrix = matrix
        self.print_flag = True
        self.maze_name = maze_name
        if 2>len(matrix[0])>=31 or 2>len(matrix)>=41:
            raise MazeError('Incorrect input.')
        for i in range(len(matrix)-1):
            if len(matrix[i])!= len(matrix[i+1]):
                raise MazeError('Incorrect input.')

    def analyse(self):

        global i
        i = 0
        possiblerows = []

        def traverse(row, col):
            global i
            if (self.matrix[row][col] == 1):
                if (col - 1 >= 0 and (row, col - 1) not in chain.from_iterable(possiblerows)):
                    possiblerows[k].append((row, col - 1))
                if (col + 1 < len(self.matrix[0]) - 1 and (
                        self.matrix[row][col + 1] != 2 and self.matrix[row][col + 1] != 3) and (
                        row, col + 1) not in chain.from_iterable(possiblerows)):
                    possiblerows[k].append((row, col + 1))
                if (row + 1 < len(self.matrix) - 1) and (
                        self.matrix[row + 1][col] != 1 and self.matrix[row + 1][col] != 3) and (
                        row + 1, col) not in chain.from_iterable(possiblerows):
                    possiblerows[k].append((row + 1, col))

            if (self.matrix[row][col] == 2):
                if (row - 1 >= 0 and (row - 1, col) not in chain.from_iterable(possiblerows)):
                    possiblerows[k].append((row - 1, col))
                if (col + 1 < len(self.matrix[0]) - 1 and (
                        self.matrix[row][col + 1] != 2 and self.matrix[row][col + 1] != 3) and (
                        row, col + 1) not in chain.from_iterable(possiblerows)):
                    possiblerows[k].append((row, col + 1))
                if (row + 1 < len(self.matrix) - 1) and self.matrix[row + 1][col] != 1 and self.matrix[row + 1][
                    col] != 3 and (
                        row + 1, col) not in chain.from_iterable(possiblerows):
                    possiblerows[k].append((row + 1, col))

            if (self.matrix[row][col] == 3):
                if (col + 1 < len(self.matrix[0]) - 1 and (
                        self.matrix[row][col + 1] != 2 and self.matrix[row][col + 1] != 3) and (
                        row, col + 1) not in chain.from_iterable(possiblerows)):
                    possiblerows[k].append((row, col + 1))
                if row + 1 < len(self.matrix) - 1 and (
                        self.matrix[row + 1][col] != 1 and self.matrix[row + 1][col] != 3) and (
                        row + 1, col) not in chain.from_iterable(possiblerows):
                    possiblerows[k].append((row + 1, col))

            if (self.matrix[row][col] == 0):
                if col - 1 >= 0 and (row, col - 1) not in chain.from_iterable(possiblerows):
                    possiblerows[k].append((row, col - 1))
                if (col + 1 < len(self.matrix[0]) - 1 and (
                        self.matrix[row][col + 1] != 2 and self.matrix[row][col + 1] != 3) and (
                        row, col + 1) not in chain.from_iterable(possiblerows)):
                    possiblerows[k].append((row, col + 1))
                if row + 1 < len(self.matrix) - 1 and self.matrix[row + 1][col] != 1 and self.matrix[row + 1][
                    col] != 3 and (
                        row + 1, col) not in chain.from_iterable(possiblerows):
                    possiblerows[k].append((row + 1, col))
                if (row - 1 >= 0 and (row - 1, col) not in chain.from_iterable(possiblerows)):
                    possiblerows[k].append((row - 1, col))

            while (i < len(possiblerows[k])):
                rows, cols = possiblerows[k][i]
                i += 1
                traverse(rows, cols)

        k = -1
        for p in range(len(self.matrix) - 1):
            for q in range(len(self.matrix[0]) - 1):
                if (len(possiblerows) == 0):
                    possiblerows.append([])
                    k += 1
                    traverse(p, q)
                else:
                    if ((p, q) not in chain.from_iterable(possiblerows)):
                        i = 0
                        possiblerows.append([])
                        k += 1
                        traverse(p, q)
                        if (len(possiblerows[k]) == 0):
                            possiblerows[k].append((p, q))
            # -------------------------------gates------------------------------------------
        gates = []
        row = 0
        count = 0
        # top
        for col in range(len(self.matrix[0])-1):
            if (self.matrix[row][col] == 0 or self.matrix[row][col] == 2): 
                count += 1
                gates.append((row, col))
        # up to down right
        col = len(self.matrix[0])-1
        for row in range(len(self.matrix)-1):
            if (self.matrix[row][col] == 0):
                count += 1
                gates.append((row, col-1))
        row = len(self.matrix) - 1
        # right to left
        for col in  range(len(self.matrix[0]) - 1):
            if (self.matrix[row][col] == 0):
                count += 1
                gates.append((row - 1, col))
        col = 0
        # up to down left
        for row in range(len(self.matrix) - 1):
            if (self.matrix[row][col] == 1 or self.matrix[row][col] == 0) :
                count += 1
                gates.append((row,col))
        if self.print_flag:
            if(len(gates)==0):
                print('The maze has no gate.')
            elif len(gates) == 1:
                print('The maze has a single gate.')
            else:
                print('The maze has',len(gates), 'gates.')
        self.gates = gates
        # -------------------------------walls------------------------------------------
        possiblemoves = [[]]
        i = 0
        k = -1

        def explore(row, col):
            global i
            if (self.matrix[row][col] == 0):
                pass
            if (self.matrix[row][col] == 1 and (row, col + 1) not in chain.from_iterable(possiblemoves)):
                possiblemoves[k].append((row, col + 1))
            if (self.matrix[row][col] == 2 and (row + 1, col) not in chain.from_iterable(possiblemoves)):
                possiblemoves[k].append((row + 1, col))
            if (self.matrix[row][col] == 3):
                if ((row + 1, col) not in chain.from_iterable(possiblemoves)):
                    possiblemoves[k].append((row + 1, col))
                if ((row, col + 1) not in chain.from_iterable(possiblemoves)):
                    possiblemoves[k].append((row, col + 1))
            if ((row - 1, col) not in chain.from_iterable(possiblemoves) and (
                    self.matrix[row - 1][col] == 2 or self.matrix[row - 1][col] == 3)):
                possiblemoves[k].append((row - 1, col))
            if ((row, col - 1) not in chain.from_iterable(possiblemoves) and (
                    self.matrix[row][col - 1] == 1 or self.matrix[row][col - 1] == 3)):
                possiblemoves[k].append((row, col - 1))

            while (i < len(possiblemoves[k])):
                rows, cols = possiblemoves[k][i]
                i += 1
                explore(rows, cols)

        for p in range(len(self.matrix)):
            for q in range(len(self.matrix[0])):
                if (len(possiblemoves) == 0):
                    possiblemoves.append([])
                    k += 1
                    explore(p, q)
                else:
                    if ((p, q) not in chain.from_iterable(possiblemoves)):
                        i = 0
                        possiblemoves.append([])
                        k += 1
                        explore(p, q)
        walls = []
        for lists in possiblemoves:
            if (lists != []):
                walls.append(lists)
        self.walls = walls
        if self.print_flag:
            if len(walls) == 0:
                print('The maze has no wall.')
            elif len(walls) == 1:
                print('The maze has walls that are all connected.')
            else:
                print('The maze has',len(walls),'sets of walls that are all connected.')

        # -------------------------------inacc areas------------------------------------------
        inacc_areas = 0
        inacc_points = []
        for i in range(len(possiblerows)):
            count = 0
            for j in range(len(possiblerows[i])):
                if (possiblerows[i][j] in self.gates):
                    break
                else:
                    count += 1
            if (count == len(possiblerows[i])):
                inacc_points.append(possiblerows[i])
                inacc_areas += len(possiblerows[i])
        if self.print_flag:
            if(inacc_areas==0):
                print('The maze has no inaccessible inner point.')
            elif inacc_areas == 1:
                print('The maze has a unique inaccessible inner point.')
            else:
                print('The maze has',inacc_areas,'inaccessible inner points.')
        # -------------------------------acc areas------------------------------------------
        acc_areas = 0
        for i in range(len(possiblerows)):
            count = 0
            for j in range(len(possiblerows[i])):
                if (possiblerows[i][j] in self.gates):
                    break
                else:
                    count += 1
            if (count != len(possiblerows[i])):
                acc_areas += 1
        if self.print_flag:
            if(acc_areas == 1):
                print('The maze has a unique accessible area.')
            elif acc_areas == 0:
                print('The maze has no accessible area.')
            else:
                print('The maze has',acc_areas,'accessible areas.')

        # -------------------------------cul de sac------------------------------------------
        listoflists = []
        for row in range(len(self.matrix) - 1):
            countlist = []
            for col in range(len(self.matrix[row]) - 1):
                count = 0
                if (self.matrix[row][col] == 1):
                    if (col - 1 >= 0):
                        count += 1
                    if (col + 1 < len(self.matrix[0]) - 1 and (
                            self.matrix[row][col + 1] != 2 and self.matrix[row][col + 1] != 3)):
                        count += 1
                    if (row + 1 < len(self.matrix) - 1) and (
                            self.matrix[row + 1][col] != 1 and self.matrix[row + 1][col] != 3):
                        count += 1

                if (self.matrix[row][col] == 2):
                    if (row - 1 >= 0):
                        count += 1
                    if (col + 1 < len(self.matrix[0]) - 1 and (
                            self.matrix[row][col + 1] != 2 and self.matrix[row][col + 1] != 3)):
                        count += 1
                    if (row + 1 < len(self.matrix) - 1) and self.matrix[row + 1][col] != 1 and self.matrix[row + 1][
                        col] != 3:
                        count += 1

                if (self.matrix[row][col] == 3):
                    if (col + 1 < len(self.matrix[0]) - 1 and (
                            self.matrix[row][col + 1] != 2 and self.matrix[row][col + 1] != 3)):
                        count += 1
                    if row + 1 < len(self.matrix) - 1 and (
                            self.matrix[row + 1][col] != 1 and self.matrix[row + 1][col] != 3):
                        count += 1

                if (self.matrix[row][col] == 0):
                    if col - 1 >= 0:
                        count += 1
                    if (col + 1 < len(self.matrix[0]) - 1 and (
                            self.matrix[row][col + 1] != 2 and self.matrix[row][col + 1] != 3)):
                        count += 1
                    if row + 1 < len(self.matrix) - 1 and self.matrix[row + 1][col] != 1 and self.matrix[row + 1][
                        col] != 3:
                        count += 1
                    if (row - 1 >= 0):
                        count += 1
                countlist.append(count)
            listoflists.append(countlist)

        for j in self.gates:
            listoflists[j[0]][j[1]] += 1

        coordinates_of_1_initial = []

        for p in range(len(listoflists)):
            for q in range(len(listoflists[p])):
                if listoflists[p][q] == 1:
                    coordinates_of_1_initial.append((p, q))
        coordinates_of_1 = []

        def neighbors_up(row, col, row1, col1):
            if (row1 >= 0 and (self.matrix[row][col] != 1 and self.matrix[row][col] != 3)):
                return True
            return False

        def neighbors_down(row, col, row1, col1):
            if (row1 < len(self.matrix) - 1 and (self.matrix[row1][col] != 1 and self.matrix[row1][col] != 3)):
                return True
            return False

        def neighbors_left(row, col, row1, col1):
            if (col1 >= 0 and (self.matrix[row][col] != 2 and self.matrix[row][col] != 3)):
                return True
            return False

        def neighbors_right(row, col, row1, col1):
            if (col1 < len(self.matrix[0]) - 1 and (self.matrix[row][col1] != 2 and self.matrix[row][col1] != 3)):
                return True
            return False

        i = 0

        def culdesac(row, col):
            global i
            if row - 1 >= 0:
                if listoflists[row - 1][col] > 1 and (row - 1, col) not in coordinates_of_1 and neighbors_up(row, col,
                                                                                                             row - 1,
                                                                                                             col):
                    listoflists[row - 1][col] -= 1
                    if (listoflists[row - 1][col] == 1):
                        coordinates_of_1.append((row - 1, col))

            if row + 1 < len(self.matrix) - 1:
                if listoflists[row + 1][col] > 1 and neighbors_down(row, col, row + 1, col) and (
                        row + 1, col) not in coordinates_of_1:
                    listoflists[row + 1][col] -= 1
                    if (listoflists[row + 1][col] == 1):
                        coordinates_of_1.append((row + 1, col))

            if col - 1 >= 0:
                if listoflists[row][col - 1] > 1 and (row, col - 1) not in coordinates_of_1 and neighbors_left(row, col,
                                                                                                               row,
                                                                                                               col - 1):
                    listoflists[row][col - 1] -= 1
                    if (listoflists[row][col - 1] == 1):
                        coordinates_of_1.append((row, col - 1))

            if col + 1 < len(self.matrix[0]) - 1:
                if listoflists[row][col + 1] > 1 and neighbors_right(row, col, row, col + 1) and (
                        row, col + 1) not in coordinates_of_1:
                    listoflists[row][col + 1] -= 1
                    if (listoflists[row][col + 1] == 1):
                        coordinates_of_1.append((row, col + 1))

            while (i < len(coordinates_of_1)):
                rows = coordinates_of_1[i][0]
                cols = coordinates_of_1[i][1]
                i += 1
                culdesac(rows, cols)

        for p in coordinates_of_1_initial:
            x = p[0]
            y = p[1]
            culdesac(x, y)

        #'-------------------------------------count culde sac------------------------------------------'

        possible_cul = []
        i = 0
        k = -1

        def traverse_cul(row, col):
            global i
            if (self.matrix[row][col] == 1):
                if (col - 1 >= 0 and (row, col - 1) not in chain.from_iterable(possible_cul) and listoflists[row][
                    col - 1] == 1):
                    possible_cul[k].append((row, col - 1))
                if (col + 1 < len(self.matrix[0]) - 1 and (
                        self.matrix[row][col + 1] != 2 and listoflists[row][col + 1] == 1 and self.matrix[row][
                    col + 1] != 3) and (row, col + 1) not in chain.from_iterable(possible_cul)):
                    possible_cul[k].append((row, col + 1))
                if (row + 1 < len(self.matrix) - 1) and (
                        self.matrix[row + 1][col] != 1 and listoflists[row + 1][col] == 1 and self.matrix[row + 1][
                    col] != 3) and (row + 1, col) not in chain.from_iterable(possible_cul):
                    possible_cul[k].append((row + 1, col))

            if (self.matrix[row][col] == 2):
                if (row - 1 >= 0 and listoflists[row - 1][col] == 1 and (row - 1, col) not in chain.from_iterable(
                        possible_cul)):
                    possible_cul[k].append((row - 1, col))
                if (col + 1 < len(self.matrix[0]) - 1 and listoflists[row][col + 1] == 1 and (
                        self.matrix[row][col + 1] != 2 and self.matrix[row][col + 1] != 3) and (
                        row, col + 1) not in chain.from_iterable(possible_cul)):
                    possible_cul[k].append((row, col + 1))
                if (row + 1 < len(self.matrix) - 1) and listoflists[row + 1][col] == 1 and self.matrix[row + 1][
                    col] != 1 and self.matrix[row + 1][col] != 3 and (row + 1, col) not in chain.from_iterable(
                    possible_cul):
                    possible_cul[k].append((row + 1, col))

            if (self.matrix[row][col] == 3):
                if (col + 1 < len(self.matrix[0]) - 1 and listoflists[row][col + 1] == 1 and (
                        self.matrix[row][col + 1] != 2 and self.matrix[row][col + 1] != 3) and (
                        row, col + 1) not in chain.from_iterable(possible_cul)):
                    possible_cul[k].append((row, col + 1))
                if row + 1 < len(self.matrix) - 1 and listoflists[row + 1][col] == 1 and (
                        self.matrix[row + 1][col] != 1 and self.matrix[row + 1][col] != 3) and (
                        row + 1, col) not in chain.from_iterable(possible_cul):
                    possible_cul[k].append((row + 1, col))

            if (self.matrix[row][col] == 0):
                if col - 1 >= 0 and listoflists[row][col - 1] == 1 and (row, col - 1) not in chain.from_iterable(
                        possible_cul):
                    possible_cul[k].append((row, col - 1))
                if (col + 1 < len(self.matrix[0]) - 1 and listoflists[row][col + 1] == 1 and (
                        self.matrix[row][col + 1] != 2 and self.matrix[row][col + 1] != 3) and (
                        row, col + 1) not in chain.from_iterable(possible_cul)):
                    possible_cul[k].append((row, col + 1))
                if row + 1 < len(self.matrix) - 1 and listoflists[row + 1][col] == 1 and self.matrix[row + 1][
                    col] != 1 and self.matrix[row + 1][col] != 3 and (row + 1, col) not in chain.from_iterable(
                    possible_cul):
                    possible_cul[k].append((row + 1, col))
                if (row - 1 >= 0 and listoflists[row - 1][col] == 1 and (row - 1, col) not in chain.from_iterable(
                        possible_cul)):
                    possible_cul[k].append((row - 1, col))

            while (i < len(possible_cul[k])):
                rows, cols = possible_cul[k][i]
                i += 1
                traverse_cul(rows, cols)

        for p in range(len(listoflists)):
            for q in range(len(listoflists[0])):
                if (listoflists[p][q] == 1 and (p, q) not in chain.from_iterable(possible_cul)):
                    i = 0
                    possible_cul.append([])
                    k += 1
                    traverse_cul(p, q)
                    if (len(possible_cul[k]) == 0):
                        possible_cul[k].append((p, q))

        count_cul = len(possible_cul)
        dup_list = []
        for j in possible_cul:
            for x in inacc_points:
                if set(j) == set(x):
                    dup_list.append(j)
                    count_cul -= 1
        for j in dup_list:
            possible_cul.remove(j)
        self.possible_cul = possible_cul
        if self.print_flag:
            if count_cul==0:
                print('The maze has no accessible cul-de-sac.')
            elif count_cul==1:
                print('The maze has accessible cul-de-sacs that are all connected.')
            else:
                print('The maze has',count_cul,'sets of accessible cul-de-sacs that are all connected.')

        possible_uniq = []
        i = 0
        k = -1

        def unique_traverse(row, col):
            global i
            global print_flag
            if (self.matrix[row][col] == 1):
                if (col - 1 >= 0 and (row, col - 1) not in chain.from_iterable(possible_uniq) and listoflists[row][
                    col - 1] == 2):
                    possible_uniq[k].append((row, col - 1))
                if (col + 1 < len(self.matrix[0]) - 1 and (
                        self.matrix[row][col + 1] != 2 and listoflists[row][col + 1] == 2 and self.matrix[row][
                    col + 1] != 3) and (row, col + 1) not in chain.from_iterable(possible_uniq)):
                    possible_uniq[k].append((row, col + 1))
                if (row + 1 < len(self.matrix) - 1) and (
                        self.matrix[row + 1][col] != 1 and listoflists[row + 1][col] == 2 and self.matrix[row + 1][
                    col] != 3) and (row + 1, col) not in chain.from_iterable(possible_uniq):
                    possible_uniq[k].append((row + 1, col))

            if (self.matrix[row][col] == 2):
                if (row - 1 >= 0 and listoflists[row - 1][col] == 2 and (row - 1, col) not in chain.from_iterable(
                        possible_uniq)):
                    possible_uniq[k].append((row - 1, col))
                if (col + 1 < len(self.matrix[0]) - 1 and listoflists[row][col + 1] == 2 and (
                        self.matrix[row][col + 1] != 2 and self.matrix[row][col + 1] != 3) and (
                row, col + 1) not in chain.from_iterable(possible_uniq)):
                    possible_uniq[k].append((row, col + 1))
                if (row + 1 < len(self.matrix) - 1) and listoflists[row + 1][col] == 2 and self.matrix[row + 1][
                    col] != 1 and self.matrix[row + 1][col] != 3 and (row + 1, col) not in chain.from_iterable(
                        possible_uniq):
                    possible_uniq[k].append((row + 1, col))

            if (self.matrix[row][col] == 3):
                if (col + 1 < len(self.matrix[0]) - 1 and listoflists[row][col + 1] == 2 and (
                        self.matrix[row][col + 1] != 2 and self.matrix[row][col + 1] != 3) and (
                row, col + 1) not in chain.from_iterable(possible_uniq)):
                    possible_uniq[k].append((row, col + 1))
                if row + 1 < len(self.matrix) - 1 and listoflists[row + 1][col] == 2 and (
                        self.matrix[row + 1][col] != 1 and self.matrix[row + 1][col] != 3) and (
                row + 1, col) not in chain.from_iterable(possible_uniq):
                    possible_uniq[k].append((row + 1, col))

            if (self.matrix[row][col] == 0):
                if col - 1 >= 0 and listoflists[row][col - 1] == 2 and (row, col - 1) not in chain.from_iterable(
                        possible_uniq):
                    possible_uniq[k].append((row, col - 1))
                if (col + 1 < len(self.matrix[0]) - 1 and listoflists[row][col + 1] == 2 and (
                        self.matrix[row][col + 1] != 2 and self.matrix[row][col + 1] != 3) and (
                row, col + 1) not in chain.from_iterable(possible_uniq)):
                    possible_uniq[k].append((row, col + 1))
                if row + 1 < len(self.matrix) - 1 and listoflists[row + 1][col] == 2 and self.matrix[row + 1][
                    col] != 1 and self.matrix[row + 1][col] != 3 and (row + 1, col) not in chain.from_iterable(
                        possible_uniq):
                    possible_uniq[k].append((row + 1, col))
                if (row - 1 >= 0 and listoflists[row - 1][col] == 2 and (row - 1, col) not in chain.from_iterable(
                        possible_uniq)):
                    possible_uniq[k].append((row - 1, col))

            while (i < len(possible_uniq[k])):
                rows, cols = possible_uniq[k][i]
                i += 1
                unique_traverse(rows, cols)

        for p in range(len(listoflists)):
            for q in range(len(listoflists[0])):
                if (listoflists[p][q] == 2 and (p, q) not in chain.from_iterable(possible_uniq)):
                    i = 0
                    possible_uniq.append([])
                    k += 1
                    unique_traverse(p, q)
                    if (len(possible_uniq[k]) == 0):
                        possible_uniq[k].append((p, q))

        count_uniq = []
        count = 0
        for p in possible_uniq:
            if (len(p) == 1):
                if gates.count(p[0]) == 2:
                    count_uniq.append(p[0])
            else:
                count = 0
                for q in p:
                    if q in gates:
                        count += 1
                if count == 2:
                    count_uniq.append(p)
        self.count_uniq = count_uniq
        if self.print_flag:
            if len(count_uniq)==1:
                print('The maze has a unique entry-exit path with no intersection not to cul-de-sacs.')
            elif len(count_uniq) == 0:
                print('The maze has no entry-exit path with no intersection not to cul-de-sacs.')
            else:
                print('The maze has',len(count_uniq),'entry-exit paths with no intersections not to cul-de-sacs.')

    def display(self):
        self.maze_name = self.maze_name[:-3]+'tex'
        start_hor = []
        end_hor = []
        pillars = []
        self.print_flag = False
        self.analyse()
        culde = []
        uniq = self.count_uniq
        
        for i in range(len(self.matrix)):
             for j in range(len(self.matrix[i])):
                 if (i, j) not in chain.from_iterable(self.walls):
                     pillars.append((j,i))
                     

        for i in range(len(self.matrix)):
            j = 0
            while j < (len(self.matrix[i])):
                if (self.matrix[i][j] == 1 or self.matrix[i][j] == 3):
                    start_hor.append((j, i))
                    if (self.matrix[i][j + 1] != 1 and self.matrix[i][j + 1] != 3):
                        end_hor.append((j + 1, i))
                        j += 1
                    else:
                        while (self.matrix[i][j + 1] == 1 or self.matrix[i][j + 1] == 3):
                            j += 1
                        end_hor.append((j + 1, i))
                        j += 1
                j += 1

        new_matrix = np.transpose(self.matrix)
        
        for i in self.possible_cul:
            for j in i:
                culde.append((j[1]+0.5,j[0]+0.5))
        
        
        culde = sorted(culde, key = lambda j : (j[1],j[0]))
        uniq_start = []
        uniq_end = []
        
        def neighbors_up(row, col):
            if (row-1 >= 0 and (self.matrix[row][col] != 1 and self.matrix[row][col] != 3)):
                return True
            return False

        def neighbors_down(row, col):
            if (row+1 < len(self.matrix) - 1 and (self.matrix[row+1][col] != 1 and self.matrix[row+1][col] != 3)):
                return True
            return False

        def neighbors_left(row, col):
            if (col-1 >= 0 and (self.matrix[row][col] != 2 and self.matrix[row][col] != 3)):
                return True
            return False

        def neighbors_right(row, col):
            if (col+1 < len(self.matrix[0]) - 1 and (self.matrix[row][col+1] != 2 and self.matrix[row][col+1] != 3)):
                return True
            return False
        
        for i in range(len(uniq)):
            for j in range(len(uniq[i])):
                row = uniq[i][j][0]
                col = uniq[i][j][1]
                uniq_start.append((row,col))
                if neighbors_down(row,col):
                    uniq_end.append((row+1,col))
                if neighbors_up(row,col):
                    uniq_end.append((row-1,col))
                if neighbors_left(row,col):
                    uniq_end.append((row,col-1))
                if neighbors_right(row,col):
                    uniq_end.append((row,col+1))
                    
        print(uniq_start)
        print(uniq_end)

        start_ver = []
        end_ver = []


        for i in range(len(new_matrix)):
            j = 0
            while j < (len(new_matrix[i])):
                if (new_matrix[i][j] == 2 or new_matrix[i][j] == 3):
                    start_ver.append((i, j))
                    if (new_matrix[i][j + 1] != 2 and new_matrix[i][j + 1] != 3):
                        end_ver.append((i, j + 1))
                        j += 1
                    else:
                        while (new_matrix[i][j + 1] == 2 or new_matrix[i][j + 1] == 3):
                            j += 1
                        end_ver.append((i, j + 1))
                        j += 1
                j += 1

        with open(self.maze_name, 'w') as tex_file:
            print('\\documentclass[10pt]{article}\n'
                  '\\usepackage{tikz}\n'
                  '\\usetikzlibrary{shapes.misc}\n'
                  '\\usepackage[margin=0cm]{geometry}\n'
                  '\\pagestyle{empty}\n'
                  '\\tikzstyle{every node}=[cross out, draw, red]\n'
                  '\n'
                  '\\begin{document}\n'
                  '\n'
                  '\\vspace*{\\fill}\n'
                  '\\begin{center}\n'
                  '\\begin{tikzpicture}[x=0.5cm, y=-0.5cm, ultra thick, blue]\n'
                  '% Walls', file=tex_file
                  )
            for i in range(len(start_hor)):
                print('    \\draw ('+str(start_hor[i][0])+','+str(start_hor[i][1])+') -- ('+str(end_hor[i][0])+','+str(end_hor[i][1])+');', file=tex_file)
            for i in range(len(start_ver)):
                print('    \\draw ('+str(start_ver[i][0])+','+str(start_ver[i][1])+') -- ('+str(end_ver[i][0])+','+str(end_ver[i][1])+');', file=tex_file)
            print('% Pillars', file=tex_file)
            for i in pillars:
                print('    \\fill[green] ('+str(i[0])+','+str(i[1])+') circle(0.2);', file=tex_file)
            print('% Inner points in accessible cul-de-sacs', file=tex_file)
            for i in culde:
                print('    \\node at ('+str(i[0])+','+str(i[1])+') {};', file=tex_file)
            print('\\end{tikzpicture}\n'
                  '\\end{center}\n'
                  '\\vspace*{\\fill}\n\n'
                  '\\end{document}', file=tex_file)
            
        self.print_flag = True



m = Maze('maze_1.txt')
m.display()
m.analyse()
# print(m.possible_cul)