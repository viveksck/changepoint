from __future__ import absolute_import
from __future__ import print_function

import numpy as np
from builtins import object

from changepoint.utils import ts_stats_significance

__author__ = "Vivek Kulkarni"
__email__ = "viveksck@gmail.com"

LOGFORMAT = "%(asctime).19s %(levelname)s %(filename)s: %(lineno)s %(message)s"


class MeanShiftModel(object):
    @staticmethod
    def get_ts_stats_significance(ts, stat_ts_func, null_ts_func, B=1000, permute_fast=False):
        """ Returns the statistics, pvalues and the actual number of bootstrap
            samples. """
        stats_ts, pvals, nums = ts_stats_significance(ts, stat_ts_func, null_ts_func, B=B, permute_fast=permute_fast)
        return stats_ts, pvals, nums

    @staticmethod
    def generate_null_timeseries(ts, mu, sigma):
        """ Generate a time series with a given mu and sigma. This serves as the
        NULL distribution. """
        l = len(ts)
        return np.random.normal(mu, sigma, l)

    @staticmethod
    def shuffle_timeseries(ts):
        """ Shuffle the time series. This also can serve as the NULL distribution. """
        return np.random.permutation(ts)

    @staticmethod
    def compute_balance_mean(ts, t):
        """ Compute the balance. The right end - the left end."""
        """ For changed words we expect an increase in the mean, and so only 1 """
        return np.mean(ts[t + 1:]) - np.mean(ts[:t + 1])

    @staticmethod
    def compute_balance_mean_ts(ts):
        """ Compute the balance at each time 't' of the time series."""
        balance = [MeanShiftModel.compute_balance_mean(ts, t) for t in np.arange(0, len(ts) - 1)]
        return balance

    @staticmethod
    def compute_balance_median(ts, t):
        """ Compute the balance at either end."""
        return np.median(ts[t + 1:]) - np.median(ts[:t + 1])

    @staticmethod
    def compute_balance_median_ts(ts):
        """ Compute the balance at each time 't' of the time series."""
        balance = [MeanShiftModel.compute_balance_median(ts, t) for t in np.arange(0, len(ts) - 1)]
        return balance

    @staticmethod
    def compute_cusum_ts(ts):
        """ Compute the Cumulative Sum at each point 't' of the time series. """
        mean = np.mean(ts)
        cusums = np.zeros(len(ts))
        cusums[0] = (ts[0] - mean)
        for i in np.arange(1, len(ts)):
            cusums[i] = cusums[i - 1] + (ts[i] - mean)

        assert (np.isclose(cusums[-1], 0.0))
        return cusums

    def detect_mean_shift(self, ts, B=1000):
        """ Detect mean shift in a time series. B is number of bootstrapped
            samples to draw.
        """
        stat_ts_func = self.compute_balance_mean_ts
        null_ts_func = self.shuffle_timeseries
        stats_ts, pvals, nums = self.get_ts_stats_significance(ts, stat_ts_func, null_ts_func, B=B, permute_fast=True)
        return stats_ts, pvals, nums
