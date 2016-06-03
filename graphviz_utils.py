from graphviz import Graph


BG_COLOR = 'darkgoldenrod'
DEFAULT_COLOR = 'dimgray'
GRAPH_ATTRS = {
    'bgcolor': BG_COLOR,
    'margin': '0.1',
    'model': 'mds',
    'orientation': 'landscape',
    'outputOrder': 'nodesfirst',
    'pad': '0.5',
    'rankdir': 'TD',
    'start': 'self?10?',
}
EDGE_ATTRS = {
    'color': DEFAULT_COLOR,
}
NODE_ATTRS = {
    'fillcolor': 'white',
    'shape': 'circle',
    'style': 'filled',
}


def create_graph_from_map_data(map_data):
    """Build a Graph object from a map dictionary
    Args:
        map_data (dict):

    Returns:
        Graph: the graph of the map_data
    """
    cities = map_data.get('cities', {})
    segments = map_data.get('segments', [])

    graph = Graph(name=map_data.get('name'),
                  format='svg',
                  engine='neato',
                  edge_attr=EDGE_ATTRS,
                  graph_attr=GRAPH_ATTRS,
                  node_attr=NODE_ATTRS)

    for key, name in cities.items():
        graph.node(key, key.upper())

    for segment in segments:
        city1, city2 = segment.get('cities', [None, None])
        length = segment.get('length', 0)
        args = {
            'tail_name': city1,
            'head_name': city2,
            'label': str(length),
            'len': str(length),
        }
        color = segment.get('color', '')
        if color:
            args['color'] = color
        if city1 and city2:
            graph.edge(**args)

    return graph


def render_graph(graph):
    """Render the graph to graphviz output files

    Args:
        graph (Graph)
    """
    return graph.render(filename='{}.gv'.format(graph.name),
                        directory='graphs',
                        view=False)


def render_graph_from_map_data(map_data):
    return render_graph(create_graph_from_map_data(map_data))

if __name__ == '__main__':
    render_graph_from_map_data(load_map('usa'))
