import Weather
import sys
import io
import datetime
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import (QApplication, QLineEdit, QMainWindow, QWidget, QLabel,
                             QDateEdit, QPushButton, QComboBox, QFormLayout, QDialog, QMenu, QVBoxLayout, QMessageBox)
from PyQt5.QtWebEngineWidgets import QWebEngineView


class ApplicationInformation(QDialog):
    def __init__(self):
        super(ApplicationInformation, self).__init__()

        self.central_widget = QWidget(self)
        self.setWindowTitle("Application Description")
        self.resize(800, 200)
        self.setMaximumWidth(800)
        self.layout = QVBoxLayout()

        description_label = QLabel("Welcome to my CS361 portfolio project! This applications name is Weather Routing and its purpose is to find weather along a driving route. You will be asked to provide a starting and ending city/address/location, choose the type of weather to search for (three options provided) and your travel date (1-4 days from current day). \n The driving route is provided using Google Maps Directions API. The forecast data is provided using a microservice created by my partner, Jared Chang, which calls OpenWeatherMap's 5 Day / 3 Hour Forecast.\nLimitations: 1) Addresses must be able to be ")
        description_label.setStyleSheet("font-size: 13pt;")
        description_label.setWordWrap(True)
        self.layout.addWidget(description_label, Qt.AlignCenter)

        self.open_mainwindow_button = QPushButton()
        self.open_mainwindow_button.setText("Continue")
        self.open_mainwindow_button.setStyleSheet(
            "QPushButton"
            "{"
            "font-size: 14pt; border-radius: 10px; background-color: rgba(145, 255, 246, 190); background-color: qlineargradient(spread:pad, x1:0.091, y1:0.101636, x2:0.991379,y2:0.977, stop:0 rgba(28, 76, 173, 190), stop:1 rgba(122, 166, 255,190));"
            "}"
            "QPushButton::hover"
            "{"
            "font-size: 14pt; border-radius: 10px;background-color: rgba(145, 255, 246,190); background-color: qlineargradient(spread:pad, x1:0.091, y1:0.101636, x2:0.991379,y2:0.977, stop:0 rgba(10, 50, 133, 190), stop:1 rgba(122, 166, 255,190));"
            "}"
            "QPushButton::pressed"
            "{"
            "font-size: 14pt; border-radius: 10px; background-color: rgba(0, 217, 199, 190)"
            "}"
        )
        self.open_mainwindow_button.clicked.connect(self.handle_login)
        self.layout.addWidget(self.open_mainwindow_button, Qt.AlignCenter)

        #
        self.setLayout(self.layout)

    def handle_login(self):
        self.accept()

    def exit_app(self):
        sys.exit()


