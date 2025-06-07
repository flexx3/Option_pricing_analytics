#import dependencies
import dash
from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Container import Container

#instantiate app
app = Dash(
    __name__,
    use_pages = True,
    assets_folder = 'assets',
    external_stylesheets = [dbc.themes.BOOTSTRAP],
    title = 'Built by Flexxie', 
    meta_tags = [{'name': 'viewport',
                      'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.5, minimum-scale=0.5'}]
)

#instantiate server
server = app.server

#instantiate logo source
brand_logo = './assets/logo.png',
pointing_logo = './assets/pngegg.png',
linkedin_logo = './assets/linkedin-logo.png',
github_logo = './assets/github-white.png'

#left sidebar inline styling
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "76px",
    "left": 0,
    "bottom": 0,
    "overflow": "auto"    
}

#left-Navigationbar
Navigation_bar= dbc.Navbar([
    dbc.Nav([
        dbc.NavLink([
        html.Div(page["name"], className="ms-2"),
        ], href=page["path"],
           active="exact",
        )
        for page in dash.page_registry.values()
    ],
     vertical=True,
    pills=True,                      
    ),
], color='dark', dark=True, style=SIDEBAR_STYLE)

#app layout
app.layout = dbc.Container([
    # row1 for top bar design
    dbc.Row([
        dbc.Navbar([
          dbc.Col(html.Img(src = brand_logo, height = '85px')),
          dbc.Col(dbc.NavbarBrand('OptionPricer', className = 'ms-2')),
          dbc.Col(html.H4('Wanna Reach Out?', style={'color':'#BF9B30'})),
          dbc.Col(html.Img(src = pointing_logo, height = '50px')),
          dbc.Col(dbc.NavLink(html.Img(src= github_logo, style = {'height':'60px'}), href='https://github.com/flexx3')),
          dbc.Col(dbc.NavLink(html.Img(src = linkedin_logo, style = {'height':'60px'}), href = 'https://www.linkedin.com/in/felix-obioma-nkwuzor-828a20215/'))
        ], color = '#011222', dark = True, fixed = 'top'),
    ],align = 'center', className = 'g-0'),
    #row2 for the body
   dbc.Row([
        dbc.Col([Navigation_bar], width=2),
        dbc.Col([dash.page_container
                ], width=10)
    ]), 
   
], fluid = True)

#run app
if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port=8050, use_reloader=False)
