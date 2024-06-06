import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from decomposition import Ui_Decomposition
from graphviz import Graph
from G_coloring_BT import Graph_coloring
from Graph_draw import Draw_Graph
from Alt_max_ind_set import find_maximal_independent_set, filter_edges_by_max_ind_set , Draw_Max_Graph

class Ui_Window01(object):
    def openWindow(self):
        try:
            self.window = QtWidgets.QMainWindow()
            self.ui = Ui_Decomposition(self.get_data())
            self.ui.setupUi(self.window)
            self.window.show()
        except Exception as e:
            print("Invalid input:", str(e))


    def btn_refresh(self):
        self.get_data()
        self.graph_show()

    def get_data(self):
        user_input = self.textEdit.toPlainText()
        print('user input is', user_input)
        user_input = user_input.replace(" ", "")
        edge_list = user_input.split(";")
        #print(edge_list)
        return edge_list

    def graph_show(self):
        import time
        # start_time = time.time()

        edges = self.get_data()

        newedges = []
        for edge in edges:
            temp = edge.strip("(").strip(")")
            newedges.append(temp)

        edges = newedges
        try:
            G = Graph("graph")
            G.attr("node", shape="circle")

            # Extract vertices from edges
            vertices = set()
            for edge in edges:
                u, v = edge.split(",")
                vertices.add(u)
                vertices.add(v)

            # Add vertices to the graph
            for vertex in vertices:
                G.node(vertex)

            # Add edges to the graph
            for edge in edges:
                u, v = edge.split(",")
                G.edge(u, v)

            G.format = 'png'
            G.render('graph', view=False)
            # Draw_Graph(edges, 'graph')

            pixmap = QPixmap('graph.png')
            #self.scene.clear() # DONT REMOVE THE GRAPH from the window
            self.scene.addPixmap(pixmap)
        except Exception as e:
            print("Invalid String:", str(e))
        # end_time = time.time()
        # self.time_taken = round(end_time - start_time, 2)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(981, 558)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Create a vertical layout for the left side
        self.leftLayout = QtWidgets.QVBoxLayout()
        self.leftLayout.setObjectName("leftLayout")
        self.leftLayout.addSpacing(10)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.leftLayout.addWidget(self.textEdit)  # Add the text edit to the left layout
        self.textEdit.setPlaceholderText(
            "The input should look like this (a,b);(b,c);(c,a) etc")  # Set the placeholder text

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(15, -5, 77, 23))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.refresh = QtWidgets.QPushButton(self.centralwidget)
        self.refresh.setObjectName("refresh")
        self.refresh.clicked.connect(self.graph_show)  # Refresh Button
        self.leftLayout.addWidget(self.refresh)

        self.next = QtWidgets.QPushButton(self.centralwidget)
        self.next.setObjectName("next")
        self.next.clicked.connect(self.openWindow)
        self.leftLayout.addWidget(self.next)

        self.color_bt = QtWidgets.QPushButton(self.centralwidget)
        self.color_bt.setObjectName("color_bt")
        self.color_bt.clicked.connect(self.color_bt_graph)  # Color BT Button
        self.leftLayout.addWidget(self.color_bt)

        self.max_set = QtWidgets.QPushButton(self.centralwidget)
        self.max_set.setObjectName("color_bt")
        self.max_set.clicked.connect(self.generate_max_ind_set)  # Color BT Button
        self.leftLayout.addWidget(self.max_set)

        # self.leftLayout.addStretch() # to make the left part as the right part(size)

        self.horizontalLayout.addLayout(self.leftLayout)

        # Add the graphics view to the right side
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)
        self.scene = QtWidgets.QGraphicsScene(self.centralwidget)  # important lines
        self.graphicsView.setScene(self.scene)


        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def generate_max_ind_set(self):
        edges = self.get_data()
       # print(edges)
        newedges = []
        for edge in edges:
            temp = edge.strip("(").strip(")")
            newedges.append(temp)

        edges = newedges

        self.edges = edges

        try:
            start = time.time()
            # Generate Maximal Independent Set
            max_ind_set = find_maximal_independent_set(edges)
            # Create a new graph with only the edges in the Maximal Independent Set
            new_edges = filter_edges_by_max_ind_set(edges, max_ind_set)
            # Color the graph
            graph = Graph_coloring(new_edges)
            graph.color_bt()
            Draw_Max_Graph(edges, 'graph', max_ind_set)
            pixmap = QPixmap("graph.gy.png")
            end = time.time()
            self.time_taken = str(round(end - start, 2))

            self.max_ind_set_window = QtWidgets.QMainWindow()
            self.max_ind_set_window.setWindowTitle("Maximum Independent Set")
            self.max_ind_set_window.setGeometry(100, 100, 800, 600)

            self.central_widget = QtWidgets.QWidget(self.max_ind_set_window)
            self.max_ind_set_window.setCentralWidget(self.central_widget)

            self.layout = QtWidgets.QVBoxLayout(self.central_widget)

            self.max_ind_set_graphicsView = QtWidgets.QGraphicsView(self.central_widget)
            self.max_ind_set_graphicsView.setGeometry(
                QtCore.QRect(10, 10, 780, 540))
            self.max_ind_set_scene = QtWidgets.QGraphicsScene(self.central_widget)
            self.max_ind_set_graphicsView.setScene(self.max_ind_set_scene)

            self.max_ind_set_scene.clear()
            self.max_ind_set_scene.addPixmap(pixmap)

            self.layout.addWidget(self.max_ind_set_graphicsView)

            self.time_taken_label = QtWidgets.QLabel(self.central_widget)
            self.time_taken_label.setGeometry(
                QtCore.QRect(20, 550, 200, 27))

            self.time_taken_label.setText(f"Max ind set takes time: {self.time_taken} seconds")
            self.layout.addWidget(self.time_taken_label)

            self.max_ind_set_label = QtWidgets.QLabel(self.central_widget)
            self.max_ind_set_label.setGeometry(
                QtCore.QRect(20, 570, 500, 27))  # Position the label next to the time taken label
            max_ind_set_text = ", ".join(max_ind_set)
            self.max_ind_set_label.setText(f"Maximal Independent Set: [{max_ind_set_text}]")
            self.layout.addWidget(self.max_ind_set_label)

            self.exit_button = QtWidgets.QPushButton("Exit", self.central_widget)
            # self.exit_button.setGeometry(QtCore.QRect(690, 560, 80, 27))
            self.exit_button.setFixedSize(280, 40)
            self.exit_button.clicked.connect(self.max_ind_set_window.close)
            self.layout.addWidget(self.exit_button, alignment=QtCore.Qt.AlignRight)

            self.max_ind_set_window.show()

        except Exception as e:
            print("Maximal Independent Set generation failed:", str(e))

    def color_bt_graph(self):
        edges = self.get_data()
        newedges = []
        for edge in edges:
            # print('edge before strip', edge)
            temp = edge.strip("(").strip(")")
            newedges.append(temp)
        edges = newedges

        self.edges = edges
        try:
            start = time.time()
            graph = Graph_coloring(newedges)
            graph.color_bt()
            colored_graph = graph.create_colored_graph()
            Draw_Graph(edges, 'graph', colored_graph)
            end = time.time()

            self.time_taken = str(round(end - start, 2))
            pixmap = QPixmap("graph.gy.png")

            self.color_bt_window = QtWidgets.QMainWindow()
            self.color_bt_window.setWindowTitle("Coloring With Backtracking")
            self.color_bt_window.setGeometry(100, 100, 800, 600)

            self.color_bt_centralwidget = QtWidgets.QWidget(self.color_bt_window)
            self.color_bt_window.setCentralWidget(self.color_bt_centralwidget)

            self.color_bt_layout = QtWidgets.QVBoxLayout(self.color_bt_centralwidget)

            self.color_bt_graphicsView = QtWidgets.QGraphicsView(self.color_bt_centralwidget)
            self.color_bt_graphicsView.setObjectName("color_bt_graphicsView")
            self.color_bt_layout.addWidget(self.color_bt_graphicsView)

            self.color_bt_scene = QtWidgets.QGraphicsScene(self.color_bt_window)
            self.color_bt_graphicsView.setScene(self.color_bt_scene)

            self.color_bt_scene.clear()
            self.color_bt_scene.addPixmap(pixmap)

            self.time_taken_label = QtWidgets.QLabel(self.color_bt_centralwidget)
            self.time_taken_label.setText(f"Coloring with BT Takes time: {self.time_taken}s")
            self.color_bt_layout.addWidget(self.time_taken_label)

            self.colors_used_label = QtWidgets.QLabel(self.color_bt_centralwidget)
            num_colors_used = max(graph.get_colors().values()) + 1
            self.colors_used_label.setText(f"Number of Colors Used: {num_colors_used}")
            self.color_bt_layout.addWidget(self.colors_used_label)

            self.exit_button = QtWidgets.QPushButton("Exit", self.color_bt_centralwidget)
            self.exit_button.clicked.connect(self.color_bt_window.close)
            self.exit_button.setFixedSize(280, 40)
            # self.color_bt_layout.addStretch(1)
            self.color_bt_layout.addWidget(self.exit_button, alignment=QtCore.Qt.AlignRight)

            self.color_bt_centralwidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            self.color_bt_graphicsView.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

            self.color_bt_window.show()

        except Exception as e:
            print("Graph coloring failed:", str(e))


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.refresh.setText(_translate("MainWindow", "Refresh"))
        self.next.setText(_translate("MainWindow", "Tree_Decomposition"))
        self.label.setText(_translate("MainWindow", "Edges : "))
        self.color_bt.setText(_translate("MainWindow", "Coloring with Backtracking"))
        self.max_set.setText(_translate("MainWindow", "Maximum Independent Set with Backtracking"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Window01()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
