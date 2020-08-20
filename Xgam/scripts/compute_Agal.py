#%%
from Xgam.utils import foregroundfit_ as ffit
import numpy as np
import healpy as hp
import os
from Xgam.utils.logging_ import logger, startmsg
from itertools import product
# %%

#%%

def fit_foreground_poisson(fore_map, data_map, mask_map=None, n_guess=1.,
                           c_guess=0.1,exp=None, smooth=False, show=False):
    """
    Performs the poissonian fit, recursively computing the log likelihood
    (using poisson_likelihood) for a grid of values of fit parameters around
    the guess. Returns the values of parameters which minimize the log
    likelihood, togather to the 1-sigma error

    Parameters
    ----------
    n_guess : float
          initial guess for normalization parameter
    c_guess : float
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
    smooth : bool
          not implemented yet...
    show : bool
          if true it shows some usefull plot to check if the fit is functioning
          
    Returns
    -------
    float, float, float, float, float, float
        In order: best fit N, best fit C, N's right error, N's left error, 
        C's right error, C's left error
    """
    #show=True
    #mask_map=None
    logger.info('Performing poissonian fit...')
    norm_guess = n_guess
    igrb_guess = c_guess
    nside_out = 64
    mask = 0.
    logger.info('N guess = %.2f - C guess = %.1e'%(norm_guess, igrb_guess))
    if mask_map is None:
        logger.info('fit outside default mask: 30deg gp, 2 deg srcs.')
        mask_f = os.path.join(X_OUT, 'fits/Mask_hp64_src2_gp30.fits')
        mask = hp.read_map(mask_f)
    else:
        logger.info('fit outside mask given in config file.')
        mask = mask_map
        mask = np.array(hp.ud_grade(mask, nside_out=nside_out,
                                      power=-2))
        mask[np.where(mask!=np.amax(mask))[0]] = 0
        mask[np.where(mask==np.amax(mask))[0]] = 1
    logger.info('down grade...')
    fore_repix = np.array(hp.ud_grade(fore_map, nside_out=nside_out))
    data_repix = np.array(hp.ud_grade(data_map, nside_out=nside_out, power=-2))
    _unmask = np.where(mask > 1e-30)[0]

    norm_list = np.linspace(norm_guess-0.2, norm_guess+0.2, 1000)
    igrb_list = np.logspace(np.log10(igrb_guess*0.01), np.log10(igrb_guess*10), 1000)
    
    logger.info('-------------------------------')
    logger.info('Minimization likelihood run1...')
    lh_list = []
    combinations = list(product(norm_list, igrb_list))
    if exp is not None:
        exposure = exp
        exposure = np.array(hp.ud_grade(exposure, nside_out=nside_out))
        areapix = 4*np.pi/(len(data_repix))
        for i,j in product(norm_list, igrb_list):
            lh = ffit.poisson_likelihood(i, j, fore_repix[_unmask],
                                    data_repix[_unmask],
                                    exp=exposure[_unmask],
                                    sr=areapix)
            lh_list.append(np.minimum(lh, 1e30))
    else:
        for i,j in product(norm_list, igrb_list):
            lh = ffit.poisson_likelihood(i, j, fore_repix[_unmask], data_repix[_unmask])
            lh_list.append(lh)
    
    lh_list = np.array(lh_list)
    lh_matrix = lh_list.reshape(len(norm_list), len(igrb_list))
    prof_lh_norm, prof_lh_igrb = ffit.get_2params_profile_likelihood(lh_matrix, norm_list, igrb_list)
    
    nn = np.linspace(np.amin(norm_list), np.amax(norm_list), 1000)
    cc = np.linspace(np.amin(igrb_list), np.amax(igrb_list), 1000)
    
    lh_min = np.amin(prof_lh_norm(nn))
    logger.info('Minimum -LogL = %s'%lh_min)
    
    norm_min = nn[np.argmin(prof_lh_norm(nn))]
    igrb_min = cc[np.argmin(prof_lh_igrb(cc))]
    logger.info('Run1 results: n=%.3f c=%e'%(norm_min, igrb_min))
    
    
    norm_sxerr, norm_dxerr = ffit.get_param_error(prof_lh_norm, nn, lh_delta=2.3)
    logger.info('Norm err: %.4f - %.4f'%(norm_sxerr, norm_dxerr))
    igrb_sxerr, igrb_dxerr = ffit.get_param_error(prof_lh_igrb, cc, lh_delta=2.3)
    logger.info('Igrb err: %.2e - %.2e'%(igrb_sxerr, igrb_dxerr))
    

    """
    logger.info('-------------------------------')
    logger.info('Minimization likelihood run2...')
    norm_list = np.linspace(norm_min-0.3, norm_min+0.3, 100)
    igrb_list = np.linspace(igrb_min*0.1, igrb_min*10, 200)
    lh_list = []
    combinations = np.array(list(product(norm_list, igrb_list)))
    if exp is not None:
        exposure = exp
        exposure = np.array(hp.ud_grade(exposure, nside_out=nside_out))
        areapix = 4*np.pi/(len(data_repix))
        for i,j in product(norm_list, igrb_list):
            lh = poisson_likelihood(i, j, fore_repix[_unmask],
                                    data_repix[_unmask],
                                    exp=exposure[_unmask],
                                    sr=areapix)
            lh_list.append(lh)
    else:
        for i,j in product(norm_list, igrb_list):
            lh = poisson_likelihood(i, j, fore_repix[_unmask],
                                    data_repix[_unmask])
            lh_list.append(lh)
            
    lh_list = np.array(lh_list)
    lh_matrix = lh_list.reshape(len(norm_list), len(igrb_list))
    prof_lh_norm, prof_lh_igrb = get_2params_profile_likelihood(lh_matrix, norm_list, igrb_list)
    
    nn = np.linspace(np.amin(norm_list), np.amax(norm_list), 500)
    cc = np.linspace(np.amin(igrb_list), np.amax(igrb_list), 1000)
    
    lh_min = np.amin(prof_lh_norm(nn))
    lh_delta = lh_min+2.3
    logger.info('Minimum -LogL = %s'%lh_min)
    
    norm_min = nn[np.argmin(prof_lh_norm(nn))]
    igrb_min = cc[np.argmin(prof_lh_igrb(cc))]
    logger.info('Run2 results: n=%.3f c=%e'%(norm_min, igrb_min))
    
    norm_sxerr, norm_dxerr = get_param_error(prof_lh_norm, nn, lh_delta)
    logger.info('Norm err: %.4f - %.4f'%(norm_sxerr, norm_dxerr))
    igrb_sxerr, igrb_dxerr = get_param_error(prof_lh_igrb, cc, lh_delta)
    logger.info('Norm err: %.4f - %.4f'%(igrb_sxerr, igrb_dxerr))
    """
    if show == True:
        
        plt.figure(facecolor='white')
        plt.plot(nn, prof_lh_norm(nn), '-', color='black')
        plt.plot([norm_min, norm_min], [lh_min-10, lh_min+40], color='red')
        plt.plot([norm_sxerr, norm_sxerr], [lh_min-2, lh_min+40], 'r--', alpha=0.7)
        plt.plot([norm_dxerr, norm_dxerr], [lh_min-2, lh_min+40], 'r--', alpha=0.7)
        plt.xlabel('Normalization')
        plt.ylabel('-Log(Likelihood)')
        plt.ylim(lh_min-5, lh_min+30)
        plt.xlim(norm_min-0.2, norm_min+0.2)
        
        plt.figure(facecolor='white')
        plt.plot(cc, prof_lh_igrb(cc), '-', color='black')
        plt.plot([igrb_min, igrb_min], [lh_min-10, lh_min+40], color='red')
        plt.plot([igrb_sxerr, igrb_sxerr], [lh_min-2, lh_min+40], 'r--', alpha=0.7)
        plt.plot([igrb_dxerr, igrb_dxerr], [lh_min-2, lh_min+40], 'r--', alpha=0.7)
        plt.xlabel('Constant')
        plt.ylabel('-Log(Likelihood)')
        plt.ylim(lh_min-5, lh_min+30)
        plt.xlim(igrb_min*0.9, igrb_min*1.1)
        plt.xscale('log')
        
        """
        fig = plt.figure(facecolor='white')
        ax = fig.add_subplot(111)
        
        x, y = np.mgrid(norm_list, igrb_list)
        X, Y = np.mgrid(nn, cc)
        print('---------------', lh_matrix.shape, X.shape, Y.shape)
        print('---------------', lh_matrix.shape, x.shape, y.shape)
        Z = griddata((x, y), lh_matrix, (X, Y), method='linear')


        contours = plt.contour(X, Y, Z, 20, colors='0.4')
        cax = ax.matshow(Z, origin='lower', cmap='RdGy',
                         extent=[np.amin(norm_list), np.amax(norm_list), 
                                np.amin(igrb_list), np.amax(igrb_list)], 
                         aspect='auto', alpha=0.5)
        plt.clabel(contours, inline=True, fontsize=8)
        plt.ylabel('C [cm$^{-2}$s$^{-1}$sr$^{-1}$]')
        plt.xlabel('N')
        ax.xaxis.set_ticks_position('bottom')
        plt.grid('off')
        cb = plt.colorbar(cax, format='$%.1e$')
        cb.set_label('-Log(Likelihood)', rotation=90)
        """
        plt.show()
        
    return norm_min, igrb_min, norm_sxerr, norm_dxerr, igrb_sxerr, igrb_dxerr


