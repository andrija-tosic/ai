# 6. Data je tabla N×N sa nizom zabranjenih polja na njoj (označena crvenom bojom), startno
# (označena plavom bojom) i ciljno (označena zelenom bojom) polje na tabli. Igrač može da pokreće
# figuru na tabli samo na jedno od susednih polja u horizontalnom i vertikalnom pravcu. Odrediti
# najkraći put od startnog do ciljnog polja. Zapamtiti put kojim se kretao igrač od starta do cilja.

from colorama import Fore,  Style
from queue import PriorityQueue
from typing import NamedTuple


class Point2D(NamedTuple):
    x: int
    y: int

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


Key = Point2D

Cost = int


Graph = dict[Key, list[Key]]


def within_bounds(n: int, i: int, j: int) -> bool:
    return 0 <= i < n and 0 <= j < n


def board_to_graph(n: int, start: Point2D, end: Point2D, forbidden: set[Point2D]) -> tuple[Graph, Key, Key]:
    graph = Graph()

    for i in range(n):
        for j in range(n):
            if Point2D(i, j) not in forbidden:
                point = Point2D(i, j)
                graph[point] = list[Key]()

                adjacent = [(i + 1, j), (i, j + 1),
                            (i - 1, j), (i, j - 1)]

                for p in adjacent:
                    (x, y) = p
                    if Point2D(x, y) not in forbidden and within_bounds(n, x, y):
                        graph[point].append(Point2D(x, y))

    return (graph, start, end)


def h(a: Point2D, b: Point2D) -> Cost:
    return abs(a.x - b.x) + abs(a.y - b.y)


def search(graph: Graph, start: Key, goal: Key):
    queue = PriorityQueue[tuple[Cost, Key]](len(graph))
    came_from = dict[Key, Key]()
    queue.put((0, start))

    cost_so_far = dict[Key, Cost]()
    cost_so_far[start] = 0

    reached_goal = False

    iterations = 0

    while not reached_goal and not queue.empty():
        _, node_key = queue.get()

        iterations += 1

        for adj_key in graph[node_key]:
            new_cost = cost_so_far[node_key] + 1

            if adj_key not in cost_so_far or new_cost < cost_so_far[adj_key]:
                came_from[adj_key] = node_key

                if adj_key == goal:
                    reached_goal = True
                    break

                cost_so_far[adj_key] = new_cost
                priority = new_cost + h(adj_key, goal)
                queue.put((priority, adj_key))

    path = list[Key]()

    if reached_goal:
        node_ptr = goal
        while node_ptr != start:
            path.append(node_ptr)
            node_ptr = came_from[node_ptr]
        path.append(start)
        path.reverse()

    return path, iterations


def draw_board(n: int, start: Point2D, end: Point2D, forbidden: set[Point2D], path: list[Point2D]) -> None:

    out_str = ""

    for i in range(n):
        for j in range(n):
            point = Point2D(j, i)

            if point == start:
                out_str += Fore.BLUE + "[s]"
            elif point == end:
                out_str += Fore.GREEN + "[c]"
            elif point in forbidden:
                out_str += Fore.RED + "[■]"
            elif point in path:
                # out_str += "[" + f"{path.index(point)}".center(3) + "]"
                out_str += Fore.YELLOW + "[*]"
            else:
                out_str += Style.RESET_ALL + "[ ]"

        out_str += "\n"
    print(out_str)


def diag_wall(n: int, start: Point2D, length: int, positive: bool) -> set[Point2D]:
    points = set[Point2D]()

    i = start.x
    j = start.y

    while (i < start.x+length and within_bounds(n, i, j)):
        # if i != start.x + int(length/2):
        points.add(Point2D(i, j))

        i += 1
        if positive:
            j -= 1
        else:
            j += 1

    return points


def wall(n: int, start: Point2D, length: int, vertical: bool) -> set[Point2D]:
    points = set[Point2D]()

    i = start.x
    j = start.y

    while (i < start.x+length and within_bounds(n, i, j)):
        # if i != start.x + int(length/2):
        points.add(Point2D(i, j))

        if vertical:
            j += 1
        else:
            i += 1

    return points
