import pygame
import time
from mutagen.mp3 import MP3

class Operate_music():
    def __init__(self):
        pygame.mixer.init()
        self.file = ""
        self.len = 0
        self.datainit()

    def datainit(self):
        self.start = 0.0  # 记录起始时间
        self.pause = 0.0  # 记录暂停时间
        self.unpause = 0.0  # 记录继续时间
        #self.pos = 0.0  # 记录已播放部分长度
        self.paused = 0.0  # 记录暂停的时长
        self.playing = False #歌曲是否处于播放或暂停状态

    def start_at_local(self, file, loop=0, start=0.0):
        #pygame.mixer.init()
        self.file = file
        self.track = pygame.mixer.music.load(self.file)
        #self.pos = 0.0
        pygame.mixer.music.play(loops=loop, start=start)
        self.start = time.time()
        self.playing = True
        self.len = MP3(self.file).info.length

    def set_music_pos(self, pos):
        self.music_stop()
        self.start_at_local(start=pos, file=self.file)
        self.start -= pos

    def get_music_pos(self):
        stoped = pygame.mixer.music.get_pos()
        passedtime = self.start + self.paused
        now = time.time()
        # 正确的返回是 (now - self.start) - self.paused
        if int(now - passedtime) >= int(self.len) or stoped == -1:
            return 0
        else:
            return now - passedtime

    def start_at_internet(self, music):
        pass

    def music_stop(self):
        pygame.mixer.music.stop()
        self.playing = False
        self.datainit()

    def music_pause(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.pause = time.time()
            #当前坐标定在此时
            self.pos = self.pause - self.start


    def music_unpause(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.unpause()
            self.unpause = time.time()
            #暂停时间累加
            self.paused += self.unpause - self.pause

    def isplay(self):
        if pygame.mixer.music.get_pos() == -1:
            self.playing = False
        return self.playing