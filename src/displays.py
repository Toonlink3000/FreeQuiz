from customtkinter import *
from tkinter import *
import widgets


class DisplayManager():
	def __init__(self, window):
		self.current_display = 0
		self.window = window

	def jump_to_display(self, display:int, **displayargs):
		self.clear_window()
		DISPLAYS[self.current_display](self.window, displayargs)


	def clear_window(self):
		widget_list =  self.window.winfo_children()
		for item in widget_list:
			item.destroy()

class StartScreen():
	def __init__(self, window, displayargs:dict):
		window.control_buttons = widgets.ControlButtons(window, self.open_quiz)
		window.control_buttons.grid(row=2, column=0, pady=50)
		window.title_text = CTkLabel(text="FreeQuiz", text_font=("default", -70))
		window.title_text.grid(row=0, column=0, pady=50)

		window.grid_columnconfigure(0, weight=1)
		window.grid_rowconfigure(1, weight=1)

	def open_quiz(self):
		file_name = askopenfilename(filetypes=(("OpenQuiz quiz file", "*.qwz"), ("JSON files", "*.json"), ("All files", "*")))
		file = open(file_name, "r")
		data = json.loads(file.read())
		file.close()
		self.quiz = Quiz(self, data)
		self.quiz.start_quiz()

class QuizWelcome():
	def __init__(self, window, displayargs:dict):
		pass

class QuizPage():
	def __init__(self, window, displayargs:dict):
		pass
		
class QuizEnd():
	def __init__(self, window, displayargs:dict):
		pass

DISPLAYS = [StartScreen, QuizWelcome, QuizPage, QuizEnd] #Constant with displays assigned to numbers