from dash import html, dcc, Dash
import dash_bootstrap_components as dbc
import pandas as pd


class Layout:
    def __init__(self, symbol_dict: dict, countries_dict: dict) -> None:
        self._symbol_dict = symbol_dict

        self._olympics_options_dropdown = [
            {"label": name, "value": symbol} for symbol, name in symbol_dict.items()
        ]
        self._countries_options = [
            {"label": noc, "value": country} for country, noc in countries_dict.items()
        ]

    def layout(self):
        return dbc.Container(
            [
                dbc.Card(dbc.CardBody(html.H1("Vive La France")), className="mt-3"),
                dbc.Card(
                    dbc.CardBody(
                        dbc.Row(
                            children=[
                                dbc.Card(
                                    dbc.CardBody(
                                        children=[
                                            dbc.Col(
                                                html.Header(html.H2("Athlete Events")),
                                                className="mx-4",
                                                xs=12,
                                                sm=12,
                                                md=6,
                                                lg=3,
                                            ),
                                            dbc.Col(
                                                dcc.Dropdown(
                                                    id="olympic-dropdown",
                                                    options=self._olympics_options_dropdown,
                                                    value="athlete",
                                                ),
                                                className="mx-4",
                                                xs=12,
                                                sm=12,
                                                md=6,
                                                lg=3,
                                            ),
                                        ],
                                    )
                                )
                            ],
                        ),
                    )
                ),
                dbc.Row(
                    id="france-trophy",
                    className="mt-4",
                    children=[
                        dbc.Col(
                            className="mx-1",
                            children=[
                                dcc.Graph(
                                    id="france-max-graph",
                                ),
                            ],
                            xs=12,
                            sm=12,
                            md=12,
                            lg=5,
                        ),
                        dbc.Col(
                            className="mx-1",
                            children=[
                                dcc.Graph(
                                    id="france-all-ages",
                                ),
                            ],
                            xs=12,
                            sm=12,
                            md=12,
                            lg=5,
                        ),
                    ],
                ),
                dbc.Row(
                    className="mt-4",
                    children=[
                        dbc.Col(
                            children=[
                                dcc.Graph(
                                    id="france-medal-distribution",
                                    style={"display": "inline-block"},
                                ),
                            ],
                            xs=12,
                            sm=12,
                            md=12,
                            lg=8,
                        ),
                        dbc.Col(
                            children=[
                                dcc.Graph(
                                    id="top_10",
                                    style={"display": "inline-block"},
                                )
                            ],
                            xs=12,
                            sm=12,
                            md=12,
                            lg=3,
                        ),
                    ],
                ),
                dbc.Row(
                    className="mt-4",
                    children=[
                        dbc.Col(
                            className="mr-1",
                            children=[
                                dcc.Graph(
                                    id="goat-gold",
                                    style={"display": "inline-block"},
                                )
                            ],
                            xs=12,
                            sm=12,
                            md=12,
                            lg=4,
                        ),
                        dbc.Col(
                            className="mr-1",
                            children=[
                                dcc.Graph(
                                    id="goat-silver",
                                    style={"display": "inline-block"},
                                )
                            ],
                            xs=12,
                            sm=12,
                            md=12,
                            lg=4,
                        ),
                        dbc.Col(
                            children=[
                                dcc.Graph(
                                    id="goat-bronze",
                                    style={"display": "inline-block"},
                                )
                            ],
                            xs=12,
                            sm=12,
                            md=12,
                            lg=4,
                        ),
                    ],
                ),
                dbc.Row(
                    className="mt-4 w-full",
                    children=[
                        dcc.Graph(
                            id="sweden-france",
                        ),
                    ],
                ),
                dbc.Row(
                    className="mt-4",
                    children=[
                        dbc.Col(
                            className="mx-2",
                            children=[
                                dcc.Graph(
                                    id="country-info",
                                )
                            ],
                            xs=12,
                            sm=12,
                            md=12,
                            lg=9,
                        ),
                        dbc.Col(
                            className="mx-2",
                            children=[
                                dcc.Dropdown(
                                    id="country-picker-dropdown",
                                    options=self._countries_options,
                                    value="SWE",
                                    clearable=True,
                                )
                            ],
                            xs=12,
                            sm=12,
                            md=12,
                            lg=2,
                        ),
                    ],
                ),
              dbc.Row(
                    className="mt-4",
                    children=[
                        dbc.Col(
                            className="mr-1",
                            children=[
                                dcc.Graph(
                                    id="line_gender_from_start",
                                )
                            ],
                            xs=12,
                            sm=12,
                            md=12,
                            lg=6,
                        ),
                        dbc.Col(
                            className="",
                            children=[
                                dcc.Graph(
                                    id="scatter_gender_from_start",
                                    
                                )
                            ],
                            xs=12,
                            sm=12,
                            md=12,
                            lg=6,
                        ),
                    ],
                ),
                # storing intermediate value on clients browser in order to share between several callbacks
                dcc.Store(id="filtered-df"),
            ],
            fluid=True,
        )
