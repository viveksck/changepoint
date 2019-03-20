# changepoint

[![Pypi Status](http://badge.fury.io/py/changepoint.png)](http://badge.fury.io/py/changepoint)
[![Build Status](https://travis-ci.org/viveksck/changepoint.png?branch=master)](https://travis-ci.org/viveksck/changepoint)


Change point detection in Time series

* Free software: BSD license
* Documentation: https://changepoint.readthedocs.org.

## Features

* This package implements a mean shift model for change point detection in time series
* This package also provides a python binding to some of the R functions in the changepoint package to detect change points.

## Example Usage
```python
import numpy as np
from changepoint.mean_shift_model import MeanShiftModel
ts = np.concatenate([np.random.normal(0, 0.1, 100), np.random.normal(10, 0.1, 100)])
model = MeanShiftModel()
stats_ts, pvals, nums = model.detect_mean_shift(ts, B=1000)
```

## Requirements
* numpy
* scipy
* rpy2
* more_itertools
* joblib
* argparse
* future

(may have to be independently installed) 


## Installation
```bash
cd changepoint
pip install -r requirements.txt
python setup.py install
```
