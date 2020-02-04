import logging
import re
import traceback
import numpy as np
import pandas as pd
import scipy.stats.stats as stats
import pandas.core.algorithms as algos
#from tqdm.notebook import tqdm

from .conf import MAX_BIN, FORCE_BIN


logger = logging.getLogger(__name__)


class InformationValue:

    def __init__(self):
        self.max_bin = MAX_BIN
        self.force_bin = FORCE_BIN

    def mono_bin(self, Y, X, n=MAX_BIN):
        df1 = pd.DataFrame({"X": X, "Y": Y})
        justmiss = df1[['X', 'Y']][df1.X.isnull()]
        notmiss = df1[['X', 'Y']][df1.X.notnull()]
        r = 0
        while np.abs(r) < 1:
            try:
                d1 = pd.DataFrame(
                    {"X": notmiss.X, "Y": notmiss.Y, "Bucket": pd.qcut(notmiss.X, n)})
                d2 = d1.groupby('Bucket', as_index=True)
                r, p = stats.spearmanr(d2.mean().X, d2.mean().Y)
                n = n - 1
            except Exception as e:
                n = n - 1

        if len(d2) == 1:
            n = self.force_bin
            bins = algos.quantile(notmiss.X, np.linspace(0, 1, n))
            if len(np.unique(bins)) == 2:
                bins = np.insert(bins, 0, 1)
                bins[1] = bins[1] - (bins[1] / 2)
            d1 = pd.DataFrame({"X": notmiss.X, "Y": notmiss.Y, "Bucket": pd.cut(
                notmiss.X, np.unique(bins), include_lowest=True)})
            d2 = d1.groupby('Bucket', as_index=True)

        d3 = pd.DataFrame({}, index=[])
        d3["MIN_VALUE"] = d2.min().X
        d3["MAX_VALUE"] = d2.max().X
        d3["COUNT"] = d2.count().Y
        d3["EVENT"] = d2.sum().Y
        d3["NONEVENT"] = d2.count().Y - d2.sum().Y
        d3 = d3.reset_index(drop=True)

        if len(justmiss.index) > 0:
            d4 = pd.DataFrame({'MIN_VALUE': np.nan}, index=[0])
            d4["MAX_VALUE"] = np.nan
            d4["COUNT"] = justmiss.count().Y
            d4["EVENT"] = justmiss.sum().Y
            d4["NONEVENT"] = justmiss.count().Y - justmiss.sum().Y
            d3 = d3.append(d4, ignore_index=True)

        d3["EVENT_RATE"] = d3.EVENT / d3.COUNT
        d3["NON_EVENT_RATE"] = d3.NONEVENT / d3.COUNT
        d3["DIST_EVENT"] = d3.EVENT / d3.sum().EVENT
        d3["DIST_NON_EVENT"] = d3.NONEVENT / d3.sum().NONEVENT
        d3["WOE"] = np.log(d3.DIST_EVENT / d3.DIST_NON_EVENT)
        d3["IV"] = (d3.DIST_EVENT - d3.DIST_NON_EVENT) * \
            np.log(d3.DIST_EVENT / d3.DIST_NON_EVENT)
        d3["VAR_NAME"] = "VAR"
        d3 = d3[['VAR_NAME', 'MIN_VALUE', 'MAX_VALUE', 'COUNT', 'EVENT', 'EVENT_RATE',
                 'NONEVENT', 'NON_EVENT_RATE', 'DIST_EVENT', 'DIST_NON_EVENT', 'WOE', 'IV']]
        d3 = d3.replace([np.inf, -np.inf], 0)
        d3.IV = d3.IV.sum()

        return(d3)

    def char_bin(self, Y, X):
        df1 = pd.DataFrame({"X": X, "Y": Y})
        justmiss = df1[['X', 'Y']][df1.X.isnull()]
        notmiss = df1[['X', 'Y']][df1.X.notnull()]
        df2 = notmiss.groupby('X', as_index=True)

        d3 = pd.DataFrame({}, index=[])
        d3["COUNT"] = df2.count().Y
        d3["MIN_VALUE"] = df2.sum().Y.index
        d3["MAX_VALUE"] = d3["MIN_VALUE"]
        d3["EVENT"] = df2.sum().Y
        d3["NONEVENT"] = df2.count().Y - df2.sum().Y

        if len(justmiss.index) > 0:
            d4 = pd.DataFrame({'MIN_VALUE': np.nan}, index=[0])
            d4["MAX_VALUE"] = np.nan
            d4["COUNT"] = justmiss.count().Y
            d4["EVENT"] = justmiss.sum().Y
            d4["NONEVENT"] = justmiss.count().Y - justmiss.sum().Y
            d3 = d3.append(d4, ignore_index=True)

        d3["EVENT_RATE"] = d3.EVENT / d3.COUNT
        d3["NON_EVENT_RATE"] = d3.NONEVENT / d3.COUNT
        d3["DIST_EVENT"] = d3.EVENT / d3.sum().EVENT
        d3["DIST_NON_EVENT"] = d3.NONEVENT / d3.sum().NONEVENT
        d3["WOE"] = np.log(d3.DIST_EVENT / d3.DIST_NON_EVENT)
        d3["IV"] = (d3.DIST_EVENT - d3.DIST_NON_EVENT) * \
            np.log(d3.DIST_EVENT / d3.DIST_NON_EVENT)
        d3["VAR_NAME"] = "VAR"
        d3 = d3[['VAR_NAME', 'MIN_VALUE', 'MAX_VALUE', 'COUNT', 'EVENT', 'EVENT_RATE',
                 'NONEVENT', 'NON_EVENT_RATE', 'DIST_EVENT', 'DIST_NON_EVENT', 'WOE', 'IV']]
        d3 = d3.replace([np.inf, -np.inf], 0)
        d3.IV = d3.IV.sum()
        d3 = d3.reset_index(drop=True)

        return(d3)

    def data_vars(self, df1, target):
        stack = traceback.extract_stack()
        filename, lineno, function_name, code = stack[-2]
        vars_name = re.compile(r'\((.*?)\).*$').search(code).groups()[0]
        final = (re.findall(r"[\w']+", vars_name))[-1]

        tname = target.name
        numerical_features = set(df1.select_dtypes(np.number).columns)

        x = df1.dtypes.index

        has_target_nan = target.isna().any()
        target_map = {}

        # if target variable is not np.number type convert to category type
        if target.name not in numerical_features:
            target = target.astype('category')
            target, target_map = target.factorize()
            target_map = dict(enumerate(target_map))

            # map NaN to -1 if NaN record present
            if has_target_nan:
                target_map[-1] = 'NaN'
        count = -1

        for i in x:
            if i.upper() not in (final.upper()):
                if np.issubdtype(df1[i], np.number) and df1[i].nunique() > 2:
                    conv = self.mono_bin(target, df1[i])
                    conv["VAR_NAME"] = i
                    count = count + 1
                else:
                    conv = self.char_bin(target, df1[i])
                    conv["VAR_NAME"] = i
                    count = count + 1

                if count == 0:
                    iv_df = conv
                else:
                    iv_df = iv_df.append(conv, ignore_index=True)

        iv = pd.DataFrame({'IV': iv_df.groupby('VAR_NAME').IV.max()})
        iv = iv.sort_values("IV", ascending=False)
        iv = iv.reset_index()
        return (iv_df, iv, target_map)

    def compute_numerical_bin(self, target, feature, bin_num=MAX_BIN):
        df = pd.DataFrame({'X': feature, 'Y': target})
        null_records = df[['X', 'Y']][df.X.isnull()]
        records = df[['X', 'Y']][df.X.notnull()]
        r = 0
        logger.debug(
            "starting while loop, inside compute_numerical_bin")
        while np.abs(r) < 1:
            try:
                logger.debug("quantile_cut")
                quantile_cut = pd.qcut(records.X, bin_num)
                logger.debug("bin_df")
                bin_df = pd.DataFrame({'X': records.X, 'Y': records.Y,
                                       'Bucket': quantile_cut})
                logger.debug("bin_df groupby")
                bin_df = bin_df.groupby('Bucket', as_index=True)
                logger.debug("calling spearmanr")
                r, p = stats.spearmanr(bin_df.mean().X, bin_df.mean().Y)
                logger.debug("r: %s, p: %s" % (r, p))
                bin_num = bin_num - 1
            except Exception as e:
                bin_num = bin_num - 1

        logger.debug("out of while loop, column")
        if len(bin_df) == 1:
            bin_num = self.force_bin
            bins = algos.quantile(records.X, np.linspace(0, 1, bin_num))

            if len(np.unique(bins)) == 2:
                bins = np.insert(bins, 0, 1)
                bins[1] = bins[1] - (bins[1] / 2)
                quantile_cut = pd.cut(records.X, np.unique(bins),
                                      include_lowest=True)
                bin_df = pd.DataFrame({'X': records.X, 'Y': records.Y,
                                       'Bucket': quantile_cut})
                bin_df = bin_df.groupby('Bucket', as_index=True)

        logger.debug("creating num_iv")
        num_iv = pd.DataFrame({}, index=[])
        logger.debug("num_iv created")
        num_iv["MIN_VALUE"] = bin_df.min().X
        num_iv["MAX_VALUE"] = bin_df.max().X
        num_iv["COUNT"] = bin_df.count().Y
        num_iv["EVENT"] = bin_df.sum().Y
        num_iv["NONEVENT"] = bin_df.count().Y - bin_df.sum().Y

        num_iv = num_iv.reset_index(drop=True)
        logger.debug("reset index")
        if len(null_records.index) > 0:
            logger.debug("creating temp_num_iv")
            temp_num_iv = pd.DataFrame({'MIN_VALUE': np.nan}, index=[0])
            logger.debug("done creating temp_num_iv")
            temp_num_iv["MAX_VALUE"] = np.nan
            temp_num_iv["COUNT"] = null_records.count().Y
            temp_num_iv["EVENT"] = null_records.sum().Y
            temp_num_iv["NONEVENT"] = (null_records.count().Y -
                                       null_records.sum().Y)

            num_iv = num_iv.append(temp_num_iv, ignore_index=True, sort=False)

        num_iv["EVENT_RATE"] = num_iv.EVENT / num_iv.COUNT
        num_iv["NON_EVENT_RATE"] = num_iv.NONEVENT / num_iv.COUNT
        num_iv["DIST_EVENT"] = num_iv.EVENT / num_iv.sum().EVENT
        num_iv["DIST_NON_EVENT"] = num_iv.NONEVENT / num_iv.sum().NONEVENT
        num_iv["WOE"] = np.log(num_iv.DIST_EVENT / num_iv.DIST_NON_EVENT)
        num_iv["IV"] = ((num_iv.DIST_EVENT - num_iv.DIST_NON_EVENT) *
                        np.log(num_iv.DIST_EVENT / num_iv.DIST_NON_EVENT))
        num_iv["VAR_NAME"] = "VAR"
        num_iv = num_iv[['VAR_NAME', 'MIN_VALUE', 'MAX_VALUE', 'COUNT',
                         'EVENT', 'EVENT_RATE', 'NONEVENT', 'NON_EVENT_RATE',
                         'DIST_EVENT', 'DIST_NON_EVENT', 'WOE', 'IV']]
        num_iv = num_iv.replace([np.inf, -np.inf], 0)
        num_iv.IV = round(num_iv.IV.sum(), 2)

        # clear memory
        del df
        del records
        del quantile_cut
        if len(bin_df) == 1:
            del bins
        del bin_df
        if len(null_records.index) > 0:
            del temp_num_iv
        del null_records

        logger.debug("coming out of compute_numerical_bin")

        return num_iv

    def compute_char_bin(self, target, feature):
        df = pd.DataFrame({'X': feature, 'Y': target})
        null_records = df[['X', 'Y']][df.X.isnull()]
        records = df[['X', 'Y']][df.X.notnull()]

        bin_df = records.groupby('X', as_index=True)

        char_iv = pd.DataFrame({}, index=[])
        char_iv["COUNT"] = bin_df.count().Y
        char_iv["MIN_VALUE"] = bin_df.sum().Y.index
        char_iv["MAX_VALUE"] = char_iv["MIN_VALUE"]
        char_iv["EVENT"] = bin_df.sum().Y
        char_iv["NONEVENT"] = bin_df.count().Y - bin_df.sum().Y

        if len(null_records.index) > 0:
            temp_char_iv = pd.DataFrame({'MIN_VALUE': np.nan}, index=[0])
            temp_char_iv["MAX_VALUE"] = np.nan
            temp_char_iv["COUNT"] = null_records.count().Y
            temp_char_iv["EVENT"] = null_records.sum().Y
            temp_char_iv["NONEVENT"] = null_records.count().Y - \
                null_records.sum().Y
            char_iv = char_iv.append(
                temp_char_iv, ignore_index=True, sort=False)

        char_iv["EVENT_RATE"] = char_iv.EVENT / char_iv.COUNT
        char_iv["NON_EVENT_RATE"] = char_iv.NONEVENT / char_iv.COUNT
        char_iv["DIST_EVENT"] = char_iv.EVENT / char_iv.sum().EVENT
        char_iv["DIST_NON_EVENT"] = char_iv.NONEVENT / char_iv.sum().NONEVENT
        char_iv["WOE"] = np.log(char_iv.DIST_EVENT / char_iv.DIST_NON_EVENT)
        char_iv["IV"] = ((char_iv.DIST_EVENT - char_iv.DIST_NON_EVENT) *
                         np.log(char_iv.DIST_EVENT / char_iv.DIST_NON_EVENT))
        char_iv["VAR_NAME"] = "VAR"
        char_iv = char_iv[['VAR_NAME', 'MIN_VALUE', 'MAX_VALUE', 'COUNT',
                           'EVENT', 'EVENT_RATE', 'NONEVENT', 'NON_EVENT_RATE',
                           'DIST_EVENT', 'DIST_NON_EVENT', 'WOE', 'IV']]
        char_iv = char_iv.replace([np.inf, -np.inf], 0)
        char_iv.IV = round(char_iv.IV.sum(), 2)
        char_iv = char_iv.reset_index(drop=True)

        # clear memory
        del df
        del bin_df
        if len(null_records.index) > 0:
            del temp_char_iv
        del null_records
        return(char_iv)

    def compute_iv_table(self, df, target):
        tname = target.name

        numerical_features = set(df.select_dtypes(np.number).columns)
        x = df.dtypes.index

        has_target_nan = target.isna().any()
        target_map = {}

        # if target variable is not np.number type convert to category type
        if target.name not in numerical_features:
            target = target.astype('category')
            target, target_map = target.factorize()
            target_map = dict(enumerate(target_map))

            # map NaN to -1 if NaN record present
            if has_target_nan:
                target_map[-1] = 'NaN'

        count = -1

        for colname in x:
            if colname.upper() not in (tname.upper()):
                logger.debug(
                    "checking for unique values in a column:%s to be greater than 2" % colname)
                if (colname in numerical_features) and (  # len(pd.Series(df[colname]).unique())
                        df[colname].nunique()) > 2:
                    logger.debug(
                        "done checking number of unique values for column %s" % colname)
                    logger.debug(
                        "calling compute_numerical_bin column: %s" % (colname))
                    conv = self.compute_numerical_bin(target,
                                                      df[colname])
                    logger.debug(
                        "done computing numerical bin column: %s" % (colname))
                    conv["VAR_NAME"] = colname
                    count += 1
                else:
                    logger.debug(
                        "calling compute_char_bin: target column: %s" % (colname))
                    conv = self.compute_char_bin(target, df[colname])
                    logger.debug(
                        "done computing char bin: target column: %s" % (colname))
                    conv["VAR_NAME"] = colname
                    count += 1

                if count == 0:
                    iv_df = conv
                else:
                    iv_df = iv_df.append(conv, ignore_index=True, sort=False)

        iv = pd.DataFrame({'IV': iv_df.groupby('VAR_NAME').IV.max()})
        iv = iv.sort_values("IV", ascending=False).reset_index()
        return (iv_df, iv, target_map)

    def get_iv_scores(self, df, target):
        iv_df, iv_scores, tmap = self.compute_iv_table(df, target)
        # iv_df, iv_scores, tmap = self.data_vars(df, target)
        return iv_scores

    def get_iv_df(self, df, target):
        iv_df, iv, tmap = self.compute_iv_table(df, target)
        return iv_df

    # Calculate information value
    def calc_iv(self, df, feature, target, pr=False):
        """
        Set pr=True to enable printing of output.

        Output:
          * iv: float,
          * data: pandas.DataFrame
        """

        lst = []

        df[feature] = df[feature].fillna("NULL")

        for i in range(df[feature].nunique()):
            val = list(df[feature].unique())[i]
            lst.append([feature,                                                        # Variable
                        val,                                                            # Value
                        # All
                        df[df[feature] == val].count()[feature],
                        df[(df[feature] == val) & (df[target] == 0)].count()[
                            feature],  # Good (think: Fraud == 0)
                        df[(df[feature] == val) & (df[target] == 1)].count()[feature]])  # Bad (think: Fraud == 1)

        data = pd.DataFrame(
            lst, columns=['Variable', 'Value', 'All', 'Good', 'Bad'])

        data['Share'] = data['All'] / data['All'].sum()
        data['Bad Rate'] = data['Bad'] / data['All']
        data['Distribution Good'] = (
            data['All'] - data['Bad']) / (data['All'].sum() - data['Bad'].sum())
        data['Distribution Bad'] = data['Bad'] / data['Bad'].sum()
        data['WoE'] = np.log(data['Distribution Good'] /
                             data['Distribution Bad'])

        data = data.replace({'WoE': {np.inf: 0, -np.inf: 0}})

        data['IV'] = data['WoE'] * \
            (data['Distribution Good'] - data['Distribution Bad'])

        data = data.sort_values(
            by=['Variable', 'Value'], ascending=[True, True])
        data.index = range(len(data.index))

        if pr:
            print(data)
            print('IV = ', data['IV'].sum())

        iv = data['IV'].sum()
        # print(iv)

        return iv, data
