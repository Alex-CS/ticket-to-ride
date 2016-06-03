import json
from collections import namedtuple

import networkx as nx

from constants import EDGE_COLOR
from constants import GRAPH_CONFIG

Route = namedtuple('Route', 'cities, length, color')
Ticket = namedtuple('Ticket', 'cities, points')


class GameMap(object):

    def __init__(self, name, cities, routes, tickets, length_scale):
        """
        Keyword Args:
            name (str): The name of the map

            cities (dict): The cities in the game map as values w/ unique keys

            routes (list[dict]): The routes that connect cities, each a
                                   dictionary with the following keys:
                cities (list[str]): A list of the keys of the two cites that
                                    the route connects.
                color (string): The color of the route, one of 'yellow',
                                'red', 'green', 'blue', 'orange', 'pink',
                                'black', 'white', or '' (for a wildcard route)
                length (int): The number of cards required to play that route

            tickets (list[dict]): A list of dictionaries representing ticket
                                  cards with the following keys:
                cities(list[str]): The keys of the two cities to connect in
                                   order to complete the ticket
                points(int): The number of points the completed ticket is worth

            length_scale(dict): A mapping of route length to the number of
                                 points it is worth
        """
        self.name = name
        self.cities = cities
        self.routes = [Route(**route) for route in routes]
        self.tickets = [Ticket(**ticket) for ticket in tickets]
        self.length_scale = {int(key): val for key, val
                             in length_scale.items()}

        self.graph = nx.MultiGraph(name=self.name, **GRAPH_CONFIG)

        # Construct the graph
        for key, name in self.cities.items():
            self.graph.add_node(key,
                                xlabel=name,
                                label='',
                                tooltip=name)

        for route in self.routes:
            attrs = {
                'label': str(route.length),
                'len': str(route.length),
                'color': route.color or EDGE_COLOR
            }
            self.graph.add_edge(*route.cities, **attrs)


def load_map(json_map_filename):
    """Load a json map file from the data directory.
    Args:
        json_map_filename (str): name of the file to load w/o the extension

    Returns:
        (dict): The loaded content of the json map file
    """
    with open('data/{}.json'.format(json_map_filename)) as map_file:
        return json.load(map_file)


def save_graph(graph, raw_ext=None, ext='svg', engine='neato'):
    """Save the graph to graphviz output files

    Args:
        graph (pygraphviz.AGraph):
        raw_ext (str):
        ext (str):
        engine (str): What rendering engine to use.
                      Options are neato|dot|twopi|circo|fdp|nop
    """
    path = 'graphs/'
    if raw_ext:
        path = "{}{}.{}".format(path, graph.name, raw_ext)
        print("Rendering to", path)
        graph.draw(path=path, prog=engine)
    if ext:
        path = '{}.{}'.format(path, ext)

    print("Rendering to", path)
    graph.draw(path=path, prog=engine)


if __name__ == '__main__':
    usa = GameMap(**load_map('usa'))
    pygv = nx.nx_agraph.to_agraph(usa.graph)
    save_graph(pygv, 'dot')
