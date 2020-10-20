from PyQt5 import QtWidgets, uic
import sys

from gui.mainwindow import MainWindow


if __name__ == '__main__':
    # Setup the terminal arguments
    app = QtWidgets.QApplication(sys.argv)
    # Create and show app
    mainwindow = MainWindow()
    mainwindow.show()
    # Execute the application
    app.exec_()

