# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 10:16:25 2018

@author: liurf
"""
import os, sys
import time
import random
import csv
import pygame
from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QMessageBox, QHBoxLayout, QVBoxLayout, QApplication)
from PyQt5.QtGui import QPixmap, QIcon


class OkGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 图片
        self.lb0 = QLabel(self)
        self.lb0.setPixmap(QPixmap("res/image/0001.png"))
        self.lb0.resize(480, 320)
        self.lb0.move(100, 20)

        # 提示框
        self.tips = QLabel("\n\n\tprint something\t\n\n", self)

        # 按钮
        self.btn0 = QPushButton('\n\n\tStart\t\n\n', self)
        self.btn0.clicked.connect(self.OnClicked)
        self.btn0.setShortcut('S')

        self.btn1 = QPushButton('\n\nNext\n\n', self)
        self.btn1.clicked.connect(self.OnClicked)
        self.btn1.setShortcut('D')

        self.imglist = [a for a in os.listdir("./res/image") if a[-4:] == ".png"]
        self.imgsize = len(self.imglist)
        self.musiclist = [a for a in os.listdir("./res/radio") if a[-4:] == ".mp3"]
        self.musicsize = len(self.musiclist)
        pygame.mixer.init()

        # Widget
        hbox = QHBoxLayout()
        hbox.addWidget(self.tips)
        hbox.addStretch(2)
        hbox.addWidget(self.btn0)
        hbox.addWidget(self.btn1)

        vbox = QVBoxLayout()
        vbox.addWidget(self.lb0)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.setWindowTitle('Action Experiment V0.1')
        self.setWindowIcon(QIcon('res/icon.ico'))
        self.show()

        self.start_test = False
        self.last_image = None
        self.last_music = None
        self.delta_time = []

    def OnClicked(self):
        source = self.sender()

        if 'Start' in source.text():
            print('start test')
            self.start_test = True
            self.btn0.setText("\n\n\tEnd\t\n\n")
            self.btn0.setShortcut('S')

            # start test
            self.last_image = self.imglist[random.randrange(self.imgsize)]
            self.last_music = self.musiclist[random.randrange(self.musicsize)]
            text = 'image = ' + self.last_image + '\n'
            text += 'music = ' + self.last_music
            self.tips.setText(str(text))

            self.lb0.setPixmap(QPixmap("./res/image/" + self.last_image).scaled(self.lb0.size()))
            # self.lb0.resize(480, 320)
            pygame.mixer.music.load("./res/radio/" + self.last_music)
            pygame.mixer.music.play()

            self.start_time = time.time()
        elif 'End' in source.text():
            print('end test')
            self.start_test = False
            self.btn0.setText("\n\n\tStart\t\n\n")
            self.btn0.setShortcut('S')
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            with open('result.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                for row in self.delta_time:
                    writer.writerow(row)
            QMessageBox.information(self, "Warning", "Write Test Result to File \"result.csv\" OK",
                                    QMessageBox.Ok)
            # print('write result ok')

        elif 'Next' in source.text():
            if not self.start_test:
                QMessageBox.information(self, "Warning", "Press \"Start\" Button to Start Experiment First!",
                                        QMessageBox.Ok)
                return

            self.delta_time.append([self.last_image, self.last_music, time.time() - self.start_time])

            # start test
            text = "%s / %s, test time = %f s\n-----------------------------\n" % \
                   (self.last_image, self.last_music, self.delta_time[-1][-1])
            self.last_image = self.imglist[random.randrange(self.imgsize)]
            self.last_music = self.musiclist[random.randrange(self.musicsize)]
            text += 'image = ' + self.last_image + '\n'
            text += 'music = ' + self.last_music
            self.tips.setText(str(text))

            self.lb0.setPixmap(QPixmap("./res/image/" + self.last_image).scaled(self.lb0.size()))

            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            pygame.mixer.music.load("./res/radio/" + self.last_music)
            pygame.mixer.music.play()
            self.start_time = time.time()
        else:
            print('somethine wrong.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = OkGUI()
    sys.exit(app.exec_())
