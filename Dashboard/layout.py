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
                dbc.Row(
                    className="mt-4",
                    children=[
                        dbc.Col(
                            html.Header(html.H2("Athlete Events")),
                            className="mt-1",
                            xs=12,
                            sm=12,
                            md=6,
                            lg=4,
                            xl={"offset": 2, "size": 2},
                        ),
                        dbc.Col(
                            dcc.Dropdown(
                                id="olympic-dropdown",
                                options=self._olympics_options_dropdown,
                                value="athlete",
                            ),
                            xs=12,
                            sm=12,
                            md=12,
                            lg=4,
                            xl={"offset": 2, "size": 2},
                        ),
                    ],
                ),
                dbc.Row(
                    className="mt-4",
                    children=[
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id="france-max-graph",
                                    style={"display": "inline-block"},
                                ),
                            ],
                            xs=12,
                            sm=12,
                            md=12,
                            lg=4,
                            xl={"offset": 2, "size": 2},
                        ),
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id="france-all-ages",
                                    style={"display": "inline-block"},
                                ),
                            ],
                            xs=12,
                            sm=12,
                            md=12,
                            lg=4,
                            xl={"offset": 2, "size": 4},
                        ),
                    ],
                ),
                dbc.Row(
                    className="mt-4",
                    children=[
                        dcc.Graph(
                            id="france-medal-distribution",
                            style={"display": "inline-block"},
                        ),
                    ],
                ),
                dbc.Row(
                    className="mt-4",
                    children=[
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id="goat-gold",
                                    style={"display": "inline-block"},
                                )
                            ],
                            xs=12,
                            sm=12,
                            md=12,
                            lg=4,
                            xl={"offset": 2, "size": 2},
                        ),
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id="goat-silver",
                                    style={"display": "inline-block"},
                                )
                            ],
                            xs=12,
                            sm=12,
                            md=12,
                            lg=4,
                            xl={"offset": 2, "size": 2},
                        ),
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id="goat-bronze",
                                    style={"display": "inline-block"},
                                )
                            ],
                            xs=12,
                            sm=12,
                            md=12,
                            lg=4,
                            xl={"offset": 2, "size": 2},
                        ),
                    ],
                ),
                dbc.Row(
                    className="mt-4",
                    children=[
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id="sweden-france",
                                    style={"display": "inline-block"},
                                )
                            ],
                            xs=12,
                            sm=12,
                            md=12,
                            lg=4,
                            xl={"offset": 2, "size": 2},
                        ),
                    ],
                ),
                dbc.Row(
                    className="mt-4",
                    children=[
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id="country-info",
                                    style={"display": "inline-block"},
                                )
                            ],
                            xs=12,
                            sm=12,
                            md=12,
                            lg=4,
                            xl={"offset": 2, "size": 2},
                        ),
                        dbc.Col(
                            [
                                dcc.Dropdown(
                                    id="country-picker-dropdown",
                                    options=self._countries_options,
                                    value="SWE",
                                    clearable=True,
                                    style={"text-align": "left"},
                                )
                            ],
                            xs=12,
                            sm=12,
                            md=12,
                            lg=4,
                            xl={"offset": 2, "size": 2},
                        ),
                    ],
                ),
                # storing intermediate value on clients browser in order to share between several callbacks
                dcc.Store(id="filtered-df"),
            ],
            fluid=False,
        )
