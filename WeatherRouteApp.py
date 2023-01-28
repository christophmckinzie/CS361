import sys
from PyQt5.QtGui import QPixmap, QTextCursor
from PyQt5.QtCore import QSize, Qt, QRect, QDate, QDateTime, QUrl
from PyQt5.QtWidgets import (
    QApplication,
    QLineEdit,
    QMainWindow,
    QWidget,
    QLabel,
    QDateEdit,
    QPushButton,
    QComboBox,
    QFormLayout,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Weather On Route')
        self.resize(800, 600)
        self.layout = QFormLayout()  # layout object
        self.setStyleSheet("background-color: white")

        self.origin = QLineEdit()
        self.origin.setStyleSheet("background: white;")
        self.origin.setPlaceholderText("Starting address here")

        self.destination = QLineEdit()
        self.destination.setPlaceholderText("Ending address here")

        self.weather_type = QComboBox()
        self.weather_type.addItems(['Snow', 'Rain', 'Clouds'])

        self.date = QDateEdit()

        self.number_of_checks = QLineEdit()
        self.number_of_checks.setPlaceholderText(
            "Number of locations to check for weather")

        self.qlabel_origin = QLabel("Origin")
        self.layout.addRow(self.qlabel_origin, self.origin)

        self.qlabel_destination = QLabel("Destination")
        self.layout.addRow(self.qlabel_destination, self.destination)

        self.weather_type_label = QLabel("Weather Type")
        self.layout.addRow(self.weather_type_label, self.weather_type)

        self.travel_date_label = QLabel("Date of Travel")
        self.layout.addRow(self.travel_date_label, self.date)

        # adding pushbutton
        self.pushButton = QPushButton()
        self.pushButton.setText("Produce Map")
        self.pushButton.setStyleSheet("font-size: 10pt; \
                                border-style: solid; \
                                border-radius: 15px; \
                                border-width: 1.5px; \
                                border-color: rgb(20, 173, 173);")
        self.pushButton.setGeometry(QRect(200, 150, 93, 28))

        # adding signal and slot
        self.pushButton.clicked.connect(self.find_route_and_weather)
        self.layout.addWidget(self.pushButton)

        # add layout to widget and set as central widget
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def find_route_and_weather(self):
        print("Function to find route will go here.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
