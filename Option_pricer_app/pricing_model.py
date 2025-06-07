import numpy as np
from scipy.stats import norm
import binotree as bt
import matplotlib.pyplot as plt
from plotly.tools import mpl_to_plotly

class options_pricing:
    #initialize variables
    def __init__(self, S_0, r, sigma, N, N_sim):
        self.S_0 = S_0
        self.r = r
        self.sigma = sigma
        self.N = N
        self.N_sim = N_sim
        
    #Simulate stock price paths using GBM
    def custom_gbm(self, T_expiry, mu, random_seed=42):
        np.random.seed(random_seed)
        #calculate time step
        dt= T_expiry/self.N
        #derive the black scholes constant
        dW= np.random.normal(scale=np.sqrt(dt), size=(self.N_sim, self.N))
        W= dW.T
        #solve using the derived gbm expression
        St= np.exp((mu - (0.5 * self.sigma**2))* dt + self.sigma * W)
        #put in a vstack with an array of ones
        St= np.vstack([np.ones(self.N_sim), St])
        #multiply through with s_0 and return the cumprod of elements along a specific simulation path (axis=0)
        St= self.S_0 * St.cumprod(axis=0)
        #define time interval
        time= np.linspace(0, T_expiry, self.N + 1)
        #make it to be same shape as St
        tt= np.full(shape=(self.N_sim, self.N + 1), fill_value=time).T
        self.simulations_= St 
        self.time_interval_= tt

    #visualize the simulations
    def Show_viz(self, T_expiry, mu):
        self.custom_gbm(T_expiry=T_expiry, mu=mu)
        simulations_ = self.simulations_
        time_interval_ = self.time_interval_
        plt.plot(time_interval_, simulations_)
        plt.title('Monte Carlo Simulation of Stock Price Paths For A Maximum Of 2 Years Using GBM')
        plt.xlabel('Simulation Time Steps(T)')
        plt.ylabel('Simulated Price Paths(S_0)')
        figure = mpl_to_plotly(plt.gcf())
        #increase font size
        figure.update_layout(
            title = dict(text='Monte Carlo Simulation of Stock Price Using GBM', font=dict(size=16)),
            xaxis = dict(title=dict(text='Simulation Time Steps(T Years)', font=dict(size=16))),
            yaxis = dict(title=dict(text='Simulated Price Paths($ S_0)', font=dict(size=16)))
        )
        plt.close()
        return figure

    #American Options pricing using LSM
    def LSM(self, K, T_expiry, mu, option_type, poly_degree= 5 ):
        #set expiry time to months in a year
        T_expiry= T_expiry/12
        #calculate time steps
        dt= T_expiry/self.N
        #calculate discount factor
        discount_factor= np.exp(-self.r * dt)
        #simulate stock price paths
        self.custom_gbm(T_expiry=T_expiry, mu=mu)
        simulations_ = self.simulations_
        #calculate options payoff
        if option_type == 'call':
            payoff_matrix= np.maximum((simulations_ - K), np.zeros_like(simulations_))
        elif option_type == 'put':
            payoff_matrix= np.maximum((K - simulations_), np.zeros_like(simulations_))
        #define value matrix and fill-in the last column(time T)
        value_matrix= np.zeros_like(payoff_matrix)
        value_matrix[:, -1] = payoff_matrix[:, -1]
        #iteratively calculate the continuation value and value vector in a given time
        for t in range(self.N-1, 0, -1):
            regression= np.polyfit(simulations_[:,t], value_matrix[:, t+1]*discount_factor, poly_degree)
            continuation_value= np.polyval(regression, simulations_[:,t])
            value_matrix[:,t]= np.where(
                payoff_matrix[:,t] > continuation_value,
                payoff_matrix[:,t],
                value_matrix[:, t+1]*discount_factor
            )
        option_premium= np.mean(value_matrix[:, -1] * discount_factor)
        return option_premium
        
    #European option pricing using Black-Scholes-Merton
    def BSM(self, K, T_expiry, option_type):
        #set expiry time to months in a year
        T_expiry= T_expiry/12
        #calculate d1 and d2
        d1= (np.log(self.S_0 / K) + (self.r + 0.5 * self.sigma ** 2) * T_expiry) / (self.sigma * np.sqrt(T_expiry))
        d2 = (np.log(self.S_0 / K) + (self.r - 0.5 * self.sigma ** 2) * T_expiry) / (self.sigma * np.sqrt(T_expiry))
        #estimate 'call' and 'put'
        if option_type == 'call':
            option_price = (self.S_0 * norm.cdf(d1, 0, 1) - K * np.exp(-self.r * T_expiry) * norm.cdf(d2, 0, 1))
        elif option_type == 'put':
            option_price = (K * np.exp(-self.r * T_expiry) * norm.cdf(-d2, 0, 1) - self.S_0 * norm.cdf(-d1, 0, 1))
        else:
            raise ValueError('Wrong input for type!')           
        return option_price

    #European and American option pricing using BinomialTrees
    def BinomialTree(self, T_expiry, K, option_type):
        tree_object = bt.tree(
           fname = 'NormalTree', 
            spot = self.S_0, strike = K, 
            T = T_expiry/12, dt = 1/12, dtfreq = 'm', periods=T_expiry,
            vola = self.sigma, r = self.r 
        )
        return tree_object.ecTree
        