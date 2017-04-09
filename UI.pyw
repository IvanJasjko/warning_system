import sys
import twit_stream
import analysis


from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import pyqtSlot
from threading import Thread


model_t = Thread(target=analysis.run_model,daemon = True)
stream_t = Thread(target=twit_stream.run_stream,daemon = True)




class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Menu'
        self.left = 360
        self.top = 150
        self.width = 320
        self.height = 120
        self.initUI()


    def initUI(self):

        button = QPushButton('Start Stream', self)
        button.setToolTip('This is an example button')
        button.clicked.connect(self.on_click_stream)
        button.move(125, 20)

        button = QPushButton('Exit', self)
        button.setToolTip('This is an example button')
        button.clicked.connect(self.on_click_stop)
        button.move(125, 60)

        self.show()

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

    def on_click_stream(self):
        stream_t.start()
        model_t.start()


    def on_click_stop(self):
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()

    sys.exit(app.exec_())