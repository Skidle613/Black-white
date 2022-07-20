import random
import sqlite3

from PyQt5 import QtMultimedia
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QPushButton, QLabel, QWidget, QTableView, QSlider, QFileDialog, QMainWindow
from PyQt5.Qt import QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPainter, QColor
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
import time


class RecordsForm(QWidget):
    def __init__(self, parent, size):
        super().__init__()
        self.screensize = size
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, self.screensize[0] - 800, self.screensize[1] - 400)
        self.setFixedSize(self.screensize[0] - 800, self.screensize[1] - 400)
        self.setWindowTitle('Рекорды песен')
        self.widget_icon = QIcon('Images\\кубок.png')
        self.setWindowIcon(self.widget_icon)
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('records.db')
        db.open()
        self.view = QTableView(self)
        model = QSqlTableModel(self, db)
        model.setTable('songs')
        model.select()
        self.view.setModel(model)
        self.view.move(0, 0)
        self.view.resize(self.screensize[0] - 800, self.screensize[1] - 400)
        for i in range(6):
            self.view.setColumnWidth(i, (self.screensize[0] - 800) // 6 - 2)
        for i in range(model.rowCount()):
            self.view.setRowHeight(i, 70)


class SettingsForm(QWidget):
    def __init__(self, parent, size):
        super().__init__()
        self.parent = parent
        self.screensize = size
        self.key = False
        self.initUI()

    def initUI(self):
        self.setGeometry(1350 // 2, 200, self.screensize[0] - 1350, self.screensize[1] - 400)
        self.x, self.y = self.screensize[0] - 1350, self.screensize[1] - 400
        self.setFixedSize(self.screensize[0] - 1350, self.screensize[1] - 400)
        self.setWindowTitle('Настройки')
        self.widget_icon = QIcon('Images\\настройки.png')
        self.setWindowIcon(self.widget_icon)
        self.background = QLabel(self)
        self.background.move(0, 0)
        self.background.resize(self.x, self.y)
        self.background.setStyleSheet("background-color: #808080")

        self.label_key_1 = QLabel(self)
        self.label_key_1.setFont(QFont('Times', 16))
        self.label_key_1.move(5, 20)
        self.label_key_1.setText("""Левая клавиша
(назначить можно только буквы A-Z и цифры 0-9""")
        self.label_key_1.resize(500, 50)

        self.key_1 = QPushButton(self.parent.keys[self.parent.key_1], self)
        self.key_1.move(500, 20)
        self.key_1.resize(40, 40)
        self.key_1.clicked.connect(self.key_rename)

        self.label_key_2 = QLabel(self)
        self.label_key_2.setFont(QFont('Times', 16))
        self.label_key_2.move(5, 80)
        self.label_key_2.setText("""Левая средняя клавиша
(назначить можно только буквы A-Z и цифры 0-9""")
        self.label_key_2.resize(500, 50)

        self.key_2 = QPushButton(self.parent.keys[self.parent.key_2], self)
        self.key_2.move(500, 80)
        self.key_2.resize(40, 40)
        self.key_2.clicked.connect(self.key_rename)

        self.label_key_3 = QLabel(self)
        self.label_key_3.setFont(QFont('Times', 16))
        self.label_key_3.move(5, 140)
        self.label_key_3.setText("""Правая средняя клавиша
(назначить можно только буквы A-Z и цифры 0-9""")
        self.label_key_3.resize(500, 50)

        self.key_3 = QPushButton(self.parent.keys[self.parent.key_3], self)
        self.key_3.move(500, 140)
        self.key_3.resize(40, 40)
        self.key_3.clicked.connect(self.key_rename)

        self.label_key_4 = QLabel(self)
        self.label_key_4.setFont(QFont('Times', 16))
        self.label_key_4.move(5, 200)
        self.label_key_4.setText("""Правая клавиша
(назначить можно только буквы A-Z и цифры 0-9""")
        self.label_key_4.resize(500, 50)

        self.key_4 = QPushButton(self.parent.keys[self.parent.key_4], self)
        self.key_4.move(500, 200)
        self.key_4.resize(40, 40)
        self.key_4.clicked.connect(self.key_rename)

        self.accept_button = QPushButton('ПРИМЕНИТЬ', self)
        self.accept_button.move(100, self.y - 100)
        self.accept_button.resize(self.x - 200, 70)
        self.accept_button.clicked.connect(self.accept)

        self.volume_label = QLabel(self)
        self.volume_label.setText('Громкость')
        self.volume_label.move(self.x // 12, 400)
        self.volume_label.resize(200, 50)
        self.volume_label.setFont(QFont('Times', 20))
        self.volume = QSlider(self)
        self.volume.setOrientation(1)
        self.volume.setValue(self.parent.volume)
        self.volume.move(self.x // 2, 400)
        self.volume.resize(self.x // 3, 50)

    def key_rename(self):
        self.key = True
        if self.sender() == self.key_1:
            self.current_key = 1
        elif self.sender() == self.key_2:
            self.current_key = 2
        elif self.sender() == self.key_3:
            self.current_key = 3
        elif self.sender() == self.key_4:
            self.current_key = 4

    def keyPressEvent(self, event):
        if self.key:
            if event.key() in self.parent.keys.keys():
                if self.current_key == 1:
                    self.key_1.setText(self.parent.keys[event.key()])
                elif self.current_key == 2:
                    self.key_2.setText(self.parent.keys[event.key()])
                elif self.current_key == 3:
                    self.key_3.setText(self.parent.keys[event.key()])
                elif self.current_key == 4:
                    self.key_4.setText(self.parent.keys[event.key()])
        self.key = False

    def accept(self):
        self.parent.key_1 = [elem[0] for elem in self.parent.keys.items() if elem[1] == self.key_1.text()][0]
        self.parent.key_2 = [elem[0] for elem in self.parent.keys.items() if elem[1] == self.key_2.text()][0]
        self.parent.key_3 = [elem[0] for elem in self.parent.keys.items() if elem[1] == self.key_3.text()][0]
        self.parent.key_4 = [elem[0] for elem in self.parent.keys.items() if elem[1] == self.key_4.text()][0]
        self.parent.volume = self.volume.value()
        self.parent.player.setVolume(self.parent.volume)
        self.close()


class PauseForm(QWidget):
    def __init__(self, parent, size):
        super().__init__()
        self.parent = parent
        self.screensize = size
        self.parent.player.pause()
        self.parent.block_timer.stop()
        self.initUI()

    def initUI(self):
        self.setGeometry(self.screensize[0] * 0.35, self.screensize[1] * 0.2,
                         self.screensize[0] * 0.3, self.screensize[1] * 0.6 - 140)
        self.setFixedSize(self.screensize[0] * 0.3, self.screensize[1] * 0.6 - 140)
        self.widget_icon = QIcon('Images\\pause.png')
        self.setWindowIcon(self.widget_icon)
        self.setWindowTitle('ПАУЗА')
        self.pause_label = QLabel(self)
        self.pause_label.setText('ПАУЗА')
        self.pause_label.move(self.screensize[0] * 0.1, 30)
        self.pause_label.resize(self.screensize[0] * 0.1, 100)
        self.pause_label.setFont(QFont("Arial black", 34))
        self.volume_label = QLabel(self)
        self.volume_label.setText('Громкость')
        self.volume_label.move(20, 200)
        self.volume_label.resize(100, 50)
        self.volume_label.setFont(QFont('Times', 16))
        self.volume = QSlider(self)
        self.volume.setOrientation(1)
        self.volume.setValue(self.parent.volume)
        self.volume.move(250, 200)
        self.volume.resize(self.screensize[0] * 0.3 - 260, 50)
        self.volume.valueChanged.connect(self.parent.changeVolume)

        self.button_continue = QPushButton(self)
        self.continue_icon = QIcon()
        self.continue_icon.addPixmap(QPixmap('Images\\play.png'))
        self.button_continue.resize(round(0.125 * self.screensize[0]), round(0.05 * self.screensize[0]))
        self.button_continue.move(20, 400)
        self.button_continue.setIcon(self.continue_icon)
        self.button_continue.setIconSize(
            QSize(round(0.05 * self.screensize[0]) - 10, round(0.05 * self.screensize[0]) - 10))
        self.button_continue.clicked.connect(self.close)

        self.button_return = QPushButton(self)
        self.return_icon = QIcon()
        self.return_icon.addPixmap(QPixmap('Images\\exit.png'))
        self.button_return.resize(round(0.125 * self.screensize[0]), round(0.05 * self.screensize[0]))
        self.button_return.move(300, 400)
        self.button_return.setIcon(self.return_icon)
        self.button_return.setIconSize(
            QSize(round(0.05 * self.screensize[0]) - 10, round(0.05 * self.screensize[0]) - 10))
        self.button_return.clicked.connect(self.menu_pesen)

    def menu_pesen(self):
        if self.parent.key:
            for elem in self.parent.bricks:
                elem.y -= 100000
        self.parent.menu_pesen()
        self.hide()

    def closeEvent(self, event):
        self.parent.timer()


class InfoForm(QWidget):
    def __init__(self, parent, size):
        super().__init__()
        self.screensize = size
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setGeometry(self.screensize[0] * 0.35, self.screensize[1] * 0.2,
                         self.screensize[0] * 0.3, self.screensize[1] * 0.4)
        self.setFixedSize(self.screensize[0] * 0.3, self.screensize[1] * 0.4)
        self.setWindowTitle('Информация')
        self.widget_icon = QIcon('Images\\информация.png')
        self.setWindowIcon(self.widget_icon)
        self.label1 = QLabel(self)
        self.label1.setText('ИГРА РАЗРАБОТАНА')
        self.label1.move(self.screensize[0] * 0.07, 50)
        self.label1.resize(self.screensize[0] * 0.2, 50)
        self.label1.setFont(QFont("Times", 24))

        self.cat_b = QPushButton(self)
        self.cat_icon = QIcon()
        self.cat_icon.addPixmap(QPixmap('Images\\smile.png'))
        self.cat_b.move(self.screensize[0] * 0.3 - 20, self.screensize[1] * 0.4 - 20)
        self.cat_b.resize(20, 20)
        self.cat_b.setIcon(self.cat_icon)
        self.cat_b.setIconSize(QSize(20, 20))
        self.cat_b.clicked.connect(self.cat)

        self.label_cat = QLabel(self)
        self.label_cat.move(self.screensize[0] * -0.05, 0)
        self.label_cat.resize(self.screensize[0] * 0.3, self.screensize[1] * 0.4)
        self.cat_pixmap = QPixmap('Images\\cat.png')
        self.label_cat.setPixmap(self.cat_pixmap)
        self.label_cat.setVisible(False)

        self.text_labels = ['В городе Мичуринск', '12.11.2021', 'Кирилловым Владимиром']
        self.labels = []
        for i in range(3):
            self.label = QLabel(self)
            self.label.setText(self.text_labels[i])
            self.label.move(30, 150 + 80 * i)
            self.label.resize(250, 50)
            self.label.setFont(QFont("Times", 16))
            self.labels.append(self.label)

    def cat(self):
        if self.label_cat.isVisible():
            self.label_cat.setVisible(False)
            self.label1.setVisible(True)
            for elem in self.labels:
                elem.setVisible(True)
        else:
            self.label_cat.setVisible(True)
            self.label1.setVisible(False)
            for elem in self.labels:
                elem.setVisible(False)


class Block:
    def __init__(self, parent, time, line):
        self.y = round(427.5 - round(float(time) * 666.6667)) + 16 + round(parent.screensize[1] * 0.08)
        self.x = round(372.5 * line) + 20 + round(parent.screensize[0] * 0.112)
        self.line = line
        self.nashat = False


class GameEnd(QWidget):
    def __init__(self, parent, size, win, score, key=1):
        super().__init__()
        if key == 1:
            self.parent = parent
            self.parent.key = False
            self.setGeometry(size[0] * 0.35, size[1] * 0.2, size[0] * 0.3, size[1] * 0.5)
            self.setWindowTitle('Игра окончена')
            self.label_win = QLabel(self)
            self.label_win.move(size[0] * 0.07, 50)
            self.label_win.resize(size[0] * 0.2, 150)
            self.label_win.setFont(QFont('Times', 30))
            if win == 0:
                self.label_win.setText('Вы проиграли')
            else:
                self.label_win.setText('Вы выиграли')

            self.score = QLabel(self)
            self.score.move(size[0] * 0.09, 200)
            self.score.resize(size[0] * 0.2, 150)
            self.score.setText('Ваш счет:' + str(int(score)))
            self.score.setFont(QFont('Times', 26))

            self.con = sqlite3.connect('records.db')
            self.cur = self.con.cursor()
            self.now_record = self.cur.execute("""SELECT Рекорд FROM songs WHERE id = ?""",
                                               (self.parent.current_song,)).fetchone()
            if score > self.now_record[0]:
                self.cur.execute(
                    """UPDATE songs SET Рекорд = ? WHERE id = ?""", (score, self.parent.current_song))
            self.con.commit()
            self.con.close()

            self.button_return = QPushButton(self)
            self.return_icon = QIcon()
            self.return_icon.addPixmap(QPixmap('Images\\exit.png'))
            self.button_return.resize(round(0.25 * size[0]), round(0.05 * size[0]))
            self.button_return.move(50, 400)
            self.button_return.setIcon(self.return_icon)
            self.button_return.setIconSize(
                QSize(round(0.05 * size[0]) - 10, round(0.05 * size[0]) - 10))
            self.button_return.clicked.connect(self.close)

    def closeEvent(self, event):
        self.parent.menu_pesen()
        self.close()


class Song(QMainWindow):
    def __init__(self, parent, size, id):
        super().__init__()
        self.fname = ''
        self.id = id
        self.parent = parent
        self.parent.ids.append(id)
        self.screensize = size
        self.times = []
        self.times_lines = []
        self.parent.player = QtMultimedia.QMediaPlayer()

    def record_times(self):
        self.setGeometry(self.screensize[0] * 0.3, self.screensize[1] * 0.4,
                         self.screensize[0] * 0.4, self.screensize[1] * 0.18)
        self.setWindowTitle('Записать тайм-коды нот')
        self.button = QPushButton('Добавить тайм-код', self)
        self.button.move(0, 0)
        self.button.resize(self.screensize[0] * 0.1, self.screensize[1] * 0.1)
        self.button.clicked.connect(self.add_time)
        self.button_clear = QPushButton('Очистить тайм-коды', self)
        self.button_clear.move(self.screensize[0] * 0.1, 0)
        self.button_clear.resize(self.screensize[0] * 0.1, self.screensize[1] * 0.1)
        self.button_clear.clicked.connect(self.clear)
        self.button_retry = QPushButton('Перезапустить песню', self)
        self.button_retry.move(self.screensize[0] * 0.2, 0)
        self.button_retry.resize(self.screensize[0] * 0.1, self.screensize[1] * 0.1)
        self.button_retry.clicked.connect(self.retry)
        self.button_choice = QPushButton('Выбрать песню', self)
        self.button_choice.move(self.screensize[0] * 0.3, 0)
        self.button_choice.resize(self.screensize[0] * 0.1, self.screensize[1] * 0.1)
        self.button_choice.clicked.connect(self.choice_song)

        self.button_accept = QPushButton('Добавить', self)
        self.button_accept.move(0, self.screensize[1] * 0.1)
        self.button_accept.resize(self.screensize[0] * 0.4, self.screensize[1] * 0.05)
        self.button_accept.clicked.connect(self.accept)

        self.start = time.time()
        self.show()
        self.parent.player.play()

    def add_time(self):
        self.times.append(time.time() - self.start - (self.parent.end_pause - self.parent.start_pause))

    def clear(self):
        self.times = []

    def retry(self):
        self.start = time.time()
        self.parent.player.stop()
        self.parent.player.play()

    def choice_song(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Выбрать песню', '', 'Песня (*.mp3)')[0]
        # for elem in self.parent.songs:
        #     if elem.fname == self.fname:
        #         self.statusBar().showMessage('Нельзя добавлять повторяющиеся песни')
        #         self.fname = ''
        self.parent.player.setMedia(
            QtMultimedia.QMediaContent(QUrl.fromLocalFile(self.fname)))

    def closeEvent(self, event):
        self.parent.player.stop()
        self.parent.menu_pesen()

    def accept(self):
        self.parent.player.stop()
        self.record_times_lines()
        self.add_to_database()

    def record_times_lines(self):
        past_last = 0
        last = 0
        while len(self.times_lines) < len(self.times):
            number = random.choice(range(4))
            if number != last and number != past_last:
                self.times_lines.append(number)
                past_last = last
                last = number

    def play(self):
        self.parent.player.setMedia(
            QtMultimedia.QMediaContent(QUrl.fromLocalFile(self.fname)))
        self.parent.player.play()
        self.parent.build_bricks(self.times, self.times_lines)

    def add_to_database(self):
        self.con = sqlite3.connect('records.db')
        self.cur = self.con.cursor()
        self.cur.execute(
            """INSERT INTO songs VALUES (?, ?, ?, 0, ?, ?)""", (
                self.id, self.fname.split('/')[-1].split('.')[0], str(self.parent.player.duration())[:-3],
                random.choice(range(1, 6)),
                random.choice(range(1, 4))))
        self.con.commit()
        self.con.close()

    def add_to_songs(self):
        self.parent.songs.append(self)

    # def delete(self):
    #     self.con = sqlite3.connect('records.db')
    #     self.cur = self.con.cursor()
    #     self.parent.songs.remove(self)
    #     self.parent.ids.remove(self.id)
    #     self.cur.execute("""DELETE from song WHERE id = ?""", (self.id,))
    #     self.con.commit()
    #     self.con.close()
