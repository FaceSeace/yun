import time
import pygame
from mutagen.mp3 import MP3
import untitled
import sys
from PyQt5 import QtGui, QtCore, QtWidgets


class Operate_music():
    def __init__(self):
        global len
        pygame.mixer.init()
        self.file = ""
        self.datainit()

    def datainit(self):
        self.start = 0.0  # 记录起始时间
        self.pause = 0.0  # 记录暂停时间
        self.unpause = 0.0  # 记录继续时间
        #self.pos = 0.0  # 记录已播放部分长度
        self.paused = 0.0  # 记录暂停的时长

    def start_at_local(self, file, loop=0, start=0.0):
        #pygame.mixer.init()
        self.file = file
        self.track = pygame.mixer.music.load(self.file)
        #self.pos = 0.0
        pygame.mixer.music.play(loops=loop, start=start)
        self.start = time.time()

    def set_music_pos(self, pos):
        self.music_stop()
        self.start_at_local(start=pos, file=self.file)
        self.start -= pos

    def get_music_pos(self):
        stoped = pygame.mixer.music.get_pos()
        print(stoped)
        passedtime = self.start + self.paused
        # 正确的返回是 (now - self.start) - self.paused
        now = time.time()
        if (now - passedtime) >= int(len) or stoped == -1:
            return 0
        else:
            return now - passedtime

    def start_at_internet(self, music):
        pass

    def music_stop(self):
        pygame.mixer.music.stop()
        self.datainit()

    def music_pause(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.pause = time.time()
            #当前坐标定在此时
            self.pos = self.pause - self.start


    def music_unpause(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.unpause()
            self.unpause = time.time()
            #暂停时间累加
            self.paused += self.unpause - self.pause


class qslider(QtWidgets.QSlider):
    global music, len
    flag = False #xx来标记鼠标是否按下

    def mouseMoveEvent(self, QMouseEvent):
        global len
        if self.flag:
            self.setValue(int(QMouseEvent.x() / 331 * len))

    def mousePressEvent(self, QMouseEvent):
        self.flag = True
        self.setValue(int(QMouseEvent.x()/331 * len))

    def mouseReleaseEvent(self, QMouseEvent):
        self.flag = False
        #print(self.value()/100*(len//1)*1000)
        #int(self.value() / 100 * (len // 1) * 1000)
        #pygame.mixer.music.stop()
        #time.sleep(5)
        #pygame.mixer.music.play(start=200.0)
        #pygame.mixer.music.set_pos()
        #pygame.mixer.music.rewind()
        pos = int(self.value())
        music.set_music_pos(pos)


class newtime(QtCore.QThread):
    time = QtCore.pyqtSignal(str)
    process = QtCore.pyqtSignal(int)

    def __init__(self):
        super(newtime, self).__init__()
        global music

    def run(self):
        global ex
        len = ex.audio.info.length
        ex.horizontalSlider.setMaximum(int(len))
        while True:
            #print("0:", pygame.mixer.music)
            #pos = pygame.mixer.music.get_pos()
            pos = music.get_music_pos()
            #print(pos)
            # if pos == -1:
            #     # self.time.emit(str(int(ex.audio.info.length // 1)) + "/" + str(int(ex.audio.info.length // 1)))
            #     # self.process.emit(len)
            #     # #pygame.mixer.music.stop()
            #     # music.music_stop()
            #     pos = 0
            if pos == 0: # 单曲循环
                music.start_at_local(r"F:\Users\Administrator\PycharmProjects\untitled21\music\123.mp3")
            pos = int(pos)
            ttime = str(int(pos // 1))+"/"+str(int(len // 1))
            self.time.emit(ttime)
            tprocess = pos // 1
            self.process.emit(tprocess)
            print(5)
            time.sleep(1)
            print(6)



class main_window(untitled.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(main_window, self).__init__()
        self.setupUi(self)
        self.showtime = newtime()
        self.showtime.time.connect(self.timechange)
        self.showtime.process.connect(self.updateprocess)
        self.horizontalSlider = qslider(self.centralwidget)
        self.xx = False
        global music
        self.horizontalSlider.setGeometry(QtCore.QRect(10, 10, 331, 22))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.start()


    def start(self):
        self.show()
        self.file = r"F:\Users\Administrator\PycharmProjects\untitled21\music\123.mp3"
        self.audio = MP3(self.file)
        self.pushButton.clicked.connect(self.playmusic)


    def playmusic(self):
        # self.track = pygame.mixer.music.load(self.file)
        #pygame.mixer.music.play()
        music.start_at_local(file=self.file)
        self.showtime.start()

    def updateprocess(self, process):
        if not self.horizontalSlider.xx:    #鼠标未按下状态
            self.horizontalSlider.setValue(process)
        else:                               #鼠标按下了
            self.horizontalSlider.valueChanged.connect(lambda: self.label.setText(str(self.horizontalSlider.value()) + "/" + str(int(self.audio.info.length//1))))

    def timechange(self, time):
        if not self.horizontalSlider.xx:
            self.label.setText(time)


app = QtWidgets.QApplication(sys.argv)
ex = main_window()
music = Operate_music()
len = ex.audio.info.length
sys.exit(app.exec_())

