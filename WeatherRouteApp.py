import sys
import datetime
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import (QApplication, QLineEdit, QMainWindow, QWidget, QLabel,
                             QDateEdit, QPushButton, QComboBox, QFormLayout, QGridLayout, QMessageBox, QDialog)


class LoginWindow(QDialog):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)

        self.setWindowTitle("Login Form")
        self.resize(500, 200)

        layout = QGridLayout()
        self.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0.091, y1:0.101636, x2:0.991379,y2:0.977, stop:0 rgba(209, 107, 165, 255), stop:1 rgba(255,255,255,255));")

        username_label = QLabel("Username:")
        username_label.setStyleSheet("font-size: 12pt; \
                                      background-color: rgba(0,0,0,0%); \
                                      color: white;")

        self.username_lineEdit = QLineEdit()
        self.username_lineEdit.setStyleSheet(
            "font-size: 12pt; background-color: rgba(0,0,0,0%);")
        self.username_lineEdit.setPlaceholderText("Please enter username")
        layout.addWidget(username_label, 0, 0)
        layout.addWidget(self.username_lineEdit, 0, 1)

        password_label = QLabel("Password:")
        password_label.setStyleSheet("font-size: 12pt;\
                                      background-color: rgba(0,0,0,0%);")

        self.password_lineEdit = QLineEdit()
        self.password_lineEdit.setStyleSheet(
            "font-size: 12pt; background-color: rgba(0,0,0,0%);")
        self.password_lineEdit.setPlaceholderText("Please enter password")
        layout.addWidget(password_label, 1, 0)
        layout.addWidget(self.password_lineEdit, 1, 1)

        self.login_QPushButton = QPushButton()
        self.login_QPushButton.setText("Login")
        self.login_QPushButton.setStyleSheet(
            "QPushButton"
            "{"
            "font-size: 14pt; \
                                border-style: solid; \
                                border-radius: 10px; \
                                background-color: rgb(145, 255, 246)"
            "}"
            "QPushButton::pressed"
            "{"
            "font-size: 14pt; \
                                border-style: solid; \
                                border-radius: 10px; \
                                background-color: rgb(0, 217, 199)"
            "}"
        )
        self.login_QPushButton.clicked.connect(self.handle_login)
        layout.addWidget(self.login_QPushButton, 2, 1)

        self.setLayout(layout)

    def handle_login(self):

        if self.username_lineEdit.text() == "" and self.password_lineEdit.text() == "":
            self.accept()
        else:
            QMessageBox.warning(
                self, "Error", "Invalid Credentials. Please Try again.")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Weather On Route')
        self.resize(800, 600)
        self.layout = QFormLayout()
        self.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0.091, y1:0.101636, x2:0.991379,y2:0.977, stop:0 rgba(209, 107, 165, 255), stop:1 rgba(255,255,255,255));")

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
        self.origin_label.setStyleSheet(
            "font-size: 14pt; background-color: rgba(0,0,0,0%);")
        self.layout.addRow(self.origin_label, self.origin)

        self.destination_label = QLabel("Destination:")
        self.destination_label.setStyleSheet(
            "font-size: 14pt; background-color: rgba(0,0,0,0%);")
        self.layout.addRow(self.destination_label, self.destination)

        self.weather_type_label = QLabel("Weather Type:")
        self.weather_type_label.setStyleSheet(
            "font-size: 14pt; background-color: rgba(0,0,0,0%);")
        self.layout.addRow(self.weather_type_label, self.weather_type)

        self.travel_date_label = QLabel("Date of Travel:")
        self.travel_date_label.setStyleSheet(
            "font-size: 14pt; background-color: rgba(0,0,0,0%);")
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
                                background-color: rgb(145, 255, 246)"
            "}"
            "QPushButton::pressed"
            "{"
            "font-size: 14pt; \
                                border-style: solid; \
                                border-radius: 10px; \
                                border-width: 1.5px; \
                                border-color: white; \
                                background-color: rgb(0, 217, 199)"
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

    login = LoginWindow()

    if login.exec_() == QDialog.Accepted:
        print("hi")
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec_())
