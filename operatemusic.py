import pygame
import time
import random
from mutagen.mp3 import MP3

class Operate_music():
    def __init__(self):
        pygame.mixer.init()
        self.file = ""
        self.len = 0
        self.datainit()
        self.mode = 0  # 0 列表循环  1 单曲循环  2 随机播放
        self.songlist = [r'F:\Users\Administrator\PycharmProjects\yun\music\123.mp3',
                         r'F:\Users\Administrator\PycharmProjects\yun\music\456.mp3',
                         r'F:\Users\Administrator\PycharmProjects\yun\music\789.mp3']

    def datainit(self):
        self.start = 0.0  # 记录起始时间
        self.pause = 0.0  # 记录暂停时间
        self.unpause = 0.0  # 记录继续时间
        self.paused = 0.0  # 记录暂停的时长
        self.playing = False  # 歌曲是否处于播放或暂停状态
        self.ispause = False  # 歌曲是否处于暂停状态
        self.now = 0.0  # 当前时间

    def start_at_local(self, file, loop=0, start=0.0):
        # 不能初始化数据！
        self.file = file
        self.audio = MP3(self.file)
        self.track = pygame.mixer.music.load(self.file)
        pygame.mixer.music.play(loops=loop, start=start)
        self.start = time.time()
        self.playing = True
        self.len = self.audio.info.length
        self.ispause = False

    def set_music_pos(self, pos):
        self.music_stop()
        self.start_at_local(start=pos, file=self.file)
        self.start -= pos

    def get_music_pos(self):
        stoped = pygame.mixer.music.get_pos()
        passedtime = self.start + self.paused
        if not self.ispause:
            self.now = time.time()
        # 正确的返回是 (now - self.start) - self.paused
        if int(self.now - passedtime) >= int(self.len) or stoped == -1:
            self.playing = False
            self.mode_next()
            return -1
        else:
            return self.now - passedtime

    def start_at_internet(self, music):
        pass

    def music_stop(self):
        pygame.mixer.music.stop()
        self.playing = False
        self.paused = False
        self.datainit()

    def music_pause(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.pause = time.time()
            #当前坐标定在此时
            self.pos = self.pause - self.start
            self.ispause = True


    def music_unpause(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.unpause()
            self.unpause = time.time()
            #暂停时间累加
            self.paused += self.unpause - self.pause
            self.ispause = False

    def isplay(self):
        if pygame.mixer.music.get_pos() == -1:
            self.playing = False
        return self.playing

    def setvolum(self, volume):
        pygame.mixer.music.set_volume(volume)

    def getvolum(self):
        return pygame.mixer.music.get_volume()

    def addsong(self):
        pass

    def nextsong(self):
        next_in_songs = self.now_in_songs() + 1
        print('歌曲索引:', next_in_songs)
        if next_in_songs < len(self.songlist):
            self.music_stop()
            self.start_at_local(self.songlist[next_in_songs])

    def lastsong(self):
        last_in_songs = self.now_in_songs() - 1
        if last_in_songs >= 0:
            self.music_stop()
            self.start_at_local(self.songlist[last_in_songs])

    # 返回0开始的位置
    def now_in_songs(self):
        return self.songlist.index(self.file)

    def mode_next(self):
        self.datainit()
        # 0 列表循环  1 单曲循环  2 随机播放
        if self.mode == 0:
            print('列表循环')
            if self.now_in_songs() >= len(self.songlist) - 1:
                self.start_at_local(self.songlist[0])
                return
            self.nextsong()
        elif self.mode == 1:
            print('单曲循环')
            self.start_at_local(self.songlist[self.now_in_songs()])
        elif self.mode == 2:
            print('随机播放')
            self.start_at_local(random.choice(self.songlist))