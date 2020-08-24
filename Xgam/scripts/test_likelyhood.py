#%%
from Xgam.utils import foregroundfit_ as ffit
import numpy as np
import healpy as hp
import os
from itertools import product
import matplotlib.pyplot as plt
from scipy.special import factorial

def poisson_likelihood(norm_guess, const_guess, fore_map, data_map, exp=None, sr=None):
    """
    Compute the log-likelihood as decribed here:
    http://iopscience.iop.org/article/10.1088/0004-637X/750/1/3/pdf
    where the model to fit to data is given by norm*fore_map+const.

    Parameters
    ----------
    norm_guess : float
          initial guess for normalization parameter
    const_guess : float
          initial guess for constant parameter
    fore_map : numpy array
          helapix map of foreground model
    data_map : numpy array
          helapix map of data. It could be either a count map or a flux map.
          If a counts map is given, an exposure map should be given too. See
          next parameter.
    exp :  numpy array or None
          helapix map of the exposure. Should be given if the data map is in
          counts (beacause foreground map is in flux units by default and it
          needs to be turned to counts to be fitted). While, If data map is
          in flux units, do not declare this parameter, which is None by
          default.
    sr : float or None
          pixel area -> 4*pi/Npix
          
    Returns
    -------
    float
        likelihood value.
        
    """
    a = norm_guess
    b = const_guess
    
    

    # lambda_arr = data_map
    # k_arr = (a*fore_map+b)*exp*sr
    # lambda_arr = (a*fore_map+b)*exp*sr # valore previsto 
    # k_arr = data_map # valore osservato
    # k_factorial = factorial(k_arr)
    # log_k_factorial = np.log(k_factorial)
    # factorial_data = factorial(data_map)
    # factorial_data = data_map

    lh = 0
    if exp is not None:
        lambda_arr = (a*fore_map+b)*exp*sr # valore previsto 
        k_arr = data_map # valore osservato
        k_factorial = factorial(k_arr)
        log_k_factorial = np.log(k_factorial)

        lh = np.sum(log_k_factorial - k_arr*np.log(lambda_arr) + lambda_arr)

        
    else:
        lambda_arr = (a*fore_map+b) # valore previsto 
        k_arr = data_map # valore osservato
        k_factorial = factorial(k_arr)
        log_k_factorial = np.log(k_factorial)

        lh = np.sum(log_k_factorial - k_arr*np.log(lambda_arr) + lambda_arr)

    return lh
#%%
x = np.arange(1, 10)
data_map = 3.41*x + 1.12 
fore_map = x
# %%
def arg(x):
    return poisson_likelihood(x[0],x[1], fore_map, data_map)
# %%
from scipy.optimize import minimize
#%%
res=minimize(arg, x0=(1.0, 0.1), bounds=((0.1, 5.0),(0.1, 3)), tol=1e-8)
#%%
res.x
# %%
