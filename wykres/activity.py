from __future__ import unicode_literals
from matplotlib.backends import qt4_compat
use_pyside = qt4_compat.QT_API == qt4_compat.QT_API_PYSIDE

from PyQt4 import QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import time


class MyMplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.axes.hold(False)

        self.axes.set_autoscaley_on(False)
        self.axes.set_ylim(bottom=1)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyDynamicMplCanvas(MyMplCanvas):

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.n = 10
        self.x = [0]
        self.y = [0]
        self.a = [0]
        self.time_init = time.time()

    def compute_initial_figure(self):
        self.axes.plot([], [], 'r')

    def update_figure(self, timey):

        timex = time.time()-self.time_init
        if len(self.a) >= self.n:
            self.a.pop(0)
        self.a.append(timey)

        if len(self.x) >= self.n:
            self.x.pop(0)
        self.x.append(timex)

        if len(self.y) >= self.n:
            self.y.pop(0)
        self.y.append(sum(self.a)/len(self.a))

        self.axes.plot(self.x, self.y, 'r')
        self.draw()