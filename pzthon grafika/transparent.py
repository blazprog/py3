import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class TransparentWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
    
    def paintEvent(self, event=None):
        pix = QPixmap(self.size())
        print(self.size())
        painter = QPainter()
        painter.begin(pix)
        painter.drawPixmap(self.rect(), QPixmap('stein.jpg'))
        painter.end()
        bmp= QBitmap(self.size())
        bmp.fill()
        painter.begin(bmp)
        painter.setPen(QPen(Qt.color1))
        painter.setFont(QFont('Times', 75, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, 'Draw Text')
        painter.end()

        pix.setMask(bmp)
        painter.begin(self)
        painter.drawPixmap(self.rect(), pix)
        painter.end()


class Window(QLabel):
    def __init__(self, parent= None):
        super().__init__(parent, Qt.FramelessWindowHint | Qt.Window)




if __name__ == '__main__':
    app = QApplication([])
    #w = TransparentWidget()
    #w.show()
    win = Window()
    pix = QPixmap('unixoids.png')
    win.setPixmap(pix)
    #win.setMask(pix.mask())
    win.show()
    sys.exit(app.exec_())





