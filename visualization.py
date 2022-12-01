# -*- coding: utf-8 -*-
import json
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import dash_cytoscape as cyto

import graph
import networkx as nx

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

def get_node_and_edges(title, num_node, scale, e_option, w_option, c_option, r):
    KG = graph.KnowledgeGraph(title, num_node, scale, e_option, w_option, c_option, r)
    pos = nx.spring_layout(KG.cut_G)

    nodes = [
        {
            'data': {'id': elem, 'label': elem},
            'position': {'x': pos[elem][0]*300, 'y': pos[elem][1]*300}
        }
        for elem in pos
    ]

    edges = [
        {'data': {'source': source, 'target': target}}
        for (source, target) in KG.cut_G.edges
    ]
    
    return nodes, edges

title = "녹차 속 폴리페놀"
num_node = 14
scale = 7
edge_option = "scs"
word_option = "Term-Frequency"
cut_option = "PFNET"
r = float("inf")

nodes, edges = get_node_and_edges(title, num_node, scale, edge_option, word_option, cut_option, r)

default_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'background-color': '#BFD7B5',
            'label': 'data(label)'
        }
    }
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
    ], style={'width': '60%', 'height': '450px', 'float': 'left', 'margin': '10px', }),
    
    html.Span([
        "Select edge option",
        dcc.Dropdown(
            ['ss', 'ps', 'scs', 'pcs'],
            value='ss',
            id='edge-option'
        )
    ], style={'width': '15%', 'float': 'left', 'margin': '10px'}),
    
    html.Span([
        "Select word rank option",
        dcc.Dropdown(
            ['Term-Frequency', 'TextRank'],
            value='Term-Frequency',
            id='word-option'
        )
    ], style={'width': '15%', 'float': 'left', 'margin': '10px'}),
    
    html.Span([
        "Select edge cutting option",
        dcc.Dropdown(
            ['dijkstra', 'MST', 'PFNET'],
            value='PFNET',
            id='cut-option'
        )
    ], style={'width': '15%', 'float': 'left', 'margin': '10px'}),

    html.Span([
        "Select r value",
        dcc.Dropdown(
            [1, 2, 4, 10, 'INF'],
            value='INF',
            id='r'
        )
    ], style={'width': '15%', 'float': 'left', 'margin': '10px'}),

    html.Span([
        "num node  ",
        dcc.Input(id='num-node', type='number', value=14)   
    ], style={'width': '15%', 'float': 'left', 'margin': '10px'}),
    
    html.Span([
        "scale( > 1 )  ",
        dcc.Input(id='scale', type='number', value=7),
    ], style={'width': '15%', 'float': 'left', 'margin': '10px'}),
        
    html.Div([
        html.Button(id='submit-button-state', n_clicks=0, children='Update'),
    ], style={'width': '20%', 'float': 'left', 'display': 'block', 'margin': '10px'}),
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
    nodes, edges = get_node_and_edges(title, num_node, scale, edge_option, word_option, cut_option, r)
    return edges+nodes



if __name__ == '__main__':
    app.run_server(debug=True)