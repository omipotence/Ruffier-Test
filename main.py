from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivy.core.window import Window
from seconds import Seconds
from runner import Runner
from sits import Sits
from ruffier import test

colour = (0.74, 0.19, 0.82, 1)
Window.clearcolor = (0.5, 0.14, 0.88, 1)

name = "The"
age = 0
r1 = 0
r2 = 0 
r3 = 0
txt_instruction = '''
Данное приложение позволит вам с помощью теста Руфье \n провести первичную диагностику вашего здоровья.\n
Проба Руфье представляет собой нагрузочный комплекс, \n предназначенный для оценки работоспособности сердца \n при физической нагрузке.\n
У испытуемого определяют частоту пульса за 15 секунд.\n
Затем в течение 45 секунд испытуемый выполняет 30 приседаний.\n
После окончания нагрузки пульс подсчитывается вновь: \nчисло пульсаций за первые 15 секунд, 30 секунд отдыха,\n число пульсаций за последние 15 секунд.\n'''
txt_test3 = '''В течение минуты замерьте пульс два раза:\n 
за первые 15 секунд минуты, затем за последние 15 секунд.\n
Результаты запишите в соответствующие поля.''' 

def check_int(str_num):
    try:
        return int(str_num)
    except:
        return False

class FirstScr(Screen):
    def __init__(self, name="instructions"):
        super().__init__(name=name)
        instr = Label(text=txt_instruction, pos_hint={"center_x":0.55})
        startbtn = Button(text = "Начать", background_color=(colour), size_hint=(0.3, 0.2), pos_hint={"center_x":0.5})
        namelabel = Label(text="Введите имя:")
        agelabel = Label(text="Введите возраст:")
        self.nameinput = TextInput(size_hint=(0.8, 0.13), pos_hint={"center_y":0.5})
        self.ageinput = TextInput(size_hint=(0.8, 0.13), pos_hint={"center_y":0.5})
        layout_main = BoxLayout(orientation = "vertical", padding=6, spacing=20)
        layout = BoxLayout(orientation = "horizontal")
        layout_main.add_widget(instr)
        layout.add_widget(namelabel)
        layout.add_widget(self.nameinput)
        layout.add_widget(agelabel)
        layout.add_widget(self.ageinput)
        layout_main.add_widget(layout)
        layout_main.add_widget(startbtn)
        startbtn.on_press = self.next
        self.add_widget(layout_main)

    def next(self):
        global name, age
        self.manager.transition.direction = "left"
        name = self.nameinput.text
        age = check_int(self.ageinput.text)
        if age == False or age <7:
            age = 0
            self.ageinput.text = str(age)
        else: 
            age = int(self.ageinput.text)
            self.manager.current = "measure1"


class SecondScr(Screen):
    def __init__(self, name="measure1"):
        self.next_screen = False
        super().__init__(name=name)
        instr = Label(text="Замерьте пульс за 15 секунд.")
        self.secondslabel = Seconds(15)
        self.secondslabel.bind(done=self.sec_finished)
        resultlabel = Label(text="Введите результат:")
        self.resultinput = TextInput(text='0', size_hint=(0.8, 0.16), pos_hint={"center_y":0.5})
        self.resultinput.set_disabled(True)
        self.btn = Button(text="Начать",  background_color=(colour), size_hint=(0.3, 0.2), pos_hint={"center_x":0.5})
        layout_main = BoxLayout(orientation = "vertical")
        layout = BoxLayout(orientation = "horizontal")
        layout_main.add_widget(instr)
        layout_main.add_widget(self.secondslabel)
        layout.add_widget(resultlabel)
        layout.add_widget(self.resultinput)
        layout_main.add_widget(layout)
        layout_main.add_widget(self.btn)
        self.btn.on_press = self.next
        self.add_widget(layout_main)

    def sec_finished(self, *args):
        self.next_screen = True
        self.resultinput.set_disabled(False)
        self.btn.set_disabled(False)
        self.btn.text = "Продолжить"


    def next(self):
        if not self.next_screen:
            self.btn.set_disabled(True)
            self.secondslabel.start()
        else:
            global r1
            r1 = check_int(self.resultinput.text)
            if r1 == False or r1 <= 0:
                r1 = 0 
                self.resultinput.text = str(r1)
            else:
                r1 = int(self.resultinput.text)
                self.manager.transition.direction = "left"
                self.manager.current = "measure2"

