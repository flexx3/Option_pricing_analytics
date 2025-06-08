This is a web based program for pricing an American or European option(either Call or Put).
The geometric brownian motion of a stock price path over a particular time is simulated using numpy and scipy libraries,
visualized with matplotlib and the resulting visualization converted to a plotly graph using mpl.to_plotly from plotly.tools for use in the plotly dash web app.
You can value the American Call or Put Option using either of Least-squares-montecarlo method or Binomial trees(using bino_tree library).
The European Call or Put Option can also be valued using either of Black-Scholes-Merton Model or Binomial trees with its corresponding greeks.
The entire program is put together in a plotly dash web application with input parameters including implied volatility, interest rate, mean,
asset price, strike price, expiry time and time step. 
The web app was wrapped around a docker container, deployed on render.
This is just the beginner stages of my foray into options pricing.
 There surely will be improvements like using the heston and the chavelier models, and so much more..anticipate!!
