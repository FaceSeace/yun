import yun
import operatemusic
import time
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import sys
from mutagen.mp3 import MP3

class prog_qslider(QSlider):
    def __init__(self, window):
        super(prog_qslider, self).__init__()
        self.flag = False  # xx来标记鼠标是否按下
        self.yunui = window

    def mousePressEvent(self, QMouseEvent):
        self.len = self.yunui.progress.width()
        self.mulen = om.audio.info.length
        #print(self.mulen, QMouseEvent.x(), self.len)
        self.flag = True
        pos = int(QMouseEvent.x() / self.len * self.mulen)
        if pos > self.mulen:
            pos = self.mulen
        elif pos < 0:
            pos = 0
        #print(pos)
        self.setValue(pos)
        time = self.totime(pos)
        self.yunui.progress_text.setText(time[0] + ':' + time[1])

    def mouseMoveEvent(self, QMouseEvent):
        self.len = self.yunui.progress.width()
        self.mulen = om.audio.info.length
        if self.flag:
            pos = int(QMouseEvent.x() / self.len * self.mulen)
            if pos > self.mulen:
                pos = self.mulen
            elif pos < 0:
                pos = 0
            self.setValue(pos)
            time = self.totime(pos)
            self.yunui.progress_text.setText(time[0] + ':' + time[1])


    def mouseReleaseEvent(self, QMouseEvent):
        self.len = self.yunui.progress.width()
        self.mulen = om.audio.info.length
        self.flag = False
        pos = int(QMouseEvent.x() / self.len * self.mulen)
        if pos > self.mulen:
            pos = self.mulen
        elif pos < 0:
            pos = 0
        self.setValue(pos)
        time = self.totime(pos)
        self.yunui.progress_text.setText(time[0] + ':' + time[1])
        #print(self.value()/100*(len//1)*1000)
        #int(self.value() / 100 * (len // 1) * 1000)
        #pygame.mixer.music.stop()
        #time.sleep(5)
        #pygame.mixer.music.play(start=200.0)
        #pygame.mixer.music.set_pos()
        # #pygame.mixer.music.rewind()
        pos = int(self.value())
        #print(pos)
        om.set_music_pos(pos)

    def totime(self, time):
        time = int(time)
        second = time % 60
        min = time//60
        second = "%02d" % second
        if min < 100:
            min = "%02d" % min
        return [min, second]

class volum_qslider(QSlider):
    def __init__(self, window):
        super(volum_qslider, self).__init__()
        self.flag = False  # xx来标记鼠标是否按下
        self.yunui = window
        self.setMinimum(0)
        self.setMaximum(100)
        self.setValue(100*int(om.getvolum()))

    def mousePressEvent(self, QMouseEvent):
        self.len = self.yunui.progress.width()
        self.flag = True
        pos = int(QMouseEvent.x() / self.len * 100)
        self.setValue(pos)
        om.setvolum(pos/100)


    def mouseMoveEvent(self, QMouseEvent):
        self.len = self.yunui.progress.width()
        if self.flag:
            pos = int(QMouseEvent.x() / self.len * 100)
            self.setValue(pos)
            om.setvolum(pos / 100)


    def mouseReleaseEvent(self, QMouseEvent):
        self.len = self.yunui.progress.width()
        self.flag = False
        pos = int(QMouseEvent.x() / self.len * 100)
        self.setValue(pos)
        #print(pos)
        om.setvolum(pos / 100)
        #print(self.value()/100*(len//1)*1000)
        #int(self.value() / 100 * (len // 1) * 1000)
        #pygame.mixer.music.stop()
        #time.sleep(5)
        #pygame.mixer.music.play(start=200.0)
        #pygame.mixer.music.set_pos()
        # #pygame.mixer.music.rewind()
        #print(pos)