class ThirdScr(Screen):
    def __init__(self, name="measure2"):
        super().__init__(name=name)
        self.next_screen = False
        instr = Label(text="Выполните 30 приседаний за 45 секунд.")
        self.sitslabel = Sits(30)
        self.run = Runner(total=30, steptime=1.5, size_hint=(0.4, 1))
        self.run.bind(finished=self.run_finished)
        self.btn = Button(text="Начать",  background_color=(colour), size_hint=(0.3, 0.2), pos_hint={"center_x":0.5})
        layout = BoxLayout(orientation = "vertical")
        layout2 = BoxLayout(orientation="horizontal")
        layout2.add_widget(instr)
        layout2.add_widget(self.run)
        layout2.add_widget(self.sitslabel)
        layout.add_widget(layout2)
        layout.add_widget(self.btn)
        self.btn.on_press = self.next
        self.add_widget(layout)

    def run_finished(self, instance, value):
        self.btn.set_disabled(False)
        self.btn.text = "Продолжить"
        self.next_screen = True

    def next(self):
        if not self.next_screen:
            self.btn.set_disabled(True)
            self.run.start()
            self.run.bind(value=self.sitslabel.next)
        else:
            self.manager.transition.direction = "left"
            self.manager.current = "measure3"

class FourthScr(Screen):
    def __init__(self, name="measure3"):
        self.next_screen = False
        self.stage = 0
        super().__init__(name=name)
        instr = Label(text=txt_test3)
        self.btn = Button(text = "Начать",  background_color=(colour), size_hint=(0.3, 0.2), pos_hint={"center_x":0.5})
        self.secondslabel = Seconds(15)
        self.secondslabel.bind(done=self.sec_finished)
        self.pulselabel = Label(text="Считайте пульс")   
        self.resultlabel1 = Label(text="Результат:")
        self.resultlabel2 = Label(text="Результат после отдыха:")
        self.result1input = TextInput(text="0", size_hint=(0.8, 0.2), pos_hint={"center_y":0.5})
        self.result2input = TextInput(text="0", size_hint=(0.8, 0.2), pos_hint={"center_y":0.5})
        self.result1input.set_disabled(True)
        self.result2input.set_disabled(True)
        layout_main = BoxLayout(orientation = "vertical")
        layout = BoxLayout(orientation = "horizontal")
        layout_main.add_widget(instr)
        layout.add_widget(self.resultlabel1)
        layout.add_widget(self.result1input)
        layout.add_widget(self.resultlabel2)
        layout.add_widget(self.result2input)
        layout_main.add_widget(layout)
        layout_main.add_widget(self.secondslabel)
        layout_main.add_widget(self.pulselabel) 
        layout_main.add_widget(self.btn)
        self.btn.on_press = self.next
        self.add_widget(layout_main)

    def sec_finished(self, *args):
        if self.secondslabel.done:
            if self.stage == 0:
                self.stage = 1
                self.pulselabel.text = "Отдыхайте"
                self.secondslabel.restart(30)
                self.result1input.set_disabled(False)
            elif self.stage == 1:
                self.stage = 2
                self.pulselabel.text = "Считайте пульс"
                self.secondslabel.restart(15)
            elif self.stage == 2:
                self.result2input.set_disabled(False)
                self.btn.set_disabled(False)
                self.btn.text = "Завершить"
                self.next_screen = True

    def next(self):
        if not self.next_screen:
            self.btn.set_disabled(True)
            self.secondslabel.start()
        else:
            global r2, r3
            r2 = check_int(self.result1input.text)
            r3 = check_int(self.result2input.text)
            if r2 == False or r2 <= 0:
                r2 = 0  
                self.result1input.text = str(r2)
            elif r3 == False or r3 <= 0:
                r3 = 0  
                self.result2input.text = str(r3)
            else:
                r2 = int(self.result1input.text)
                r3 = int(self.result2input.text)
                self.manager.transition.direction = "left"
                self.manager.current = "results"

class FifthScr(Screen):
    def __init__(self, name="results"):
        super().__init__(name=name)
        self.layout_main = BoxLayout(orientation="vertical")
        self.instr = Label(text="")
        self.layout_main.add_widget(self.instr)
        self.add_widget(self.layout_main)
        self.on_enter = self.before

    def before(self):
        global name
        self.instr.text = str(name) + "\n " + str(test(r1, r2, r3, age))
        print(test(r1, r2, r3, age))
        



class RuffierTestApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FirstScr(name="instructions"))
        sm.add_widget(SecondScr(name="measure1"))
        sm.add_widget(ThirdScr(name="measure2"))
        sm.add_widget(FourthScr(name="measure3"))
        sm.add_widget(FifthScr(name="results"))
        return sm

app = RuffierTestApp()
app.run()