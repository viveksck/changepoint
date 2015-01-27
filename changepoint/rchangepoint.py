import numpy as np
import rpy2.robjects as robjects
import scipy


def estimate_cp(ts, method="mean", Q=1, penalty_value=0.175):
    """ Estimate changepoints in a time series by using R. """

    """ 
        ts: time series
        method: look for a single changepoint in 'mean' , 'var', 'mean and var'
                or use binary segmentatiom to detect multiple changepoints in
                mean (binseg).
        Q: Number of change points to look for (only for binseg)
        penalty_value: Penalty to use as threshold (only for binseg)

        Returns: returns indices of the changepoints
    """
    robjects.r("library(changepoint)")
    method_map = {
        "mean": "cpt.mean({})",
        "var": "cpt.var({})",
        "meanvar": "cpt.meanvar({})",
        "binseg.mean.CUSUM": "cpt.mean({},penalty='Manual', test.stat='CUSUM',method='BinSeg',Q={},pen.value={})"
    }
    mt = robjects.FloatVector(ts)
    robjects.globalenv["mt"] = mt
    if method == "binseg.mean.CUSUM":
        cmd = method_map[method].format("mt", Q, penalty_value)
    else:
        cmd = method_map[method].format("mt")
    robjects.globalenv["mycpt"] = robjects.r(cmd)
    ecp = robjects.r("cpts(mycpt)")
    return ecp


def estimate_cp_pval(ts, method="mean"):
    """ Estimate changepoints in a time series by using R. """

    """ 
        ts: time series
        method: look for a single changepoint in 'mean' , 'var', 'mean and var'
        Returns: returns index of the changepoint, and pvalue. Here pvalue = 1
                 means statistically significant
    """
    robjects.r("library(changepoint)")
    method_map = {
        "mean": "cpt.mean({}, class=FALSE)",
        "var": "cpt.var({}, class=FALSE)",
        "meanvar": "cpt.meanvar({}, class=FALSE)",
    }
    mt = robjects.FloatVector(ts)
    robjects.globalenv["mt"] = mt
    cmd = method_map[method].format("mt")
    robjects.globalenv["mycpt"] = robjects.r(cmd)
    ecp_pval = robjects.r("mycpt")
    ecp = ecp_pval[0]
    pval = ecp_pval[1]
    return ecp, pval
