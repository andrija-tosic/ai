# 6. Napisati funkciju koja formira stablo traženja za zadati graf, zadati polazni čvor i izabrani algoritam
# koji se koristiti za obilazak stabla. Student sam bira algoritam za koji se formira stablo traženja.
import queue
from typing import NamedTuple

Key = str

Priority = int


class GraphNode(NamedTuple):
    priority: Priority
    adj: list[Key]


Graph = dict[Key, GraphNode]

NodeChildren = list[Key]

Node = dict[Key, NodeChildren]


def tree_from_best_first_search(graph: Graph, start: Key, end: Key) -> Node:
    priority_queue = queue.PriorityQueue[tuple[Priority, Key]](len(graph))
    visited = set[Key]()
    prev_nodes = dict[Key, Key | None]()
    prev_nodes[start] = None
    visited.add(start)
    priority_queue.put((graph[start].priority, start))
    found_dest = False

    tree = Node()

    while (not found_dest) and (not priority_queue.empty()):
        priority, node_key = priority_queue.get()

        tree[node_key] = NodeChildren()

        for adj_key in graph[node_key].adj:

            tree[node_key].append(adj_key)

            print(node_key, "->", adj_key)

            if adj_key not in visited:
                prev_nodes[adj_key] = node_key
                if adj_key is end:
                    found_dest = True
                    break
                visited.add(adj_key)

                priority_queue.put((graph[adj_key].priority, adj_key))

    return tree


graph_simple: Graph = {
    "A": GraphNode(9, ["B", "C"]),
    "B": GraphNode(6, ["D", "E"]),
    "C": GraphNode(7, ["F", "G"]),
    "D": GraphNode(4, ["H"]),
    "E": GraphNode(8, ["G", "I"]),
    "F": GraphNode(3, ["J"]),
    "G": GraphNode(4, ["J"]),
    "H": GraphNode(4, []),
    "I": GraphNode(3, ["J"]),
    "J": GraphNode(0, [])
}

tree = tree_from_best_first_search(graph_simple, "A", "J")

print("Tree:", tree)
