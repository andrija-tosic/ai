# 6. Implementirati Backtracking traženje u kombinaciji sa Forward checking tehnikom i MVR
# heuristikom za raspoređivanje kraljica na šahovskoj tabli dimenzije 8x8 tako da se ne napadaju.

from collections import deque
from copy import deepcopy
from colorama import Fore, Style

Graph = dict[int, set[int]]


def print_search_step(N: int, row: int, col: int, available: Graph):
    str_out = ""
    for i in range(N):
        for j in range(N):
            if i == row and j == col:
                str_out += (Fore.YELLOW + "[Q]" + Style.RESET_ALL)
            elif j in available[i]:
                str_out += ("[ ]")
            else:
                str_out += (Fore.RED + "[x]" + Style.RESET_ALL)
        str_out += ('\n')

    print(str_out)


def print_solution(N: int, visited_rows_columns: list[tuple[int, int]]):
    str_out = ""
    for i in range(N):
        for j in range(N):
            if (i, j) in visited_rows_columns:
                str_out += (Fore.YELLOW + "[Q]" + Style.RESET_ALL)
            else:
                str_out += ("[ ]")
        str_out += ('\n')
    print(str_out)


def solve(N: int, k: int, availability_graph: Graph, visited_rows: deque, visited_columns: deque) -> list[tuple[int, int]]:
    for col in availability_graph[k]:
        remaining_values = deepcopy(availability_graph)
        for c in range(0, N):
            remaining_values[k].discard(c)

        j = 0
        for row in range(k+1, N):
            j += 1
            remaining_values[row].discard(col)
            if col-j >= 0:
                remaining_values[row].discard(col-j)
            if col+j < N:
                remaining_values[row].discard(col+j)

        j = 0
        for row in range(k-1, -1, -1):
            j += 1
            remaining_values[row].discard(col)
            if col-j >= 0:
                remaining_values[row].discard(col-j)
            if col+j < N:
                remaining_values[row].discard(col+j)

        if k not in visited_rows:
            visited_rows.append(k)

        if col not in visited_columns:
            visited_columns.append(col)

        # Forward checking: Find MRV
        min = N+1
        min_key = 0
        for key in remaining_values:
            if key not in visited_rows and len(remaining_values[key]) < min:
                min = len(remaining_values[key])
                min_key = key

        result_so_far = list(zip(list(visited_rows), list(visited_columns)))

        print(result_so_far)
        print_search_step(N, k, col, remaining_values)

        if len(visited_columns) == N:
            return result_so_far

        if len(remaining_values[min_key]) == 0:
            print("Backtracking\n\n")
            return []

        remaining_values[k].discard(col)

        list_of_visited = solve(N, min_key, remaining_values,
                                visited_rows, visited_columns)
        if (len(list_of_visited) > 0):
            return list_of_visited
        else:
            visited_rows.pop()
            visited_columns.pop()

    return []
