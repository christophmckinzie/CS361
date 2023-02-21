import Weather
import sys
import io
import datetime
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import (QApplication, QLineEdit, QMainWindow, QWidget, QLabel,
                             QDateEdit, QPushButton, QComboBox, QFormLayout, QGridLayout, QMessageBox, QDialog, QMenu, QMenuBar)


from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QWidget, QFrame,
                             QPushButton, QGridLayout, QSpacerItem, QMessageBox,
                             QSizePolicy, QLabel, QApplication, QLineEdit)


class LoginForm(QDialog):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.setObjectName('Custom_Dialog')
        self.setWindowFlags(self.windowFlags() |
                            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet(Stylesheet)

        self.initUi()

        QMessageBox.information(
            self, "Logging In", "New! Log in a with your credentials to load your personal settings.")

    def initUi(self):
        # widget is used as background and rounded corners.
        self.widget = QWidget(self)
        self.widget.setObjectName('Custom_Widget')
        layout = QVBoxLayout(self)
        layout.addWidget(self.widget)

        # user interface to widgets
        layout = QGridLayout(self.widget)
        # layout.addItem(QSpacerItem(
        #     0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum), 1, 0)

        self.login_exit_button = QPushButton(
            'r', self, clicked=self.accept, objectName='closeButton')
        self.login_exit_button.clicked.connect(self.exit_app)
        layout.addWidget(self.login_exit_button, 0, 4)

        login_label = QLabel("       ")
        layout.addWidget(login_label, 1, 2, Qt.AlignCenter)

        self.username_lineEdit = QLineEdit()
        self.username_lineEdit.setPlaceholderText("  Username")
        self.username_lineEdit.setStyleSheet(
            "background-color: rgba(0,0,0,0); font-size: 14pt; border: none; color:white;")
        layout.addWidget(self.username_lineEdit, 2, 3)

        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line1, 3, 3)

        self.password_lineEdit = QLineEdit()
        self.password_lineEdit.setPlaceholderText("  Password")
        self.password_lineEdit.setStyleSheet(
            "background-color: rgba(0,0,0,0); font-size: 14pt; border: none; color: white;")
        layout.addWidget(self.password_lineEdit, 4, 3)

        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line2, 5, 3)

        self.login_QPushButton = QPushButton()
        self.login_QPushButton.setText("Login")
        self.login_QPushButton.setStyleSheet(
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
        self.login_QPushButton.clicked.connect(self.handle_login)
        layout.addWidget(self.login_QPushButton, 6, 3)

        layout.setRowStretch(0, 0)
        layout.setRowStretch(1, 3)
        layout.setRowStretch(1, 2)

    def handle_login(self):

        if self.username_lineEdit.text() == "" and self.password_lineEdit.text() == "":
            self.accept()
        else:
            QMessageBox.warning(
                self, "Error", "Invalid Credentials. Please Try again.")

    def sizeHint(self):
        return QSize(400, 520)

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
        self.travel_date_widget.setDate(datetime.date.today())
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

        # add layout to widget and set as central widget
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def get_user_input(self):
        self.start_address = self.start_address_widget.text()
        self.end_address = self.end_address_widget.text()
        self.weather_type = self.weather_type_widget.currentText()
        self.travel_date = self.travel_date_widget.date().toPyDate().strftime("%d-%m-%Y")

    def create_and_display_map(self):
        # get user input
        self.get_user_input()

        # call WeatherClass.py and create map
        wmap = Weather.WeatherMapping(start_address=self.start_address, end_address=self.end_address,
                                      weather_type=self.weather_type, travel_date=self.travel_date)
        self.map = wmap.create_map()

        # save map data
        data = io.BytesIO()
        self.map.save(data, close_file=False)

        # get map data
        self.browser.setHtml(data.getvalue().decode())
        self.layout.addWidget(self.browser)

    def _create_menu_bar(self):
        menuBar = self.menuBar()
        menuBar.setStyleSheet("background-color: rgb(255,255,255)")
        menuBar.addMenu(QMenu("&File", self))
        menuBar.addMenu(QMenu("&Settings", self))
        menuBar.addMenu(QMenu("&Help", self))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    login = LoginForm()

    if login.exec_() == QDialog.Accepted:
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec_())
