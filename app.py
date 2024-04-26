import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QAction, QToolBar, QVBoxLayout, QWidget, QCheckBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class FileInputReader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excel File Reader")
        self.setGeometry(100, 100, 800, 600)

        self.label = QLabel("No file selected.", self)
        self.label.setGeometry(20, 20, 560, 30)

        # Create toolbar
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        # Create open file action and add it to the toolbar
        open_action = QAction("Open Excel File", self)
        open_action.triggered.connect(self.open_file)
        self.toolbar.addAction(open_action)

        # Create a widget to hold the graph
        self.graph_widget = GraphWidget()

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xls *.xlsx)")
        if file_path:
            try:
                df = pd.read_excel(file_path, index_col=0)
                self.graph_widget.plot_data(df)  # Pass data to the graph widget
                self.graph_widget.show()  # Show the graph widget
                self.label.setText("Excel file loaded: " + file_path)
            except Exception as e:
                self.label.setText("Error loading Excel file: " + str(e))
        else:
            self.label.setText("No file selected.")

class GraphWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Graph Window")
        self.setGeometry(100, 100, 800, 600)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        # Create a widget to hold the checkboxes
        self.checkbox_widget = QWidget()
        self.checkbox_layout = QVBoxLayout()
        self.checkbox_widget.setLayout(self.checkbox_layout)
        layout.addWidget(self.checkbox_widget)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Dictionary to store checkbox objects
        self.checkboxes = {}

    def plot_data(self, data):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        self.lines = []  # Store line objects for each curve

        for col in data.columns:
            line, = ax.plot(data.index, data[col], label=str(col))
            self.lines.append(line)
            checkbox = QCheckBox(str(col))
            checkbox.setChecked(True)  # Checkbox is checked by default
            checkbox.stateChanged.connect(lambda state, line=line: self.toggle_visibility(line, state))
            self.checkbox_layout.addWidget(checkbox)
            self.checkboxes[col] = checkbox

        ax.set_xlabel("Timestamp")
        ax.set_ylabel("Value")
        ax.set_title("Data")
        ax.legend()
        ax.grid(True)
        ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d %H:%M:%S'))
        self.canvas.draw()

    def toggle_visibility(self, line, state):
        line.set_visible(state)
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileInputReader()
    window.show()
    sys.exit(app.exec_())
