# -*- coding: utf-8 -*-
import json
from dash import Dash, dcc, html, ctx
from dash.dependencies import Input, Output, State
import dash_cytoscape as cyto
import util

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

title1 = "txt/KT/천재교육_고등_확률과통계_1단원"
title2 = "txt/KT/천재교육_고등_확률과통계_2단원"
num_node = 14
scale = 7
edge_option = "ss"
word_option = "TF"
cut_option = "PFNET"
r = float("inf")
KG1 = graph.KnowledgeGraph(title1, num_node, scale, edge_option, word_option, cut_option, r)
KG2 = graph.KnowledgeGraph(title2, num_node, scale, edge_option, word_option, cut_option, r)

def get_node_and_edges(KG, common_nodes=None, common_edges=None):
    print("common edges : ", common_edges)
    print("ddddd : ", KG.cut_G.edges(data=True))
    pos = nx.spring_layout(KG.cut_G)
    nodes = [
        {
            'data': {'id': elem, 'label': elem},
            'position': {'x': pos[elem][0]*300, 'y': pos[elem][1]*300}, 
            'classes': 'normal_node' if common_nodes == None or elem.split()[0] not in common_nodes else 'yellow'
        }
        for elem in pos
    ]

    edges = [
        {
            'data': {'source': source, 'target': target, 'weight': w['weight']},
            'classes': 'normal_edge' if common_edges == None \
            or ((source.split()[0], target.split()[0]) not in common_edges and \
            (target.split()[0], source.split()[0]) not in common_edges) else 'orange'
        }
        for (source, target, w) in KG.cut_G.edges(data=True)
    ]
    
    return nodes, edges

nodes1, edges1 = get_node_and_edges(KG1)
nodes2, edges2 = get_node_and_edges(KG2)

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

    # Class selectors
    {
        'selector': '.red',
        'style': {
            'background-color': 'red',
            'line-color': 'red'
        }
    },
    {
        'selector': '.yellow',
        'style': {
            'background-color': '#F7D219',
            'line-color': '#'
        }
    },
    {
        'selector': '.orange',
        'style': {
            'background-color': '#CB6B22',
            'line-color': '#CB6B22'
        }
    },
    {
        'selector': '.normal_node',
        'style': {
            'background-color': '#13E6B5',
            'line-color': '#13E6B5'
        }
    },
    {
        'selector': '.normal_edge',
        'style': {
            'background-color': '#235AF0',
            'line-color': '#235AF0'
        }
    },    


]

