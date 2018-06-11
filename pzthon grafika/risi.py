#Vaje za uporabo QPainter, ki jih bom uporabil pri CostumDelegate v MVP
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
import chess_pieces
class ChessPiece(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
    def paintEvent(self, event=None):
        painter = QPainter(self)
        renderer = QSvgRenderer(":/white_king")
        renderer.render(painter)

class MyLabel(QLabel):
    def __init__(self, caption, paintFunc,
            paint_script="", parent = None):
        self.paintFunc = paintFunc
        self.paint_script = paint_script
        super().__init__(caption, parent)
        self.color = Qt.green
        self.text = "ppainting"
        self.slikar = None 
        self.setFixedHeight(400)

    #def paintEvent(self, event = None):

        #if self.paintFunc == 1:
        #    self.paintText(event)
        #elif self.paintFunc ==2:
        #    self.paintCommands(event)

    def paintText(self, event=None):
        painter = QPainter(self)
        painter.setPen(self.color)
        painter.setFont(QFont("Arial", 30))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text)
        painter.drawLine(0,10,568, 10)

    def paintCommands(self, event=None):
        try:
            eval(self.paint_script )
        except:
            pass

    def paintPie(self, event=None):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing,True)
        brush = QBrush(Qt.green, Qt.DiagCrossPattern)
        painter.setBrush(brush)
        pen = QPen(Qt.blue)
        pen.setWidth(8)
        painter.setPen(pen)
        painter.drawPie(self.rect(),0*16, -135*16)



class Picasso(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        # self.cavnas = MyLabel("Platno")
        self.pixList = []
        self.counter = 1
        self.cavnas = MyLabel("",1) 
        #self.cavnas = QLabel("Platno z arisanje")
        self.clicks = 0
        self.pbDraw = QPushButton("Draw")
        self.old_pic_layout = QHBoxLayout()
        self.rbGroup = QGroupBox("Izberi lik za risanje")
        self.radioLine = QRadioButton("Line")
        self.radioRectangle = QRadioButton("Rectangle")
        self.radioEllipse = QRadioButton("Ellipse")
        self.radioPicture = QRadioButton("Picture")
        self.radioLine.setChecked(True)
        vbox = QVBoxLayout()
        vbox.addWidget(self.radioLine)
        vbox.addWidget(self.radioRectangle)
        vbox.addWidget(self.radioEllipse)
        vbox.addWidget(self.radioPicture)
        vbox.addStretch(1)
        self.rbGroup.setLayout(vbox)        
        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(self.cavnas,0, 0)
        self.grid_layout.addWidget(self.rbGroup,1, 0)
        self.grid_layout.addWidget(self.pbDraw, 2, 0)
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.old_pic_layout)
        main_layout.addLayout(self.grid_layout)
        self.setLayout(main_layout)
        self.setGeometry(200,200,600,700)
        self.pbDraw.clicked.connect(self.drawOnLabel)
        self.pbDraw.setIcon(QIcon(":/white_bishop"))
    
    def drawOnLabel(self):
        #I have no idea, why I have to make here two calls
        #but it works only if I do so
        self.draw(False)
        self.draw(True)

    def draw(self, draw=True):
        w = self.cavnas.rect().width()
        h = self.cavnas.height()
        pix = QPixmap(w,h)
        self.pixList.append(pix)
        painter = QPainter(pix)
        painter.fillRect(self.cavnas.rect(),QBrush(Qt.white))
        painter.setRenderHint(QPainter.Antialiasing,True)
        brush = QBrush(Qt.green, Qt.DiagCrossPattern)
        painter.setBrush(brush)
        pen = QPen(Qt.blue)
        pen.setWidth(8)
        painter.setPen(pen)
        if not draw:  #Ce tega ni, potem mi like riše enega prek drugega
            return
        if self.radioLine.isChecked():
            painter.drawLine(10, 10, w-10, h-10)
            self.cavnas.setPixmap(pix)
        elif self.radioRectangle.isChecked():
            painter.drawRect(20,20,w-40, h-40)
            self.cavnas.setPixmap(pix)
        elif self.radioEllipse.isChecked():
            painter.drawEllipse(QPoint(w/2,h/2),100,100)
            self.cavnas.setPixmap(pix)
        elif self.radioPicture.isChecked():
            painter.drawPixmap(0, 0, w, h, QPixmap("unixoids.png"))
            self.cavnas.setPixmap(pix)
    
    def drawImage(self):
        img = QImage(self.cavnas.rect(), QImage.Format_ARGB32_Premultiplied)
        painter = QPainter()
        painter.begin(img)
        # Metoda initFrom inicializira QPainter s takimi nastavitvami z widgeta kot so barva podlage, stil svincnika, pisava in podobno.
        painter.initFrom(self.cavnas)
        painter.setRenderHint(QPainter.Antialiasing,True)
        paitner.eraseRect(self.cavnas.rect())
        painter.drawEllipse(0, 0, self.cavnas.width(), self.cavnas.height())
        painter.end()

        painter.begin(self.cavnas)
        painter.drawImage(0, 0, img)
        painter.end()

    def drawPixmap(self):
        painter = QPainter(self)
        pixmap = QPixmap('forest.jpg')
        painter.drawPixmap(0, 0, pixmap )





if __name__ == "__main__":
    app = QApplication(sys.argv)
    drawForm = Picasso()
    drawForm.show()
    sys.exit(app.exec_())
