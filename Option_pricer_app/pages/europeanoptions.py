#import dependencies
import dash
from dash import Dash, html, dcc, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Container import Container
from pricing_model import options_pricing
from options_greeks import greeks

#instantiate app
dash.register_page(__name__, name='European Options')

#styling for the right-sidebar navigation
right_sidebar= {
    "position": "fixed",
    "top": 0,
    "right": 0,
    "bottom": 0,
    "width":"16%",
    "overflow": "auto"    
}

#app layout
layout = html.Div([
    dbc.Container([
        dbc.Col([
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.Label('Expiry Time(Per Month)'),
                    dcc.Input(id='T_expiry', type='number',
                              inputMode='numeric', step=1, value=2, min=1, max=12, style={'border-radius':'50px', 'width':'100px', 'text-align':'center'})
                ], style={'align':'center', 'font-weight':'bold'})
            ),
            dbc.Col(
               html.Div([
                    html.Label('No of Simulations'),
                    dcc.Input(id='N_sims', type='number',
                              inputMode='numeric', step=50, value=50, style={'border-radius':'50px', 'width':'100px','text-align':'center'})
                ], style={'align':'center', 'font-weight':'bold'}) 
            ),
            dbc.Col(
               html.Div([
                    html.Label('Time steps'),
                    dcc.Input(id='T-steps', type='number',
                              inputMode='numeric', step=50, value=50, style={'border-radius':'50px', 'width':'100px','text-align':'center'})
                ], style={'align':'center', 'font-weight':'bold'}) 
            ),
            dbc.Col(dbc.Button('Submit',id='submit-button',n_clicks=0, style={'background-color':'black'}))   
        ]),
        dbc.Row([
            dcc.Graph(id='simulation-graph', figure={})
        ]),
        dbc.Row([
            html.Div([
                html.Label('Select Pricing Method'),
                dcc.RadioItems(id = 'pricing-method',
                        options = [
                            {'label':'Black-Scholes-Merton', 'value':'BSM'},
                            {'label':'Binomial Trees', 'value':'Binomial_Trees'}
                        ], value='BSM', inline = True, style={'align':'center'})
            ], style={'align':'center', 'font-weight':'bold', 'marginTop':'50px'})
        ]),
        dbc.Row([html.Pre(id='option-output')]),
       dbc.Row([
           html.Div([html.Label('Greeks Table'),dash_table.DataTable(data=[], id='greeks-table')],
                        style={'font-weight':'bold', 'text-align':'center', 'width':'150px'})
       ]),          
    ], width = 10),
       dbc.Col([
           dbc.Navbar(
               dbc.Nav([
                   dbc.NavItem(html.Div(
                    dcc.RadioItems(
                        id = 'option-type',
                        options = [
                            {'label':'Call Option', 'value':'call'},
                            {'label':'Put Option', 'value':'put'}
                        ], value='call', inline=False,
                    ), style={'fontWeight':'bold', 'color':'white'})
                ),
                dbc.NavItem(
                    html.Div([
                        html.Label('%ImpliedVolatility(sigma)', style={'color':'#FF00FF'}),
                        dcc.Input(id='implied-volatility', type='number',
                                  inputMode='numeric', step=5, value=30, style={'border-radius':'50px', 'width':'150px','text-align':'center'})
                    ], style={'text-align':'center', 'font-weight':'bold'})
                ),
                dbc.NavItem(
                    html.Div([
                        html.Label('%Mean(mu)', style={'color':'#FF00FF'}),
                        dcc.Input(id='mean-mu', type='number', inputMode='numeric',
                                  step=5, value=10, style={'border-radius':'50px', 'width':'150px','text-align':'center'})
                    ], style={'text-align':'center', 'font-weight':'bold'})
                ),
                dbc.NavItem(
                    html.Div([
                        html.Label('%InterestFreeRate(r)', style={'color':'#FF00FF'}),
                        dcc.Input(id='interest-r', type='number', inputMode='numeric',
                                  step=1, value=2, style={'border-radius':'50px', 'width':'150px','text-align':'center'})
                    ], style={'text-align':'center', 'font-weight':'bold'})
                ),
                dbc.NavItem(
                    html.Div([
                        html.Label('Asset Price($)', style={'color':'#FF00FF'}),
                        dcc.Input(id='asset-price', type='number', inputMode='numeric',
                                 value=100, style={'border-radius':'50px', 'width':'150px','text-align':'center'})
                    ], style={'text-align':'center', 'font-weight':'bold'})
                ),
                dbc.NavItem(
                    html.Div([
                        html.Label('Strike Price(K$)', style={'color':'#FF00FF'}),
                        dcc.Input(id='strike-price', type='number', inputMode='numeric',
                                  value=105, style={'border-radius':'50px', 'width':'150px','text-align':'center'})
                    ], style={'text-align':'center', 'font-weight':'bold'})
                )
           ], vertical=True, navbar=True), color='#0D1717', style=right_sidebar)
       ], width=2)
    ], fluid=True)
], style={"margin-top":"110px"})

