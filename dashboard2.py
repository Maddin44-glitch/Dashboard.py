from dash import Dash, html, dcc, dash_table, Input, Output, callback
import pandas as pd
import plotly.express as px

# Daten laden
nasa = pd.read_csv(
    "NASA Exoplanets Data.csv", parse_dates=False
)


numeric_cols = [
    "distance",
    "stellar_magnitude",
    "mass_multiplier",
    "radius_multiplier",
    "orbital_radius",
    "orbital_period",
    "eccentricity",
]
categorical_cols = [
    "planet_type",
    "discovery_year",
    "mass_wrt",
    "radius_wrt",
    "detection_method",
]

# Farben
BG_COLOR = "#121416"
CARD_COLOR = "#1c1f21"
ACCENT_COLOR = "#3a86ff"
TEXT_COLOR = "#f0f0f0"
BORDER_COLOR = "#2b2f33"

# App erstellen
app = Dash(__name__)
app.title = "NASA Exoplanet Dashboard"

# Inline CSS für Dropdown Dark Mode
app.index_string = f"""
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>NASA Exoplanet Dashboard</title>
        {{%favicon%}}
        {{%css%}}
        <style>
            .Select-menu-outer div,
            .Select-value-label,
            .Select--single > .Select-control .Select-value {{
                color: {TEXT_COLOR} !important;
                background-color: {CARD_COLOR} !important;
            }}
            .Select-option:hover {{
                background-color: #2a2e32 !important;
                color: #ffffff !important;
            }}
            .Select-control {{
                background-color: {CARD_COLOR} !important;
                border-color: {BORDER_COLOR} !important;
            }}
            .Select-control:hover {{
                border-color: {ACCENT_COLOR} !important;
            }}
        </style>
    </head>
    <body>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>
"""

# Einheitliche Dropdown-Styles
DROPDOWN_STYLE = {
    "width": "260px",
    "borderRadius": "8px",
    "padding": "4px",
    "fontSize": "15px",
}

# Layout
app.layout = html.Div(
    [
        html.H1(
            "NASA Exoplanet Dashboard",
            style={
                "textAlign": "center",
                "color": TEXT_COLOR,
                "marginBottom": "35px",
                "fontWeight": "600",
                "letterSpacing": "0.5px",
            },
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Label(
                            "Diagrammtyp",
                            style={"fontWeight": "600", "color": TEXT_COLOR},
                        ),
                        dcc.Dropdown(
                            id="chart-type",
                            options=[
                                {"label": "Histogramm", "value": "histogram"},
                                {"label": "Streudiagramm", "value": "scatter"},
                                {"label": "Balkendiagramm", "value": "bar"},
                                {"label": "Boxplot", "value": "box"},
                            ],
                            value="histogram",
                            clearable=False,
                            style=DROPDOWN_STYLE,
                        ),
                    ],
                    style={"display": "inline-block", "marginRight": "20px"},
                ),
                html.Div(
                    [
                        html.Label(
                            "X-Achse", style={"fontWeight": "600", "color": TEXT_COLOR}
                        ),
                        dcc.Dropdown(
                            id="x-axis",
                            clearable=False,
                            value="distance",
                            style=DROPDOWN_STYLE,
                        ),
                    ],
                    style={"display": "inline-block", "marginRight": "20px"},
                ),
                html.Div(
                    [
                        html.Label(
                            "Y-Achse", style={"fontWeight": "600", "color": TEXT_COLOR}
                        ),
                        dcc.Dropdown(
                            id="y-axis",
                            clearable=False,
                            value="stellar_magnitude",
                            style=DROPDOWN_STYLE,
                        ),
                    ],
                    style={"display": "inline-block"},
                ),
            ],
            style={"textAlign": "center", "marginBottom": "35px"},
        ),
        html.Div(
            [
                dcc.Graph(
                    id="main-graph", style={"height": "65vh", "borderRadius": "12px"}
                )
            ],
            style={
                "margin": "auto",
                "width": "90%",
                "backgroundColor": CARD_COLOR,
                "borderRadius": "15px",
                "padding": "25px",
                "boxShadow": "0 6px 18px rgba(0,0,0,0.4)",
            },
        ),
        html.Div(
            [
                html.H3(
                    "Datenvorschau",
                    style={
                        "textAlign": "center",
                        "color": TEXT_COLOR,
                        "marginTop": "45px",
                        "marginBottom": "10px",
                        "fontWeight": "600",
                    },
                ),
                dash_table.DataTable(
                    data=nasa.to_dict("records"),
                    page_size=10,
                    style_table={"overflowX": "auto"},
                    style_header={
                        "backgroundColor": BORDER_COLOR,
                        "color": TEXT_COLOR,
                        "fontWeight": "bold",
                        "border": "none",
                    },
                    style_data={
                        "backgroundColor": CARD_COLOR,
                        "color": TEXT_COLOR,
                        "borderBottom": f"1px solid {BORDER_COLOR}",
                    },
                    style_cell={
                        "textAlign": "left",
                        "padding": "10px",
                        "fontFamily": "Arial, sans-serif",
                        "fontSize": "14px",
                    },
                    css=[
                        {
                            "selector": "tr:hover",
                            "rule": f"background-color: {BORDER_COLOR} !important;",
                        }
                    ],
                ),
            ],
            style={"width": "90%", "margin": "auto", "marginBottom": "40px"},
        ),
    ],
    style={
        "backgroundColor": BG_COLOR,
        "fontFamily": "Arial, sans-serif",
        "minHeight": "100vh",
        "padding": "20px",
    },
)


