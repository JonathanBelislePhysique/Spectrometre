from PyQt5 import QtWidgets, QtGui, QtCore


class MyLabelROI(QtWidgets.QLabel):

    def __init__(self):
        super(MyLabelROI, self).__init__()
        self.roi_start_draw = False
        self.roi_draw_data = [20, 20, 80, 80]

    def mousePressEvent(self, QMouseEvent):
        xcursor, ycursor = QMouseEvent.pos().x(), QMouseEvent.pos().y()
        self.roi_draw_data = [xcursor, ycursor, xcursor, ycursor]
        self.roi_start_draw = True

    def mouseMoveEvent(self, QMouseEvent):
        super().mouseMoveEvent(QMouseEvent)
        if self.roi_start_draw:
            xcursor, ycursor = QMouseEvent.pos().x(), QMouseEvent.pos().y()
            if xcursor > self.width():
                xcursor = self.width()
            if xcursor < 0:
                xcursor = 0
            if ycursor > self.height():
                ycursor = self.height()
            if ycursor < 0:
                ycursor = 0

            self.roi_draw_data[2:] = [xcursor, ycursor]
        self.update()

    def mouseReleaseEvent(self, QMouseEvent):
        self.roi_start_draw = False
        super().mouseReleaseEvent(QMouseEvent)
        if self.roi_draw_data[0] > self.roi_draw_data[2]:
            temp = self.roi_draw_data[0]
            self.roi_draw_data[0] = self.roi_draw_data[2]
            self.roi_draw_data[2] = temp
        if self.roi_draw_data[1] > self.roi_draw_data[3]:
            temp = self.roi_draw_data[1]
            self.roi_draw_data[1] = self.roi_draw_data[3]
            self.roi_draw_data[3] = temp

    def paintEvent(self, event):
        super().paintEvent(event)
        self.drawRectangle()

    def drawRectangle(self):
        if self.roi_draw_data[2] > self.roi_draw_data[0]:
            x = self.roi_draw_data[0]
            width = self.roi_draw_data[2] - self.roi_draw_data[0]
        else:
            x = self.roi_draw_data[2]
            width = self.roi_draw_data[0] - self.roi_draw_data[2]
        if self.roi_draw_data[3] > self.roi_draw_data[1]:
            y = self.roi_draw_data[1]
            height = self.roi_draw_data[3] - self.roi_draw_data[1]
        else:
            y = self.roi_draw_data[3]
            height = self.roi_draw_data[1] - self.roi_draw_data[3]

        rect = QtCore.QRect(x, y, width, height)
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtCore.Qt.yellow, 2, QtCore.Qt.SolidLine))
        painter.drawRect(rect)
