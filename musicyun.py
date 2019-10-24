import yun
import operatemusic
import time
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import sys
from mutagen.mp3 import MP3

class qslider(QSlider):
    def __init__(self, window):
        super(qslider, self).__init__()
        self.flag = False  # xx来标记鼠标是否按下
        self.yunui = window

    def mousePressEvent(self, QMouseEvent):
        self.len = self.yunui.progress.width()
        self.mulen = self.yunui.audio.info.length
        print(self.mulen,QMouseEvent.x(), self.len)
        self.flag = True
        pos = int(QMouseEvent.x() / self.len * self.mulen)
        print(pos)
        self.setValue(pos)

    def mouseMoveEvent(self, QMouseEvent):
        self.len = self.yunui.progress.width()
        self.mulen = self.yunui.audio.info.length
        if self.flag:
            pos = int(QMouseEvent.x() / self.len * self.mulen)
            self.setValue(pos)


    def mouseReleaseEvent(self, QMouseEvent):
        self.len = self.yunui.progress.width()
        self.mulen = self.yunui.audio.info.length
        self.flag = False
        pos = int(QMouseEvent.x() / self.len * self.mulen)
        self.setValue(pos)
        #print(self.value()/100*(len//1)*1000)
        #int(self.value() / 100 * (len // 1) * 1000)
        #pygame.mixer.music.stop()
        #time.sleep(5)
        #pygame.mixer.music.play(start=200.0)
        #pygame.mixer.music.set_pos()
        # #pygame.mixer.music.rewind()
        pos = int(self.value())
        om.set_music_pos(pos)


class newtime(QtCore.QThread):
    global om, ex
    time = QtCore.pyqtSignal(str)
    process = QtCore.pyqtSignal(int)

    def __init__(self):
        super(newtime, self).__init__()

    def run(self):
        len = ex.audio.info.length
        ex.progress.setMaximum(int(len))
        while True:
            #print("0:", pygame.mixer.music)
            #pos = pygame.mixer.music.get_pos()
            pos = om.get_music_pos()
            #print(pos)
            # if pos == -1:
            #     # self.time.emit(str(int(ex.audio.info.length // 1)) + "/" + str(int(ex.audio.info.length // 1)))
            #     # self.process.emit(len)
            #     # #pygame.mixer.music.stop()
            #     # music.music_stop()
            #     pos = 0
            if pos == 0: # 单曲循环
                om.start_at_local(r"F:\Users\Administrator\PycharmProjects\untitled21\music\123.mp3")
            pos = int(pos)
            ttime = str(int(pos // 1))+"/"+str(int(len // 1))
            self.time.emit(ttime)
            tprocess = pos // 1
            self.process.emit(tprocess)
            time.sleep(0.2)


class yunui(yun.Main_window):
    global om
    def __init__(self):
        super(yunui, self).__init__()
        self.setupUi(self)
        self.file = r'F:\Users\Administrator\PycharmProjects\untitled21\music\123.mp3'

        self.audio = MP3(self.file)

        self.start()
        self.show()

    def start(self):
        self.last = QPushButton('上一首', self.centralwidget)
        self.last.setGeometry(QtCore.QRect(230, 230, 75, 23))
        self.last.setObjectName("pushButton")

        self.play = QPushButton('播放', self.centralwidget)
        self.play.setGeometry(QtCore.QRect(230, 230, 75, 23))
        self.play.setObjectName("pushButton")

        self.next = QPushButton('下一首', self.centralwidget)
        self.next.setGeometry(QtCore.QRect(230, 230, 75, 23))
        self.next.setObjectName("pushButton")

        self.progress_text = QLabel('0:0', self.centralwidget)
        self.progress_text.setGeometry(QtCore.QRect(500, 380, 54, 12))
        self.progress_text.setObjectName("label")

        self.progress = qslider(self)
        self.progress.setGeometry(QtCore.QRect(150, 440, 160, 22))
        self.progress.setOrientation(QtCore.Qt.Horizontal)
        self.progress.setObjectName("horizontalSlider")

        self.times = QLabel('1:1', self.centralwidget)
        self.times.setGeometry(QtCore.QRect(500, 380, 54, 12))
        self.times.setObjectName("label")

        self.volume_ico = QPushButton('声音', self.centralwidget)
        self.volume_ico.setGeometry(QtCore.QRect(230, 230, 75, 23))
        self.volume_ico.setObjectName("pushButton")

        self.volume = qslider(self)
        self.volume.setGeometry(QtCore.QRect(150, 440, 160, 22))
        self.volume.setOrientation(QtCore.Qt.Horizontal)
        self.volume.setObjectName("horizontalSlider")

        self.mode = QPushButton('模式', self.centralwidget)
        self.mode.setGeometry(QtCore.QRect(230, 230, 75, 23))
        self.mode.setObjectName("pushButton")

        self.words = QPushButton('歌词', self.centralwidget)
        self.words.setGeometry(QtCore.QRect(230, 230, 75, 23))
        self.words.setObjectName("pushButton")

        self.songs = QPushButton('播放列表', self.centralwidget)
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

        self.play.clicked.connect(self.switch_change)

    def switch_change(self):
        print(self.progress.width())
        if self.play.text() == '播放':
            self.start_or_continue()
            self.play.setText('暂停')
            self.showtime = newtime()
            self.showtime.time.connect(self.timechange)
            self.showtime.process.connect(self.updateprocess)
            self.showtime.start()
        else:
            self.play.setText('播放')
            self.pause()

    def start_or_continue(self):
        now = om.isplay()
        if now:
            om.music_unpause()
        else:
            om.start_at_local(self.file)
            self.times.setText(str(int(self.audio.info.length)))

    def pause(self):
        if om.isplay():
            om.music_pause()

    def updateprocess(self, process):
        #print('@', process, self.progress.flag)
        if not self.progress.flag:    #鼠标未按下状态
            self.progress.setValue(process)
        else:                               #鼠标按下了
            self.progress.valueChanged.connect(lambda: self.progress_text.setText(str(self.progress.value()) + "/" + str(int(self.audio.info.length//1))))

    def timechange(self, time):
        #print('#', time, self.progress.flag)
        if not self.progress.flag:
            self.progress_text.setText(time)


app = QApplication(sys.argv)
ex = yunui()
om = operatemusic.Operate_music()
sys.exit(app.exec_())