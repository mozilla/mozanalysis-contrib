# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

def metricDAU(data, needed_dimension_variables, usage_col, sampling_multiplier):
"""Generate a Spark DataFrame with the specified DAU metric in a format to be documented.
    Args:
        data: a Spark DataFrame in a format to be documented.
        needed_dimension_variables: a list of strings representing the variables that
                                    should be available for slicing.
        usage_col: a string representing the usage criteria for which to calculate DAU.
        sampling_multiplier: a multiplier to account for sampling in the provided data.
    """
  data = data.select(
    ["date", usage_col, "bucket"] + needed_dimension_variables
  ).groupBy(
  ["date", "bucket"] + needed_dimension_variables
  ).agg(
      (F.sum(usage_col) * sampling_multiplier).alias(usage_col)
  )

  data = data.unionByName(
    data.groupBy(
      ["date"] + needed_dimension_variables
    ).agg(
      F.sum(feature_col).alias(feature_col)
    ).withColumn(
      'bucket', lit("ALL")
    )
  )
  return data
