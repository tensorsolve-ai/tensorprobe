# All content widgets goes here
import qgrid
import logging
import pandas as pd
from ipywidgets.widgets import Output, Button, HTML, VBox, HBox, Layout, Accordion, Tab, Label
from IPython.display import display

from .helpers import apply_thresh_style, predictors, progressbar
from .vis_widgets import pp_barplot_widget, pplot_output_widget, histogram_widget, pie_chart_widget, iv_plot_widget


logger = logging.getLogger(__name__)

layout = Layout(width='100%', height='100%')
predbtn_layout = Layout(width='auto', height='30px')
pred_wiget_layout = Layout(width='300px', height='auto')
# output_layout = Layout(height='auto', width='auto',
#                       border='1.5px solid', display='flex')

# summary stats


def summary_stats(df):
    summaryDF = pd.DataFrame([df.dtypes, df.count(), df.nunique(), df.isnull().sum(),
                              df.mean(), df.std(), df.median(), df.max(),
                              df.min()]).T
    summaryDF.columns = summaryDF.columns = ['type', 'count', 'unique', 'missing', 'mean',
                                             'std', 'median', 'max', 'min']

    return summaryDF


# summary stats widget
def summary_stats_widget(df):
    stats_output = Output()
    with stats_output:
        logger.info("invoking summary_stats")
        summ_stats = summary_stats(df)
        logger.info("got summary statistics from summary_stats")
        logger.info("applying threshold color")
        display(apply_thresh_style(summary_stats(df)))
        logger.info("finished applying threshold")
    return stats_output


# Data frame info
def table_info_widget(df):
    return HTML("<b><span style='color:blue;font-weight:bold'>%s</span> Rows and <span style='color:blue;font-weight:bold'>%s</span> Columns</b>" % df.shape)


# predictors widget
def predictors_widget(preds, target):
    # plen = len(preds)
    logger.debug("inside predictors_widget")
    preds_btn = []
    for key, val in preds:
        btn = Button(description='%s : %s' % (key, val), disabled=False, button_style='',
                     tooltip=str(val), layout=predbtn_layout, display='flex',
                     flex_flow='column', align_items='stretch')  # , icon='check')
        # set btn color
        btn.style.button_color = 'lightgreen'
        preds_btn.append(btn)

    logger.info("Done creating predictor buttons")

    head_out = HTML(
        "<h3> Predictors of `%s` with their predictive power </h3>" % (target))
    preds_btn.insert(0, head_out)
    children = preds_btn
    preds_widget = VBox(children, layout=pred_wiget_layout)
    bar_w = pp_barplot_widget(preds)
    # set width of bar plot
    bar_w.layout.width = 450

    rightside_vis = HBox([bar_w], display='flex', align_items="stretch")
    #rightside_vis.layout.align_items = 'center'
    rightside_vis.layout.flex = "1.5 1 auto"
    rightside_vis.layout.width = "60%"
    rightside_vis.layout.border = '1px solid black'
    preds_widget.layout.flex = "1 1 auto"
    preds_widget = HBox([preds_widget, rightside_vis],
                        layout=layout, display='flex')
    return preds_widget


def interactive_df_widget(df):
    int_df = qgrid.show_grid(df, grid_options={'forceFitColumns': False},
                             show_toolbar=True)
    return int_df


def glimpse_output_widget(df):
    stats_info = summary_stats_widget(df)
    table_info = table_info_widget(df)
    glimpse_output = VBox([table_info, stats_info],
                          layout=layout, display='flex')
    return glimpse_output


def cf_output_widget(df):
    idf = interactive_df_widget(df)
    cf_output = VBox([idf])
    return cf_output


def pp_output_widget(df):
    pp = pplot_output_widget(df)
    pp_output = VBox([pp])
    return pp_output


@progressbar
def column_output_widget(df, colname, **kwargs):
    logger.debug("inside column_output_widget")
    output = Output()
    with output:
        vis_output = Output()
        preds_output = Output()

        with vis_output:
            if df[colname].dtype.name in ['int64', 'float64']:
                logger.debug("invoking histogram_widget for %s" % (colname))
                hplot = histogram_widget(df, colname)
                logger.debug("histogram widget created for %s" % (colname))
                hist_html = HTML("<h2>Histogram Plot of %s</h2>" % (colname))
                display(hist_html)
                display(hplot)
            else:
                logger.debug("invoking histogram_widget for %s" % (colname))
                hplot = histogram_widget(df, colname)
                logger.debug("histogram widget created for %s" % (colname))
                logger.debug("invoking pie_chart_widget for %s" % (colname))
                pie_widg = pie_chart_widget(df, colname)
                logger.debug("pie widget created for %s" % (colname))
                pie_html = HTML("<h2>Pie Plot of %s</h2>" % (colname))
                hist_html = HTML("<h2>Histogram Plot of %s</h2>" % (colname))
                display(hist_html)
                # histogram plot
                display(hplot)
                # plot pie chart
                display(pie_html)
                display(pie_widg)

        with preds_output:
            # get preds and scores
            logger.debug("invoking predictors of %s" % colname)
            preds = predictors(df, df[colname])
            logger.debug("got predictors of %s" % colname)
            logger.debug("creating predictors_widget for %s" % colname)
            pw = predictors_widget(preds, colname)
            logger.debug("done creating predictors_widget for %s" % colname)
            display(pw)

        tab = Tab([vis_output, preds_output])
        tab.set_title(0, "Visualize")
        tab.set_title(1, "Predictors")
        # display tab
        display(tab)
    logger.debug("returning from column_output_widget")

    return output


def columns_accordion_widget(df):
    accordion = Accordion(selected_index=None, layout=layout)
    children = []
    for i, colname in enumerate(df.columns):
        accordion.set_title(i, colname)

        # build each column dummy output (accordion children)
        child_widget = Label()  # column_output_widget(df, colname)
        children.append(child_widget)

    # set accordion children
    accordion.children = children

    # create accordion handler
    flag = {}

    def accordion_handler(change):
        children = list(change.owner.children)
        for i in range(len(children)):
            if change.new == i and (not flag.get(i, 0)):
                # build child widget
                colname = change.owner._titles[str(i)]
                column_output_widget(df, colname, index=i,
                                     children=children, parent=change.owner)
                flag[i] = 1
                break
        return

    # set observer
    accordion.observe(accordion_handler)

    return accordion


# def monitor(func):
#     flag = {}

#     def wrapper(*args, **kwargs):
#         change = args[0]
#         # print(args[1])
#         children = list(change.owner.children)
#         for i in range(len(children)):
#             if change.new == i and (not flag.get(i, 0)):
#                 print(i)
#                 children.pop(i)
#                 # build child widget
#                 colname = change.owner._titles[str(i)]
#                 child_widget = column_output_widget(df, colname)
#                 children.insert(i, child_widget)
#                 change.owner.children = children
#                 flag[i] = 1
#                 break
#         return
#     return wrapper


# @monitor
# def accordion_handler(change):
#     pass


def columns_output_widget(df):
    col_acc = columns_accordion_widget(df)

    # set an observer handler
    # col_acc.observe(accordion_handler)
    co_widget = VBox([col_acc])
    return co_widget
