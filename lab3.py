# 7. Napisati funkciju koja na osnovu zadatog neusmerenog grafa i dva zadata (ciljna) čvora G1 i G2
# formira neusmereni graf sa heuristikom. Heuristika proizvoljnog čvora C se određuje kao
# udaljenost čvora C do bližeg od čvorova G1 i G2. Udaljenost se određuje kao dužina najkraćeg puta
# između dva čvora. Dužina puta se određuje kao broj potega koji čine taj put. Dozvoljeno je najviše
# dva puta pozvati prilagođeni algoritam obilaska grafa.

import queue


def flood(graph: dict[str, list[str]], start: str, heuristics: dict[str, int]) -> int:
    queue_nodes = queue.Queue[tuple[str, int]](len(graph))
    visited = set[str]()
    visited.add(start)
    queue_nodes.put((start, 0))

    while not queue_nodes.empty():
        (node, distance) = queue_nodes.get()

        # if node in heuristics:
        #     heuristics[node] = min(heuristics[node], distance)
        # else:

        heuristics[node] = distance

        for adj in graph[node]:
            if adj not in visited and (adj not in heuristics or (adj in heuristics and distance + 1 < heuristics[adj])):
                visited.add(adj)
                queue_nodes.put((adj, distance + 1))

    return len(visited)


def create_heuristic_graph(graph: dict[str, list[str]], G1: str, G2: str):

    heuristics = dict[str, int]()

    nodes_visited = flood(graph, G1, heuristics)
    nodes_visited += flood(graph, G2, heuristics)

    print("visited " + str(nodes_visited) + " nodes")

    new_graph = dict[str, tuple[int, list[str]]]()

    for node in graph:
        new_graph[node] = (heuristics[node], graph[node])

    return new_graph


graph_example = {
    "A": ["B", "C"],  # G1
    "B": ["D", "A"],  # G2
    "C": ["D", "E", "A"],
    "D": ["B", "F"],
    "E": ["F", "C"],
    "F": ["D", "E"]
}

graph_result = create_heuristic_graph(graph_example, "A", "B")

print(graph_result)

graph_result_primer: dict[str, tuple[int, list[str]]] = {
    "A": (0, ["B", "C"]),  # G1
    "B": (0, ["D", "A"]),  # G2
    "C": (1, ["D", "E", "A"]),
    "D": (1, ["B", "F"]),
    "E": (2, ["F", "C"]),
    "F": (2, ["D", "E"])
}
