import Weather
import sys
import io
import datetime
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import (QApplication, QLineEdit, QMainWindow, QWidget, QLabel,
                             QDateEdit, QPushButton, QComboBox, QFormLayout, QDialog, QMenu, QVBoxLayout, QMessageBox)
from PyQt5.QtWebEngineWidgets import QWebEngineView


class ApplicationInformation(QDialog):
    """
    Applications first screen. Contains a description of the application and its limitations.
    Parameters:
        None
    Returns:
        None
    """

    def __init__(self):
        super(ApplicationInformation, self).__init__()

        self.central_widget = QWidget(self)
        self.setWindowTitle("Application Description")
        self.resize(800, 200)
        self.setMaximumWidth(800)
        self.layout = QVBoxLayout()

        description_label = QLabel("Welcome to my CS361 portfolio project! This applications name is Weather Routing and its purpose is to find weather along a driving route. You will be asked to provide a starting and ending city/address/location, choose the type of weather to search for (three options provided) and your travel date (1-4 days from current day).\nThe driving route is provided using Google Maps Directions API. The forecast data is provided using a microservice created by my partner, Jared Chang, which calls OpenWeatherMap's 5 Day / 3 Hour Forecast.\nLimitations: 1) Addresses must be connected via roadway system 2) Weather is checked every 20 miles along route 3) Only 'snow', 'clouds' and 'rain' may be searched for along route.")
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

        self.open_mainwindow_button.clicked.connect(self.open_mainwindow)
        self.layout.addWidget(self.open_mainwindow_button, Qt.AlignCenter)

        self.setLayout(self.layout)

    def open_mainwindow(self):
        """
        accept signal for QDialog 
        """
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
        background-color: qlineargradient(spread:pad, x1:0.091, y1:0.101636, x2:0.991379,y2:0.977, stop:0 rgba(240, 163, 231, 255), stop:1 rgba(255,255,255,255));")

        self.centralwidget = QWidget(self)
        self.setWindowTitle('Weather On Route')
        self.resize(800, 600)
        self.layout = QFormLayout()

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

        directions_text = f"""To find your route directions and the weather along it, please enter your starting address and ending address\nNext choose the type of weather you would like search for along your route using the available options in the drop down menu.\nFinally select your date of travel (1-4 days of present day), then click Produce Map\nYou may make changes to the form and clicking Find Weather Along Route will produce the adjusted map."""
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

        self.pushButton = QPushButton()
        self.pushButton.setText("Find Weather Along Route")
        self.pushButton.setStyleSheet(
            "QPushButton"
            "{"
            "font-size: 14pt; \
                                border-style: solid; \
                                border-radius: 10px; \
                                border-width: 1.5px; \
                                background-color: rgb(0, 255, 234)"
            "}"
            "QPushButton::hover"
            "{"
            "font-size: 14pt; \
                                border-style: solid; \
                                border-radius: 10px; \
                                border-width: 1.5px; \
                                background-color: rgb(153, 255, 247)"
            "}"
        )
        self.pushButton.setGeometry(QRect(200, 150, 93, 28))

        # connect push button to create and display map function
        self.pushButton.clicked.connect(self.create_and_display_map)
        self.layout.addWidget(self.pushButton)

        # view/edit html doc
        self.browser = QWebEngineView()

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def create_and_display_map(self):
        """
        Generates and displays map
        Parameters:
            None
        Returns:
            None
        """

        self._get_user_input()

        try:
            wmap = Weather.WeatherMapping(
                self.start_address, self.end_address, self.weather_type, self.travel_date)
            self.map = wmap.create_map()

            # save map data
            data = io.BytesIO()
            self.map.save(data, close_file=False)

            # embed map data into widget then display
            self.browser.setHtml(data.getvalue().decode())
            self.layout.addWidget(self.browser)
            self.resize(1200, 850)

        # if the user inputs locations that cannot be connected via roadways, google api will not return data
        # thus throwing an index out of range error
        except Exception as e:
            if str(e) == 'list index out of range':
                e = 'Google Directions API could not create driving directions with the addresses provided.\nPlease ensure the addresses real and connected via roadways.'
            msgbox = QMessageBox()
            msgbox.setWindowTitle("Error Creating Map")
            msgbox.setText(f"Error when creating map \n{e}")
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.exec()

    def _get_user_input(self):
        """
        Assigns user input from form fields to class variables 
        Parameters:
            None
        Returns:
            None
        """
        self.start_address = self.start_address_widget.text()
        self.end_address = self.end_address_widget.text()
        self.weather_type = self.weather_type_widget.currentText()
        self.travel_date = self.travel_date_widget.date().toPyDate().strftime("%Y-%m-%d")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # display info screen
    app_info_screen = ApplicationInformation()

    # display main window when user clicks button on info screen
    if app_info_screen.exec_() == QDialog.Accepted:
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec_())
