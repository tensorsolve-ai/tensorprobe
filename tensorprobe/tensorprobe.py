# -*- coding: utf-8 -*-
# All API(s) here

"""Main module."""
from tensorprobe.dashboard import Dashboard
from tensorprobe.utils.content_widgets import summary_stats_widget, table_info_widget
from IPython.display import display


def nan_check(df):
    # drop columns with all nan values
    drop_cols = [col for col in df.columns if df[col].isna().all()]
    df.drop(drop_cols, axis=1, inplace=True)


def probe(df):
    nan_check(df)
    dashboard = Dashboard()(df)
    # print(type(dashboard))
    # display(dashboard)
    return dashboard


def summ_stats(df):
    sw = summary_stats_widget(df)
    return sw


def table(df):
    t = table_info_widget(df)
    return t