app.layout = html.Div([

    html.Div([
        html.Div([
            cyto.Cytoscape(
                id='cytoscape-event-callbacks-1',
                layout={'name': 'preset'},
                elements=edges1+nodes1,
                stylesheet=default_stylesheet,
                style={'width': '100%', 'height': '450px', 'display': 'inline-block'}
            ),
        ], style={'width': '50%', 'display': 'inline-block', 'float': 'left', 'margin': '10px', }),

        
        html.Div([
            html.Span([
                "Select edge option",
                dcc.Dropdown(
                    ['ss', 'ps', 'scs', 'pcs'],
                    value='ss',
                    id='edge-option1'
                )
            ], style={'width': '40%', 'float': 'left', 'margin': '10px'}),
            
            html.Span([
                "Select word rank option",
                dcc.Dropdown(
                    ['TF', 'TextRank'],
                    value='TF',
                    id='word-option1'
                )
            ], style={'width': '40%', 'float': 'left', 'margin': '10px'}),
            
            html.Span([
                "Select edge cutting option",
                dcc.Dropdown(
                    ['dijkstra', 'MST', 'PFNET'],
                    value='PFNET',
                    id='cut-option1'
                )
            ], style={'width': '40%', 'float': 'left', 'margin': '10px'}),

            html.Span([
                "Select r value",
                dcc.Dropdown(
                    [1, 2, 4, 10, 'INF'],
                    value='INF',
                    id='r1'
                )
            ], style={'width': '40%', 'float': 'left', 'margin': '10px'}),

            html.Span([
                html.Div([
                "Scale( > 1 )  ",
                ]),
                dcc.Input(id='scale1', type='number', value=7),
            ], style={'width': '40%', 'float': 'left', 'margin': '10px'}),

            html.Span([
                html.Div([
                    "Number of node  ",
                ]),
                dcc.Input(id='num-node1', type='number', value=14)   
            ], style={'width': '40%', 'float': 'left', 'margin': '10px'}),
                
            html.Span([
                "Layout option",
                dcc.Dropdown(
                    id='dropdown-update-layout1',
                    value='cola',
                    clearable=False,
                    options=[
                        {'label': name.capitalize(), 'value': name}
                        for name in ['cola', 'grid', 'circle', 'cose', 'euler', 'dagre']
                    ]
                ),
            ], style={'width': '40%', 'float': 'left', 'margin': '10px'}),

            html.Div([
                html.Div([
                "Update",
                ]),
                html.Button(id='submit-button-state1', n_clicks=0, children='Update'),
            ], style={'width': '40%', 'float': 'left', 'display': 'block', 'margin': '10px'}),

            html.Div([
                "Correlation(Coherence) : ",
                html.Span(id='correlation1', children=0),
            ], style={'width': '80%', 'float': 'left', 'display': 'block', 'margin': '10px', }),

        ], style={'width': '30%', 'float': 'left', 'display': 'inline-block', 'margin': '10px'}),

    ], style={'width': '100%', 'float': 'left', 'display': 'inline-block', 'margin': '10px'}),
    
    html.Span([
        "Graph similarity : ",
        html.Span(id='graphsim', children=0, style={'margin': '20px', 'display':'inline-block'}),
        html.Button(id='simiarity-button', n_clicks=0, children='Calculate simiarity'),
    ], style={'width': '80%', 'float': 'right', 'display': 'inline-block', 'margin': '10px'}),


    html.Div([
        html.Div([
            cyto.Cytoscape(
                id='cytoscape-event-callbacks-2',
                layout={'name': 'preset'},
                elements=edges2+nodes2,
                stylesheet=default_stylesheet,
                style={'width': '100%', 'height': '450px', 'display': 'inline-block'}
            ),
        ], style={'width': '50%', 'display': 'inline-block', 'float': 'left', 'margin': '10px', }),

        
        html.Div([
            html.Span([
                "Select edge option",
                dcc.Dropdown(
                    ['ss', 'ps', 'scs', 'pcs'],
                    value='ss',
                    id='edge-option2'
                )
            ], style={'width': '40%', 'float': 'left', 'margin': '10px'}),
            
            html.Span([
                "Select word rank option",
                dcc.Dropdown(
                    ['TF', 'TextRank'],
                    value='TF',
                    id='word-option2'
                )
            ], style={'width': '40%', 'float': 'left', 'margin': '10px'}),
            
            html.Span([
                "Select edge cutting option",
                dcc.Dropdown(
                    ['dijkstra', 'MST', 'PFNET'],
                    value='PFNET',
                    id='cut-option2'
                )
            ], style={'width': '40%', 'float': 'left', 'margin': '10px'}),

            html.Span([
                "Select r value",
                dcc.Dropdown(
                    [1, 2, 4, 10, 'INF'],
                    value='INF',
                    id='r2'
                )
            ], style={'width': '40%', 'float': 'left', 'margin': '10px'}),

            html.Span([
                html.Div([
                "Scale( > 1 )  ",
                ]),
                dcc.Input(id='scale2', type='number', value=7),
            ], style={'width': '40%', 'float': 'left', 'margin': '10px'}),

            html.Span([
                html.Div([
                    "Number of node  ",
                ]),
                dcc.Input(id='num-node2', type='number', value=14)   
            ], style={'width': '40%', 'float': 'left', 'margin': '10px'}),
                
            html.Span([
                "Layout option",
                dcc.Dropdown(
                    id='dropdown-update-layout2',
                    value='cola',
                    clearable=False,
                    options=[
                        {'label': name.capitalize(), 'value': name}
                        for name in ['cola', 'grid', 'circle', 'cose', 'euler', 'dagre']
                    ]
                ),
            ], style={'width': '40%', 'float': 'left', 'margin': '10px'}),

            html.Div([
                html.Div([
                "Update",
                ]),
                html.Button(id='submit-button-state2', n_clicks=0, children='Update'),
            ], style={'width': '40%', 'float': 'left', 'display': 'block', 'margin': '10px'}),

            html.Div([
                "Correlation(Coherence) : ",
                html.Span(id='correlation2', children=0),
            ], style={'width': '80%', 'float': 'left', 'display': 'block', 'margin': '10px', }),

        ], style={'width': '30%', 'float': 'left', 'display': 'inline-block', 'margin': '10px'}),

    ], style={'width': '100%', 'float': 'left', 'display': 'inline-block', 'margin': '10px'}),

])

