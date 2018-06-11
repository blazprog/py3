import sys
import functools
import random
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

PointSize = 10

class BoxItem(QGraphicsItem):

    def __init__(self, position, scene, style=Qt.SolidLine,
                 rect=None):
        super().__init__()
        self.setFlags(QGraphicsItem.ItemIsSelectable|
                      QGraphicsItem.ItemIsMovable|
                      QGraphicsItem.ItemIsFocusable)
        if rect is None:
            rect = QRectF(PointSize, -PointSize,
                          30 * PointSize, 2 * PointSize)
        self.rect = rect
        self.style = style
        self.setPos(position)
        scene.clearSelection()
        scene.addItem(self)
        self.setSelected(True)
        self.setFocus()

    def parentWidget(self):
        return self.scene().views()[0]


    def boundingRect(self):
        return self.rect.adjusted(-2, -2, 2, 2)


    def paint(self, painter, option, widget):
        pen = QPen(self.style)
        pen.setColor(Qt.black)
        pen.setWidth(1)
        if option.state & QStyle.State_Selected:
            pen.setColor(Qt.blue)
        painter.setPen(pen)
        painter.drawRect(self.rect)

    def setStyle(self, style):
        self.style = style
        self.update()
    
    
    def mousePressEvent(self, event):
        """
        Capture mouse press events and find where the mosue was pressed on the object
        """
        if event.modifiers() & Qt.ShiftModifier:
            self.startPos = event.scenePos()
            self.mouseIsShiftPressed = True
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Capture nmouse press events.
        """
        if event.modifiers() & Qt.ShiftModifier:
            self.endPos = event.scenePos()
            dx, dy = self.calculateDistance(self.startPos, self.endPos)
            self.rect.setRight(self.rect.right() + dx)
            self.rect.setBottom(self.rect.bottom() + dy)
            self.update()
            self.mouseIsShiftPressed = False
        else:
            super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if event.modifiers() & Qt.ShiftModifier:
            pass
        else:
            super().mouseMoveEvent(event)

    def keyPressEvent(self, event):
        factor = PointSize / 4
        changed = False
        if event.modifiers() & Qt.ShiftModifier:
            if event.key() == Qt.Key_Left:
                self.rect.setRight(self.rect.right() - factor)
                changed = True
            elif event.key() == Qt.Key_Right:
                self.rect.setRight(self.rect.right() + factor)
                changed = True
            elif event.key() == Qt.Key_Up:
                self.rect.setBottom(self.rect.bottom() - factor)
                changed = True
            elif event.key() == Qt.Key_Down:
                self.rect.setBottom(self.rect.bottom() + factor)
                changed = True
        if changed:
            self.update()
            global Dirty
            Dirty = True
        else:
            QGraphicsItem.keyPressEvent(self, event)

    def calculateDistance(self, startPos, endPos):
        x1 = startPos.x()
        y1 = startPos.y()
        x2 = endPos.x()
        y2 = endPos.y()

        return x1 -x2, y1 -y2

class Slog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pbAddDiv = QPushButton("Add div")
        self.pbAddDiv.clicked.connect(self.addBlock)
        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.pbAddDiv)
        buttons_layout.addStretch()

        self.view = QGraphicsView()
        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)
        view_layout = QHBoxLayout()
        view_layout.addWidget(self.view)

        main_layout = QHBoxLayout()
        main_layout.addLayout(buttons_layout)
        main_layout.addLayout(view_layout)
        self.setLayout(main_layout)
        self.setGeometry(20,20,800,600)

    def addBlock(self):
        BoxItem(self.position(), self.scene)

    
    def position(self):
        point = self.mapFromGlobal(QCursor.pos())
        if not self.view.geometry().contains(point):
            coord = random.randint(36, 144)
            point = QPoint(coord, coord)
        else:
            if point == self.prevPoint:
                point += QPoint(self.addOffset, self.addOffset)
                self.addOffset += 5
            else:
                self.addOffset = 5
                self.prevPoint = point
        return self.view.mapToScene(point)


def main():
    qapp = QApplication(sys.argv)
    mWin = Slog()
    mWin.show()
    sys.exit(qapp.exec_())
    

if __name__ == '__main__':
    main()

