import sys
import sqlite3
from random import randint, choice

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, \
    QTableWidgetItem
from pyqt5_plugins.examplebuttonplugin import QtGui

from data.ui1 import Ui_MainWindow
from data.ui2 import Ui_Training
from data.ui3 import Ui_TestChoice
from data.ui4 import Ui_Test
from data.ui5 import Ui_Result
from data.ui6 import Ui_StartSolve
from data.ui7 import Ui_Solve
from data.ui8 import Ui_BestResults
from data.ui9 import Ui_Name


def convert_to(number, base, upper=True):
    digits = '0123456789abcdefghijklmnopqrstuvwxyz'
    if base > len(digits):
        return None
    result = ''
    while number > 0:
        result = digits[number % base] + result
        number //= base
    return result.upper() if upper else result


class MyWidget1(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.train = MyWidget2()
        self.test_choice = MyWidget3()
        self.training_button.clicked.connect(self.show_training)
        self.test_button.clicked.connect(self.show_choice_testing)
        self.quit_button.clicked.connect(self.close)

    def show_training(self):
        self.train.show()
        self.hide()

    def show_choice_testing(self):
        self.test_choice.show()
        self.hide()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Выход',
                                     "Вы действительно хотите выйти?",
                                     QMessageBox.Yes |
                                     QMessageBox.No,
                                     QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class MyWidget2(QMainWindow, Ui_Training):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.convert_button.clicked.connect(self.converting)
        self.back_button.clicked.connect(self.backing)
        self.clean_button.clicked.connect(self.cleaning)
        self.explanation.hide()
        self.show_explanation.stateChanged.connect(self.changelabel)

    def converting(self):
        try:
            old_n_in_ns = int(self.old_n.text(), int(self.old_ns.text()))
            new_n_in_ns = convert_to(old_n_in_ns, int(self.new_ns.text()))
            self.new_n.setText(str(new_n_in_ns))
            old_n1 = str(self.old_n.text())
            old_ns1 = str(self.old_ns.text())
            text1 = str()
            text2 = str()
            for i in range(len(old_n1)):
                text1 += (str(
                    int(old_n1[i], int(self.old_ns.text()))) + '*' + old_ns1
                          + '^' + str(len(old_n1) - i - 1) + ' + ')
                text2 += str(
                    int(old_n1[i], int(self.old_ns.text())) *
                    (int(old_ns1) ** int(len(old_n1) - i - 1))) + ' + '
            old_n_in_ns1 = int(old_n_in_ns)
            new_ns1 = str(self.new_ns.text())
            text3 = str()
            text4 = str()
            paragraph1 = ''
            paragraph2 = ''
            while old_n_in_ns1 > 0:
                text3 = str(old_n_in_ns1) + '%' + new_ns1 + ' + ' + text3
                text4 = str(old_n_in_ns1 % int(new_ns1)) + ' + ' + text4
                old_n_in_ns1 //= int(self.new_ns.text())
                paragraph1 = (('Перевод в десятичную систему счисления (символ'
                               ' "^" означает возведение в степень):\n') +
                              text1[:-3] + ' = ' + text2[:-3] + ' = ' + str(
                            old_n_in_ns))
                paragraph2 = (('Перевод из десятичной системы счисления '
                               '(символ "%" означает остаток от деления):\n')
                              + text3[:-3]
                              + ' = ' + text4[:-3] + ' = ' + str(new_n_in_ns))
            if old_ns1 == new_ns1:
                self.explanation.setText('Перевод из одной системы '
                                         'счисления в другую не производился')
            elif old_ns1 != '10' and new_ns1 != '10':
                self.explanation.setText(paragraph1 + '\n' + paragraph2)
            elif new_ns1 != '10':
                self.explanation.setText(paragraph2)
            else:
                self.explanation.setText(paragraph1)
        except ValueError:
            self.new_n.setText('Ошибка')
            self.explanation.setText('Введены не все данные, или система '
                                     'счисления записана не числом.')
        self.explanation.setWordWrap(True)

    def backing(self):
        self.explanation.setText('')
        self.old_n.setText('')
        self.old_ns.setText('')
        self.new_n.setText('')
        self.new_ns.setText('')
        self.show_explanation.setChecked(False)
        menu.show()
        self.hide()

    def cleaning(self):
        self.explanation.setText('')
        self.old_n.setText('')
        self.old_ns.setText('')
        self.new_n.setText('')
        self.new_ns.setText('')

    def changelabel(self, state):
        if state:
            self.explanation.show()
        else:
            self.explanation.hide()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Выход',
                                     "Вы действительно хотите выйти?",
                                     QMessageBox.Yes |
                                     QMessageBox.No,
                                     QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class MyWidget3(QMainWindow, Ui_TestChoice):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.questions = 5
        self.back_button.clicked.connect(self.backing)
        self.start_button.clicked.connect(self.starting)

        self.how_many_questions.addItem('5')
        self.how_many_questions.addItem('10')
        self.how_many_questions.addItem('15')
        self.how_many_questions.addItem('20')
        self.how_many_questions.addItem('25')
        self.how_many_questions.currentTextChanged.connect(self.text_changed)

        self.convert_action.triggered.connect(self.converting)
        self.solve_action.triggered.connect(self.solving)

    def converting(self):
        pass

    def solving(self):
        self.solve_choice = MyWidget6()
        self.solve_choice.show()
        self.hide()

    def backing(self):
        menu.show()
        self.hide()

    def starting(self):
        choice = 0
        if self.radioButton_1.isChecked():
            choice = 1
        elif self.radioButton_2.isChecked():
            choice = 2
        elif self.radioButton_3.isChecked():
            choice = 3
        if choice:
            number = 1
            self.auth = MyWidget9(choice, self.questions, number)
            self.auth.show()
            self.hide()

    def text_changed(self, questions):
        self.questions = int(questions)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Выход',
                                     "Вы действительно хотите выйти?",
                                     QMessageBox.Yes |
                                     QMessageBox.No,
                                     QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class MyWidget4(QMainWindow, Ui_Test):
    def __init__(self, choice, questions, number, id):
        super().__init__()
        self.setupUi(self)

        self.question_number = 'Вопрос №'
        self.id = id
        self.number = number
        self.questions = questions
        self.choice = choice
        self.digits = '0123456789abcdefghijklmnopqrstuvwxyz'
        self.f = open('resources/answers.txt', 'w')

        self.question_number1.setText(self.question_number + str(self.number))
        self.question_number2.setText(str(self.number) + '/' +
                                      str(self.questions))
        self.questions_progressBar.setValue(100 * (self.number - 1) //
                                            self.questions)
        self.end_button.clicked.connect(self.ending)
        self.continue_button.clicked.connect(self.continueing)
        if self.choice == 1:
            self.question1 = '0'
            self.old_ns = randint(2, 16)
            while self.old_ns == 10:
                self.old_ns = randint(2, 16)
            while self.question1[0] == '0':
                self.question1 = ''
                for i in range(randint(2, 3)):
                    self.question1 += str(
                        self.digits[randint(0, self.old_ns - 1)]).upper()
            self.new_ns = 10
        elif self.choice == 2:
            self.old_ns = 10
            self.new_ns = randint(2, 16)
            while self.new_ns == 10:
                self.new_ns = randint(2, 16)
            self.question1 = randint(self.new_ns + 1, 200)
        elif self.choice == 3:
            self.question1 = '0'
            self.old_ns = randint(2, 16)
            self.new_ns = randint(2, 16)
            while self.old_ns == self.new_ns:
                self.old_ns = randint(2, 16)
                self.new_ns = randint(2, 16)
            while self.question1[0] == '0':
                self.question1 = ''
                for i in range(randint(2, 3)):
                    self.question1 += str(
                        self.digits[randint(0, self.old_ns - 1)]).upper()
        self.question.setText('Переведите число {} из {}-ичной системы '
                              'счисления\nв {}-ичную систему счисления'
                              .format(self.question1,
                                      self.old_ns, self.new_ns))
        self.question.setWordWrap(True)

    def continueing(self):

        answer1 = self.answer.text().upper()
        answer2 = convert_to(
            int(str(self.question1), int(self.old_ns)), int(self.new_ns))
        self.f.write(str(answer1) + ' ' + str(answer2) + '\n')

        self.answer.setText('')
        self.number += 1
        self.question_number1.setText(self.question_number + str(self.number))
        self.question_number2.setText(str(self.number) + '/' +
                                      str(self.questions))
        self.questions_progressBar.setValue(100 * (self.number - 1) //
                                            self.questions)
        if self.choice == 1:
            self.question1 = '0'
            self.old_ns = randint(2, 16)
            while self.old_ns == 10:
                self.old_ns = randint(2, 16)
            while self.question1[0] == '0':
                self.question1 = ''
                for i in range(randint(2, 3)):
                    self.question1 += str(
                        self.digits[randint(0, self.old_ns - 1)]).upper()
            self.new_ns = 10
        elif self.choice == 2:
            self.old_ns = 10
            self.new_ns = randint(2, 16)
            while self.new_ns == 10:
                self.new_ns = randint(2, 16)
            self.question1 = randint(self.new_ns + 1, 200)
        elif self.choice == 3:
            self.question1 = '0'
            self.old_ns = randint(2, 16)
            self.new_ns = randint(2, 16)
            while self.old_ns == self.new_ns:
                self.old_ns = randint(2, 16)
                self.new_ns = randint(2, 16)
            while self.question1[0] == '0':
                self.question1 = ''
                for i in range(randint(2, 3)):
                    self.question1 += str(
                        self.digits[randint(0, self.old_ns - 1)]).upper()
        self.question.setText('Переведите число {} из {}-ичной системы '
                              'счисления\nв {}-ичную систему '
                              'счисления'.format(self.question1, self.old_ns,
                                                 self.new_ns))
        self.question.setWordWrap(True)
        if self.number > self.questions:
            self.f.close()
            self.result = MyWidget5(self.questions, self.id)
            self.result.show()
            self.hide()

    def ending(self):
        self.f.close()
        self.result = MyWidget5(self.questions, self.id)
        self.result.show()
        self.hide()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Выход',
                                     "Вы действительно хотите выйти?",
                                     QMessageBox.Yes |
                                     QMessageBox.No,
                                     QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class MyWidget5(QMainWindow, Ui_Result):
    def __init__(self, questions, id):
        super().__init__()
        self.setupUi(self)

        self.questions = questions
        self.id = id
        self.score = 0
        self.f = open('resources/answers.txt')
        self.list = self.f.readlines()
        pixmap = QtGui.QPixmap("resources/firework.png")
        self.picture1.setPixmap(pixmap)
        self.picture2.setPixmap(pixmap)

        for i in range(len(self.list)):
            if len(self.list[i].split()) > 1:
                n1, n2 = self.list[i].split()
                if n1 == n2:
                    self.score += 1
        self.f.close()

        connect = sqlite3.connect('resources/task catalog.db')
        self.cur = connect.cursor()
        self.cur.execute(f"INSERT INTO results (name, result) "
                         f"VALUES ("
                         f"{self.id}, {self.score * 100 // self.questions})")
        connect.commit()
        connect.close()
        self.result_num.setText('Вы ответили верно на {} вопросов из {}'
                                ''.format(self.score, self.questions))
        self.result_progressBar.setValue(self.score * 100 // self.questions)

        self.retry_button.clicked.connect(self.retrying)
        self.results_button.clicked.connect(self.resulting)
        self.back_button.clicked.connect(self.backing)

    def backing(self):
        menu.show()
        self.hide()

    def resulting(self):
        self.best_results = MyWidget8()
        self.best_results.show()
        self.hide()

    def retrying(self):
        self.test_choice = MyWidget3()
        self.test_choice.show()
        self.hide()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Выход',
                                     "Вы действительно хотите выйти?",
                                     QMessageBox.Yes |
                                     QMessageBox.No,
                                     QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class MyWidget6(QMainWindow, Ui_StartSolve):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.questions = 5
        self.back_button.clicked.connect(self.backing)
        self.start_button.clicked.connect(self.starting)

        self.how_many_questions.addItem('5')
        self.how_many_questions.addItem('10')
        self.how_many_questions.addItem('15')
        self.how_many_questions.addItem('20')
        self.how_many_questions.addItem('25')
        self.how_many_questions.currentTextChanged.connect(self.text_changed)

        self.convert_action.triggered.connect(self.converting)
        self.solve_action.triggered.connect(self.solving)

    def converting(self):
        self.test_choice = MyWidget3()
        self.test_choice.show()
        self.hide()

    def solving(self):
        pass

    def backing(self):
        menu.show()
        self.hide()

    def starting(self):
        self.auth = MyWidget9(0, self.questions, 0)
        self.auth.show()
        self.hide()

    def text_changed(self, questions):
        self.questions = int(questions)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Выход',
                                     "Вы действительно хотите выйти?",
                                     QMessageBox.Yes |
                                     QMessageBox.No,
                                     QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class MyWidget7(QMainWindow, Ui_Solve):
    def __init__(self, questions, id):
        super().__init__()
        self.setupUi(self)

        self.question_number = 'Вопрос №'
        self.id = id
        self.number = 1
        self.questions = questions
        self.questions_list = []
        self.f = open('resources/answers.txt', 'w')

        self.question_number1_2.setText(self.question_number +
                                        str(self.number))
        self.question_number2_2.setText(str(self.number) + '/' +
                                        str(self.questions))
        self.questions_progressBar_2.setValue(100 * (self.number - 1) //
                                              self.questions)
        self.end_button_2.clicked.connect(self.ending)
        self.continue_button_2.clicked.connect(self.continueing)
        self.con = sqlite3.connect("resources/task catalog.db")
        self.cur = self.con.cursor()
        result = self.cur.execute("""SELECT * FROM tasks""").fetchall()
        question1 = choice(result)
        self.questions_list.append(question1)
        self.question_2.setText(question1[2])
        self.question_2.setWordWrap(True)

    def ending(self):
        self.f.close()
        self.con.close()
        self.result = MyWidget5(self.questions, self.id)
        self.result.show()
        self.hide()

    def continueing(self):
        answer1 = str(self.answer_2.text())
        answer2 = str(self.questions_list[self.number - 1][3])
        self.f.write(str(answer1) + ' ' + str(answer2) + '\n')
        self.answer_2.setText('')
        self.number += 1
        self.question_number1_2.setText(self.question_number +
                                        str(self.number))
        self.question_number2_2.setText(str(self.number) + '/' +
                                        str(self.questions))
        self.questions_progressBar_2.setValue(100 * (self.number - 1) //
                                              self.questions)
        result = self.cur.execute("""SELECT * FROM tasks""").fetchall()
        question1 = choice(result)
        while question1 in self.questions_list:
            question1 = choice(result)
        self.questions_list.append(question1)
        self.question_2.setText(question1[2])
        if self.number > self.questions:
            self.f.close()
            self.con.close()
            self.result = MyWidget5(self.questions, self.id)
            self.result.show()
            self.hide()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Выход',
                                     "Вы действительно хотите выйти?",
                                     QMessageBox.Yes |
                                     QMessageBox.No,
                                     QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class MyWidget8(QMainWindow, Ui_BestResults):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.back_button.clicked.connect(self.backing)
        self.con = sqlite3.connect("resources/task catalog.db")
        self.load_button.clicked.connect(self.update_result)
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.save_button.clicked.connect(self.save_results)
        self.del_button.clicked.connect(self.delete_elem)
        self.modified = {}
        self.titles = None


    def update_result(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM results WHERE name=?",
                             (item_id := self.idbox.text(),)).fetchall()
        self.tableWidget.setRowCount(len(result))
        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            return
        else:
            self.statusBar().showMessage(f"Нашлась запись с id = {item_id}")
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setRowCount(len(result))

        self.tableWidget.setHorizontalHeaderLabels(
            ["id Теста", "id Пользователя", "Результат в процентах"])

        self.tableWidget.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
        self.tableWidget.horizontalHeaderItem(1).setTextAlignment(
            Qt.AlignHCenter)
        self.tableWidget.horizontalHeaderItem(2).setTextAlignment(
            Qt.AlignRight)
        self.tableWidget.resizeColumnsToContents()

        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def item_changed(self, item):
        self.modified[self.titles[item.column()]] = item.text()

    def save_results(self):
        try:
            if self.idbox.text() and self.name_edit.text():
                cur = self.con.cursor()
                cur.execute('''UPDATE names SET name = ? WHERE id = ?''',
                            (self.name_edit.text(), self.idbox.text()))
                self.con.commit()
                self.modified.clear()
                self.statusBar().showMessage('Изменение прошло успешно')
            elif self.idbox.text() and not self.name_edit.text():
                self.statusBar().showMessage('Нет нового имени')
            elif not self.idbox.text() and self.name_edit.text():
                self.statusBar().showMessage('Нет id')
            else:
                self.statusBar().showMessage('Нет данных')
        except Exception:
            self.statusBar().showMessage('Нет данных')

    def delete_elem(self):
        try:
            valid = QMessageBox.question(
                self, 'Предупреждение', "Действительно удалить элементы\n"
                    "с id пользователя " + "".join(self.idbox.text()) + '?',
                QMessageBox.Yes, QMessageBox.No)
            if valid == QMessageBox.Yes:
                cur = self.con.cursor()
                cur.execute(f"DELETE FROM results WHERE "
                            f"name = {self.idbox.text()}")
                cur.execute(f"DELETE FROM names WHERE "
                            f"id = {self.idbox.text()}")
                self.con.commit()
        except Exception:
            self.statusBar().showMessage('Ошибка')

    def backing(self):
        self.con.close()
        menu.show()
        self.hide()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Выход',
                                     "Вы действительно хотите выйти?",
                                     QMessageBox.Yes |
                                     QMessageBox.No,
                                     QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            self.con.close()
            event.accept()
        else:
            event.ignore()


class MyWidget9(QMainWindow, Ui_Name):
    def __init__(self, choice=0, questions=0, number=0):
        super().__init__()
        self.setupUi(self)

        self.number = number
        self.questions = questions
        self.choice = choice

        self.back_button.clicked.connect(self.backing)
        self.start_button.clicked.connect(self.starting)
        self.connect = sqlite3.connect('resources/task catalog.db')
        self.cur = self.connect.cursor()

    def backing(self):
        menu.show()
        self.hide()

    def starting(self):
        self.name = self.nameEdit.text()
        if self.name:
            data = self.cur.execute(f"""SELECT * FROM names WHERE name
            ='{self.name}'""").fetchall()
            dlg = QMessageBox(self)
            if data:
                dlg.setWindowTitle("Похожее имя")
                self.id = data[0][0]
                dlg.setText(
                    f"Найден пользователь с таким же именем.\nПродолжить "
                    f"с id {self.id}?")
            else:
                dlg.setWindowTitle("Подтверждение имени")
                self.id = self.cur.execute("""SELECT * FROM 
                names""").fetchall()[-1][0] + 1
                dlg.setText(f"Продолжить с id {self.id}?")
            dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            dlg.setIcon(QMessageBox.Question)
            button = dlg.exec()

            if button == QMessageBox.Yes:
                if not data:
                    self.cur.execute(f"INSERT INTO names (id, name) "
                                     f"VALUES ({self.id}, '{self.name}')")
                self.connect.commit()
                self.connect.close()
                if self.choice:
                    self.test = MyWidget4(self.choice, self.questions,
                                          self.number, self.id)
                    self.test.show()
                    self.hide()
                else:
                    self.test = MyWidget7(self.questions, self.id)
                    self.test.show()
                    self.hide()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Выход',
                                     "Вы действительно хотите выйти?",
                                     QMessageBox.Yes |
                                     QMessageBox.No,
                                     QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    menu = MyWidget1()
    menu.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
