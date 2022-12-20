# -*- coding: utf-8 -*-
import json
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import dash_cytoscape as cyto

import graph
import networkx as nx

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# Load extra layouts
cyto.load_extra_layouts()

app = Dash(__name__, external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

title = "녹차 속 폴리페놀"
num_node = 14
scale = 7
edge_option = "scs"
word_option = "Term-Frequency"
cut_option = "PFNET"
r = float("inf")
KG = graph.KnowledgeGraph(title, num_node, scale, edge_option, word_option, cut_option, r)

def get_node_and_edges():
    pos = nx.spring_layout(KG.cut_G)

    nodes = [
        {
            'data': {'id': elem, 'label': elem},
            'position': {'x': pos[elem][0]*300, 'y': pos[elem][1]*300}
        }
        for elem in pos
    ]

    edges = [
        {'data': {'source': source, 'target': target, 'weight': w['weight']}}
        for (source, target, w) in KG.cut_G.edges(data=True)
    ]
    
    return nodes, edges

nodes, edges = get_node_and_edges()

default_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'background-color': '#BFD7B5',
            'label': 'data(label)'
        }
    },
    {
        'selector': 'edge',
        'style': {
            'label': 'data(weight)'
        }
    },
]

app.layout = html.Div([

    html.Div([
        cyto.Cytoscape(
            id='cytoscape-event-callbacks-1',
            layout={'name': 'preset'},
            elements=edges+nodes,
            stylesheet=default_stylesheet,
            style={'width': '100%', 'height': '450px'}
        ),
    ], style={'width': '40%', 'display': 'block', 'float': 'left', 'margin': '10px', }),

    html.Div([
        html.Span(id='correlation', children=KG.r),
    ], style={'width': '60%', 'float': 'left', 'display': 'block', 'margin': '10px', }),

    html.Div([
        html.Span([
            "Select edge option",
            dcc.Dropdown(
                ['ss', 'ps', 'scs', 'pcs'],
                value='ss',
                id='edge-option'
            )
        ], style={'width': '30%', 'float': 'left', 'margin': '10px'}),
        
        html.Span([
            "Select word rank option",
            dcc.Dropdown(
                ['Term-Frequency', 'TextRank'],
                value='Term-Frequency',
                id='word-option'
            )
        ], style={'width': '30%', 'float': 'left', 'margin': '10px'}),
        
        html.Span([
            "Select edge cutting option",
            dcc.Dropdown(
                ['dijkstra', 'MST', 'PFNET'],
                value='PFNET',
                id='cut-option'
            )
        ], style={'width': '30%', 'float': 'left', 'margin': '10px'}),

        html.Span([
            "Select r value",
            dcc.Dropdown(
                [1, 2, 4, 10, 'INF'],
                value='INF',
                id='r'
            )
        ], style={'width': '30%', 'float': 'left', 'margin': '10px'}),

        html.Span([
            "Layout option",
            dcc.Dropdown(
                id='dropdown-update-layout',
                value='cola',
                clearable=False,
                options=[
                    {'label': name.capitalize(), 'value': name}
                    for name in ['cola', 'grid', 'circle', 'cose', 'euler', 'dagre']
                ]
            ),
        ], style={'width': '30%', 'float': 'left', 'margin': '10px'}),

        html.Span([
            html.Div([
                "num node  ",
            ]),
            dcc.Input(id='num-node', type='number', value=14)   
        ], style={'width': '30%', 'float': 'left', 'margin': '10px'}),
        
        html.Span([
            html.Div([
            "scale( > 1 )  ",
            ]),
            dcc.Input(id='scale', type='number', value=7),
        ], style={'width': '30%', 'float': 'left', 'margin': '10px'}),
            
        html.Div([
            html.Button(id='submit-button-state', n_clicks=0, children='Update'),
        ], style={'width': '30%', 'float': 'left', 'display': 'block', 'margin': '10px'}),

    ], style={'width': '40%', 'float': 'left', 'display': 'block', 'margin': '10px'}
    )
])

@app.callback(
    Output('cytoscape-event-callbacks-1', 'elements'),
    Input('submit-button-state', 'n_clicks'),
    State('num-node', 'value'),
    State('scale', 'value'),
    State('r', 'value'),
    State('edge-option', 'value'),
    State('word-option', 'value'),
    State('cut-option', 'value'),
)
def update_graph(n_clicks, num_node, scale, r, edge_option, word_option, cut_option):
    #print("num_node, scale, e, w, c, r : ", num_node, scale, edge_option, word_option)
    if r == 'INF':
        r = float('inf')
    global KG
    KG = graph.KnowledgeGraph(title, num_node, scale, edge_option, word_option, cut_option, r)
    nodes, edges = get_node_and_edges()
    return edges+nodes

@app.callback(
    Output('cytoscape-event-callbacks-1', 'layout'),
    Input('submit-button-state', 'n_clicks'),
    State('dropdown-update-layout', 'value'),
)
def layout_change(n_clicks, layout):
    return {
        'name': layout,
        'animate': True
    }

@app.callback(
    Output('correlation', 'children'),
    Input('cytoscape-event-callbacks-1', 'elements'),
)
def update_corr(element):
    return 'Correlation score : {}'.format(KG.r)

if __name__ == '__main__':
    app.run_server(debug=True)