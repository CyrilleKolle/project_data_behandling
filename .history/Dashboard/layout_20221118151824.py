from dash import html, dcc, Dash
import dash_bootstrap_components as dbc
import pandas as pd

class Layout:
    def __init__(self, data_dict:dict) -> None:
        self.data_dict = data_dict


    def layout(self):
        return dbc.Container(
            [
                dbc.Card(
                    dbc.CardBody(html.H1("Vive La France")), className="mt-3"
                ),
                dbc.Row(
                    className="mt-4",
                    children=[
                        dbc.Col(
                            html.P("Most dominated sports by France"),
                            className="mt-1",
                            xs=12,
                            sm=12,
                            md=6,
                            lg=4,
                            xl={"offset": 2, "size": 2},
                        ),
                        dbc.Col(
                            dcc.Dropdown(
                                id="data-dropdown",
                         ZZZ
                                value="france_most",
                            ),
                            xs=12,
                            sm=12,
                            md=12,
                            lg=4,
                            xl=3,
                        ),
                    ],
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(id="france-max-graph"),
                     
                            ],
                            xs="12",
                            sm="12",
                            md="12",
                            lg={"size": 6},
                            xl="6",
                        ),
                       
                    ]
                ),
                # storing intermediate value on clients browser in order to share between several callbacks
                dcc.Store(id="filtered-df"),
            ],
            fluid=False,
        )
