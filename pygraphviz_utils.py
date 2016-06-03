from pygraphviz import AGraph


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
    """Build a pygraphviz.AGraph object from a map dictionary
    Args:
        map_data (dict): A dictionary with the following keys:
            name (string): The name of the map.
            cities (dict): The cities on the map as values with unique keys.
            segments (dict[]): The segments that connect cities, each a
                             dictionary with the following keys:
                cities (string[]): A list of the keys of the two cites that the
                               segment connects.
                color (string): The color of the segment, one of 'yellow',
                                'red', 'green', 'blue', 'orange', 'pink',
                                'black', 'white', or '' (for a wildcard route)
                length (int): The number of cards required to play that segment
            tickets (dict[]): A list of dictionaries representing ticket cards
                              with the following keys:
                cities(string[]): The keys of the two cities to be connected
                                  for the ticket
                points(int): The number of points the completed ticket is worth
            length_scale(dict): A mapping of the number of points a segment
                                 of a given length is worth

    Returns:
        Graph: the graph of the map_data
    """
    cities = map_data.get('cities', {})
    segments = map_data.get('segments', [])

    graph = AGraph(name=map_data.get('name'),
                   strict=False,
                   directed=False,
                   **GRAPH_ATTRS)

    for key, name in cities.items():
        graph.add_node(key,
                       # label=key.upper(),
                       tooltip=name,
                       **NODE_ATTRS)

    for segment in segments:
        cities = segment.get('cities', None)
        length = segment.get('length', 0)
        attrs = {
            'label': str(length),
            'len': str(length),
            'color': segment.get('color', EDGE_ATTRS['color'])
        }
        if cities:
            graph.add_edge(*cities, **attrs)

    return graph


def render_graph(graph, raw_ext=None, ext='svg', engine='neato'):
    """Render the graph to graphviz output files

    Args:
        graph (pygraphviz.AGraph):
    """
    path = 'graphs/'
    if raw_ext:
        path = "{}{}.{}".format(path, graph.name, raw_ext)
        graph.draw(path=path)

    return graph.draw(path='{}.{}'.format(path, ext),
                      prog=engine)


def render_graph_from_map_data(map_data):
    return render_graph(create_graph_from_map_data(map_data))