Stylesheet = """
# Custom_Widget {
    background: rgba(34, 93, 138, 190);
    border-radius: 20px;
    opacity: 180;
}
# closeButton {
    min-width: 36px;
    min-height: 36px;
    font-family: "Webdings";
    qproperty-text: "r";
    border-radius: 10px;
}
# closeButton:hover {
    color: #ccc;
    background: white;
}
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setStyleSheet(
            "border-radius: 20px; \
        background-color: qlineargradient(spread:pad, x1:0.091, y1:0.101636, x2:0.991379,y2:0.977, stop:0 rgba(209, 107, 165, 255), stop:1 rgba(255,255,255,255));")

        # Widget
        self.centralwidget = QWidget(self)
        self.setWindowTitle('Weather On Route')
        self.resize(800, 600)
        self.layout = QFormLayout()

        self._create_menu_bar()

        self.start_address_widget = QLineEdit()
        self.start_address_widget.setPlaceholderText("Example: Seattle, WA")
        self.start_address_widget.setStyleSheet(
            "font-size: 14pt; border-color: none none white none; border: 1.5px; background-color: rgba(0,0,0,0);")

        self.end_address_widget = QLineEdit()
        self.end_address_widget.setPlaceholderText("Example: Spokane, WA")
        self.end_address_widget.setStyleSheet(
            "font-size: 14pt; background-color: rgba(0,0,0,0);")

        self.weather_type_widget = QComboBox()
        self.weather_type_widget.addItems(['Snow', 'Rain', 'Clouds'])
        self.weather_type_widget.setStyleSheet("font-size: 14pt;")

        self.travel_date_widget = QDateEdit()
        self.travel_date_widget.setDate(
            datetime.date.today() + datetime.timedelta(1))
        self.travel_date_widget.setStyleSheet(
            "font-size: 14pt; border-color: none none white none; border: 1.5px; background-color: rgba(0,0,0,0);")

        self.number_of_checks = QLineEdit()
        self.number_of_checks.setPlaceholderText(
            "Number of locations to check for weather")
        self.number_of_checks.setStyleSheet(
            "font-size: 14pt; border-color: none none white none; border: 1.5px; background-color: rgba(0,0,0,0);")

        # Add description of what to enter by user
        directions_text = f"""To find your route directions and the weather along it, please enter your starting address and ending address\nNext choose the type of weather you would like search for along your route using the available options in the drop down menu.\nFinally select your date of travel (within 10 days of present day), then click Produce Map\nYou can make any changes to the form and clicking Produce Map will produce the adjusted map."""
        directions = QLabel(directions_text)
        directions.setStyleSheet(
            "font-size: 10pt; background-color: rgba(0,0,0,0%);")
        self.layout.addRow(directions)

        self.origin_label = QLabel("Starting Address:")
        self.origin_label.setStyleSheet(
            "font-size: 14pt; background-color: rgba(0,0,0,0%);")
        self.layout.addRow(self.origin_label, self.start_address_widget)

        self.destination_label = QLabel("Ending Address:")
        self.destination_label.setStyleSheet(
            "font-size: 14pt; background-color: rgba(0,0,0,0%);")
        self.layout.addRow(self.destination_label, self.end_address_widget)

        self.weather_type_label = QLabel("Weather Type:")
        self.weather_type_label.setStyleSheet(
            "font-size: 14pt; background-color: rgba(0,0,0,0%);")
        self.layout.addRow(self.weather_type_label, self.weather_type_widget)

        self.travel_date_label = QLabel("Date of Travel:")
        self.travel_date_label.setStyleSheet(
            "font-size: 14pt; background-color: rgba(0,0,0,0%);")
        self.layout.addRow(self.travel_date_label, self.travel_date_widget)

        # adding pushbutton
        self.pushButton = QPushButton()
        self.pushButton.setText("Find Weather Along Route")
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
        self.pushButton.clicked.connect(self.create_and_display_map)
        self.layout.addWidget(self.pushButton)

        # add widget for housing html
        self.browser = QWebEngineView()

        # add layout to widget and set as central widget
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def _get_user_input(self):
        """
        
        """
        self.start_address = self.start_address_widget.text()
        self.end_address = self.end_address_widget.text()
        self.weather_type = self.weather_type_widget.currentText()
        self.travel_date = self.travel_date_widget.date().toPyDate().strftime("%Y-%m-%d")

    def create_and_display_map(self):

        self._get_user_input()

        # create map
        try:
            wmap = Weather.WeatherMapping(
                self.start_address, self.end_address, self.weather_type, self.travel_date)
            self.map = wmap.create_map()

            # for testing
            self.map.save('testmap.html', close_file=False)

            # save map data
            data = io.BytesIO()
            self.map.save(data, close_file=False)

            # get map data
            self.browser.setHtml(data.getvalue().decode())
            self.layout.addWidget(self.browser)
            self.resize(1250, 950)

        except Exception as e:
            if str(e) == 'list index out of range':
                e = 'Google Directions API could not create driving directions with the addresses provided.\nPlease ensure the addresses are possible to drive between.'
            msgbox = QMessageBox()
            msgbox.setWindowTitle("Error Creating Map")
            msgbox.setText(f"Error when creating map \n{e}")
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.exec()

    def _create_menu_bar(self):
        menuBar = self.menuBar()
        menuBar.setStyleSheet("background-color: rgb(255,255,255)")
        menuBar.addMenu(QMenu("&File", self))
        menuBar.addMenu(QMenu("&Settings", self))
        menuBar.addMenu(QMenu("&Help", self))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    login = ApplicationInformation()

    if login.exec_() == QDialog.Accepted:
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec_())