# %%

# %%
galactic_foreground = np.load("/archive/home/Xgam/fermi_data/foreground_fitting/galactic_foreground_1-10GeV.npz")["galactic_foreground"]

exposure_file_path = "/archive/home/Xgam/fermi_data/foreground_fitting/w9w322_SV_t1_nside64_expcube.fits"
exposure_map = hp.read_map(exposure_file_path, dtype=np.float64)

fermi_map = hp.read_map("/archive/home/Xgam/fermi_data/foreground_fitting/w9w322_SV_t1_nside64_outofbin.fits", dtype=np.float64)

deg=30
mask_idx = hp.query_strip(64, (90 - deg) * np.pi / 180, (90 + deg) * np.pi / 180)
mask_map = np.ones(hp.nside2npix(64), dtype=np.int64)
mask_map[mask_idx]=0

mask_f = '/archive/home/Xgam/fermi_data/fits/Mask_hp64_src2_gp30.fits'
mask_map2 = np.ones(hp.nside2npix(64), dtype=np.int64)
mask_map2[hp.read_map(mask_f, dtype=np.int32)]=0


#%%
# ffit.poisson_likelihood(1.8, 1e-7, galactic_foreground[mask_map2], fermi_map[mask_map2], exp=exposure_map[mask_map2], sr=4*np.pi/hp.nside2npix(64))
#%%
fit_foreground_poisson(galactic_foreground, fermi_map, mask_map=mask_map2, n_guess=1.,
                           c_guess=1e-7,exp=exposure_map, smooth=False, show=False)
# %%

# #%%
# mask.shape
# #%%
# import matplotlib.pyplot as plt
# #%%
# hp.mollview(galactic_foreground, norm="log")
# plt.show()

# hp.mollview(exposure_map, norm="log")
# plt.show()

# hp.mollview(fermi_map, norm="log")
# plt.show()
# #%%
# hp.mollview(mask)