#add functionality to output graph using callbacks
@callback(
    Output(component_id='simulation-graph', component_property='figure'),
    Input(component_id='implied-volatility', component_property='value'),
    Input(component_id='mean-mu', component_property='value'),
    Input(component_id='interest-r', component_property='value'),
    Input(component_id='asset-price', component_property='value'),
    Input(component_id='strike-price', component_property='value'),
    State(component_id='T_expiry', component_property='value'),
    State(component_id='N_sims', component_property='value'),
    State(component_id='T-steps', component_property='value'),
    Input(component_id='submit-button', component_property='n_clicks')
)
def montecarlo_viz2(volatility, mean, interest, asset_price, strike_price, expiry, N_sims, T_steps, n_clicks):
    #calculate percentage values for volatility, interest and mean
    volatility_n = volatility/100
    interest_n = interest/100
    mean_n = mean/100
    pricer= options_pricing(sigma=volatility_n, r=interest_n, S_0=asset_price, N_sim=N_sims, N=T_steps)
    #show viz
    expiry_time = None
    if expiry >= 2:
        expiry_time = 2
    else:
        expiry_time = 1
    viz = pricer.Show_viz(T_expiry=expiry_time, mu=mean_n)
    return viz
#add functionality to output option value and its corresponding greeks using callbacks
@callback(
    Output(component_id='option-output', component_property='children'),
    Output(component_id='greeks-table', component_property='data'),
    Input(component_id='option-type', component_property='value'),
    Input(component_id='implied-volatility', component_property='value'),
    Input(component_id='mean-mu', component_property='value'),
    Input(component_id='interest-r', component_property='value'),
    Input(component_id='asset-price', component_property='value'),
    Input(component_id='strike-price', component_property='value'),
    State(component_id='T_expiry', component_property='value'),
    State(component_id='N_sims', component_property='value'),
    State(component_id='T-steps', component_property='value'),
    Input(component_id='submit-button', component_property='n_clicks'),
    Input(component_id='pricing-method', component_property='value')
)
def show_option(option_type, volatility, mean, interest, asset_price, strike_price, expiry, N_sims, T_steps, clicks, pricing_method):
    import sys
    import io
    #calculate percentage values for volatility, interest and mean
    volatility_n = float(volatility / 100)
    interest_n = float(interest / 100)
    mean_n = float(mean / 100)
    #instantiate the options pricer and greeks
    pricer= options_pricing(sigma=volatility_n, r=interest_n, S_0=asset_price, N_sim=N_sims, N=T_steps)
    greeks_values = greeks(r=interest_n, S=asset_price, K=strike_price, T=expiry, sigma=volatility_n)
    #output option value based on selected pricing method
    if pricing_method == "BSM":
        option_value_bsm= pricer.BSM(K=strike_price, T_expiry=expiry, option_type=option_type)
        greeks_df= greeks_values.greeks_df(option_type=option_type)
        return option_value_bsm, greeks_df.to_dict('records')
    elif pricing_method == "Binomial_Trees":
        bino_tree= pricer.BinomialTree(T_expiry=expiry, K=strike_price, option_type=option_type)
        # Redirect stdout to a StringIO object
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        # Print the object (this is what normally goes to terminal)
        print(bino_tree)
        # Reset stdout
        sys.stdout = old_stdout
        option_value_bino_tree= new_stdout.getvalue()
        return option_value_bino_tree, None

