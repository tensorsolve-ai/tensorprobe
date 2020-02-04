# All helpers method here
import time
import logging
import threading
from .iv import InformationValue
from ipywidgets.widgets import FloatProgress
# from IPython.display import display


logger = logging.getLogger(__name__)


class Queue:
    def put(self, item):
        self.item = item

    def get(self):
        return self.item


def work(progress, q):
    total = 100
    for i in range(total):
        end = q.get()
        if end:
            progress.value = 1
            return
        elif i <= (total - 20):
            time.sleep(0.07)
            # time.sleep(0.75)
            progress.value = float(i + 1) / total
        else:
            # don't let this process finished before the main
            logger.debug("going to while loop inside work")
            inc = i
            while True:
                end = q.get()
                if end:
                    logger.debug(
                        "setting progess value to 0.98 and coming out")
                    progress.value = 1
                    # time.sleep(0.1)
                    return
                else:
                    logger.debug("inside else, worker")
                    # slowly increase time
                    if progress.value < 0.95:
                        time.sleep(1)
                        progress.value = float(inc + 1) / total
                        inc += 1
                        logger.debug(
                            "check condition; new progress value: %s" % progress.value)
        logger.debug("i: %s" % i)
    logger.debug("out of for loop in work")
    return


def progressbar(func):
    def wrapper(*args, **kwargs):
        q = Queue()
        que = Queue()

        q.put(False)
        progress = FloatProgress(value=0.0, min=0.0, max=1.0)
        pbar_thread = threading.Thread(target=work, args=(progress, q))
        worker = threading.Thread(target=lambda q, *args, **kwargs: q.put(func(*args, **kwargs)),
                                  args=(que, *args), kwargs=kwargs)

        pbar_thread.start()
        worker.start()

        index = kwargs['index']
        children = kwargs['children']
        parent = kwargs['parent']

        # first make progess bar as child
        child = progress  # wrapper(*args, **kwargs)
        children.pop(index)
        children.insert(index, child)
        parent.children = children
        # wait for worker thread to complete
        logger.debug("waiting for the worker, with progressbar")
        worker.join()
        q.put(True)
        logger.debug("done waiting for the worker.")
        time.sleep(0.1)
        # assing main child instead of progress bar
        child = que.get()
        children.pop(index)
        children.insert(index, child)
        parent.children = children

        return
    return wrapper


def infvalue(func):
    logger.debug("invoking InformationValue object")
    iv = InformationValue()
    logger.debug("InformationValue object created")

    def preds_predpower(*args, **kwargs):
        logger.debug("calling get_iv_scores method on InformationValue object")
        preds = iv.get_iv_scores(*args, **kwargs)
        logger.debug("get_iv_scores succeded, got all predictors")
        preds = preds.to_numpy()
        return preds
    return preds_predpower


def color_lt(x, threshold, color):
    if x > threshold:
        color = color
    else:
        color = ''
    return 'color: %s' % color


def highlight_bg_gtr(x, threshold, color):
    if x > threshold:
        color = color  # '#FF4500'
    else:
        color = ''
    return 'background-color:%s' % color


def highlight_bg_ltr(x, threshold, color):
    if x <= threshold:
        color = color  # '#FF4500'
    else:
        color = ''
    return 'background-color:%s' % color


def apply_thresh_style(df):
    return df.style.\
        applymap(lambda x: highlight_bg_ltr(x, 0, 'lawngreen'), subset=['missing']).\
        applymap(lambda x: color_lt(x, 0, 'blue'),
                 subset=['missing']).\
        applymap(lambda x: highlight_bg_gtr(
            x, 0, 'orange'), subset=['missing'])


@infvalue
def predictors(df, target):
    pass
