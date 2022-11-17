import os
# from load_data import StockData
from dash.dependencies import Output, Input
import plotly_express as px
# from time_filtering import filter_time
import pandas as pd
# from layout import Layout
import dash_bootstrap_components as dbc


from dash import Dash, html
from dash_bootstrap_components.themes import BOOTSTRAP

from src.components.layout import create_layout

def main() -> None:
    app = Dash(external_stylesheets=[dbc.themes.MATERIA])
    app.title = "Olympics Dashboard"
    app.layout = create_layout(app)
    app.run()


if __name__ == "__main__":
    main()