@app.callback(
    Output('cytoscape-event-callbacks-1', 'elements'),
    Input('submit-button-state1', 'n_clicks'),
    Input('graphsim', 'children'),
#    Input('simiarity-button', 'n_clicks'),
    State('num-node1', 'value'),
    State('scale1', 'value'),
    State('r1', 'value'),
    State('edge-option1', 'value'),
    State('word-option1', 'value'),
    State('cut-option1', 'value'),
)
def update_graph1(n_clicks, children, num_node, scale, r, edge_option, word_option, cut_option):
    #print("num_node, scale, e, w, c, r : ", num_node, scale, edge_option, word_option)
    triggered_id = ctx.triggered_id
    global KG1, nodes1, edges1

    if triggered_id == 'graphsim':
        nodes1, edges1 = get_node_and_edges(KG1, util.common_nodes, util.common_edges)
        return edges1+nodes1
    elif triggered_id == 'submit-button-state1':
        if r == 'INF':
            r = float('inf')
        KG1 = graph.KnowledgeGraph(title1, num_node, scale, edge_option, word_option, cut_option, r)
        nodes1, edges1 = get_node_and_edges(KG1)
        return edges1+nodes1

@app.callback(
    Output('cytoscape-event-callbacks-1', 'layout'),
    Input('submit-button-state1', 'n_clicks'),
    State('dropdown-update-layout1', 'value'),
)
def layout_change1(n_clicks, layout):
    return {
        'name': layout,
        'animate': True
    }

@app.callback(
    Output('correlation1', 'children'),
    Input('cytoscape-event-callbacks-1', 'elements'),
)
def update_corr1(element):
    return '{}'.format(KG1.r)


@app.callback(
    Output('cytoscape-event-callbacks-2', 'elements'),
    Input('submit-button-state2', 'n_clicks'),
    Input('graphsim', 'children'),
#    Input('simiarity-button', 'n_clicks'),
    State('num-node2', 'value'),
    State('scale2', 'value'),
    State('r2', 'value'),
    State('edge-option2', 'value'),
    State('word-option2', 'value'),
    State('cut-option2', 'value'),
)
def update_graph2(n_clicks, children, num_node, scale, r, edge_option, word_option, cut_option):
    #print("num_node, scale, e, w, c, r : ", num_node, scale, edge_option, word_option)
    triggered_id = ctx.triggered_id
    global KG2, nodes2, edges2

    if triggered_id == 'graphsim':
        nodes2, edges2 = get_node_and_edges(KG2, util.common_nodes, util.common_edges)
        return edges2+nodes2
    elif triggered_id == 'submit-button-state2':
        if r == 'INF':
            r = float('inf')
        KG2 = graph.KnowledgeGraph(title2, num_node, scale, edge_option, word_option, cut_option, r)
        nodes2, edges2 = get_node_and_edges(KG2)
        return edges2+nodes2

@app.callback(
    Output('cytoscape-event-callbacks-2', 'layout'),
    Input('submit-button-state2', 'n_clicks'),
    State('dropdown-update-layout2', 'value'),
)
def layout_change2(n_clicks, layout):
    return {
        'name': layout,
        'animate': True
    }

@app.callback(
    Output('correlation2', 'children'),
    Input('cytoscape-event-callbacks-2', 'elements'),
)
def update_corr2(element):
    return '{}'.format(KG2.r)


@app.callback(
    #Output('cytoscape-event-callbacks-1', 'elements'),
    Output('graphsim', 'children'),
    Input('simiarity-button', 'n_clicks'),
)
def update_sim(n_click):
    #print("num_node, scale, e, w, c, r : ", num_node, scale, edge_option, word_option)
    util.graph_similarity(KG1, KG2)
    return util.graph_sim




if __name__ == '__main__':
    app.run_server(debug=True)