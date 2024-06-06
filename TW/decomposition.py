from PyQt5 import QtCore, QtGui, QtWidgets
import time
from nice import Ui_Nice
from Graph_draw import Draw_Graph
from PyQt5.QtGui import QPixmap
from dec1 import decomposition
from validation import TreeDecomposition

class Ui_Decomposition(object):
    def __init__(self, data):
        self.data = data
        self.edges = None

    def openWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Nice(self.edges, self.data)
        self.ui.setupUi(self.window)
        self.window.show()


    # new response window
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

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.scene = QtWidgets.QGraphicsScene(self.centralwidget)  # important lines
        self.label1 = QtWidgets.QLabel(self.centralwidget)
        self.graphicsView.setScene(self.scene)
        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.label)

        # Create a QHBoxLayout for the buttons
        self.button_layout = QtWidgets.QHBoxLayout()

        self.nice = QtWidgets.QPushButton(self.centralwidget)
        self.nice.setObjectName("nice")
        self.nice.clicked.connect(self.openWindow)
        self.button_layout.addWidget(self.nice)

        self.exit = QtWidgets.QPushButton(self.centralwidget)
        self.exit.setObjectName("exit")
        self.exit.clicked.connect(lambda: MainWindow.close())
        self.button_layout.addWidget(self.exit)

        # Add the button layout to the main layout
        self.layout.addLayout(self.button_layout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.graph_show()


    def close_window(self, MainWindow):
        MainWindow.close()

    def graph_show(self):


        _translate = QtCore.QCoreApplication.translate

        start = time.time()
        width, edges, self.edges = decomposition(self.data)
        self.edges = edges
        Draw_Graph(edges, 'decomposition')
        end = time.time()

        self.label.setText(
            _translate(
                "MainWindow",
                "Graph decomposition takes time : " + str(round(end - start, 2)) + "s",
            )
        )
        self.label1.setText(
            _translate(
                "MainWindow",
                "Tree width of Graph g is : " + str(width),
            )
        )
        pixmap = QPixmap("decomposition.gy.png")
        self.scene.addPixmap(pixmap)
        v = TreeDecomposition(self.data, edges)
        print(v.is_valid())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Tree Decomposition"))
        self.label.setText(_translate("MainWindow", "Graph decomposition takes time :"))
        self.label1.setText(_translate("MainWindow", "Tree width of Graph g is :"))
        self.nice.setText(_translate("MainWindow", "Nice Tree Decomposition"))
        self.exit.setText(_translate("MainWindow", "Exit"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Decomposition()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
