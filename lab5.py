# 6. Implementirati Backtracking traženje u kombinaciji sa Forward checking tehnikom i MVR
# heuristikom za raspoređivanje kraljica na šahovskoj tabli dimenzije 8x8 tako da se ne napadaju.

from copy import deepcopy
from itertools import pairwise
from pprint import pprint


Graph = dict[int, set[int]]

N = 4

g = {
    i: {x for x in range(N) if x != i} for i in range(N)
}

available = dict[int, set[int]]()

for i in range(N):
    available[i] = set([x for x in range(N)])

# pprint(g)
pprint(available)


def print_board(row: int, col: int, available: dict[int, set[int]]):
    str_out = ""
    for i in range(N):
        for j in range(N):
            if i == row and j == col:
                str_out += ("[Q]")
            elif j in available[i]:
                str_out += ("[ ]")
            else:
                str_out += ("[x]")
        str_out += ('\n')

    print(str_out)


def pprint_board(visited_rows_columns: list[tuple[int, int]]):
    str_out = ""
    for i in range(N):
        for j in range(N):
            if (i, j) in visited_rows_columns:
                str_out += ("[Q]")
            else:
                str_out += ("[ ]")
        str_out += ('\n')
    print(str_out)


def f(g: Graph, k: int, available: dict[int, set[int]], visited_rows: list[int], visited_columns: list[int]) -> list[tuple[int, int]]:
    for col in available[k]:
        cpy = deepcopy(available)
        for c in range(0, N):
            cpy[k].discard(c)

        j = 0
        for row in range(k+1, N):

            j += 1
            cpy[row].discard(col)
            if col-j >= 0:
                cpy[row].discard(col-j)
            if col+j < N:
                cpy[row].discard(col+j)

        j = 0
        for row in range(k-1, -1, -1):
            j += 1
            cpy[row].discard(col)
            if col-j >= 0:
                cpy[row].discard(col-j)
            if col+j < N:
                cpy[row].discard(col+j)

        # forward checking: find MRV

        if k not in visited_rows:
            visited_rows.append(k)

        if col not in visited_columns:
            visited_columns.append(col)

        min = N+1
        min_key = 0
        for key in cpy:
            if key not in visited_rows and len(cpy[key]) < min:
                min = len(cpy[key])
                min_key = key

        print_board(k, col, cpy)

        print(list(zip(visited_rows, visited_columns)))

        if len(visited_columns) == N:
            return list(zip(visited_rows, visited_columns))

        if len(cpy[min_key]) == 0:
            print("Backtracking\n\n")
            return []

        cpy[k].discard(col)

        list_of_visited = f(g, min_key, cpy, visited_rows, visited_columns)
        if (len(list_of_visited) > 0):
            return list_of_visited
        else:
            visited_rows.pop()
            visited_columns.pop()
    return []


res = f(g, 0, available, [], [])

pprint_board(res)

pprint(res)
