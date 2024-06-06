from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import time
from dec1 import coloring
from Graph_draw import Draw_Graph
from PyQt5.QtGui import QPixmap
import sys

class Ui_Coloring(object):
    def __init__(self, data=None, nice=None, node=None):
        self.data = data
        self.nice = nice
        self.node = node
        self.num = None
        print('\n',self.data, '\n')
        print(self.nice)

    def get_num(self):
        num = self.textEdit.toPlainText()
        try:
            num = int(num)
            # if num > 16:
            #     QMessageBox.critical(None, "Invalid input", "Number should not exceed 16")
            #     return None
        except ValueError:
            QMessageBox.critical(None, "Invalid input", "Please enter a valid integer")
            return None
        return num


    # new response window
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(713, 453)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.layout.setContentsMargins(10, 10, 10, 10)

        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.layout.addWidget(self.graphicsView)

        self.scene = QtWidgets.QGraphicsScene(self.centralwidget)  # important lines
        self.graphicsView.setScene(self.scene)

        self.horizontalLayout = QtWidgets.QHBoxLayout()

        self.label1 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label1.setFont(font)
        self.label1.setObjectName("label1")

        self.horizontalLayout.addSpacing(0)
        self.horizontalLayout.addWidget(self.label1)

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setMaximumSize(QtCore.QSize(95, 30))
        self.horizontalLayout.addWidget(self.textEdit)
        self.textEdit.setPlaceholderText("2 or 3 or....")
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout.addSpacing(700)
        self.horizontalLayout.addStretch(1)

        self.layout.addLayout(self.horizontalLayout)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 370, 280, 25))
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.layout.addWidget(self.label)

        self.button_layout = QtWidgets.QHBoxLayout()

        self.refresh = QtWidgets.QPushButton(self.centralwidget)
        self.refresh.setObjectName("refresh")
        self.refresh.clicked.connect(self.graph_show)
        self.button_layout.addWidget(self.refresh)

        self.exit = QtWidgets.QPushButton(self.centralwidget)
        self.exit.setObjectName("exit")
        self.exit.clicked.connect(lambda: MainWindow.close())
        self.button_layout.addWidget(self.exit)

        self.layout.addLayout(self.button_layout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    #     end res


    def close_window(self, MainWindow):
        MainWindow.close()

    def graph_show(self):

        _translate = QtCore.QCoreApplication.translate

        start = time.time()
        print('\n',self.data, '\n')
        self.num = self.get_num()
        if self.num:
            colors = coloring(self.data, self.nice, self.node, self.num)
            print('\n edges',self.data, '\n')
            Draw_Graph(self.data, 'graph', colors)
            end = time.time()
            if colors:
                self.label.setText(
                    _translate(
                        "MainWindow",
                        "Coloring takes time : " + str(round(end - start, 2)) + "s",
                    )
                )
            else:
                self.label.setText(
                    _translate(
                        "MainWindow",
                        "Graph can't be colored with given number of colors",
                    )
                )

            pixmap = QPixmap("graph.gy.png")
            self.scene.addPixmap(pixmap)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Coloring with NTD"))
        self.label.setText(_translate("MainWindow", "Coloring takes time :"))
        self.refresh.setText(_translate("MainWindow", "Show"))
        self.exit.setText(_translate("MainWindow", "Exit"))
        self.label1.setText(_translate("MainWindow", "Number of Colors :"))

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Coloring()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
