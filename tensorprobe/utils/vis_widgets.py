# All visualization widgets method goes here

import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from ipywidgets.widgets import Output, interactive


# IV/WOE visualization widgets
def woe_plot_widget(iv_table, width=500, height=500):
    data = [go.Bar(
        x=iv_table['VAR_NAME'],
        y=iv_table['WOE'],
        text=iv_table['VAR_NAME'],
        marker=dict(
            color='orange',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity=0.6
    )]

    layout = go.Layout(
        title='Weight of Evidence(WOE)',
        xaxis=dict(
            title='Features',
            tickangle=-45,
            tickfont=dict(
                size=10,
                color='rgb(107, 107, 107)'
            )
        ),
        yaxis=dict(
            title='Weight of Evidence(WOE)',
            titlefont=dict(
                size=14,
                color='rgb(107, 107, 107)'
            ),
            tickfont=dict(
                size=14,
                color='rgb(7, 7, 7)'
            )
        ),
    )

    fig = go.Figure(data, layout)
    fig.update_layout(autosize=False, width=width,
                      height=height)
    woe_widget = go.FigureWidget(fig)

    return woe_widget


def iv_plot_widget(iv, width=500, height=500):
    data = [go.Bar(
        x=iv['VAR_NAME'],
        y=iv['IV'],
        text=iv['VAR_NAME'],
        marker=dict(
            color='rgb(58,256,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity=0.6
    )]

    layout = go.Layout(
        title='Information Values',
        xaxis=dict(
            tickangle=-45,
            title='Features',
            tickfont=dict(
                size=10,
                color='rgb(7, 7, 7)'
            )
        ),
        yaxis=dict(
            title='Information Value(IV)',
            titlefont=dict(
                size=14,
                color='rgb(107, 107, 107)'
            ),
            tickfont=dict(
                size=14,
                color='rgb(107, 107, 107)'
            )
        ),
    )

    fig = go.Figure(data, layout)
    fig.update_layout(autosize=False, width=width,
                      height=height)
    iv_widget = go.FigureWidget(fig)
    return iv_widget


def pp_barplot_widget(preds):
    names, scores = [p[0]
                     for p in reversed(preds)], [p[1] for p in reversed(preds)]
    bar = go.Bar(x=scores, y=names, orientation='h')
    bar_w = go.FigureWidget(bar)
    bar_w
    return bar_w


def histogram_widget(df, colname):
    hist = go.Histogram(x=df[colname], name="Frequency Plot")
    hist_widget = go.FigureWidget(hist)
    hist_widget.layout.title = "Histogram Plot"
    hist_widget.layout.yaxis.title = "frequency"
    hist_widget.layout.xaxis.title = colname
    # check if not a string category type
    # hist_widget.data[0].nbinsx = bin_size
    return hist_widget


def pplot_output_widget(df):
    """pair plot widget"""
    pplot_output = Output()
    with pplot_output:
        # sns.pairplot(df, vars=[col1, col2])
        # dropping na values to avoid
        # ValueError: max must be larger than min in range parameter
        sns.pairplot(df.dropna())
        plt.show()
    return pplot_output


def pairwiseplot_widget(df):
    def pairwiseplot():
        return df.scatter_matrix()

    pplot_widget = interactive(pairwiseplot)
    return pplot_widget


def pie_chart_widget(df, colname):
    tempDF = df[colname].value_counts().reset_index()
    labels, values = tempDF['index'], tempDF[colname]
    fig = go.Pie(labels=labels, values=values, hole=0.5, textinfo='percent',
                 textposition='inside')
    fw = go.FigureWidget(fig)
    return fw
