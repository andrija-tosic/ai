# 6. Implementirati Backtracking traženje u kombinaciji sa Forward checking tehnikom i MVR
# heuristikom za raspoređivanje kraljica na šahovskoj tabli dimenzije 8x8 tako da se ne napadaju.

from copy import deepcopy
from colorama import Fore, Style

Graph = dict[int, set[int]]


def print_board(N: int, row: int, col: int, available: Graph):
    str_out = ""
    for i in range(N):
        for j in range(N):
            if i == row and j == col:
                str_out += (Fore.RED + "[Q]" + Style.RESET_ALL)
            elif j in available[i]:
                str_out += ("[ ]")
            else:
                str_out += ("[x]")
        str_out += ('\n')

    print(str_out)


def pprint_board(N: int, visited_rows_columns: list[tuple[int, int]]):
    str_out = ""
    for i in range(N):
        for j in range(N):
            if (i, j) in visited_rows_columns:
                str_out += (Fore.RED + "[Q]" + Style.RESET_ALL)
            else:
                str_out += ("[ ]")
        str_out += ('\n')
    print(str_out)


def solve(N: int, k: int, free_graph: Graph, visited_rows: list[int], visited_columns: list[int]) -> list[tuple[int, int]]:
    for col in free_graph[k]:
        graph_copy = deepcopy(free_graph)
        for c in range(0, N):
            graph_copy[k].discard(c)

        j = 0
        for row in range(k+1, N):
            j += 1
            graph_copy[row].discard(col)
            if col-j >= 0:
                graph_copy[row].discard(col-j)
            if col+j < N:
                graph_copy[row].discard(col+j)

        j = 0
        for row in range(k-1, -1, -1):
            j += 1
            graph_copy[row].discard(col)
            if col-j >= 0:
                graph_copy[row].discard(col-j)
            if col+j < N:
                graph_copy[row].discard(col+j)

        if k not in visited_rows:
            visited_rows.append(k)

        if col not in visited_columns:
            visited_columns.append(col)

        # Forward checking: find MRV
        min = N+1
        min_key = 0
        for key in graph_copy:
            if key not in visited_rows and len(graph_copy[key]) < min:
                min = len(graph_copy[key])
                min_key = key

        print_board(N, k, col, graph_copy)

        print(list(zip(visited_rows, visited_columns)))

        if len(visited_columns) == N:
            return list(zip(visited_rows, visited_columns))

        if len(graph_copy[min_key]) == 0:
            print("Backtracking\n\n")
            return []

        graph_copy[k].discard(col)

        list_of_visited = solve(N, min_key, graph_copy,
                                visited_rows, visited_columns)
        if (len(list_of_visited) > 0):
            return list_of_visited
        else:
            visited_rows.pop()
            visited_columns.pop()
    return []
