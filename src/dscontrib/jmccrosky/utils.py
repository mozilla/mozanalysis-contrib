# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import numpy as np
from astropy.stats import jackknife_stats

def jackknifeCountCI(data, string_mode=False):
  count = np.sum(data)
  jackknife_buckets = len(data)
  estimate, bias, stderr, conf_interval = jackknife_stats(np.array(data), np.mean, 0.95)
  if string_mode:
    # TODO: extract a CI formatting function with configurable decimal places (here and below)
    return "({:.0f} - {:.0f})".format(conf_interval[0] * jackknife_buckets, conf_interval[1] * jackknife_buckets)
  else:
    return [(count - conf_interval[0] * jackknife_buckets), (conf_interval[1] * jackknife_buckets - count)]
