import sys
import sqlite3
import ctypes
import time
from random import choice

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow
from Functions import opredelenie_main_menu, opredelenie_const, opredelenie_menu_pesen, opredelenie_song
from Classes import RecordsForm, SettingsForm, PauseForm, InfoForm, Block, GameEnd, Song


class Game(QMainWindow):
    def __init__(self):
        super().__init__()
        opredelenie_const(self)
        opredelenie_main_menu(self)
        opredelenie_menu_pesen(self)
        opredelenie_song(self)
        self.main_menu()

    def records(self):
        self.records_form = RecordsForm(self, self.screensize)
        self.records_form.show()

    def settings(self):
        self.settings_form = SettingsForm(self, self.screensize)
        self.settings_form.show()

    def open_pause(self):
        self.start_pause = time.time()
        self.pause_form = PauseForm(self, self.screensize)
        self.pause_form.show()

    def open_info(self):
        self.info_form = InfoForm(self, self.screensize)
        self.info_form.show()

    def open_end(self, win, score):
        self.player.stop()
        self.block_timer.stop()
        for elem in self.bricks:
            elem.y -= 1000000
        self.menu_pesen()
        self.end_form = GameEnd(self, self.screensize, win, score)
        self.end_form.show()

    def main_menu(self):
        self.background.setVisible(True)
        self.play_button.setVisible(True)
        self.title_1.setVisible(True)
        self.title_2.setVisible(True)
        self.title_3.setVisible(True)
        self.table_of_records.setVisible(True)
        self.settings_button.setVisible(True)
        self.info.setVisible(True)

        self.song_background.setVisible(False)
        self.play_button_2.setVisible(False)
        self.return_main_menu.setVisible(False)
        self.choice_songs.setVisible(False)

    def menu_pesen(self):
        self.play_button.setVisible(False)
        self.title_1.setVisible(False)
        self.title_2.setVisible(False)
        self.title_3.setVisible(False)
        self.table_of_records.setVisible(False)
        self.settings_button.setVisible(False)
        self.info.setVisible(False)
        self.song_background.setVisible(False)

        self.background.setVisible(True)
        self.play_button_2.setVisible(True)
        self.return_main_menu.setVisible(True)
        self.choice_songs.setVisible(True)

        self.choice_songs.clear()
        self.data = self.cur.execute("""SELECT Название, Рекорд, Скорость FROM songs""").fetchall()
        for i in range(len(self.cur.execute("""SELECT id FROM songs""").fetchall())):
            item = f'{self.data[i][0]}       Рекорд: {self.data[i][1]}      Скорость: {self.data[i][2]}'
            self.choice_songs.addItem(item)

    def song(self):
        self.score = 0
        self.label_score.setText('Счет:' + '\n  ' + str(self.score))
        self.background.setVisible(False)
        self.song_background.setVisible(True)
        for elem in self.songs:
            if elem.id == self.choice_songs.currentIndex() + 1:
                self.current_song = elem.id
                self.proshlo = []
                elem.play()

    def timer(self):
        self.pause_form.close()
        self.pause.setEnabled(False)
        self.player.pause()
        self.block_timer.stop()
        self.label_1.setVisible(True)
        self.now = 3
        self.label_1.setText(str(self.now))
        self.timeer = QTimer(self)
        self.timeer.timeout.connect(self.numbers_show)
        self.timeer.start(1000)

    def numbers_show(self):
        self.now -= 1
        if self.now == 0:
            self.pause.setEnabled(True)
            self.label_1.setText('')
            self.label_1.setVisible(False)
            for elem in self.bricks:
                elem.y -= 140
            self.end_pause = time.time()
            self.player.play()
            self.block_timer.start(6)
            self.timeer.stop()
        else:
            self.label_1.setText(str(self.now))

    def changeVolume(self):
        self.volume = self.pause_form.volume.value()
        self.player.setVolume(self.volume)

    def closeEvent(self, event):
        if self.settings_form.isVisible():
            self.settings_form.close()
        if self.pause_form.isVisible():
            self.pause_form.close()
        if self.info_form.isVisible():
            self.info_form.close()
        if self.records_form.isVisible():
            self.records_form.close()
        if self.end_form.isVisible():
            self.end_form.close()

    def build_bricks(self, my_list, lines):
        self.bricks = []
        self.key = True
        for i in range(len(my_list)):
            self.block = Block(self, my_list[i], lines[i])
            self.bricks.append(self.block)
        self.repaint()
        self.block_timer = QTimer()
        self.block_timer.timeout.connect(self.repaint)
        self.block_timer.start(6)

    def brick_move(self, qp, elem):
        elem.y += 4
        if elem.y > (448 + round(self.screensize[1] * 0.08)):
            qp.eraseRect(elem.x, elem.y - 4, 332, 352)
            qp.drawRect(elem.x, elem.y, 332, (800 + round(self.screensize[1] * 0.08)) - elem.y)
            qp.fillRect(elem.x, elem.y, 332, (800 + round(self.screensize[1] * 0.08)) - elem.y, QColor(0, 0, 0))
        else:
            qp.eraseRect(elem.x, elem.y - 4, 332, 352)
            qp.drawRect(elem.x, elem.y, 332, 352)
            qp.fillRect(elem.x, elem.y, 332, 352, QColor(0, 0, 0))

    def paintEvent(self, event):
        if self.key:
            qp = QPainter()
            qp.setBrush(QColor(0, 0, 0))
            qp.begin(self)
            for elem in self.bricks:
                self.brick_move(qp, elem)
                if elem.y >= self.screensize[1] * 0.82:
                    if not elem.nashat:
                        self.open_end(0, self.score)
                    else:
                        if elem not in self.proshlo:
                            self.proshlo.append(elem)
            if len(self.proshlo) == len(self.bricks):
                self.open_end(1, self.score)
            qp.end()
        qp = QPainter()
        qp.setBrush(QColor(0, 0, 0))
        qp.begin(self)
        qp.drawLine(round(self.screensize[0] * 0.31), round(self.screensize[1] * 0.08),
                    round(self.screensize[0] * 0.31), round(self.screensize[1] * 0.82))
        qp.drawLine(round(self.screensize[0] * 0.5), round(self.screensize[1] * 0.08),
                    round(self.screensize[0] * 0.5), round(self.screensize[1] * 0.82))
        qp.drawLine(round(self.screensize[0] * 0.69), round(self.screensize[1] * 0.08),
                    round(self.screensize[0] * 0.69), round(self.screensize[1] * 0.82))
        qp.end()

    def keyPressEvent(self, event):
        if self.key:
            min_razn = 1000
            self.label_press.setVisible(True)
            if event.key() == self.key_1:
                min_razn = min([abs((elem.y + 352) - self.screensize[1] * 0.82) for elem in self.bricks
                                if elem.line == 0])
                self.label_press.move(round(self.screensize[0] * 0.02), 0)
            elif event.key() == self.key_2:
                min_razn = min([abs((elem.y + 352) - self.screensize[1] * 0.82) for elem in self.bricks
                                if elem.line == 1])
                self.label_press.move(round(self.screensize[0] * 0.21), 0)
            elif event.key() == self.key_3:
                min_razn = min([abs((elem.y + 352) - self.screensize[1] * 0.82) for elem in self.bricks
                                if elem.line == 2])
                self.label_press.move(round(self.screensize[0] * 0.4), 0)
            elif event.key() == self.key_4:
                min_razn = min([abs((elem.y + 352) - self.screensize[1] * 0.82) for elem in self.bricks
                                if elem.line == 3])
                self.label_press.move(round(self.screensize[0] * 0.59), 0)
            for elem in self.bricks:
                if abs((elem.y + 352) - self.screensize[1] * 0.82) == min_razn:
                    elem.nashat = True
            if min_razn > 352:
                pass
                self.open_end(0, self.score)
            else:
                if min_razn > 45:
                    self.score += 10
                else:
                    self.score += 10 * (10 - (min_razn // 10))
                self.label_score.setText('Счет:' + '\n  ' + str(int(self.score)))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = Game()
    widget.showMaximized()
    sys.excepthook = except_hook
    sys.exit(app.exec())
