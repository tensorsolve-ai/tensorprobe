# Dashboard
from ipywidgets.widgets import HBox, VBox, Tab, Layout, HTML

from .utils.content_widgets import (glimpse_output_widget,
                                   cf_output_widget, pp_output_widget,
                                   columns_output_widget)
import logging


logging.basicConfig(filename='tensorprobe.log', filemode='a', level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

layout = Layout(height="100%", width="100%")


class Dashboard(object):
    def __init__(self):
        self.dashboard = HBox([])
        self.tab = Tab(layout=layout)
        self.titles = ['Glimpse', 'Columns', 'Cross filters',
                       'Pairwise Patterns']

        # set titles for tab cell
        for i, title in enumerate(self.titles):
            self.tab.set_title(i, title)

    def __call__(self, df):
        # build dashboard
        logger.info("building dashboard...")
        self.build_dashboard(df)
        logger.info("finished building dashboard")

        return self.dashboard

    def set_tab_children(self, children):
        self.tab.children = children

    def set_dash_children(self, children):
        self.dashboard.children = children

    def build_dashboard(self, df):
        # build tab children
        logger.info("building glimpse output widget...")
        glimpse = glimpse_output_widget(df)
        logger.info("finished building glimpse output widget")
        logger.info("building column output widget...")
        column = columns_output_widget(df)
        logger.info("finished building columns output widget")
        logger.info("building pairwise output widget..")
        pairwise = HTML("Dummy")
        logger.info("finished building pairwise output widget")
        logger.info("building cross filter widget...")
        cross_filter = cf_output_widget(df)
        logger.info("finished building cross filter widget")

        tab_children = [glimpse, column, cross_filter, pairwise]
        # set tab children
        self.set_tab_children(tab_children)
        # set dashboard children
        self.set_dash_children([self.tab])

        return self.dashboard
