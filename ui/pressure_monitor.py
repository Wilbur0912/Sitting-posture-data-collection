from PyQt5.QtWidgets import QLabel
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import QSize

history_limit = 33 * 5

class PressureMonitor(QLabel):
    pen_pressure = QPen(QColor(255,0,0), 15)
    pen_ticks_thin = QPen(QColor(0,255,0), 6)
    pen_ticks_thick = QPen(QColor(0,255,0), 10)

    def __init__(self):
        super().__init__()
        self.history = []
        self.setScaledContents(True)
        self._pixmap = None
    
    def paintEvent(self, a0: QPaintEvent) -> None:
        if self._pixmap == None:
            return
        painter = QPainter(self)
        width = self.width()
        height = self.height()
        image_width = self._pixmap.width()
        image_height = self._pixmap.height()

        scale_x = width / image_width
        scale_y = height / image_height
        painter.setTransform(QTransform().scale(scale_x, scale_y))
        painter.drawPixmap(0,0, self._pixmap)

        return super().paintEvent(a0)
        

    def add_pressure(self, value):
        """
        size = self.contentsRect().size()
        if self._pixmap and self._pixmap.size() == size:
            pixmap = self._pixmap
        else:
            pixmap = QtGui.QPixmap(size)
            self._pixmap = pixmap
        """
        size = QSize(300, 1024)
        if self._pixmap:
            pixmap = self._pixmap
        else:
            pixmap = QtGui.QPixmap(size)
            self._pixmap = pixmap

        scale_x = 1#size.width() / history_limit
        scale_y = 1#size.height() / 1024

        pixmap.fill(QColor(0,0,0))
        painter = QtGui.QPainter(pixmap)
        
        #painter.setPen(self.pen_ticks_thin)
        #for i in range(1, 10,2):
        #    painter.drawLine(0,i*size.height()//10,size.width(),i*size.height()//10)

        painter.setPen(self.pen_ticks_thick)
        for i in range(2, 10,2):
            painter.drawLine(0,i*size.height()//10,size.width(),i*size.height()//10)

        painter.setPen(self.pen_pressure)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        path = QPainterPath()
        self.history.append(value)
        if len(self.history) > history_limit:
            self.history = self.history[len(self.history) - history_limit:]
        path.moveTo(0, self.history[0] * scale_y)
        for i, pressure in enumerate(self.history):
            path.lineTo(i * scale_x, pressure * scale_y)
        

        painter.drawPath(path)
        painter.end()
        self.update()
        #self.setPixmap(pixmap)