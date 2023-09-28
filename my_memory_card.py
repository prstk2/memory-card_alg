from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QGroupBox, QVBoxLayout, QHBoxLayout, QRadioButton, QButtonGroup, QMessageBox
from random import shuffle, randint

#создание окна
app = QApplication([])
win = QWidget()
layout_main = QVBoxLayout()
app.setApplicationName("Memory Card")
win.setFixedHeight(300)
win.setFixedWidth(450)

#вопрос
question = QLabel('How many holes in a polo?')

question_wrapper = QHBoxLayout()  # _wrapper - обозначение для слоёв, которые идут в основной
question_wrapper.addWidget(question, alignment=Qt.AlignCenter) 

#выбор ответа
groupbox = QGroupBox('Answer options')
groupbox_layout = QVBoxLayout()
groupbox.setLayout(groupbox_layout)
groupbox_layout_g1 = QHBoxLayout()
groupbox_layout_g2 = QHBoxLayout()
q1 = QRadioButton('Four')
q2 = QRadioButton('Two')
q3 = QRadioButton('One')
q4 = QRadioButton('Three')
q_list = [q1, q2, q3, q4]  #список с кнопками
groupbox_layout_g1.addWidget(q1)
groupbox_layout_g1.addWidget(q2)
groupbox_layout_g2.addWidget(q3)
groupbox_layout_g2.addWidget(q4)
groupbox_layout.addLayout(groupbox_layout_g1)
groupbox_layout.addLayout(groupbox_layout_g2)

#результат теста (по умолчанию не видно)
testresult = QGroupBox('Result')
testresult_layout = QVBoxLayout()
testresult.setLayout(testresult_layout)
result = QLabel('Correct/Incorrect')
result_wrapper = QHBoxLayout()
result_wrapper.addWidget(result, alignment=Qt.AlignLeft)
right_answer = QLabel('Right answer')
right_answer_wrapper = QHBoxLayout()
right_answer_wrapper.addWidget(right_answer, alignment=Qt.AlignCenter)
testresult_layout.addLayout(result_wrapper)
testresult_layout.addLayout(right_answer_wrapper)

groupbox_wrapper = QHBoxLayout()
groupbox_wrapper.addWidget(groupbox, stretch=2)
groupbox_wrapper.addWidget(testresult, stretch=2)

#у QGroupBox нет метода setExclusive :/
radiogroup = QButtonGroup()
radiogroup.addButton(q1)
radiogroup.addButton(q2)
radiogroup.addButton(q3)
radiogroup.addButton(q4)

button = QPushButton('Answer')
button_wrapper = QHBoxLayout()
button_wrapper.addWidget(button)


layout_main.addStretch(2)
layout_main.addLayout(question_wrapper)  # вопрос
layout_main.addStretch(1)
layout_main.addLayout(groupbox_wrapper)  # тест
layout_main.addStretch(1)
layout_main.addLayout(button_wrapper)  # кнопка ответа
layout_main.addStretch(1)
testresult.hide()

correct_ans = 0
allowed_atts = 1

def click():
    if button.text() == 'Answer':
        if len(question_list) == 0:
            q_end()
        else:
            check_answer()
    else:
        nextQuestion()


button.clicked.connect(click)


class Question():
    def __init__(self, question, correct, wrong1, wrong2, wrong3):
        self.question = question
        self.correct = correct
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3

question_list = []
question_list.append(Question('Can a match box?', 'No, but a tin can', 'Yes', 'No', 'Yes, one beat Mike Tyson'))
question_list.append(Question('77+33', '110', '100', '111', '101'))
question_list.append(Question(".sdrawkcab noitseuq siht rewsnA", "K.O.", "What?", "I don't understand", "4"))
question_list.append(Question('What can you put in a bucket to make it lighter?', 'Torch', 'Gypses', 'A hole', 'Canned laughter'))
question_list.append(Question('What do you call a wingless fly?', 'A walk', 'A flap', 'A plum', 'Jason'))


def nextQuestion():
    qnum = randint(0, len(question_list)-1)
    ask(qnum)


def ask(qnum):
    shuffle(q_list)
    question.setText(question_list[qnum].question)
    q_list[0].setText(question_list[qnum].correct)
    q_list[1].setText(question_list[qnum].wrong1)
    q_list[2].setText(question_list[qnum].wrong2)
    q_list[3].setText(question_list[qnum].wrong3)
    showQuestion()
    question_list.pop(qnum)

def showQuestion():
    radiogroup.setExclusive(False)
    q1.setChecked(False)
    q2.setChecked(False)
    q3.setChecked(False)
    q4.setChecked(False)
    radiogroup.setExclusive(True)
    button.setText('Answer')
    testresult.hide()
    groupbox.show()


def check_answer():
    global allowed_atts
    if q_list[0].isChecked():  #первая кнопка была нажата
        show_result(True)
    else:  #первая кнопка не была нажата
        if q_list[1].isChecked() or q_list[2].isChecked() or q_list[3].isChecked():
            if allowed_atts == 1:
                allowed_atts = 0
                msg = QMessageBox()
                msg.setWindowTitle('Wrong')
                msg.setText('Try again')
                msg.exec_()
                return
            show_result(False)


def show_result(correct):
    global correct_ans
    global allowed_atts

    groupbox.hide()
    testresult.show()
    if correct:
        result.setText('Correct')
        correct_ans += 1
    else:
        result.setText('Incorrect')

    right_answer.setText(q_list[0].text())
    button.setText('Next question')
    
    allowed_atts = 1


def q_end():
    msg = QMessageBox()
    msg.setWindowTitle('the end')
    msg.setText("Right answers: " + str(correct_ans) + "/5")
    msg.show()
    msg.exec_()
    if msg.clickedButton():
        app.quit()
win.setLayout(layout_main)
win.show()
app.exec_()