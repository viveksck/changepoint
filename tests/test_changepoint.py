#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_changepoint
----------------------------------

Tests for `changepoint` module.
"""

import unittest

import numpy as np

from changepoint import MeanShiftModel


class TestChangepoint(unittest.TestCase):
    def test(self):
        data = np.hstack([np.random.normal(0.0, 1.0, 50), np.random.normal(5.0, 1.0, 50)])
        cd = MeanShiftModel()
        stats_ts, pvals, nums = cd.detect_mean_shift(data)
        self.assertIsNotNone(stats_ts)
        self.assertEqual(len(stats_ts), 99)
        self.assertEqual(len(pvals), 99)
        self.assertEqual(len(nums), 99)


if __name__ == '__main__':
    unittest.main()
