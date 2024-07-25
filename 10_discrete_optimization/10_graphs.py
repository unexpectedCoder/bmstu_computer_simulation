class Node:
    def __init__(self, name):
        self._name = name
    def __str__(self):
        return self.name
    @property
    def name(self):
        return self.name

class Edge:
    def __init__(self, src, dest):
        self._src = src
        self._dest = dest
    def __str__(self):
        return f"{self._src.name} -> {self._dest.name}"
    @property
    def source(self):
        return self._src
    @property
    def destination(self):
        return self._dest

class Digraph:
    def __init__(self):
        self._edges = {}
    def add_node(self, node):
        if node in self._edges:
            raise ValueError('дублирующий узел')
        self._edges[node] = []
    def add_edge(self, edge):
        src = edge.source
        dest = edge.destination
        if not (src in self.edges and dest in self.edges):
            raise ValueError('нет узла в графе')
        self._edges[src].append(dest)
    def children_of(self, node):
        return self.edges[node]
    def has_node(self, node):
        return node in self._edges
    def get_node(self, name):
        for n in self._edges:
            if n.name == name:
                return n
        raise NameError(name)
    def __str__(self):
        result = ""
        for src in self.edges:
            for dest in self.edges[src]:
                result = f"{result} {src.name} -> {dest.name}\n"
        return result[:-1]

class Graph(Digraph):
    def add_edge(self, edge):
        Digraph.add_edge(self, edge)
        rev = Edge(edge.destination, edge.source)
        Digraph.add_edge(self, rev)

def build_city_graph():
    g = Digraph()
    cities = (
        'Boston', 'Providence', 'New York', 'Chicago',
        'Denver', 'Phoenix', 'Los Angeles'
    )
    for name in cities:
        g.add_node(Node(name))
    g.add_edge(Edge(g.get_node('Boston'), g.get_node('Providence')))
    g.add_edge(Edge(g.get_node('Boston'), g.get_node('New York')))
    g.add_edge(Edge(g.get_node('Providence'), g.get_node('Boston')))
    g.add_edge(Edge(g.get_node('Providence'), g.get_node('New York')))
    g.add_edge(Edge(g.get_node('New York'), g.get_node('Chicago')))
    g.add_edge(Edge(g.get_node('Chicago'), g.get_node('Denver')))
    g.add_edge(Edge(g.get_node('Denver'), g.get_node('Phoenix')))
    g.add_edge(Edge(g.get_node('Denver'), g.get_node('New York')))
    g.add_edge(Edge(g.get_node('Chicago'), g.get_node('Phoenix')))
    g.add_edge(Edge(g.get_node('Los Angeles'), g.get_node('Boston')))

def dfs(graph, start, end, path, shortest):
    path = path + [start]
    if start == end:
        return path
    for node in graph.children_of(start):
        if node not in path: # избегаем циклов
            if shortest == None or len(path) < len(shortest):
                new_path = dfs(graph, node, end, path, shortest)
                if new_path != None:
                    shortest = new_path
    return shortest

def shortest_path(graph, start, end):
    return dfs(graph, start, end, [], None)

def test_sp(source, destination):
    g = build_city_graph()
    sp = shortest_path(g, g.get_node(source), g.get_node(destination))
    if sp != None:
        print(f"Кратчайший путь из {source} в {destination}: {print_path(sp)}")
    else:
        print(f"Нет пути из {source} в {destination}")

test_sp('Boston', 'Chicago')

def bfs(graph, start, end):
    init_path = [start]
    path_queue = [init_path]
    while len(path_queue) != 0:
        #Get and remove oldest element in pathQueue
        tmp_path = path_queue.pop(0)
        print('Current BFS path:', print_path(tmp_path))
        last_node = tmp_path[-1]
        if last_node == end:
            return tmp_path
    for next_node in graph.children_of(last_node):
        if next_node not in tmp_path:
            new_path = tmp_path + [next_node]
            path_queue.append(new_path)
    return None
