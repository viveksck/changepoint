#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import logging
import sys
from os import path
from time import time
from glob import glob
from functools import partial
import numpy as np
import cPickle as pickle

from joblib import Parallel, delayed
import more_itertools

__author__ = "Vivek Kulkarni"
__email__ = "viveksck@gmail.com"

LOGFORMAT = "%(asctime).19s %(levelname)s %(filename)s: %(lineno)s %(message)s"


def parallelize_func(iterable, func, chunksz=1, n_jobs=16, *args, **kwargs):
    """ Parallelize a function over each element of an iterable. """
    chunker = func
    chunks = more_itertools.chunked(iterable, chunksz)
    chunks_results = Parallel(n_jobs=n_jobs, verbose=50)(
        delayed(chunker)(chunk, *args, **kwargs) for chunk in chunks)
    results = more_itertools.flatten(chunks_results)
    return list(results)

# Code taken from: http://nbviewer.ipython.org/github/pv/SciPy-CookBook/blob/master/ipython/SignalSmooth.ipynb
def smooth(x, window_len=11, window='hanning'):
    """ Smoothen a time series. """
    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."
    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."
    if window_len < 3:
        return x
    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"

    s = np.r_[2 * x[0] - x[window_len - 1::-1],
              x, 2 * x[-1] - x[-1:-window_len:-1]]
    if window == 'flat':  # moving average
        w = np.ones(window_len, 'd')
    else:
        w = eval('np.' + window + '(window_len)')
    y = np.convolve(w / w.sum(), s, mode='same')
    return y[window_len:-window_len + 1]


def ts_stats_significance(ts, ts_stat_func, null_ts_func, B=1000, permute_fast=False):
    """ Compute  the statistical significance of a test statistic at each point
        of the time series.
    """
    stats_ts = ts_stat_func(ts)
    if permute_fast:
        # Permute it in 1 shot
        null_ts = map(np.random.permutation, np.array([ts, ] * B))
    else:
        null_ts = np.vstack([null_ts_func(ts) for i in np.arange(0, B)])
    stats_null_ts = np.vstack([ts_stat_func(nts) for nts in null_ts])
    pvals = []
    nums = []
    for i in np.arange(0, len(stats_ts)):
        num_samples = np.sum((stats_null_ts[:, i] >= stats_ts[i]))
        nums.append(num_samples)
        pval = num_samples / float(B)
        pvals.append(pval)

    return stats_ts, pvals, nums

# Code below taken from http://nbviewer.ipython.org/github/welch/stats-notebooks/blob/master/SubsamplingBootstrap.ipynb
def bootstrap_ts(y, func, B=1000, b=3):
    """ Bootstrap a timeseries using a window size:b. """
    beta_star = np.empty(B)
    z = y
    z_star = np.empty(len(z))
    for boot_i in range(B):
        for block_i, start in enumerate(np.random.randint(len(z) - b + 1, size=len(z) / b)):
            z_star[block_i * b:(block_i + 1) * b] = z[start:start + b]
            beta_star[boot_i] = func(z_star)
    return beta_star


def get_ci(theta_star, blockratio=1.0):
    """ Get the confidence interval. """
    # get rid of nans while we sort
    b_star = np.sort(theta_star[~np.isnan(theta_star)])
    se = np.std(b_star) * np.sqrt(blockratio)
    # bootstrap 95% CI based on empirical percentiles
    ci = [b_star[int(len(b_star) * .025)], b_star[int(len(b_star) * .975)]]
    return ci


def get_pvalue(value, ci):
    """ Get the p-value from the confidence interval."""
    from scipy.stats import norm
    se = (ci[1] - ci[0]) / (2.0 * 1.96)
    z = value / se
    pvalue = -2 * norm.cdf(-np.abs(z))
    return pvalue


def ts_stats_significance_bootstrap(ts, stats_ts, stats_func, B=1000, b=3):
    """ Compute  the statistical significance of a test statistic at each point
        of the time series by using timeseries boootstrap.
    """
    pvals = []
    for tp in np.arange(0, len(stats_ts)):
        pf = partial(stats_func, t=tp)
        bs = bootstrap_ts(ts, pf, B=B, b=b)
        ci = get_ci(bs, blockratio=b / len(stats_ts))
        pval = abs(get_pvalue(stats_ts[tp], ci))
        pvals.append(pval)
    return pvals
