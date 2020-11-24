from collections import defaultdict # this I used so that disctionary remain indexed.


def build_graph(edge_list):
    graph = defaultdict(list)
    seen_edges = defaultdict(int)
    for src, dst, weight in edge_list:
        seen_edges[(src, dst, weight)] += 1
        if seen_edges[(src, dst, weight)] > 1:  # this is for deuplicate entries
            continue
        graph[src].append((dst, weight))
    return graph


def dijkstra(graph, src, dst):
    nodes = []
    for n in graph:
        nodes.append(n)
        nodes += [x[0] for x in graph[n]]

    q = set(nodes)
    nodes = list(q)
    dist = dict()
    prev = dict()
    for n in nodes:
        dist[n] = float('inf')
        prev[n] = None

    dist[src] = 0

    while q:
        u = min(q, key=dist.get)
        q.remove(u)

        if dst is not None and u == dst:
            return dist[dst], prev

        for v, w in graph.get(u, ()):
            alt = dist[u] + w
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u

    return dist, prev


def find_path(pr, node):
    p = []
    while node != None:
        p.append(node)
        node = pr[node]
    return p[::-1]

def find_most_different(bevs1, bevs2):
    for bev1 in bevs1:
        for bev2 in bevs2:
            edges = [
                ("MILK", "LASSI", 2),
                ("LASSI", "RAITA", 1),
                ("RAITA", "SODA", 4),
                ("SODA", "TEA", 5),
                ("TEA", "MILKSHAKES", 3),
                ("MILKSHAKES", "TEA", 5),
                ("LEMONADE", "SODA", 2),
                ("JUICES", "LEMONADE", 1),
                ("COFFEE", "TEA", 3),
                ("SMOOTHIE", "MILKSHAKE", 1),
                ("SOFT DRINKS", "SMOOTIE", 4),
                ("MOCKTAILS", "SOFT DRINKS", 10),
                ("HOT CHOCOLATE", "COFFEE", 5),
                ("SHAKES", "FLOATS", 6),
                ("FLOATS", "THANDAI", 10),
                ("THANDAI", "LEMONADE", 5),
            ]

            g = build_graph(edges)

            print("Using Dijkstra's single source algorithm")

            d, prev = dijkstra(g,bev1, bev2)
            path = find_path(prev, bev2)
            print("S -> T: distance = "+str(d)+", path = "+str(path))