class newtime(QtCore.QThread):
    time = QtCore.pyqtSignal(str)
    process = QtCore.pyqtSignal(int)

    def __init__(self,mainwindow):
        super(newtime, self).__init__()
        self.mainwindow = mainwindow

    def run(self):
        while True:
            #time = self.totime(om.audio.info.length)
            #self.mainwindow.times.setText(time[0] + ':' + time[1])
            #print("0:", pygame.mixer.music)
            #pos = pygame.mixer.music.get_pos()
            pos = om.get_music_pos()
            #print(pos)
            if pos == -1:
                self.mainwindow.play.setText('播放')
                pos = 0
            # elif pos >=0:
            #     self.mainwindow.play.setText('暂停')
            #     # self.time.emit(str(int(ex.audio.info.length // 1)) + "/" + str(int(ex.audio.info.length // 1)))
            #     # self.process.emit(len)
            #     # #pygame.mixer.music.stop()
            #     # mu sic.music_stop()
            #     pos = 0
            # if pos == 0: # 单曲循环
            #     om.start_at_local(r"F:\Users\Administrator\PycharmProjects\untitled21\music\123.mp3")
            pos = int(pos)
            ttime = self.totime(pos)[0] + ":" + self.totime(pos)[1]
            self.time.emit(ttime)
            tprocess = pos // 1
            self.process.emit(tprocess)
            time.sleep(0.1)

    def totime(self,time):
        time = int(time)
        second = time % 60
        min = time//60
        second = "%02d" % second
        if min < 100:
            min = "%02d" % min
        return [min, second]


class yunui(yun.Main_window):
    def __init__(self):
        super(yunui, self).__init__()
        self.setupUi()
        self.file = r'F:\Users\Administrator\PycharmProjects\yun\music\123.mp3'
        self.tstarted = False
        self.start()
        self.show()

    def start(self):
        self.progress = prog_qslider(self)
        self.progress.setGeometry(QtCore.QRect(150, 440, 160, 22))
        self.progress.setOrientation(QtCore.Qt.Horizontal)
        self.progress.setObjectName("horizontalSlider")
        self.progress.setEnabled(False)

        self.volume = volum_qslider(self)
        self.volume.setGeometry(QtCore.QRect(150, 440, 160, 22))
        self.volume.setOrientation(QtCore.Qt.Horizontal)
        self.volume.setObjectName("horizontalSlider")

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
        self.play.clicked.connect(self.runtheard)
        self.last.clicked.connect(self.lastsong)
        self.next.clicked.connect(self.nextsong)
        self.mode.clicked.connect(self.changemode)

        self.mode.setText('列表循环')

        self.showtime = newtime(self)
        self.showtime.time.connect(self.timechange)
        self.showtime.time.connect(self.changemusic)
        self.showtime.process.connect(self.updateprocess)

    def runtheard(self):
        if not self.tstarted:
            self.showtime.start()
            self.progress.setEnabled(True)
        self.tstarted = True

    def switch_change(self):
        if self.play.text() == '播放':
            self.start_or_continue()
            self.play.setText('暂停')
        else:
            self.play.setText('播放')
            self.pause()

    def start_or_continue(self):
        now = om.isplay()
        if now:
            om.music_unpause()
        else:
            om.start_at_local(self.file)

    def pause(self):
        if om.isplay():
            om.music_pause()

    def updateprocess(self, process):
        #print('@', process, self.progress.flag)
        if not self.progress.flag:    #鼠标未按下状态
            self.progress.setValue(process)
        else:                               #鼠标按下了
            pass
            #self.progress.valueChanged.connect(lambda: self.progress_text.setText(str(self.progress.value()) + "/" + str(int(self.audio.info.length//1))))

    def timechange(self, time):
        #print('#', time, self.progress.flag)
        if not self.progress.flag:
            self.progress_text.setText(time)

    def totime(self,time):
        time = int(time)
        second = time % 60
        min = time//60
        second = "%02d" % second
        if min < 100:
            min = "%02d" % min
        return [min, second]

    def nextsong(self):
        try:
            om.mode_next()
        except:
            pass

    def lastsong(self):
        try:
            om.lastsong()
        except:
            pass

    def changemusic(self,temp):
        self.play.setText('暂停')
        len = int(om.audio.info.length)
        self.progress.setMaximum(len)
        time = self.totime(len)
        self.times.setText(time[0] + ':' + time[1])

    def changemode(self):
        if om.mode == 0:
            om.mode = 1
            self.mode.setText('单曲循环')
        elif om.mode == 1:
            om.mode = 2
            self.mode.setText('随机播放')
        elif om.mode == 2:
            om.mode = 0
            self.mode.setText('列表循环')

app = QApplication(sys.argv)
om = operatemusic.Operate_music()
ex = yunui()
sys.exit(app.exec_())