# Dropdown-Optionen
@callback(
    Output("x-axis", "options"),
    Output("y-axis", "options"),
    Output("y-axis", "disabled"),
    Input("chart-type", "value"),
)
def update_axis_dropdowns(chart_type):
    if chart_type == "histogram":
        return (
            [{"label": c, "value": c} for c in numeric_cols + categorical_cols],
            [],
            True,
        )
    elif chart_type == "scatter":
        return (
            [{"label": c, "value": c} for c in numeric_cols],
            [{"label": c, "value": c} for c in numeric_cols],
            False,
        )
    elif chart_type == "bar":
        return (
            [{"label": c, "value": c} for c in categorical_cols],
            [{"label": c, "value": c} for c in numeric_cols],
            False,
        )
    elif chart_type == "box":
        return (
            [{"label": c, "value": c} for c in categorical_cols],
            [{"label": c, "value": c} for c in numeric_cols],
            False,
        )


# Diagramm
@callback(
    Output("main-graph", "figure"),
    Input("chart-type", "value"),
    Input("x-axis", "value"),
    Input("y-axis", "value"),
)
def update_graph(chart_type, x_col, y_col):
    if not x_col or (chart_type != "histogram" and not y_col):
        return {}

    if chart_type == "histogram":
        fig = px.histogram(nasa, x=x_col, color="planet_type")
    elif chart_type == "scatter":
        fig = px.scatter(nasa, x=x_col, y=y_col, color="planet_type", hover_name="name")
    elif chart_type == "bar":
        fig = px.bar(nasa, x=x_col, y=y_col, color="planet_type", barmode="group")
    elif chart_type == "box":
        fig = px.box(nasa, x=x_col, y=y_col, color="planet_type")
    else:
        fig = {}

    fig.update_layout(
        paper_bgcolor=CARD_COLOR,
        plot_bgcolor=CARD_COLOR,
        font_color=TEXT_COLOR,
        margin={"t": 40, "l": 40, "r": 40, "b": 40},
        hoverlabel=dict(bgcolor="#2a2e32"),
        title_font_size=18,
    )
    return fig


if __name__ == "__main__":
    app.run(debug=True)
