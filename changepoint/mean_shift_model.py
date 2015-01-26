from argparse import ArgumentParser
import logging
import numpy as np
import itertools
import more_itertools
import os

from functools import partial
from utils.ts_stats import ts_stats_significance
from utils.ts_stats import parallelize_func

__author__ = "Vivek Kulkarni"
__email__ = "viveksck@gmail.com"

LOGFORMAT = "%(asctime).19s %(levelname)s %(filename)s: %(lineno)s %(message)s"


class MeanShiftModel(object):

    def get_ts_stats_significance(self, x, ts, stat_ts_func, null_ts_func, B=1000, permute_fast=False, label_ts=''):
        """ Returns the statistics, pvalues and the actual number of bootstrap
            samples. """
        stats_ts, pvals, nums = ts_stats_significance(
            ts, stat_ts_func, null_ts_func, B=B, permute_fast=permute_fast)
        return stats_ts, pvals, nums

    def generate_null_timeseries(self, ts, mu, sigma):
        """ Generate a time series with a given mu and sigma. This serves as the
        NULL distribution. """
        l = len(ts)
        return np.random.normal(mu, sigma, l)

    def shuffle_timeseries(self, ts):
        """ Shuffle the time series. This also can serve as the NULL distribution. """
        return np.random.permutation(ts)

    def compute_balance_mean(self, ts, t):
        """ Compute the balance. The right end - the left end."""
        """ For changed words we expect an increase in the mean, and so only 1 """
        return np.mean(ts[t + 1:]) - np.mean(ts[:t + 1])

    def compute_balance_mean_ts(self, ts):
        """ Compute the balance at each time 't' of the time series."""
        balance = [self.compute_balance_mean(ts, t) for t in np.arange(0, len(ts) - 1)]
        return balance

    def compute_balance_median(self, ts, t):
        """ Compute the balance at either end."""
        return np.median(ts[t + 1:]) - np.median(ts[:t + 1])

    def compute_balance_median_ts(self, ts):
        """ Compute the balance at each time 't' of the time series."""
        balance = [self.compute_balance_median(ts, t) for t in np.arange(0, len(ts) - 1)]
        return balance

    def compute_cusum_ts(self, ts):
        """ Compute the Cumulative Sum at each point 't' of the time series. """
        mean = np.mean(ts)
        cusums = np.zeros(len(ts))
        cusum[0] = (ts[0] - mean)
        for i in np.arange(1, len(ts)):
            cusums[i] = cusums[i - 1] + (ts[i] - mean)

        assert(np.isclose(cumsum[-1], 0.0))
        return cusums

    def detect_mean_shift(self, ts, B=1000):
        """ Detect mean shift in a time series. B is number of bootstrapped
            samples to draw.
        """
        x = np.arange(0, len(ts))
        stat_ts_func = self.compute_balance_mean_ts
        null_ts_func = self.shuffle_timeseries
        stats_ts, pvals, nums = self.get_ts_stats_significance(x, ts, stat_ts_func, null_ts_func, B=B, permute_fast=True)
        return stats_ts, pvals, nums

    def test(self):
        print "Testing a time series with a significant mean shift"
        ts = np.hstack([np.random.normal(0.0, 1.0, 50), np.random.normal(5.0, 1.0, 50)])
        x = np.arange(0, len(ts))
        stat_ts_func = self.compute_balance_mean_ts
        print "Using NULL"
        null_ts_func = partial(self.generate_null_timeseries, mu=0.0, sigma=1.0)
        stats_ts, pvals, nums = self.get_ts_stats_significance(
            x, ts, stat_ts_func, null_ts_func,
            label_ts='test', B=1000)
        print "Minimum p-value is", np.min(pvals), pvals

        print "Using permutation"
        null_ts_func = self.shuffle_timeseries
        stats_ts, pvals, nums = self.get_ts_stats_significance(x, ts, stat_ts_func, null_ts_func, label_ts='test', B=1000)
        print "Minimum p-value is", np.min(pvals), pvals

        print "************************************************************************"

        print "Testing a time series with no mean shift"
        ts = np.random.normal(0.0, 0.000001, 1000)
        x = np.arange(0, len(ts))
        stat_ts_func = self.compute_balance_mean_ts
        print "Using NULL"
        null_ts_func = partial(self.generate_null_timeseries, mu=0.0, sigma=1.0)
        stats_ts, pvals, nums = self.get_ts_stats_significance(x, ts, stat_ts_func, null_ts_func, label_ts='test', B=1000)
        print "Minimum p-value is", np.min(pvals), pvals

        print "Using permutation"
        null_ts_func = self.shuffle_timeseries
        stats_ts, pvals, nums = self.get_ts_stats_significance(x, ts, stat_ts_func, null_ts_func, label_ts='test', B=1000)
        print "Minimum p-value is", np.min(pvals), pvals
