from PyQt5 import QtGui, QtWidgets, QtCore
import sys


class Top_Widget(QtWidgets.QWidget):
    def __init__(self, window):
        super(Top_Widget, self).__init__()
        self.m_flag = False
        self.window = window

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.window.pos()
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.window.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False

    def paintEvent(self, event):
        opt = QtWidgets.QStyleOption()
        opt.initFrom(self)
        painter = QtGui.QPainter(self)
        self.style().drawPrimitive(QtWidgets.QStyle.PE_Widget, opt, painter, self)

class StatusBar(QtWidgets.QStatusBar):
    def __init__(self):
        super(StatusBar, self).__init__()

class Main_window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main_window, self).__init__()
        self.setupUi()

    def setupUi(self):
        self.setMinimumSize(1020, 670)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.Main_Window = QtWidgets.QWidget(self)

        self.Main_Layout = QtWidgets.QGridLayout()
        self.Main_Layout.setSpacing(0)
        self.Main_Layout.setContentsMargins(0, 0, 0, 0)
        self.Main_Layout.setColumnStretch(2, 1)

        self.Main_Window.setLayout(self.Main_Layout)
        self.setCentralWidget(self.Main_Window)

        self.top_widget = Top_Widget(self)
        self.top_layout = QtWidgets.QHBoxLayout()
        self.top_widget.setLayout(self.top_layout)
        self.top_layout.setSpacing(0)
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_widget.setMinimumHeight(50)
        self.top_widget.setMaximumHeight(50)
        self.top_widget.setStyleSheet("background-color: rgba(180, 180, 180, 0.8);")

        self.left_widget = QtWidgets.QWidget()
        self.left_layout = QtWidgets.QGridLayout()
        self.left_widget.setLayout(self.left_layout)
        self.left_layout.setSpacing(0)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_widget.setMinimumWidth(200)
        self.left_widget.setMaximumWidth(200)
        self.left_widget.setStyleSheet("background-color: rgba(160, 160, 160, 0.8);")

        self.left_bottom_widget = QtWidgets.QWidget()
        self.left_bottom_layout = QtWidgets.QGridLayout()
        self.left_bottom_widget.setLayout(self.left_bottom_layout)
        self.left_bottom_layout.setSpacing(0)
        self.left_bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.left_bottom_widget.setMinimumWidth(200)
        self.left_bottom_widget.setMaximumWidth(200)
        self.left_bottom_widget.setMinimumHeight(56)
        self.left_bottom_widget.setMaximumHeight(56)
        self.left_bottom_widget.setStyleSheet("background-color: rgba(200, 200, 200, 0.8);")

        self.right_widget = QtWidgets.QWidget()
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)
        self.right_layout.setSpacing(0)
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_widget.setStyleSheet("background-color: rgba(100, 100, 100, 0.8);")

        self.Main_Layout.addWidget(self.top_widget, 0, 0, 1, 12)
        self.Main_Layout.addWidget(self.left_widget, 2, 0, 11, 2)
        self.Main_Layout.addWidget(self.left_bottom_widget, 12, 0, 1, 2)
        self.Main_Layout.addWidget(self.right_widget, 2, 2, 11, 10)

        self.statusbar = QtWidgets.QStatusBar(self.Main_Window)
        self.statusbar.setStyleSheet("background-color: rgba(180, 180, 180, 0.8); height: 37px;")
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.mini = QtWidgets.QPushButton('最小化', self.Main_Window)
        self.mini.setGeometry(QtCore.QRect(230, 230, 75, 23))
        self.mini.setObjectName("pushButton")
        self.mini.clicked.connect(self.showMinimized)
        self.top_layout.addStretch(1)
        self.top_layout.addWidget(self.mini)

        self.max = QtWidgets.QPushButton('最大化', self.Main_Window)
        self.max.setGeometry(QtCore.QRect(230, 230, 75, 23))
        self.max.setObjectName("pushButton")
        self.max.clicked.connect(self.max_window)
        self.top_layout.addWidget(self.max)

        self.close = QtWidgets.QPushButton('关闭', self.Main_Window)
        self.close.setGeometry(QtCore.QRect(230, 230, 75, 23))
        self.close.setObjectName("pushButton")
        self.close.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.top_layout.addWidget(self.close)

        self.listWidget = QtWidgets.QListWidget(self.Main_Window)
        self.listWidget.setGeometry(QtCore.QRect(210, 120, 256, 192))
        self.listWidget.setObjectName("listWidget")

        self.recommend = QtWidgets.QListWidgetItem('推荐')
        self.recommend.setFlags(QtCore.Qt.ItemIsUserCheckable)
        self.rank = QtWidgets.QListWidgetItem('排行榜')
        self.my_songs = QtWidgets.QListWidgetItem('我的音乐')
        self.my_songs.setFlags(QtCore.Qt.ItemIsUserCheckable)
        #self.item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.local = QtWidgets.QListWidgetItem('本地音乐')
        self.download = QtWidgets.QListWidgetItem('下载管理')
        self.sheets = QtWidgets.QListWidgetItem('我的歌单')
        self.sheets.setFlags(QtCore.Qt.ItemIsUserCheckable)
        self.prefer = QtWidgets.QListWidgetItem('我喜欢的音乐')

        self.listWidget.addItem(self.recommend)
        self.listWidget.addItem(self.rank)
        self.listWidget.addItem(self.my_songs)
        self.listWidget.addItem(self.local)
        self.listWidget.addItem(self.download)
        self.listWidget.addItem(self.sheets)
        self.listWidget.addItem(self.prefer)
        self.left_layout.addWidget(self.listWidget)

        self.last = QtWidgets.QPushButton('上一首', self.Main_Window)
        self.last.setGeometry(QtCore.QRect(230, 230, 75, 23))
        self.last.setObjectName("pushButton")

        self.play = QtWidgets.QPushButton('播放', self.Main_Window)
        self.play.setGeometry(QtCore.QRect(230, 230, 75, 23))
        self.play.setObjectName("pushButton")

        self.next = QtWidgets.QPushButton('下一首', self.Main_Window)
        self.next.setGeometry(QtCore.QRect(230, 230, 75, 23))
        self.next.setObjectName("pushButton")

        self.progress_text = QtWidgets.QLabel('0:0', self.Main_Window)
        self.progress_text.setGeometry(QtCore.QRect(500, 380, 54, 12))
        self.progress_text.setObjectName("label")

        self.progress = QtWidgets.QSlider(self.Main_Window)
        self.progress.setGeometry(QtCore.QRect(150, 440, 160, 22))
        self.progress.setOrientation(QtCore.Qt.Horizontal)
        self.progress.setObjectName("horizontalSlider")

        self.times = QtWidgets.QLabel('1:1', self.Main_Window)
        self.times.setGeometry(QtCore.QRect(500, 380, 54, 12))
        self.times.setObjectName("label")

        self.volume_ico = QtWidgets.QPushButton('声音', self.Main_Window)
        self.volume_ico.setGeometry(QtCore.QRect(230, 230, 75, 23))
        self.volume_ico.setObjectName("pushButton")

        self.volume = QtWidgets.QSlider(self.Main_Window)
        self.volume.setGeometry(QtCore.QRect(150, 440, 160, 22))
        self.volume.setOrientation(QtCore.Qt.Horizontal)
        self.volume.setObjectName("horizontalSlider")

        self.mode = QtWidgets.QPushButton('模式', self.Main_Window)
        self.mode.setGeometry(QtCore.QRect(230, 230, 75, 23))
        self.mode.setObjectName("pushButton")

        self.words = QtWidgets.QPushButton('歌词', self.Main_Window)
        self.words.setGeometry(QtCore.QRect(230, 230, 75, 23))
        self.words.setObjectName("pushButton")

        self.songs = QtWidgets.QPushButton('播放列表', self.Main_Window)
        self.songs.setGeometry(QtCore.QRect(230, 230, 75, 23))
        self.songs.setObjectName("pushButton")

        self.statusbar.addWidget(self.last)
        self.statusbar.addWidget(self.play)
        self.statusbar.addWidget(self.next)
        self.statusbar.addWidget(self.progress_text)
        self.statusbar.addWidget(self.progress)
        self.statusbar.addWidget(self.times)
        self.statusbar.addWidget(self.volume_ico)
        self.statusbar.addWidget(self.volume)
        self.statusbar.addWidget(self.mode)
        self.statusbar.addWidget(self.words)
        self.statusbar.addWidget(self.songs)

        _translate = QtCore.QCoreApplication.translate

    def max_window(self):
        if self.isMaximized():
            self.showNormal()

        else:
            self.showMaximized()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_PyQtForm = Main_window()
    my_PyQtForm.show()
    sys.exit(app.exec_())