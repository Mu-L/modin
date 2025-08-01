# Licensed to Modin Development Team under one or more contributor license agreements.
# See the NOTICE file distributed with this work for additional information regarding
# copyright ownership.  The Modin Development Team licenses this file to you under the
# Apache License, Version 2.0 (the "License"); you may not use this file except in
# compliance with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

import warnings

import pandas
from packaging import version

__min_pandas_version__ = "2.2"
__max_pandas_version__ = "2.4"

pandas_version = version.parse(pandas.__version__)
if pandas_version < version.parse(
    __min_pandas_version__
) or pandas_version >= version.parse(__max_pandas_version__):
    warnings.warn(
        f"The pandas version installed ({pandas.__version__}) is outside the supported range in Modin"
        + f" ({__min_pandas_version__} to {__max_pandas_version__}). This may cause undesired side effects!"
    )

# to not pollute namespace
del version, pandas_version, __min_pandas_version__, __max_pandas_version__


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import inspect

    from modin.core.storage_formats.pandas.query_compiler_caster import (
        wrap_free_function_in_argument_caster,
    )

    # To allow the extensions system to override these methods, we must wrap all objects re-exported
    # from pandas in a backend dispatcher.
    _reexport_list = (
        "eval",
        "factorize",
        "test",
        "date_range",
        "period_range",
        "Index",
        "MultiIndex",
        "CategoricalIndex",
        "bdate_range",
        "DatetimeIndex",
        "Timedelta",
        "Timestamp",
        "set_eng_float_format",
        "options",
        "describe_option",
        "set_option",
        "get_option",
        "reset_option",
        "option_context",
        "NaT",
        "PeriodIndex",
        "Categorical",
        "Interval",
        "UInt8Dtype",
        "UInt16Dtype",
        "UInt32Dtype",
        "UInt64Dtype",
        "SparseDtype",
        "Int8Dtype",
        "Int16Dtype",
        "Int32Dtype",
        "Int64Dtype",
        "StringDtype",
        "BooleanDtype",
        "CategoricalDtype",
        "DatetimeTZDtype",
        "IntervalDtype",
        "PeriodDtype",
        "RangeIndex",
        "TimedeltaIndex",
        "IntervalIndex",
        "IndexSlice",
        "Grouper",
        "array",
        "Period",
        "DateOffset",
        "timedelta_range",
        "infer_freq",
        "interval_range",
        "ExcelWriter",
        "NamedAgg",
        "NA",
        "api",
        "ArrowDtype",
        "Flags",
        "Float32Dtype",
        "Float64Dtype",
        "from_dummies",
        "testing",
    )
    for name in _reexport_list:
        item = getattr(pandas, name)
        if inspect.isfunction(item):
            # Note that this is applied to only functions, not classes.
            item = wrap_free_function_in_argument_caster(name)(item)
        globals()[name] = item
    del inspect, item, _reexport_list, name, wrap_free_function_in_argument_caster

import os

from modin.config import Parameter

_engine_initialized = {}


def _initialize_engine(engine_string: str):
    from modin.config import (
        CpuCount,
        Engine,
        IsExperimental,
        StorageFormat,
        ValueSource,
    )

    # Set this so that Pandas doesn't try to multithread by itself
    os.environ["OMP_NUM_THREADS"] = "1"

    if engine_string == "Ray":
        if not _engine_initialized.get("Ray", False):
            from modin.core.execution.ray.common import initialize_ray

            initialize_ray()
    elif engine_string == "Dask":
        if not _engine_initialized.get("Dask", False):
            from modin.core.execution.dask.common import initialize_dask

            initialize_dask()
    elif engine_string == "Unidist":
        if not _engine_initialized.get("Unidist", False):
            from modin.core.execution.unidist.common import initialize_unidist

            initialize_unidist()
    elif engine_string not in Engine.NOINIT_ENGINES:
        raise ImportError("Unrecognized execution engine: {}.".format(engine_string))

    _engine_initialized[engine_string] = True


from modin.pandas import arrays, errors
from modin.pandas.api.extensions.extensions import __getattr___impl
from modin.utils import show_versions

from .. import __version__
from .dataframe import DataFrame
from .general import (
    concat,
    crosstab,
    cut,
    get_dummies,
    isna,
    isnull,
    lreshape,
    melt,
    merge,
    merge_asof,
    merge_ordered,
    notna,
    notnull,
    pivot,
    pivot_table,
    qcut,
    to_datetime,
    to_numeric,
    to_timedelta,
    unique,
    value_counts,
    wide_to_long,
)
from .io import (
    ExcelFile,
    HDFStore,
    json_normalize,
    read_clipboard,
    read_csv,
    read_excel,
    read_feather,
    read_fwf,
    read_gbq,
    read_hdf,
    read_html,
    read_json,
    read_orc,
    read_parquet,
    read_pickle,
    read_sas,
    read_spss,
    read_sql,
    read_sql_query,
    read_sql_table,
    read_stata,
    read_table,
    read_xml,
    to_pickle,
)
from .plotting import Plotting as plotting
from .series import Series

__getattr__ = __getattr___impl


__all__ = [  # noqa: F405
    "DataFrame",
    "Series",
    "read_csv",
    "read_parquet",
    "read_json",
    "read_html",
    "read_clipboard",
    "read_excel",
    "read_hdf",
    "read_feather",
    "read_stata",
    "read_sas",
    "read_pickle",
    "read_sql",
    "read_gbq",
    "read_table",
    "read_spss",
    "read_orc",
    "json_normalize",
    "concat",
    "eval",
    "cut",
    "factorize",
    "test",
    "qcut",
    "to_datetime",
    "get_dummies",
    "isna",
    "isnull",
    "merge",
    "pivot_table",
    "date_range",
    "Index",
    "MultiIndex",
    "Series",
    "bdate_range",
    "period_range",
    "DatetimeIndex",
    "to_timedelta",
    "set_eng_float_format",
    "options",
    "describe_option",
    "set_option",
    "get_option",
    "reset_option",
    "option_context",
    "CategoricalIndex",
    "Timedelta",
    "Timestamp",
    "NaT",
    "PeriodIndex",
    "Categorical",
    "__version__",
    "melt",
    "crosstab",
    "plotting",
    "Interval",
    "UInt8Dtype",
    "UInt16Dtype",
    "UInt32Dtype",
    "UInt64Dtype",
    "SparseDtype",
    "Int8Dtype",
    "Int16Dtype",
    "Int32Dtype",
    "Int64Dtype",
    "CategoricalDtype",
    "DatetimeTZDtype",
    "IntervalDtype",
    "PeriodDtype",
    "BooleanDtype",
    "StringDtype",
    "NA",
    "RangeIndex",
    "TimedeltaIndex",
    "IntervalIndex",
    "IndexSlice",
    "Grouper",
    "array",
    "Period",
    "show_versions",
    "DateOffset",
    "timedelta_range",
    "infer_freq",
    "interval_range",
    "ExcelWriter",
    "read_fwf",
    "read_sql_table",
    "read_sql_query",
    "ExcelFile",
    "to_pickle",
    "HDFStore",
    "lreshape",
    "wide_to_long",
    "merge_asof",
    "merge_ordered",
    "notnull",
    "notna",
    "pivot",
    "to_numeric",
    "unique",
    "value_counts",
    "NamedAgg",
    "api",
    "read_xml",
    "ArrowDtype",
    "Flags",
    "Float32Dtype",
    "Float64Dtype",
    "from_dummies",
    "errors",
]

# Remove these attributes from this module's namespace.
del pandas, Parameter, __getattr___impl
