from PyQt5 import QtCore, QtGui, QtWidgets
from dec1 import max_independent_set
from Graph_draw import Draw_Graph
from PyQt5.QtGui import QPixmap
import time


class Ui_Max(object):
    def __init__(self, data, o):
        self.data = data
        self.o = o
        self.edges = None

    # response window
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(913, 453)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.layout.setContentsMargins(10, 10, 10, 10)

        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.layout.addWidget(self.graphicsView)

        self.scene = QtWidgets.QGraphicsScene(self.centralwidget)  # important lines
        self.graphicsView.setScene(self.scene)

        font = QtGui.QFont()
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 400, 280, 25))
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.layout.addWidget(self.label)


        self.label1 = QtWidgets.QLabel(self.centralwidget)
        self.label1.setGeometry(QtCore.QRect(50, 370, 350, 25))
        font.setPointSize(8)
        self.label1.setFont(font)
        self.label1.setObjectName("label1")
        self.layout.addWidget(self.label1)


        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(50, 430, 350, 25))
        self.label2.setFont(font)
        self.label2.setObjectName("label")
        self.layout.addWidget(self.label2)

        self.exit = QtWidgets.QPushButton(self.centralwidget)
        self.exit.setObjectName("exit")
        self.exit.setFixedSize(280, 40)  # Adjust the width and height as desired
        self.exit.clicked.connect(lambda: MainWindow.close())
        self.layout.addWidget(self.exit, alignment=QtCore.Qt.AlignRight)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.graph_show()


    def close_window(self, MainWindow):
        MainWindow.close()

    def graph_show(self):

        _translate = QtCore.QCoreApplication.translate

        start = time.time()
        s, val = max_independent_set(self.data, self.o)
        Draw_Graph(self.o, 'decomposition', max_set=s)
        end = time.time()
        pixmap = QPixmap("decomposition.gy.png")
        self.scene.addPixmap(pixmap)

        self.label.setText(
            _translate(
                "MainWindow",
                "Max Value : " + str(val),
            )
        )
        self.label1.setText(
            _translate(
                "MainWindow",
                "Max Independent Set : " + str(s),
            )
        )
        self.label2.setText(
            _translate(
                "MainWindow",
                "Max ind set takes time : " + str(round(end - start, 2)) + "s",
            )
        )

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Maximum Independent Set"))
        self.exit.setText(_translate("MainWindow", "Exit"))

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

