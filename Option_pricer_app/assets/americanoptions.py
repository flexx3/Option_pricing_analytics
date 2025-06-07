#import dependencies
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from pricing_model import options_pricing
from options_greeks import greeks

#instantiate web app
app = Dash(
    __name__,
    assets_folder = 'assets',
    external_stylesheets = [dbc.themes.BOOTSTRAP],
    title = 'Built by Flexxie',
    meta_tags=[{'name': 'viewport',
                      'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.5, minimum-scale=0.5'}],
)

#instantiate server
server = app.server

#style the right navigation bar
right_sidebar= {
    "position": "fixed",
    "top": 0,
    "right": 0,
    "bottom": 0,
    "overflow": "auto"    
}

#app layout
app.layout = html.Div([
    #layout for the body
    dbc.Col([], width = 8),
    #vertical navbar
    dbc.Col([
        dbc.Navbar(
            dbc.Nav([
                dbc.NavItem(
                    dcc.RadioItems(
                        id = 'option-type',
                        options = [
                            {'label':'Call Option', 'value':'Call'},
                            {'label':'Put Option', 'value':'Put'}
                        ], value = 'Call', inline = False
                    )
                ),
                dbc.NavItem(
                    html.Div([
                        html.Label('%ImpliedVolatility', style={'color':'blue'}),
                        dcc.Input(id='implied volatility', type='number',
                                  inputMode='numeric', step=5, value=30, style={'border-radius':'50px', 'width':'150px'})
                    ], style={'text-align':'center', 'font-weight':'bold'})
                ),
            ], vertical = True, navbar = True),
        color = '#171717', style= right_sidebar)
    ], width = 2)
    
])

if __name__ == '__main__':
    app.run_server(debug=False)
