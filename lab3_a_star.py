# 6. Napisati funkciju koja formira stablo traženja za zadati graf, zadati polazni čvor i izabrani algoritam
# koji se koristiti za obilazak stabla. Student sam bira algoritam za koji se formira stablo traženja.

def a_star(graph, start, end):
    found_end = False
    open_set = set(start)
    closed_set = set()
    g = {}
    prev_nodes = {}
    g[start] = 0
    prev_nodes[start] = None

    while len(open_set) > 0 and not found_end:
        node = None
        for next_node in open_set:
            if node is None or g[next_node] + graph[next_node][0] < g[node] + graph[node][0]:
                node = next_node

        if node == end:
            found_end = True
            break

        print(node, "\n")

        for (adj, cost) in graph[node][1]:
            if adj not in open_set and adj not in closed_set:
                open_set.add(adj)
                prev_nodes[adj] = node
                g[adj] = g[node] + cost
            elif g[adj] > g[node] + cost:
                g[adj] = g[node] + cost
                prev_nodes[adj] = node
                if adj in closed_set:
                    closed_set.remove(adj)
                    open_set.add(adj)

        open_set.remove(node)
        closed_set.add(node)

    path = []
    if found_end:
        prev = end
        while prev_nodes[prev] is not None:
            path.append(prev)
            prev = prev_nodes[prev]
            path.append(start)
    path.reverse()
    return path


graf = {
    "A": (9, [("B", 4), ("C", 6)]),
    "B": (6, [("D", 4), ("A", 2)]),
    "C": (2, [("D", 4), ("E", 1)]),
    "D": (2, [("E", 2), ("F", 3)]),
    "E": (3, [("F", 4)]),
    "F": (0, [("A", 1)])
}

path = a_star(graf, "A", "F")
print(path)
