
from principalWindow import PrincipalWindow
from PyQt5.QtWidgets import QApplication
import sys



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PrincipalWindow()
    window.show()
    app.exec_()