from PyQt5 import QtCore, QtGui, QtWidgets
import time
from dec1 import nice_tree
from coloring import Ui_Coloring
from max_set_gui import Ui_Max


class Ui_Nice(object):
    def __init__(self):
        pass

    def __init__(self, data, o_edges):
        self.data = data
        self.edges = None
        self.o_edges = o_edges

    def openWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Coloring(self.o_edges, self.edges, self.node)
        # self.get_edges()
        self.ui.setupUi(self.window)
        self.window.show()

    def openMaxWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Max(self.edges, self.o_edges)
        # self.get_edges()
        self.ui.setupUi(self.window)
        self.window.show()


    # new response window for ntd
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(913, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.layout.setContentsMargins(10, 10, 10, 10)

        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.layout.addWidget(self.graphicsView)

        self.scene = QtWidgets.QGraphicsScene(self.centralwidget)
        self.graphicsView.setScene(self.scene)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 560, 280, 25))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.layout.addWidget(self.label)

        self.button_layout = QtWidgets.QHBoxLayout()

        self.color_button = QtWidgets.QPushButton("Color")
        self.color_button.setObjectName("color")
        self.color_button.clicked.connect(self.openWindow)
        self.button_layout.addWidget(self.color_button)

        self.max_button = QtWidgets.QPushButton("Max")
        self.max_button.setObjectName("max")
        self.max_button.clicked.connect(self.openMaxWindow)
        self.button_layout.addWidget(self.max_button)

        self.exit_button = QtWidgets.QPushButton("Exit")
        self.exit_button.setObjectName("exit")
        self.exit_button.clicked.connect(lambda: MainWindow.close())
        self.button_layout.addWidget(self.exit_button)

        self.layout.addLayout(self.button_layout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.graph_show()

    def close_window(self, MainWindow):
        MainWindow.close()

    def graph_show(self):
        from Graph_draw import Draw_Graph
        from PyQt5.QtGui import QPixmap

        _translate = QtCore.QCoreApplication.translate

        start = time.time()
        node, edges = nice_tree(self.data)
        self.edges = edges
        self.node = node
        Draw_Graph(edges, 'nice', node=node)
        end = time.time()
        self.label.setText(
            _translate(
                "MainWindow",
                "Nice TD takes time : " + str(round(end - start, 2)) + "s",
            )
        )
        pixmap = QPixmap("nice.gy.png")
        self.scene.addPixmap(pixmap)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Nice Tree Decomposition"))
        self.label.setText(_translate("MainWindow", "Nice TD takes time :"))
        self.exit_button.setText(_translate("MainWindow", "Exit"))
        self.color_button.setText(_translate("MainWindow", "n Color"))
        self.max_button.setText(_translate("MainWindow", "Maximal  independent set"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Nice()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
