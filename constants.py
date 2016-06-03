BG_COLOR = 'darkgoldenrod'
NODE_COLOR = 'white'
EDGE_COLOR = 'dimgray'
GRAPH_CONFIG = {
    'graph': {
        'bgcolor': BG_COLOR,
        'margin': '0.1',
        'model': 'mds',
        'esep': '+3',
        #'notranslate': 'true',
        #'orientation': 'landscape',
        #'rotate': '10',
        'outputOrder': 'nodesfirst',
        'pad': '0.5',
        'rankdir': 'LR',
        'start': 'self?10?',
    },

    'node': {
        'fillcolor': NODE_COLOR,
        'style': 'filled',
        'shape': 'circle',
    },

    'edge': {},
}
