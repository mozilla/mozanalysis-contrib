# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pandas as import pd


def calculateDateWindow(
        plot_start_date, plot_end_date, smoothing, comparison_mode, metric
):
    start_window = plot_start_date - \
        pd.DateOffset(days=smoothing-1) - \
        pd.DateOffset(days=metricDaysNeededPre[metric]) - \
        pd.to_timedelta('1 second')           # Needed due to pyspark between() bug
    end_window = plot_end_date + \
        pd.to_timedelta('1 second') + \
        pd.DateOffset(days=metricDaysNeededPost[metric])
    window = [(start_window, end_window)]
    if comparison_mode in ["YoY", "Last Year"]:
        window = window + [(
            start_window - pd.DateOffset(years=1),
            end_window - pd.DateOffset(years=1)
        )]
    return window

def doSmoothing(data, usage_criteria, dimension_cols, smoothing_lookback):
    windowSpec =  Window.partitionBy(
        [data.bucket]
    ).orderBy(
        data.date
    ).rowsBetween(
        -smoothing_lookback, 0
    )

    return data.withColumn(
        "n_", F.mean(data[usage_criteria]).over(windowSpec)
    ).drop(
        usage_criteria
    ).withColumnRenamed(
        "n_", usage_criteria
    )
