# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 22:56:58 2017

@author: jaehyuk
"""
import numpy as np
import scipy.stats as ss
import pyfeng as pf

def basket_check_args(spot, vol, corr_m, weights):
    '''
    This function simply checks that the size of the vector (matrix) are consistent
    '''
    n = spot.size
    assert( n == vol.size )
    assert( corr_m.shape == (n, n) )
    return None
    
def basket_price_mc_cv(
    strike, spot, vol, weights, texp, cor_m, 
    intr=0.0, divr=0.0, cp=1, n_samples=10000
):
    # price1 = MC based on BSM
    rand_st = np.random.get_state() # Store random state first
    price1 = basket_price_mc(
        strike, spot, vol, weights, texp, cor_m,
        intr, divr, cp, True, n_samples)
    
    ''' 
    compute price2: mc price based on normal model
    make sure you use the same seed

    # Restore the state in order to generate the same state
    np.random.set_state(rand_st)  
    price2 = basket_price_mc(
        strike, spot, spot*vol, weights, texp, cor_m,
        intr, divr, cp, False, n_samples)
    '''
    np.random.set_state(rand_st)
    price2 = basket_price_mc(
        strike, spot, spot*vol, weights, texp, cor_m,
        intr, divr, cp, False, n_samples)

    ''' 
    compute price3: analytic price based on normal model
    
    price3 = basket_price_norm_analytic(
        strike, spot, vol, weights, texp, cor_m, intr, divr, cp)
    '''
    price3 = basket_price_norm_analytic(
        strike, spot, vol*spot, weights, texp, cor_m, intr, divr, cp)
    
    # return two prices: without and with CV
    return np.array([price1, price1 - (price2 - price3)])


def basket_price_mc(
    strike, spot, vol, weights, texp, cor_m,
<<<<<<< HEAD
    intr=0.0, divr=0.0, cp=1, bsm=True, n_samples = 10000
=======
    intr=0.0, divr=0.0, cp=1, bsm=True, n_samples = 100000
>>>>>>> b8d5994cb5be7256617c0b900760028b4ffc6e69
):
    basket_check_args(spot, vol, cor_m, weights)
    
    div_fac = np.exp(-texp*divr)
    disc_fac = np.exp(-texp*intr)
    forward = spot / disc_fac * div_fac

    cov_m = vol * cor_m * vol[:,None]
    chol_m = np.linalg.cholesky(cov_m)  # L matrix in slides

    n_assets = spot.size
    znorm_m = np.random.normal(size=(n_assets, n_samples))
    
    if( bsm ) :
        '''
        PUT the simulation of the geometric brownian motion below
        '''
<<<<<<< HEAD
        #prices = forward[:,None]*np.exp(-1/2*vol[:,None]**2*texp + vol[:,None] * (np.sqrt(texp)*chol_m @ znorm_m))
        prices = forward[:,None]*np.exp(-1/2*vol[:,None]**2*texp +  (np.sqrt(texp)*chol_m @ znorm_m))
=======
        prices = np.zeros_like(znorm_m)
>>>>>>> b8d5994cb5be7256617c0b900760028b4ffc6e69
    else:
        # bsm = False: normal model
        prices = forward[:,None] + np.sqrt(texp) * chol_m @ znorm_m
    
    price_weighted = weights @ prices
    
    price = np.mean( np.fmax(cp*(price_weighted - strike), 0) )
    return disc_fac * price


def basket_price_norm_analytic(
    strike, spot, vol, weights, 
    texp, cor_m, intr=0.0, divr=0.0, cp=1
):
    
    '''
    The analytic (exact) option price under the normal model
    
    1. compute the forward of the basket
    2. compute the normal volatility of basket
    3. plug in the forward and volatility to the normal price formula
<<<<<<< HEAD
    normal_formula(strike, spot, vol, texp, intr=0.0, divr=0.0, cp=1)
    it is already imorted
=======
    
    norm = pf.Norm(sigma, intr=intr, divr=divr)
    norm.price(strike, spot, texp, cp=cp)
>>>>>>> b8d5994cb5be7256617c0b900760028b4ffc6e69
    
    PUT YOUR CODE BELOW
    '''
    basket_check_args(spot, vol, cor_m, weights)
    
<<<<<<< HEAD
    div_fac = np.exp(-texp*divr)
    disc_fac = np.exp(-texp*intr)
    forward = spot / disc_fac * div_fac
    forward_basket = forward @ weights
    cov_m = vol * cor_m * vol[:,None]
    sigma = np.sqrt(weights @ cov_m @ weights.T)

    prices=normal_formula(strike, forward_basket, sigma, texp=texp, intr=intr, divr=divr, cp=1)
    
    return prices

def spread_price_kirk(strike, spot, vol, texp, corr, intr=0, divr=0, cp=1):
    div_fac = np.exp(-texp*divr)
    disc_fac = np.exp(-texp*intr)
    forward = spot / disc_fac * div_fac
    vol2 = vol[1]*forward[1]/(forward[1]+strike)
    vol_r = np.sqrt(vol[0]**2 + vol2*(vol2 - 2*corr*vol[0]))
    price = disc_fac * bsm_formula(forward[1]+strike, forward[0], vol_r, texp, cp=cp)

    return price
=======
    
    
    return 0.0
>>>>>>> b8d5994cb5be7256617c0b900760028b4ffc6e69
