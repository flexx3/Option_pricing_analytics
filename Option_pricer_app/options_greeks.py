import numpy as np
from scipy.stats import norm
import pandas as pd

class greeks:
    #initialize variables
    def __init__(self, S, r, K, T, sigma):
        self.S = S
        self.r = r
        self.K = K
        self.T = T/12
        self.sigma = sigma

    #func to calculate rho
    def get_rho(self, option_type):
        #get d1 and d2
        d1= (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = (np.log(self.S / self.K) + (self.r - 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        if option_type == "call":
            rho = (self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(d2, 0, 1))
        elif option_type == "put":
            rho = (-self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(-d2, 0, 1))
        return round(rho * 0.01, 3)
        
    #func to calculate delta
    def get_delta(self, option_type):
        #get d1
        d1= (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        if option_type == "call":
            delta = norm.cdf(d1, 0, 1)
        elif option_type == "put":
            delta = -norm.cdf(-d1, 0, 1)
        return round(delta, 3)
        
    #func to calculate gamma
    def get_gamma(self):
        #get d1
        d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        gamma = (norm.pdf(d1, 0, 1))/(self.S * self.sigma * np.sqrt(self.T))
        return round(gamma, 3)

    #func to calculate theta
    def get_theta(self, option_type):
        #get d1 and d2
        d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = (np.log(self.S / self.K) + (self.r - 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        if option_type == "call":
            theta = ((-self.S * norm.pdf(d1, 0, 1) * self.sigma)/ (2 * np.sqrt(self.T))) - (self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(d2, 0, 1))
        elif option_type == "put":
            theta = ((-self.S * norm.pdf(d1, 0, 1) * self.sigma)/ (2 * np.sqrt(self.T))) + (self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-d2, 0, 1))
        return round(theta/12, 3)

    #func to calculate vega
    def get_vega(self):
        #get d1
        d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        vega = self.S * norm.pdf(d1, 0, 1) * np.sqrt(self.T)
        return round(vega * 0.01, 3)

    #output the greeks in a pandas dataframe
    def greeks_df(self, option_type):
        #get greek values
        rho = self.get_rho(option_type)
        delta = self.get_delta(option_type)
        gamma = self.get_gamma()
        theta = self.get_theta(option_type)
        vega = self.get_vega()
        #instantiate dictionary to store the greeks
        greeks_dict = {}
        #greek names
        greeks_dict['greeks'] = ['rho', 'delta', 'gamma', 'theta', 'vega']
        #append greek values
        greeks_dict['values'] = [rho, delta, gamma, theta, vega]
        #convert to pandas dataframe
        greeks_frame = pd.DataFrame().from_dict(greeks_dict)
        return greeks_frame
        
        
        
        




        