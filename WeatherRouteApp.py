import sys
import datetime
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
        self.layout = QFormLayout()

        self.origin = QLineEdit()
        self.origin.setPlaceholderText("Starting address here")
        self.origin.setStyleSheet("font-size: 14pt; \
                                border-style: solid; \
                                border-radius: 10px; \
                                border-width: 1.5px; \
                                border-color: white;")

        self.destination = QLineEdit()
        self.destination.setPlaceholderText("Ending address here")
        self.destination.setStyleSheet("font-size: 14pt; \
                                border-style: solid; \
                                border-radius: 10px; \
                                border-width: 1.5px; \
                                border-color: white;")

        self.weather_type = QComboBox()
        self.weather_type.addItems(['Snow', 'Rain', 'Clouds'])
        self.weather_type.setStyleSheet("font-size: 14pt; \
                                border-style: solid; \
                                border-radius: 10px; \
                                border-width: 1.5px; \
                                border-color: white;")

        self.date = QDateEdit()
        self.date.setDate(datetime.date.today())
        self.date.setStyleSheet("font-size: 14pt; \
                                border-style: solid; \
                                border-radius: 10px; \
                                border-width: 1.5px; \
                                border-color: white;")

        self.number_of_checks = QLineEdit()
        self.number_of_checks.setPlaceholderText(
            "Number of locations to check for weather")
        self.number_of_checks.setStyleSheet("font-size: 14pt; \
                                border-style: solid; \
                                border-radius: 10px; \
                                border-width: 1.5px; \
                                border-color: white;")

        self.origin_label = QLabel("Origin:")
        self.origin_label.setStyleSheet("font-size: 14pt")
        self.layout.addRow(self.origin_label, self.origin)

        self.destination_label = QLabel("Destination:")
        self.destination_label.setStyleSheet("font-size: 14pt")
        self.layout.addRow(self.destination_label, self.destination)

        self.weather_type_label = QLabel("Weather Type:")
        self.weather_type_label.setStyleSheet("font-size: 14pt")
        self.layout.addRow(self.weather_type_label, self.weather_type)

        self.travel_date_label = QLabel("Date of Travel:")
        self.travel_date_label.setStyleSheet("font-size: 14pt")
        self.layout.addRow(self.travel_date_label, self.date)

        # adding pushbutton
        self.pushButton = QPushButton()
        self.pushButton.setText("Produce Map")
        self.pushButton.setStyleSheet(
            "QPushButton"
            "{"
            "font-size: 14pt; \
                                border-style: solid; \
                                border-radius: 10px; \
                                border-width: 1.5px; \
                                border-color: white; \
                                background-color: rgb(20, 173, 173)"
            "}"
            "QPushButton::pressed"
            "{"
            "font-size: 14pt; \
                                border-style: solid; \
                                border-radius: 10px; \
                                border-width: 1.5px; \
                                border-color: white; \
                                background-color: rgb(133, 230, 230)"
            "}"
        )
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
